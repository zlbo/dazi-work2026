# Cube层设计文档（V1.0）

> **版本**：V1.0  
> **创建日期**：2026年6月12日  
> **适用范围**：潘达工程-商务成本智能决策体系  
> **前置成果**：《物理表设计文档.md》、《Object Type设计文档.md》  
> **依据规范**：《本体命名规范_物理表Cube与对象.md》§4「Cube：类别与命名」  
> **工作阶段**：阶段二 - 本体设计与确认（Step 4：本体物理表模型设计）

---

## 一、设计原则

### 1.1 Cube命名规范

> **引用**：《本体命名规范_物理表Cube与对象.md》§4.1

**命名格式**：`{主题域}{分析焦点}{Cube|Analytics}`

| 规则 | 说明 |
|------|------|
| **PascalCase** | `ProjectCostCube`、`ProjectOutputCube` |
| **后缀** | 推荐 **`Cube`**（与平台 `register_cube` 一致） |
| **禁止** | 与对象 `code` 完全相同；与物理表名相同 |
| **qualified_name** | 成员为 `CubeName.member`（如 `ProjectCostCube.cost_amount`） |

### 1.2 Cube类别定义

> **引用**：《本体命名规范_物理表Cube与对象.md》§4.2

| 类别 | 用途 | 事实源 | 命名示例 |
|------|------|--------|---------|
| **流程型 Process** | 以事务/事件为主线，多维度切片 | 主 `fact_*` | `ProjectCostCube`、`ProjectOutputCube` |
| **主体型 Subject** | 以单一业务主体聚合（项目/合同/科目） | 同一 fact 或 subject 切片 | `ProjectSalesCube`、`CostSubjectCube` |
| **对比型 Comparison** | 预实、同比口径、A/B 版本 | 多个 fact 或带 version 维 | `BudgetVsActualCube` |
| **快照型 Snapshot** | 时点库存、余额（非可加事件） | 快照 fact 或 agg | `ProjectSnapshotCube` |

### 1.3 每个Cube规划必写

| 列 | 说明 |
|------|------|
| Cube 名 | 符合 §4.1 |
| **类别** | Process / Subject / Comparison / Snapshot |
| 事实源表 | 主 `fact_*` 表名 |
| 时间维 | 是否 JOIN `dim_date`；时间成员来自哪些列 |
| 维度 | GROUP BY / 筛选字段 |
| 度量 | 列名、聚合、业务含义 |
| 派生度量 | 表达式与口径 |
| **支撑的对象类型** | 哪些对象 `bind_source` 绑定本 Cube |

---

## 二、Cube清单

| Cube 名 | 类别 | 事实源表 | 支撑的对象类型 |
|---------|------|---------|---------------|
| ProjectCostCube | Process | fact_project_cost | ProjectCost, Project |
| ProjectOutputCube | Process | fact_project_output | ProjectOutput, Project |
| PaymentCube | Process | fact_payment | Payment, Project, Contract |
| ReceivableCube | Process | fact_receivable | Receivable, Project, Contract |
| CashFlowCube | Process | fact_cash_flow | CashFlow, Project |
| RiskCube | Process | fact_risk | Risk, Project |
| ChangeOrderCube | Process | fact_change_order | ChangeOrder, Project, Contract |
| ClaimCube | Process | fact_claim | Claim, Project, Contract |
| ProjectIndicatorCube | Subject | fact_project_indicator | Indicator, Project |

---

## 三、Cube详细设计

### 3.1 ProjectCostCube（项目成本分析Cube）

**基本信息**：
```yaml
Cube 名: ProjectCostCube
类别: Process
事实源表: fact_project_cost
时间维: JOIN dim_date
```

