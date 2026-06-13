"""
数据质量检查模块
潘达工程-商务成本智能决策体系
数据空间: space__panda_construction
"""

import json
import os
import logging
from typing import Dict, List, Any

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


class DataQualityChecker:
    """
    数据质量检查器
    """
    
    def __init__(self):
        self.rules = {
            "required_fields": self._check_required_fields,
            "report_period_format": self._check_report_period_format,
            "numeric_non_negative": self._check_numeric_non_negative,
            "date_key_format": self._check_date_key_format,
            "warning_level_valid": self._check_warning_level,
            "cost_level_valid": self._check_cost_level,
            "bond_amount_balance": self._check_bond_amount_balance,
            "penalty_amount_positive": self._check_penalty_amount_positive,
            "date_logic": self._check_date_logic
        }
    
    def _check_required_fields(self, record: Dict[str, Any], required_fields: List[str]) -> List[str]:
        """
        检查必填字段
        
        Args:
            record: 数据记录
            required_fields: 必填字段列表
            
        Returns:
            错误信息列表
        """
        errors = []
        for field in required_fields:
            if field not in record or record[field] is None or str(record[field]).strip() == "":
                errors.append(f"必填字段 {field} 为空")
        return errors
    
    def _check_report_period_format(self, record: Dict[str, Any]) -> List[str]:
        """
        检查报告期间格式
        
        Args:
            record: 数据记录
            
        Returns:
            错误信息列表
        """
        errors = []
        report_period = record.get("report_period")
        if report_period:
            import re
            if not re.match(r"^\d{4}-\d{2}$", str(report_period)):
                errors.append(f"report_period格式错误: {report_period}")
        return errors
    
    def _check_numeric_non_negative(self, record: Dict[str, Any], numeric_fields: List[str]) -> List[str]:
        """
        检查数值字段非负
        
        Args:
            record: 数据记录
            numeric_fields: 数值字段列表
            
        Returns:
            错误信息列表
        """
        errors = []
        for field in numeric_fields:
            if field in record and record[field] is not None:
                try:
                    if float(record[field]) < 0:
                        errors.append(f"{field}不能为负数: {record[field]}")
                except (ValueError, TypeError):
                    errors.append(f"{field}不是有效数值: {record[field]}")
        return errors
    
    def _check_date_key_format(self, record: Dict[str, Any]) -> List[str]:
        """
        检查date_key格式
        
        Args:
            record: 数据记录
            
        Returns:
            错误信息列表
        """
        errors = []
        date_key = record.get("date_key")
        if date_key:
            try:
                date_str = str(date_key)
                if len(date_str) != 8:
                    errors.append(f"date_key格式错误: {date_key}")
                else:
                    year = int(date_str[:4])
                    month = int(date_str[4:6])
                    day = int(date_str[6:8])
                    if year < 2000 or year > 2100:
                        errors.append(f"date_key年份错误: {year}")
                    if month < 1 or month > 12:
                        errors.append(f"date_key月份错误: {month}")
                    if day < 1 or day > 31:
                        errors.append(f"date_key日期错误: {day}")
            except Exception:
                errors.append(f"date_key格式错误: {date_key}")
        return errors
    
    def _check_warning_level(self, record: Dict[str, Any]) -> List[str]:
        """
        检查预警级别
        
        Args:
            record: 数据记录
            
        Returns:
            错误信息列表
        """
        errors = []
        warning_level = record.get("warning_level")
        if warning_level and warning_level not in ["green", "yellow", "red"]:
            errors.append(f"warning_level值错误: {warning_level}")
        return errors
    
    def _check_cost_level(self, record: Dict[str, Any]) -> List[str]:
        """
        检查成本层级
        
        Args:
            record: 数据记录
            
        Returns:
            错误信息列表
        """
        errors = []
        cost_level = record.get("cost_level")
        if cost_level and cost_level not in ["L1", "L2", "L3"]:
            errors.append(f"cost_level值错误: {cost_level}")
        return errors
    
    def _check_bond_amount_balance(self, record: Dict[str, Any]) -> List[str]:
        """
        检查保证金金额平衡
        
        Args:
            record: 数据记录
            
        Returns:
            错误信息列表
        """
        errors = []
        bond_amount = record.get("bond_amount")
        returned_amount = record.get("returned_amount", 0)
        unreturned_amount = record.get("unreturned_amount", 0)
        
        if bond_amount is not None and returned_amount is not None and unreturned_amount is not None:
            try:
                bond = float(bond_amount)
                returned = float(returned_amount)
                unreturned = float(unreturned_amount)
                
                if abs(bond - (returned + unreturned)) > 0.01:
                    errors.append(f"保证金金额不平衡: bond={bond}, returned={returned}, unreturned={unreturned}")
            except Exception:
                pass
        return errors
    
    def _check_penalty_amount_positive(self, record: Dict[str, Any]) -> List[str]:
        """
        检查罚款金额为正
        
        Args:
            record: 数据记录
            
        Returns:
            错误信息列表
        """
        errors = []
        penalty_amount = record.get("penalty_amount")
        if penalty_amount is not None:
            try:
                if float(penalty_amount) <= 0:
                    errors.append(f"penalty_amount必须大于0: {penalty_amount}")
            except Exception:
                errors.append(f"penalty_amount不是有效数值: {penalty_amount}")
        return errors
    
    def _check_date_logic(self, record: Dict[str, Any]) -> List[str]:
        """
        检查日期逻辑
        
        Args:
            record: 数据记录
            
        Returns:
            错误信息列表
        """
        errors = []
        
        # 检查保险日期
        purchase_date = record.get("purchase_date")
        expiry_date = record.get("expiry_date")
        if purchase_date and expiry_date:
            if purchase_date > expiry_date:
                errors.append(f"投保日期({purchase_date})晚于到期日期({expiry_date})")
        
        # 检查保证金日期
        payment_date = record.get("payment_date")
        due_date = record.get("due_date")
        if payment_date and due_date:
            if payment_date > due_date:
                errors.append(f"缴纳日期({payment_date})晚于到期日期({due_date})")
        
        return errors
    
    def check_record(self, record: Dict[str, Any], table_name: str) -> List[str]:
        """
        检查单条记录
        
        Args:
            record: 数据记录
            table_name: 表名
            
        Returns:
            错误信息列表
        """
        errors = []
        
        # 根据表名定义检查规则
        table_rules = {
            "fact_project_cost": {
                "required": ["cost_id", "project_id", "report_period"],
                "numeric": ["cost_confirmed_acc", "cost_unconfirmed_acc", "labor_cost_acc", 
                           "material_cost_acc", "equipment_cost_acc"]
            },
            "fact_project_output": {
                "required": ["output_id", "project_id", "report_period"],
                "numeric": ["confirmed_output", "unconfirmed_output", "total_output"]
            },
            "fact_project_indicator": {
                "required": ["indicator_id", "project_id", "report_period"],
                "numeric": ["indicator_value", "target_value"]
            },
            "fact_project_risk": {
                "required": ["risk_id", "project_id", "report_period"],
                "numeric": ["risk_value"],
                "check_warning": True
            },
            "fact_project_payment": {
                "required": ["payment_id", "project_id", "report_period"],
                "numeric": ["payable_confirmed", "payable_unconfirmed", "paid_amount"]
            },
            "fact_bond": {
                "required": ["bond_id", "project_id", "bond_type", "bond_amount"],
                "numeric": ["bond_amount", "returned_amount", "unreturned_amount"],
                "check_bond_balance": True
            },
            "fact_penalty": {
                "required": ["penalty_id", "project_id", "penalty_type", "penalty_amount"],
                "numeric": ["penalty_amount"],
                "check_penalty_positive": True
            },
            "fact_insurance": {
                "required": ["insurance_id", "project_id", "insurance_type", "insurance_amount"],
                "numeric": ["insurance_amount", "premium_amount"],
                "check_date_logic": True
            },
            "fact_equipment": {
                "required": ["equipment_id", "project_id", "equipment_code", "equipment_name"],
                "numeric": ["original_value", "unit_price"]
            }
        }
        
        rules = table_rules.get(table_name, {})
        
        # 检查必填字段
        if "required" in rules:
            errors.extend(self._check_required_fields(record, rules["required"]))
        
        # 检查报告期间格式
        if "report_period" in record:
            errors.extend(self._check_report_period_format(record))
        
        # 检查数值字段
        if "numeric" in rules:
            errors.extend(self._check_numeric_non_negative(record, rules["numeric"]))
        
        # 检查date_key格式
        if "date_key" in record:
            errors.extend(self._check_date_key_format(record))
        
        # 检查预警级别
        if rules.get("check_warning"):
            errors.extend(self._check_warning_level(record))
        
        # 检查成本层级
        if "cost_level" in record:
            errors.extend(self._check_cost_level(record))
        
        # 检查保证金金额平衡
        if rules.get("check_bond_balance"):
            errors.extend(self._check_bond_amount_balance(record))
        
        # 检查罚款金额为正
        if rules.get("check_penalty_positive"):
            errors.extend(self._check_penalty_amount_positive(record))
        
        # 检查日期逻辑
        if rules.get("check_date_logic"):
            errors.extend(self._check_date_logic(record))
        
        return errors
    
    def check_file(self, file_path: str, table_name: str) -> Dict[str, Any]:
        """
        检查文件中的数据质量
        
        Args:
            file_path: JSON文件路径
            table_name: 表名
            
        Returns:
            检查结果
        """
        results = {
            "file_path": file_path,
            "table_name": table_name,
            "total_records": 0,
            "valid_records": 0,
            "invalid_records": 0,
            "errors": [],
            "summary": {}
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                data = [data]
            
            results["total_records"] = len(data)
            
            for i, record in enumerate(data):
                record_errors = self.check_record(record, table_name)
                
                if record_errors:
                    results["invalid_records"] += 1
                    results["errors"].append({
                        "record_index": i,
                        "record_id": record.get("id", record.get(f"{table_name.replace('fact_', '').replace('dim_', '')}_id")),
                        "errors": record_errors
                    })
                else:
                    results["valid_records"] += 1
            
            # 计算统计信息
            results["summary"] = {
                "valid_rate": round(results["valid_records"] / results["total_records"] * 100, 2),
                "invalid_rate": round(results["invalid_records"] / results["total_records"] * 100, 2),
                "total_errors": len(results["errors"])
            }
            
            logger.info(f"数据质量检查完成，文件: {file_path}")
            logger.info(f"有效记录: {results['valid_records']}/{results['total_records']} ({results['summary']['valid_rate']}%)")
            
        except Exception as e:
            logger.error(f"检查文件失败: {str(e)}")
            results["errors"].append(f"文件读取失败: {str(e)}")
        
        return results
    
    def generate_report(self, results: Dict[str, Any]) -> str:
        """
        生成检查报告
        
        Args:
            results: 检查结果
            
        Returns:
            报告字符串
        """
        report = [
            "=" * 60,
            "数据质量检查报告",
            "=" * 60,
            f"检查文件: {results['file_path']}",
            f"目标表名: {results['table_name']}",
            f"检查时间: {self._get_current_time()}",
            "",
            "统计信息:",
            f"  总记录数: {results['total_records']}",
            f"  有效记录: {results['valid_records']}",
            f"  无效记录: {results['invalid_records']}",
            f"  有效率: {results['summary']['valid_rate']}%",
            f"  无效率: {results['summary']['invalid_rate']}%",
            f"  总错误数: {results['summary']['total_errors']}",
            ""
        ]
        
        if results["errors"]:
            report.append("错误详情:")
            for error in results["errors"]:
                report.append(f"  记录#{error['record_index']} (ID: {error.get('record_id', 'N/A')}):")
                for err in error["errors"]:
                    report.append(f"    - {err}")
                report.append("")
        
        report.append("=" * 60)
        return "\n".join(report)
    
    def _get_current_time(self) -> str:
        """获取当前时间"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="数据质量检查工具")
    parser.add_argument("--file", required=True, help="要检查的JSON文件")
    parser.add_argument("--table", required=True, help="表名")
    
    args = parser.parse_args()
    
    checker = DataQualityChecker()
    results = checker.check_file(args.file, args.table)
    
    report = checker.generate_report(results)
    print(report)
    
    # 保存报告
    report_file = f"dq_report_{args.table}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n报告已保存到: {report_file}")


if __name__ == "__main__":
    main()