"""
ETL转换工具函数模块
潘达工程-商务成本智能决策体系
数据空间: space__panda_construction
"""

import re
from datetime import datetime
from typing import Any, Dict, Optional


def calculate_date_key(report_period: str) -> int:
    """
    根据报告期间计算date_key
    格式：YYYYMMDD（当月最后一天）
    
    Args:
        report_period: 报告期间，格式为YYYY-MM
        
    Returns:
        date_key: 日期键，格式为YYYYMMDD
    """
    try:
        year = int(report_period[:4])
        month = int(report_period[5:7])
        
        # 获取当月最后一天
        if month in [1, 3, 5, 7, 8, 10, 12]:
            day = 31
        elif month == 2:
            if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
                day = 29
            else:
                day = 28
        else:
            day = 30
        
        return year * 10000 + month * 100 + day
    except Exception as e:
        raise ValueError(f"计算date_key失败: {str(e)}")


def validate_report_period(report_period: str) -> bool:
    """
    验证报告期间格式
    
    Args:
        report_period: 报告期间字符串
        
    Returns:
        True if valid, False otherwise
    """
    pattern = r"^\d{4}-\d{2}$"
    return bool(re.match(pattern, report_period))


def validate_cost_level(cost_level: str) -> bool:
    """
    验证成本层级
    
    Args:
        cost_level: 成本层级字符串
        
    Returns:
        True if valid, False otherwise
    """
    allowed_values = ["L1", "L2", "L3"]
    return cost_level in allowed_values


def warning_level_mapping(warning_level: str) -> str:
    """
    预警级别映射转换
    
    Args:
        warning_level: 原始预警级别（绿/黄/红）
        
    Returns:
        转换后的预警级别（green/yellow/red）
    """
    mapping = {
        "绿": "green",
        "黄": "yellow",
        "红": "red",
        "green": "green",
        "yellow": "yellow",
        "red": "red"
    }
    return mapping.get(warning_level, warning_level)


def convert_decimal_to_float(value: Any, precision: int = 2) -> Optional[float]:
    """
    将Decimal类型转换为Float，保留指定位数
    
    Args:
        value: 输入值
        precision: 小数位数
        
    Returns:
        转换后的float值
    """
    if value is None:
        return None
    
    try:
        return round(float(value), precision)
    except (ValueError, TypeError):
        return None


def convert_to_string(value: Any) -> Optional[str]:
    """
    转换为字符串
    
    Args:
        value: 输入值
        
    Returns:
        转换后的字符串
    """
    if value is None:
        return None
    
    try:
        return str(value).strip()
    except (ValueError, TypeError):
        return None


def convert_to_int(value: Any) -> Optional[int]:
    """
    转换为整数
    
    Args:
        value: 输入值
        
    Returns:
        转换后的整数
    """
    if value is None:
        return None
    
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def convert_to_date(value: Any) -> Optional[str]:
    """
    转换为日期字符串
    
    Args:
        value: 输入值
        
    Returns:
        转换后的日期字符串（YYYY-MM-DD）
    """
    if value is None:
        return None
    
    try:
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d")
        elif isinstance(value, str):
            # 尝试解析常见日期格式
            formats = ["%Y-%m-%d", "%Y/%m/%d", "%Y%m%d", "%d/%m/%Y"]
            for fmt in formats:
                try:
                    return datetime.strptime(value, fmt).strftime("%Y-%m-%d")
                except ValueError:
                    continue
            return value
        else:
            return str(value)
    except Exception:
        return None


def convert_to_datetime(value: Any) -> Optional[str]:
    """
    转换为datetime字符串
    
    Args:
        value: 输入值
        
    Returns:
        转换后的datetime字符串（ISO格式）
    """
    if value is None:
        return None
    
    try:
        if isinstance(value, datetime):
            return value.isoformat()
        else:
            return datetime.now().isoformat()
    except Exception:
        return datetime.now().isoformat()


def validate_numeric_non_negative(value: Any) -> bool:
    """
    验证数值字段非负
    
    Args:
        value: 输入值
        
    Returns:
        True if non-negative, False otherwise
    """
    if value is None:
        return True
    
    try:
        return float(value) >= 0
    except (ValueError, TypeError):
        return False


def validate_date_key(date_key: int) -> bool:
    """
    验证date_key格式
    
    Args:
        date_key: 日期键
        
    Returns:
        True if valid, False otherwise
    """
    try:
        date_str = str(date_key)
        if len(date_str) != 8:
            return False
        
        year = int(date_str[:4])
        month = int(date_str[4:6])
        day = int(date_str[6:8])
        
        if year < 2000 or year > 2100:
            return False
        if month < 1 or month > 12:
            return False
        if day < 1 or day > 31:
            return False
        
        return True
    except Exception:
        return False


def get_current_datetime() -> str:
    """
    获取当前时间（ISO格式）
    
    Returns:
        当前datetime字符串
    """
    return datetime.now().isoformat()