**维度**（GROUP BY / 筛选字段）：
| 维度名 | 来源字段 | 业务含义 | 显示名 |
|--------|---------|---------|--------|
| date_key | fact_project_cost.date_key | 日期键 | 日期 |
| year | dim_date.year | 公历年 | 年 |
| quarter | dim_date.quarter | 季度 | 季度 |
| month | dim_date.month | 月 | 月 |
| year_month | dim_date.year_month | 年月 | 年月 |
| project_key | fact_project_cost.project_key | 项目唯一标识 | 项目 |
| project_code | fact_project_cost.project_code | 项目编码 | 项目编码 |
| project_name | fact_project_cost.project_name | 项目名称 | 项目名称 |
| project_type | dim_project.project_type | 项目类型 | 项目类型 |
| project_category | dim_project.project_category | 项目类别 | 项目类别 |
| business_model | dim_project.business_model | 经营模式 | 经营模式 |
| project_status | dim_project.project_status | 项目状态 | 项目状态 |
| cost_subject_key | fact_project_cost.cost_subject_key | 成本科目标识 | 成本科目 |
| subject_code | fact_project_cost.subject_code | 科目编码 | 科目编码 |
| subject_name | fact_project_cost.subject_name | 科目名称 | 科目名称 |
| subject_level | fact_project_cost.subject_level | 科目层级 | 科目层级 |
| cost_type | fact_project_cost.cost_type | 成本类型 | 成本类型 |
| contract_key | fact_project_cost.contract_key | 合同唯一标识 | 合同 |
| contract_code | dim_contract.contract_code | 合同编码 | 合同编码 |
| contract_name | dim_contract.contract_name | 合同名称 | 合同名称 |
| region_key | fact_project_cost.region_key | 地区标识 | 地区 |
| organization_key | fact_project_cost.organization_key | 组织标识 | 组织 |

**度量**（列名、聚合、业务含义）：
| 度量名 | 聚合 | 业务含义 | 数据类型 |
|--------|------|---------|---------|
| cost_amount | SUM | 成本金额 | Decimal(18,2) |
| cost_count | COUNT | 成本记录数 | Int64 |

**派生度量**（表达式与口径）：
| 派生度量名 | 表达式 | 业务含义 | 数据类型 |
|-----------|--------|---------|---------|
| cost_amount_avg | cost_amount / cost_count | 平均成本金额 | Decimal(18,2) |
| cost_ratio_by_subject | cost_amount / SUM(cost_amount) OVER (PARTITION BY cost_subject_key) | 科目成本占比 | Decimal(5,4) |
| cost_ratio_by_project | cost_amount / SUM(cost_amount) OVER (PARTITION BY project_key) | 项目成本占比 | Decimal(5,4) |

**支撑的对象类型**：
| 对象类型 | bind_source映射 |
|---------|----------------|
| ProjectCost | 直接绑定，属性映射到Cube维度和度量 |
| Project | 通过project_key关联，聚合维度和度量 |

---

### 3.2 ProjectOutputCube（项目产值分析Cube）

**基本信息**：
```yaml
Cube 名: ProjectOutputCube
类别: Process
事实源表: fact_project_output
时间维: JOIN dim_date
```

**维度**（GROUP BY / 筛选字段）：
| 维度名 | 来源字段 | 业务含义 | 显示名 |
|--------|---------|---------|--------|
| date_key | fact_project_output.date_key | 日期键 | 日期 |
| year | dim_date.year | 公历年 | 年 |
| quarter | dim_date.quarter | 季度 | 季度 |
| month | dim_date.month | 月 | 月 |
| year_month | dim_date.year_month | 年月 | 年月 |
| project_key | fact_project_output.project_key | 项目唯一标识 | 项目 |
| project_code | fact_project_output.project_code | 项目编码 | 项目编码 |
| project_name | fact_project_output.project_name | 项目名称 | 项目名称 |
| project_type | dim_project.project_type | 项目类型 | 项目类型 |
| project_category | dim_project.project_category | 项目类别 | 项目类别 |
| business_model | dim_project.business_model | 经营模式 | 经营模式 |
| project_status | dim_project.project_status | 项目状态 | 项目状态 |
| output_type | fact_project_output.output_type | 产值类型 | 产值类型 |
| confirmation_status | fact_project_output.confirmation_status | 确认状态 | 确认状态 |
| contract_key | fact_project_output.contract_key | 合同唯一标识 | 合同 |
| contract_code | dim_contract.contract_code | 合同编码 | 合同编码 |
| contract_name | dim_contract.contract_name | 合同名称 | 合同名称 |
| region_key | fact_project_output.region_key | 地区标识 | 地区 |
| organization_key | fact_project_output.organization_key | 组织标识 | 组织 |

