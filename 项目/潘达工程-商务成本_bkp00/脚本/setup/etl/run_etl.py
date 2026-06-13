#!/usr/bin/env python3
"""
ETL数据接入主执行脚本
潘达工程-商务成本智能决策体系
数据空间: space__panda_construction

使用方式:
    python run_etl.py --config <配置文件路径> --table <表名>
    python run_etl.py --config config/mapping_config.yml --table fact_project_cost
"""

import argparse
import yaml
import logging
import sys
import os
from datetime import datetime
from typing import Dict, List, Any

# 添加模块路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from transform.transform_utils import (
    apply_field_mapping,
    apply_derived_fields,
    validate_data_quality,
    calculate_date_key,
    get_current_datetime
)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("etl.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ETLProcessor:
    """
    ETL处理器类
    """
    
    def __init__(self, config_path: str):
        """
        初始化处理器
        
        Args:
            config_path: 配置文件路径
        """
        self.config = self._load_config(config_path)
        self.space_id = self.config.get("space_id", "")
        self.tables_config = self.config.get("tables", {})
        self.validators = self.config.get("validators", {})
        self.transformers = self.config.get("transformers", {})
        
    def _load_config(self, config_path: str) -> Dict:
        """
        加载配置文件
        
        Args:
            config_path: 配置文件路径
            
        Returns:
            配置字典
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"加载配置文件失败: {str(e)}")
            raise
    
    def _get_table_config(self, table_name: str) -> Dict:
        """
        获取表配置
        
        Args:
            table_name: 表名
            
        Returns:
            表配置字典
        """
        config = self.tables_config.get(table_name)
        if not config:
            raise ValueError(f"未找到表 {table_name} 的配置")
        return config
    
    def transform_record(
        self,
        source_data: Dict[str, Any],
        table_name: str
    ) -> Dict[str, Any]:
        """
        转换单条记录
        
        Args:
            source_data: 源数据
            table_name: 目标表名
            
        Returns:
            转换后的目标数据
        """
        table_config = self._get_table_config(table_name)
        mappings = table_config.get("mappings", [])
        derived_fields = table_config.get("derived_fields", [])
        
        logger.debug(f"开始转换记录，表名: {table_name}")
        
        try:
            # 应用字段映射
            target_data = apply_field_mapping(source_data, mappings)
            
            # 应用派生字段
            target_data = apply_derived_fields(target_data, derived_fields)
            
            # 数据质量校验
            errors = validate_data_quality(target_data, table_name)
            if errors:
                logger.warning(f"数据质量校验警告: {', '.join(errors)}")
            
            logger.debug(f"转换完成，记录数: {len(target_data)}")
            return target_data
            
        except Exception as e:
            logger.error(f"转换记录失败: {str(e)}")
            raise
    
    def transform_batch(
        self,
        source_data_list: List[Dict[str, Any]],
        table_name: str
    ) -> List[Dict[str, Any]]:
        """
        批量转换记录
        
        Args:
            source_data_list: 源数据列表
            table_name: 目标表名
            
        Returns:
            转换后的目标数据列表
        """
        results = []
        success_count = 0
        fail_count = 0
        
        logger.info(f"开始批量转换，表名: {table_name}，记录数: {len(source_data_list)}")
        
        for i, source_data in enumerate(source_data_list):
            try:
                target_data = self.transform_record(source_data, table_name)
                results.append(target_data)
                success_count += 1
                
                # 每100条记录输出进度
                if (i + 1) % 100 == 0:
                    logger.info(f"已处理 {i + 1} 条记录")
                    
            except Exception as e:
                fail_count += 1
                logger.error(f"第 {i + 1} 条记录转换失败: {str(e)}")
                # 记录错误数据
                with open("etl_errors.log", "a", encoding="utf-8") as f:
                    f.write(f"{datetime.now()}\t{table_name}\t{i+1}\t{str(e)}\t{source_data}\n")
        
        logger.info(f"批量转换完成，成功: {success_count}，失败: {fail_count}")
        return results
    
    def load_data(
        self,
        data_list: List[Dict[str, Any]],
        table_name: str,
        mode: str = "append"
    ) -> Dict[str, Any]:
        """
        加载数据到目标表
        
        Args:
            data_list: 数据列表
            table_name: 目标表名
            mode: 加载模式（append/incremental/full）
            
        Returns:
            加载结果
        """
        logger.info(f"开始加载数据，表名: {table_name}，模式: {mode}，记录数: {len(data_list)}")
        
        # 这里模拟数据加载，实际环境中需要调用平台API或数据库驱动
        # 保存转换后的数据到文件，供后续加载使用
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = os.path.join(output_dir, f"{table_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        
        try:
            import json
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data_list, f, ensure_ascii=False, indent=2)
            
            logger.info(f"数据已保存到文件: {output_file}")
            
            return {
                "success": True,
                "table_name": table_name,
                "record_count": len(data_list),
                "output_file": output_file,
                "mode": mode,
                "timestamp": get_current_datetime()
            }
            
        except Exception as e:
            logger.error(f"加载数据失败: {str(e)}")
            return {
                "success": False,
                "table_name": table_name,
                "error": str(e),
                "timestamp": get_current_datetime()
            }
    
    def execute_etl(
        self,
        table_name: str,
        source_data: List[Dict[str, Any]],
        mode: str = "append"
    ) -> Dict[str, Any]:
        """
        执行完整ETL流程
        
        Args:
            table_name: 目标表名
            source_data: 源数据列表
            mode: 加载模式
            
        Returns:
            ETL执行结果
        """
        logger.info(f"========== 开始ETL执行，表名: {table_name} ==========")
        
        try:
            # 转换阶段
            transformed_data = self.transform_batch(source_data, table_name)
            
            # 加载阶段
            load_result = self.load_data(transformed_data, table_name, mode)
            
            if load_result["success"]:
                logger.info(f"ETL执行成功，表名: {table_name}，记录数: {len(transformed_data)}")
            else:
                logger.error(f"ETL执行失败，表名: {table_name}")
            
            return {
                "success": True,
                "table_name": table_name,
                "input_count": len(source_data),
                "output_count": len(transformed_data),
                "load_result": load_result,
                "timestamp": get_current_datetime()
            }
            
        except Exception as e:
            logger.error(f"ETL执行异常: {str(e)}")
            return {
                "success": False,
                "table_name": table_name,
                "error": str(e),
                "timestamp": get_current_datetime()
            }


def generate_test_data(table_name: str) -> List[Dict[str, Any]]:
    """
    生成测试数据
    
    Args:
        table_name: 表名
        
    Returns:
        测试数据列表
    """
    test_data = []
    
    if table_name == "fact_project_cost":
        test_data = [
            {
                "id": "COST000001",
                "project_id": "P001",
                "report_period": "2025-01",
                "cost_confirmed_acc": 1000000.00,
                "cost_unconfirmed_acc": 200000.00,
                "cost_confirmed_cmonth": 500000.00,
                "cost_unconfirmed_cmonth": 100000.00,
                "labor_cost_acc": 300000.00,
                "material_cost_acc": 600000.00,
                "equipment_cost_acc": 100000.00,
                "management_fee_rate": 0.05,
                "cost_level": "L1",
                "cost_code": "MC01",
                "target_cost": 1200000.00,
                "contract_id": "CT001",
                "cost_name": "主控费用",
                "company_id": "C001",
                "project_name": "测试项目"
            }
        ]
        
    elif table_name == "fact_project_output":
        test_data = [
            {
                "id": "OUT000001",
                "project_id": "P001",
                "report_period": "2025-01",
                "confirmed_output": 800000.00,
                "unconfirmed_output": 200000.00,
                "total_output": 1000000.00,
                "output_last_year_confirmed": 0.00,
                "output_last_year_unconfirmed": 0.00,
                "output_current_confirmed": 800000.00,
                "output_current_unconfirmed": 200000.00,
                "company_id": "C001",
                "project_name": "测试项目"
            }
        ]
        
    elif table_name == "fact_project_indicator":
        test_data = [
            {
                "id": "IND000001",
                "project_id": "P001",
                "report_period": "2025-01",
                "indicator_code": "profit_rate",
                "indicator_name": "毛利率",
                "indicator_value": 18.5,
                "target_value": 20.0,
                "warning_level": "黄",
                "remark": "测试指标",
                "company_id": "C001"
            }
        ]
        
    elif table_name == "fact_project_risk":
        test_data = [
            {
                "id": "RISK000001",
                "project_id": "P001",
                "report_period": "2025-01",
                "risk_type": "成本风险",
                "risk_code": "RK-成本-0001",
                "risk_name": "成本超支风险",
                "risk_value": 75,
                "warning_level": "红",
                "risk_description": "项目成本存在超支风险"
            }
        ]
        
    elif table_name == "fact_project_payment":
        test_data = [
            {
                "id": "PAY000001",
                "project_id": "P001",
                "contract_id": "CT001",
                "report_period": "2025-01",
                "payable_confirmed": 500000.00,
                "payable_unconfirmed": 100000.00,
                "labor_payable": 150000.00,
                "paid_amount": 400000.00,
                "payment_ratio": 0.8,
                "approval_status": "已批复",
                "approval_amount": 500000.00,
                "tax_rate": 0.09,
                "contract_name": "测试合同",
                "contract_amount": 1000000.00,
                "supplier_id": "S001",
                "supplier_name": "测试供应商",
                "contract_code": "HT-001",
                "settlement_status": "进行中"
            }
        ]
        
    elif table_name == "fact_bond":
        test_data = [
            {
                "id": "BND000001",
                "project_id": "P001",
                "contract_id": "CT001",
                "bond_type": "履约保证金",
                "bond_amount": 100000.00,
                "payment_date": "2025-01-15",
                "due_date": "2025-12-31",
                "return_conditions": "工程竣工验收",
                "returned_amount": 20000.00,
                "unreturned_amount": 80000.00,
                "forfeit_status": "无",
                "forfeit_amount": 0.00,
                "report_period": "2025-01"
            }
        ]
        
    elif table_name == "fact_penalty":
        test_data = [
            {
                "id": "PEN000001",
                "project_id": "P001",
                "penalty_type": "违约罚款",
                "penalty_amount": 50000.00,
                "penalty_reason": "施工违规",
                "issuing_unit": "建设单位",
                "penalty_date": "2025-01-31",
                "payment_status": "已缴纳",
                "appeal_status": "无",
                "report_period": "2025-01"
            }
        ]
        
    elif table_name == "fact_insurance":
        test_data = [
            {
                "id": "INS000001",
                "project_id": "P001",
                "insurance_type": "工程险",
                "insurance_company": "中国平安",
                "insurance_amount": 1000000.00,
                "premium_amount": 50000.00,
                "purchase_date": "2025-01-10",
                "expiry_date": "2026-01-09",
                "claim_status": "无理赔",
                "report_period": "2025-01"
            }
        ]
        
    elif table_name == "fact_equipment":
        test_data = [
            {
                "id": "EQP000001",
                "project_id": "P001",
                "equipment_code": "EQ-T001",
                "equipment_name": "塔吊",
                "model_spec": "QTZ80",
                "original_value": 850000.00,
                "depreciation_method": "直线法",
                "unit_price": 2000.00,
                "usage_status": "在用",
                "equipment_status": "自有",
                "report_period": "2025-01"
            }
        ]
        
    else:
        # 默认返回空列表
        pass
    
    return test_data


def main():
    """
    主函数
    """
    parser = argparse.ArgumentParser(description="ETL数据接入脚本")
    parser.add_argument("--config", required=True, help="配置文件路径")
    parser.add_argument("--table", required=True, help="目标表名")
    parser.add_argument("--mode", default="append", help="加载模式")
    parser.add_argument("--test", action="store_true", help="使用测试数据")
    
    args = parser.parse_args()
    
    try:
        # 创建ETL处理器
        etl_processor = ETLProcessor(args.config)
        
        # 获取数据
        if args.test:
            source_data = generate_test_data(args.table)
            logger.info(f"使用测试数据，记录数: {len(source_data)}")
        else:
            # 实际环境中从数据源读取数据
            # 这里演示使用测试数据
            source_data = generate_test_data(args.table)
            logger.warning("未指定数据源，使用测试数据")
        
        # 执行ETL
        result = etl_processor.execute_etl(args.table, source_data, args.mode)
        
        # 输出结果
        import json
        print("\nETL执行结果:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
        if result["success"]:
            sys.exit(0)
        else:
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"ETL执行失败: {str(e)}")
        print(f"ETL执行失败: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()