def transform_field_value(
    value: Any,
    target_type: str,
    validator: Optional[str] = None,
    transform: Optional[str] = None
) -> Any:
    """
    字段值转换主函数
    
    Args:
        value: 原始值
        target_type: 目标类型
        validator: 校验器名称
        transform: 转换器名称
        
    Returns:
        转换后的值
    """
    # 执行转换
    if transform == "warning_level_mapping":
        value = warning_level_mapping(value)
    
    # 执行类型转换
    if target_type == "string":
        value = convert_to_string(value)
    elif target_type == "float":
        value = convert_decimal_to_float(value)
    elif target_type == "int":
        value = convert_to_int(value)
    elif target_type == "date":
        value = convert_to_date(value)
    elif target_type == "datetime":
        value = convert_to_datetime(value)
    
    # 执行校验
    if validator == "report_period_validator":
        if not validate_report_period(str(value)):
            raise ValueError(f"报告期间格式错误: {value}")
    elif validator == "cost_level_validator":
        if not validate_cost_level(str(value)):
            raise ValueError(f"成本层级错误: {value}")
    
    return value


def apply_field_mapping(
    source_data: Dict[str, Any],
    mappings: list
) -> Dict[str, Any]:
    """
    应用字段映射
    
    Args:
        source_data: 源数据字典
        mappings: 映射配置列表
        
    Returns:
        转换后的目标数据字典
    """
    target_data = {}
    
    for mapping in mappings:
        source_field = mapping.get("source")
        target_field = mapping.get("target")
        target_type = mapping.get("type", "string")
        required = mapping.get("required", False)
        validator = mapping.get("validator")
        transform = mapping.get("transform")
        
        # 获取源值
        value = source_data.get(source_field)
        
        # 检查必填字段
        if required and (value is None or str(value).strip() == ""):
            raise ValueError(f"必填字段 {source_field} 为空")
        
        # 应用转换
        try:
            value = transform_field_value(value, target_type, validator, transform)
        except Exception as e:
            raise ValueError(f"字段 {source_field} 转换失败: {str(e)}")
        
        target_data[target_field] = value
    
    return target_data


def apply_derived_fields(
    data: Dict[str, Any],
    derived_fields: list
) -> Dict[str, Any]:
    """
    应用派生字段计算
    
    Args:
        data: 已有数据字典
        derived_fields: 派生字段配置列表
        
    Returns:
        添加派生字段后的数据字典
    """
    for field in derived_fields:
        field_name = field.get("name")
        default = field.get("default")
        expression = field.get("expression")
        
        if expression:
            # 简单表达式计算
            try:
                if expression == "current_datetime()":
                    data[field_name] = get_current_datetime()
                elif expression == "calculate_date_key(report_period)":
                    report_period = data.get("report_period")
                    if report_period:
                        data[field_name] = calculate_date_key(report_period)
                    else:
                        data[field_name] = None
                elif "warning_level" in expression:
                    data[field_name] = data.get("warning_level")
                else:
                    data[field_name] = default
            except Exception as e:
                data[field_name] = default
        else:
            data[field_name] = default
    
    return data


def validate_data_quality(
    data: Dict[str, Any],
    table_name: str
) -> list:
    """
    执行数据质量校验
    
    Args:
        data: 数据字典
        table_name: 表名
        
    Returns:
        错误信息列表
    """
    errors = []
    
    # 通用校验
    if "project_id" in data:
        if not data["project_id"]:
            errors.append("project_id不能为空")
    
    if "report_period" in data:
        if not validate_report_period(str(data["report_period"])):
            errors.append("report_period格式错误")
    
    # 数值字段校验
    numeric_fields = [
        "cost_confirmed_acc", "cost_unconfirmed_acc", 
        "confirmed_output", "unconfirmed_output",
        "bond_amount", "penalty_amount",
        "insurance_amount", "receipt_amount",
        "settlement_amount"
    ]
    for field in numeric_fields:
        if field in data and data[field] is not None:
            if not validate_numeric_non_negative(data[field]):
                errors.append(f"{field}不能为负数")
    
    # date_key校验
    if "date_key" in data and data["date_key"]:
        if not validate_date_key(data["date_key"]):
            errors.append("date_key格式错误")
    
    # 特定表校验
    if table_name == "fact_bond":
        if data.get("bond_amount") and data.get("returned_amount") and data.get("unreturned_amount"):
            if abs(data["bond_amount"] - (data["returned_amount"] + data["unreturned_amount"])) > 0.01:
                errors.append("bond_amount不等于returned_amount+unreturned_amount")
    
    if table_name == "fact_penalty":
        if data.get("penalty_amount") and data["penalty_amount"] <= 0:
            errors.append("penalty_amount必须大于0")
    
    if table_name == "fact_project_risk":
        warning_level = data.get("warning_level")
        if warning_level and warning_level not in ["green", "yellow", "red"]:
            errors.append("warning_level必须为green/yellow/red")
    
    return errors