**度量**（列名、聚合、业务含义）：
| 度量名 | 聚合 | 业务含义 | 数据类型 |
|--------|------|---------|---------|
| output_amount | SUM | 产值金额 | Decimal(18,2) |
| output_count | COUNT | 产值记录数 | Int64 |

**派生度量**（表达式与口径）：
| 派生度量名 | 表达式 | 业务含义 | 数据类型 |
|-----------|--------|---------|---------|
| confirmed_output_amount | SUM(CASE WHEN confirmation_status = '已确认' THEN output_amount ELSE 0 END) | 已确认产值 | Decimal(18,2) |
| unconfirmed_output_amount | SUM(CASE WHEN confirmation_status = '待确认' THEN output_amount ELSE 0 END) | 待确认产值 | Decimal(18,2) |
| output_confirm_ratio | confirmed_output_amount / output_amount | 产值确权比 | Decimal(5,4) |
| output_amount_avg | output_amount / output_count | 平均产值金额 | Decimal(18,2) |

**支撑的对象类型**：
| 对象类型 | bind_source映射 |
|---------|----------------|
| ProjectOutput | 直接绑定，属性映射到Cube维度和度量 |
| Project | 通过project_key关联，聚合维度和度量 |

---

### 3.3 PaymentCube（付款分析Cube）

**基本信息**：
```yaml
Cube 名: PaymentCube
类别: Process
事实源表: fact_payment
时间维: JOIN dim_date
```

**维度**（GROUP BY / 筛选字段）：
| 维度名 | 来源字段 | 业务含义 | 显示名 |
|--------|---------|---------|--------|
| date_key | fact_payment.date_key | 日期键 | 日期 |
| year | dim_date.year | 公历年 | 年 |
| quarter | dim_date.quarter | 季度 | 季度 |
| month | dim_date.month | 月 | 月 |
| year_month | dim_date.year_month | 年月 | 年月 |
| project_key | fact_payment.project_key | 项目唯一标识 | 项目 |
| project_code | fact_payment.project_code | 项目编码 | 项目编码 |
| project_name | fact_payment.project_name | 项目名称 | 项目名称 |
| contract_key | fact_payment.contract_key | 合同唯一标识 | 合同 |
| contract_code | fact_payment.contract_code | 合同编码 | 合同编码 |
| contract_name | fact_payment.contract_name | 合同名称 | 合同名称 |
| payment_type | fact_payment.payment_type | 付款类型 | 付款类型 |
| payment_status | fact_payment.payment_status | 付款状态 | 付款状态 |
| supplier_key | fact_payment.supplier_key | 供应商标识 | 供应商 |
| supplier_name | fact_payment.supplier_name | 供应商名称 | 供应商名称 |
| region_key | fact_payment.region_key | 地区标识 | 地区 |
| organization_key | fact_payment.organization_key | 组织标识 | 组织 |

**度量**（列名、聚合、业务含义）：
| 度量名 | 聚合 | 业务含义 | 数据类型 |
|--------|------|---------|---------|
| payment_amount | SUM | 付款金额 | Decimal(18,2) |
| payment_count | COUNT | 付款记录数 | Int64 |

**派生度量**（表达式与口径）：
| 派生度量名 | 表达式 | 业务含义 | 数据类型 |
|-----------|--------|---------|---------|
| approved_payment_amount | SUM(CASE WHEN payment_status = '已批准' THEN payment_amount ELSE 0 END) | 已批准付款 | Decimal(18,2) |
| paid_payment_amount | SUM(CASE WHEN payment_status = '已支付' THEN payment_amount ELSE 0 END) | 已支付付款 | Decimal(18,2) |
| payment_amount_avg | payment_amount / payment_count | 平均付款金额 | Decimal(18,2) |

**支撑的对象类型**：
| 对象类型 | bind_source映射 |
|---------|----------------|
| Payment | 直接绑定，属性映射到Cube维度和度量 |
| Project | 通过project_key关联，聚合维度和度量 |
| Contract | 通过contract_key关联，聚合维度和度量 |

---

### 3.4 ReceivableCube（应收账款分析Cube）

**基本信息**：
```yaml
Cube 名: ReceivableCube
类别: Process
事实源表: fact_receivable
时间维: JOIN dim_date
```

**维度**（GROUP BY / 筛选字段）：
| 维度名 | 来源字段 | 业务含义 | 显示名 |
|--------|---------|---------|--------|
| date_key | fact_receivable.date_key | 日期键 | 日期 |
| year | dim_date.year | 公历年 | 年 |
| quarter | dim_date.quarter | 季度 | 季度 |
| month | dim_date.month | 月 | 月 |
| year_month | dim_date.year_month | 年月 | 年月 |
| project_key | fact_receivable.project_key | 项目唯一标识 | 项目 |
| project_code | fact_receivable.project_code | 项目编码 | 项目编码 |
| project_name | fact_receivable.project_name | 项目名称 | 项目名称 |
| contract_key | fact_receivable.contract_key | 合同唯一标识 | 合同 |
| contract_code | fact_receivable.contract_code | 合同编码 | 合同编码 |
| contract_name | fact_receivable.contract_name | 合同名称 | 合同名称 |
| receivable_status | fact_receivable.receivable_status | 应收状态 | 应收状态 |
| region_key | fact_receivable.region_key | 地区标识 | 地区 |
| organization_key | fact_receivable.organization_key | 组织标识 | 组织 |

**度量**（列名、聚合、业务含义）：
| 度量名 | 聚合 | 业务含义 | 数据类型 |
|--------|------|---------|---------|
| receivable_amount | SUM | 应收金额 | Decimal(18,2) |
| received_amount | SUM | 已收金额 | Decimal(18,2) |
| outstanding_amount | SUM | 未收金额 | Decimal(18,2) |
| receivable_count | COUNT | 应收记录数 | Int64 |

**派生度量**（表达式与口径）：
| 派生度量名 | 表达式 | 业务含义 | 数据类型 |
|-----------|--------|---------|---------|
| receivable_ratio | received_amount / receivable_amount | 应收回收率 | Decimal(5,4) |
| overdue_receivable_amount | SUM(CASE WHEN receivable_status = '逾期' THEN outstanding_amount ELSE 0 END) | 逾期应收金额 | Decimal(18,2) |
| bad_debt_amount | SUM(CASE WHEN receivable_status = '坏账' THEN outstanding_amount ELSE 0 END) | 坏账金额 | Decimal(18,2) |

**支撑的对象类型**：
| 对象类型 | bind_source映射 |
|---------|----------------|
| Receivable | 直接绑定，属性映射到Cube维度和度量 |
| Project | 通过project_key关联，聚合维度和度量 |
| Contract | 通过contract_key关联，聚合维度和度量 |

---

### 3.5 CashFlowCube（现金流分析Cube）

**基本信息**：
```yaml
Cube 名: CashFlowCube
类别: Process
事实源表: fact_cash_flow
时间维: JOIN dim_date
```

**维度**（GROUP BY / 筛选字段）：
| 维度名 | 来源字段 | 业务含义 | 显示名 |
|--------|---------|---------|--------|
| date_key | fact_cash_flow.date_key | 日期键 | 日期 |
| year | dim_date.year | 公历年 | 年 |
| quarter | dim_date.quarter | 季度 | 季度 |
| month | dim_date.month | 月 | 月 |
| year_month | dim_date.year_month | 年月 | 年月 |
| project_key | fact_cash_flow.project_key | 项目唯一标识 | 项目 |
| project_code | fact_cash_flow.project_code | 项目编码 | 项目编码 |
| project_name | fact_cash_flow.project_name | 项目名称 | 项目名称 |
| cash_flow_type | fact_cash_flow.cash_flow_type | 现金流类型 | 现金流类型 |
| cash_flow_category | fact_cash_flow.cash_flow_category | 现金流分类 | 现金流分类 |
| approval_status | fact_cash_flow.approval_status | 审批状态 | 审批状态 |
| region_key | fact_cash_flow.region_key | 地区标识 | 地区 |
| organization_key | fact_cash_flow.organization_key | 组织标识 | 组织 |

**度量**（列名、聚合、业务含义）：
| 度量名 | 聚合 | 业务含义 | 数据类型 |
|--------|------|---------|---------|
| cash_flow_amount | SUM | 现金流金额 | Decimal(18,2) |
| cash_flow_count | COUNT | 现金流记录数 | Int64 |

**派生度量**（表达式与口径）：
| 派生度量名 | 表达式 | 业务含义 | 数据类型 |
|-----------|--------|---------|---------|
| income_amount | SUM(CASE WHEN cash_flow_type = '收入' THEN cash_flow_amount ELSE 0 END) | 收入金额 | Decimal(18,2) |
| expense_amount | SUM(CASE WHEN cash_flow_type = '支出' THEN cash_flow_amount ELSE 0 END) | 支出金额 | Decimal(18,2) |
| net_cash_flow | income_amount - expense_amount | 净现金流 | Decimal(18,2) |
| approved_cash_flow_amount | SUM(CASE WHEN approval_status = '已批复' THEN cash_flow_amount ELSE 0 END) | 已批复现金流 | Decimal(18,2) |

**支撑的对象类型**：
| 对象类型 | bind_source映射 |
|---------|----------------|
| CashFlow | 直接绑定，属性映射到Cube维度和度量 |
| Project | 通过project_key关联，聚合维度和度量 |

---

### 3.6 RiskCube（风险分析Cube）

**基本信息**：
```yaml
Cube 名: RiskCube
类别: Process
事实源表: fact_risk
时间维: JOIN dim_date
```

**维度**（GROUP BY / 筛选字段）：
| 维度名 | 来源字段 | 业务含义 | 显示名 |
|--------|---------|---------|--------|
| date_key | fact_risk.date_key | 日期键 | 日期 |
| year | dim_date.year | 公历年 | 年 |
| quarter | dim_date.quarter | 季度 | 季度 |
| month | dim_date.month | 月 | 月 |
| year_month | dim_date.year_month | 年月 | 年月 |
| project_key | fact_risk.project_key | 项目唯一标识 | 项目 |
| project_code | fact_risk.project_code | 项目编码 | 项目编码 |
| project_name | fact_risk.project_name | 项目名称 | 项目名称 |
| risk_type | fact_risk.risk_type | 风险类型 | 风险类型 |
| risk_level_key | fact_risk.risk_level_key | 风险等级标识 | 风险等级 |
| risk_level | fact_risk.risk_level | 风险等级 | 风险等级 |
| region_key | fact_risk.region_key | 地区标识 | 地区 |
| organization_key | fact_risk.organization_key | 组织标识 | 组织 |

**度量**（列名、聚合、业务含义）：
| 度量名 | 聚合 | 业务含义 | 数据类型 |
|--------|------|---------|---------|
| risk_count | COUNT | 风险记录数 | Int64 |
| risk_value_avg | AVG | 平均风险值(%) | Decimal(5,2) |

**派生度量**（表达式与口径）：
| 派生度量名 | 表达式 | 业务含义 | 数据类型 |
|-----------|--------|---------|---------|
| high_risk_count | COUNT(CASE WHEN risk_level = '严重' THEN 1 END) | 高风险数量 | Int64 |
| medium_risk_count | COUNT(CASE WHEN risk_level = '预警' THEN 1 END) | 中风险数量 | Int64 |
| low_risk_count | COUNT(CASE WHEN risk_level = '正常' THEN 1 END) | 低风险数量 | Int64 |
| risk_ratio | high_risk_count / risk_count | 高风险占比 | Decimal(5,4) |

**支撑的对象类型**：
| 对象类型 | bind_source映射 |
|---------|----------------|
| Risk | 直接绑定，属性映射到Cube维度和度量 |
| Project | 通过project_key关联，聚合维度和度量 |

---

### 3.7 ChangeOrderCube（变更签证分析Cube）

**基本信息**：
```yaml
Cube 名: ChangeOrderCube
类别: Process
事实源表: fact_change_order
时间维: JOIN dim_date
```

**维度**（GROUP BY / 筛选字段）：
| 维度名 | 来源字段 | 业务含义 | 显示名 |
|--------|---------|---------|--------|
| date_key | fact_change_order.date_key | 日期键 | 日期 |
| year | dim_date.year | 公历年 | 年 |
| quarter | dim_date.quarter | 季度 | 季度 |
| month | dim_date.month | 月 | 月 |
| year_month | dim_date.year_month | 年月 | 年月 |
| project_key | fact_change_order.project_key | 项目唯一标识 | 项目 |
| project_code | fact_change_order.project_code | 项目编码 | 项目编码 |
| project_name | fact_change_order.project_name | 项目名称 | 项目名称 |
| contract_key | fact_change_order.contract_key | 合同唯一标识 | 合同 |
| contract_code | fact_change_order.contract_code | 合同编码 | 合同编码 |
| contract_name | fact_change_order.contract_name | 合同名称 | 合同名称 |
| change_type | fact_change_order.change_type | 变更类型 | 变更类型 |
| approval_status | fact_change_order.approval_status | 审批状态 | 审批状态 |
| region_key | fact_change_order.region_key | 地区标识 | 地区 |
| organization_key | fact_change_order.organization_key | 组织标识 | 组织 |

**度量**（列名、聚合、业务含义）：
| 度量名 | 聚合 | 业务含义 | 数据类型 |
|--------|------|---------|---------|
| change_amount | SUM | 变更金额 | Decimal(18,2) |
| change_count | COUNT | 变更记录数 | Int64 |

**派生度量**（表达式与口径）：
| 派生度量名 | 表达式 | 业务含义 | 数据类型 |
|-----------|--------|---------|---------|
| approved_change_amount | SUM(CASE WHEN approval_status = '已批准' THEN change_amount ELSE 0 END) | 已批准变更金额 | Decimal(18,2) |
| change_amount_avg | change_amount / change_count | 平均变更金额 | Decimal(18,2) |

**支撑的对象类型**：
| 对象类型 | bind_source映射 |
|---------|----------------|
| ChangeOrder | 直接绑定，属性映射到Cube维度和度量 |
| Project | 通过project_key关联，聚合维度和度量 |
| Contract | 通过contract_key关联，聚合维度和度量 |

---

### 3.8 ClaimCube（索赔分析Cube）

**基本信息**：
```yaml
Cube 名: ClaimCube
类别: Process
事实源表: fact_claim
时间维: JOIN dim_date
```

**维度**（GROUP BY / 筛选字段）：
| 维度名 | 来源字段 | 业务含义 | 显示名 |
|--------|---------|---------|--------|
| date_key | fact_claim.date_key | 日期键 | 日期 |
| year | dim_date.year | 公历年 | 年 |
| quarter | dim_date.quarter | 季度 | 季度 |
| month | dim_date.month | 月 | 月 |
| year_month | dim_date.year_month | 年月 | 年月 |
| project_key | fact_claim.project_key | 项目唯一标识 | 项目 |
| project_code | fact_claim.project_code | 项目编码 | 项目编码 |
| project_name | fact_claim.project_name | 项目名称 | 项目名称 |
| contract_key | fact_claim.contract_key | 合同唯一标识 | 合同 |
| contract_code | fact_claim.contract_code | 合同编码 | 合同编码 |
| contract_name | fact_claim.contract_name | 合同名称 | 合同名称 |
| claim_type | fact_claim.claim_type | 索赔类型 | 索赔类型 |
| approval_status | fact_claim.approval_status | 审批状态 | 审批状态 |
| region_key | fact_claim.region_key | 地区标识 | 地区 |
| organization_key | fact_claim.organization_key | 组织标识 | 组织 |

**度量**（列名、聚合、业务含义）：
| 度量名 | 聚合 | 业务含义 | 数据类型 |
|--------|------|---------|---------|
| claim_amount | SUM | 索赔金额 | Decimal(18,2) |
| claim_count | COUNT | 索赔记录数 | Int64 |

**派生度量**（表达式与口径）：
| 派生度量名 | 表达式 | 业务含义 | 数据类型 |
|-----------|--------|---------|---------|
| approved_claim_amount | SUM(CASE WHEN approval_status = '已批准' THEN claim_amount ELSE 0 END) | 已批准索赔金额 | Decimal(18,2) |
| claim_amount_avg | claim_amount / claim_count | 平均索赔金额 | Decimal(18,2) |

**支撑的对象类型**：
| 对象类型 | bind_source映射 |
|---------|----------------|
| Claim | 直接绑定，属性映射到Cube维度和度量 |
| Project | 通过project_key关联，聚合维度和度量 |
| Contract | 通过contract_key关联，聚合维度和度量 |

---

### 3.9 ProjectIndicatorCube（项目指标分析Cube）

**基本信息**：
```yaml
Cube 名: ProjectIndicatorCube
类别: Subject
事实源表: fact_project_indicator
时间维: JOIN dim_date
```

**维度**（GROUP BY / 筛选字段）：
| 维度名 | 来源字段 | 业务含义 | 显示名 |
|--------|---------|---------|--------|
| date_key | fact_project_indicator.date_key | 日期键 | 日期 |
| year | dim_date.year | 公历年 | 年 |
| quarter | dim_date.quarter | 季度 | 季度 |
| month | dim_date.month | 月 | 月 |
| year_month | dim_date.year_month | 年月 | 年月 |
| project_key | fact_project_indicator.project_key | 项目唯一标识 | 项目 |
| project_code | fact_project_indicator.project_code | 项目编码 | 项目编码 |
| project_name | fact_project_indicator.project_name | 项目名称 | 项目名称 |
| project_type | dim_project.project_type | 项目类型 | 项目类型 |
| project_category | dim_project.project_category | 项目类别 | 项目类别 |
| business_model | dim_project.business_model | 经营模式 | 经营模式 |
| project_status | dim_project.project_status | 项目状态 | 项目状态 |
| region_key | fact_project_indicator.region_key | 地区标识 | 地区 |
| organization_key | fact_project_indicator.organization_key | 组织标识 | 组织 |

**度量**（列名、聚合、业务含义）：
| 度量名 | 聚合 | 业务含义 | 数据类型 |
|--------|------|---------|---------|
| total_output | SUM | 累计产值 | Decimal(18,2) |
| total_cost | SUM | 累计成本 | Decimal(18,2) |
| profit | SUM | 项目利润 | Decimal(18,2) |
| profit_rate_avg | AVG | 平均利润率(%) | Decimal(5,4) |
| cost_rigidity_avg | AVG | 平均成本刚性度(%) | Decimal(5,4) |
| output_confirm_ratio_avg | AVG | 平均产值确权比(%) | Decimal(5,4) |
| cost_deviation_rate_avg | AVG | 平均成本偏差率(%) | Decimal(5,4) |
| schedule_deviation_rate_avg | AVG | 平均进度偏差率(%) | Decimal(5,4) |

**派生度量**（表达式与口径）：
| 派生度量名 | 表达式 | 业务含义 | 数据类型 |
|-----------|--------|---------|---------|
| profit_margin | profit / total_output | 利润率 | Decimal(5,4) |
| cost_output_ratio | total_cost / total_output | 成本产值比 | Decimal(5,4) |

**支撑的对象类型**：
| 对象类型 | bind_source映射 |
|---------|----------------|
| Indicator | 直接绑定，属性映射到Cube维度和度量 |
| Project | 通过project_key关联，聚合维度和度量 |

---

## 四、平台分类

> **引用**：《本体规划指南》§91「平台分类（平台分类对齐 · 强制）」

### 4.1 Cube平台分类

| Cube 名 | 平台分类 | 说明 |
|---------|---------|------|
| ProjectCostCube | 流程型 | 成本流程分析 |
| ProjectOutputCube | 流程型 | 产值流程分析 |
| PaymentCube | 流程型 | 付款流程分析 |
| ReceivableCube | 流程型 | 应收账款流程分析 |
| CashFlowCube | 流程型 | 现金流流程分析 |
| RiskCube | 流程型 | 风险流程分析 |
| ChangeOrderCube | 流程型 | 变更签证流程分析 |
| ClaimCube | 流程型 | 索赔流程分析 |
| ProjectIndicatorCube | 主体型 | 项目指标主体分析 |

---

## 五、Cube与Object Type绑定关系（bind_source）

> **核心要求**：每个分析对象必须在Cube层有明确读模型，通过 `bind_source` 绑定

### 5.1 绑定关系清单

| Object Type | 绑定Cube | 绑定方式 | 属性映射说明 |
|-------------|---------|---------|-------------|
| Project | ProjectIndicatorCube | 间接绑定 | 通过project_key关联，聚合维度和度量 |
| Contract | PaymentCube, ReceivableCube, ChangeOrderCube, ClaimCube | 间接绑定 | 通过contract_key关联，聚合维度和度量 |
| ProjectCost | ProjectCostCube | 直接绑定 | 属性直接映射到Cube维度和度量 |
| ProjectOutput | ProjectOutputCube | 直接绑定 | 属性直接映射到Cube维度和度量 |
| Payment | PaymentCube | 直接绑定 | 属性直接映射到Cube维度和度量 |
| Receivable | ReceivableCube | 直接绑定 | 属性直接映射到Cube维度和度量 |
| CashFlow | CashFlowCube | 直接绑定 | 属性直接映射到Cube维度和度量 |
| Risk | RiskCube | 直接绑定 | 属性直接映射到Cube维度和度量 |
| ChangeOrder | ChangeOrderCube | 直接绑定 | 属性直接映射到Cube维度和度量 |
| Claim | ClaimCube | 直接绑定 | 属性直接映射到Cube维度和度量 |
| Indicator | ProjectIndicatorCube | 直接绑定 | 属性直接映射到Cube维度和度量 |

### 5.2 绑定方式说明

**直接绑定**：
- Object Type与Cube一对一映射
- Object Type属性直接映射到Cube维度和度量
- 示例：`ProjectCost` → `ProjectCostCube`

**间接绑定**：
- Object Type通过外键关联到Cube
- 需要在函数SQL中进行JOIN操作
- 示例：`Project` → `ProjectIndicatorCube`（通过project_key关联）

---

## 六、附录

### 6.1 Cube清单汇总

| 类别 | Cube 名 | 数量 |
|------|---------|------|
| 流程型 | ProjectCostCube, ProjectOutputCube, PaymentCube, ReceivableCube, CashFlowCube, RiskCube, ChangeOrderCube, ClaimCube | 8 |
| 主体型 | ProjectIndicatorCube | 1 |
| **合计** | - | **9** |

### 6.2 与物理表对照

| Cube 名 | 事实源表 | 维度表 |
|---------|---------|--------|
| ProjectCostCube | fact_project_cost | dim_date, dim_project, dim_cost_subject, dim_contract, dim_region, dim_organization |
| ProjectOutputCube | fact_project_output | dim_date, dim_project, dim_contract, dim_region, dim_organization |
| PaymentCube | fact_payment | dim_date, dim_project, dim_contract, dim_region, dim_organization |
| ReceivableCube | fact_receivable | dim_date, dim_project, dim_contract, dim_region, dim_organization |
| CashFlowCube | fact_cash_flow | dim_date, dim_project, dim_region, dim_organization |
| RiskCube | fact_risk | dim_date, dim_project, dim_risk_level, dim_region, dim_organization |
| ChangeOrderCube | fact_change_order | dim_date, dim_project, dim_contract, dim_region, dim_organization |
| ClaimCube | fact_claim | dim_date, dim_project, dim_contract, dim_region, dim_organization |
| ProjectIndicatorCube | fact_project_indicator | dim_date, dim_project, dim_region, dim_organization |

---

**版本**：V1.0  
**创建日期**：2026年6月12日  
**下一步**：更新本体设计确认文档