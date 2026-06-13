# Object Type 设计文档（V2.0）

> **版本**：V2.0（基于阶段一成果全面优化）  
> **创建日期**：2026年6月12日  
> **适用范围**：潘达工程-商务成本智能决策体系  
> **前置成果**：《核心实体清单.md》、《业务概念本体化预研总览.md》、《维度识别清单.md》  
> **依据规范**：《040-本体设计方法.md》、《000-顶层设计.md》（编码标准规范）  
> **工作阶段**：阶段二 - 本体设计与确认（Step 4：本体物理表模型设计）  
> **优化说明**：基于阶段一成果全面检查，补充遗漏的维度属性，确保设计完整性

---

## 一、设计原则与方法

### 1.1 设计原则

> **引用**：《000-顶层设计.md》§1.6「编码标准规范」

**核心原则**：
- **结构编码通识优先**：Object Type命名采用行业标准编码
- **属性值专识优先**：具体业务术语采用企业实际用语
- **相对理想型策略**：先设计理想版本，后续根据实际资源优化
- **完整性原则**：充分利用阶段一所有成果，不遗漏关键维度

### 1.2 设计方法

> **引用**：《040-本体设计方法.md》§三「Object Type 设计」

**设计流程**：
1. 基于核心实体清单识别核心实体
2. 定义实体属性（核心属性、外键属性、派生属性、维度属性）
3. 定义实体分类（Master、Transaction、Analytical）
4. 定义数据来源标记
5. **验证阶段一成果覆盖率**（新增）

### 1.3 Object Type 分类

| 分类 | 说明 | 特征 | 示例 |
|------|------|------|------|
| **Master** | 主数据，相对稳定 | 变化频率低，长期有效 | Project、Contract、Organization |
| **Transaction** | 交易数据，频繁变化 | 变化频率高，记录业务活动 | ProjectCost、Payment、Receipt |
| **Analytical** | 分析实体，用于分析 | 派生计算，支撑决策 | Indicator、Risk、AlertRecord |

---

## 二、核心 Object Type 设计

### 2.1 项目域 Object Type

#### OT001：Project（项目）

**基本信息**：
```yaml
Object Type: Project
Display Name: 项目
Description: 具有独立立项编号的建筑工程项目，是成本核算和绩效评估的基本单元
Classification: Master
Source Type: 行业通用知识 + 企业业务素材
```

**核心属性**（完整覆盖阶段一成果）：
| 属性名 | 数据类型 | 业务含义 | 约束 | 来源 | 说明 |
|-------|---------|---------|------|------|------|
| project_key | string | 项目唯一标识 | PK | 系统生成 | - |
| project_code | string | 项目编码 | UK, NOT NULL | 企业业务素材 | - |
| project_name | string | 项目名称 | NOT NULL | 企业业务素材 | - |
| **project_type** | string | 项目类型 | NOT NULL | 企业业务素材 | EPC/PPP/施工总承包/专业承包等 |
| **project_category** | string | 项目类别 | NOT NULL | 企业业务素材 | 房建/市政/公路/水利/铁路等 |
| **business_model** | string | 经营模式 | - | 企业业务素材 | 直营/联营/合伙/代建/托管 |
| contract_amount | decimal(18,2) | 合同金额 | ≥0 | 企业业务素材 | - |
| contract_amount_net | decimal(18,2) | 合同金额（不含暂列等） | ≥0 | 企业业务素材 | 来自维度识别清单 |
| management_fee_rate | decimal(5,4) | 管理费率(%) | [0, 1] | 企业业务素材 | 来自维度识别清单 |
| project_status_key | string | 项目状态标识 | FK→dim_project_status, NOT NULL | 企业业务素材 | - |
| start_date | date | 开工日期 | - | 企业业务素材 | - |
| end_date | date | 竣工日期 | - | 企业业务素材 | - |
| plan_start_date | date | 计划开工日期 | - | 企业业务素材 | 来自核心实体清单 |
| plan_end_date | date | 计划竣工日期 | - | 企业业务素材 | 来自核心实体清单 |
| region_key | string | 地区标识 | FK→dim_region | 行业通用知识 | - |
| organization_key | string | 组织标识 | FK→dim_organization | 企业业务素材 | - |
| project_manager | string | 项目经理 | - | 企业业务素材 | 来自核心实体清单 |
| is_key_client | boolean | 是否大客户项目 | - | 企业业务素材 | 来自维度识别清单 |
| is_new_increment | boolean | 是否增量项目 | - | 企业业务素材 | 来自维度识别清单 |
| engineering_scale | string | 工程规模 | - | 企业业务素材 | 来自维度识别清单 |
| partner_info | string | 合伙人信息 | - | 企业业务素材 | 来自维度识别清单 |
| client_system | string | 客户体系 | FK→dim_client | 企业业务素材 | 来自维度识别清单 |

**外键属性**：
| 属性名 | 关联维度表 | 关系说明 | 来源 |
|-------|-----------|---------|------|
| project_status_key | dim_project_status | 项目生命周期状态 | 维度识别清单 |
| region_key | dim_region | 项目所在地区 | 维度识别清单 |
| organization_key | dim_organization | 项目负责组织 | 维度识别清单 |
| client_system | dim_client | 客户体系分类 | 维度识别清单 |
| business_model_key | dim_cooperation | 经营模式（与核心属性business_model对应） | 维度识别清单 |

**派生属性**：
| 属性名 | 计算规则 | 数据类型 | 业务含义 |
|-------|---------|---------|---------|
| total_output | Σ(ProjectOutput.total_amount) WHERE project_key = ? | decimal(18,2) | 累计产值 |
| total_cost | Σ(ProjectCost.total_amount) WHERE project_key = ? | decimal(18,2) | 累计成本 |
| profit | total_output - total_cost | decimal(18,2) | 项目利润 |
| profit_rate | profit / total_output | decimal(5,4) | 利润率 |
| cost_rigidity | 已确成本 / total_cost | decimal(5,4) | 成本刚性度（≥95%正常） |
| output_confirm_ratio | 已确产值 / total_output | decimal(5,4) | 产值确权比（≥85%正常） |
| cost_deviation_rate | (total_cost - target_cost) / target_cost | decimal(5,4) | 成本偏差率 |
| schedule_deviation_rate | (实际进度 - 计划进度) / 计划进度 | decimal(5,4) | 进度偏差率 |

**维度属性**（完整覆盖阶段一维度识别成果）：
| 属性名 | 关联维度表 | 用途说明 | 来源 |
|-------|-----------|---------|------|
| project_type_key | dim_project_category | 项目类型分类（EPC/PPP等） | 维度识别清单 |
| project_category_key | dim_project_category | 项目类别分类（房建/市政等） | 维度识别清单 |
| business_model_key | dim_cooperation | 经营模式（直营/联营等） | 维度识别清单 |
| client_key | dim_client | 客户体系（大客户标识） | 维度识别清单 |
| region_key | dim_region | 地区维度（行政层级） | 维度识别清单 |
| organization_key | dim_organization | 组织维度（集团/子公司等） | 维度识别清单 |

**业务规则**：
- **计算规则**：
  - CR001：利润率 = (total_output - total_cost) / total_output
  - CR002：成本刚性度 = 已确成本 / total_cost（≥95%为正常）
  - CR003：产值确权比 = 已确产值 / total_output（≥85%为正常）
  - CR004：成本偏差率 = (total_cost - target_cost) / target_cost（>5%预警）
- **约束条件**：
  - CC001：合同金额 ≥ 0
  - CC002：竣工日期 ≥ 开工日期
  - CC003：管理费率 ∈ [0, 1]
- **数据标准**：
  - DS001：金额保留2位小数
  - DS002：百分比保留4位小数
  - DS003：日期格式 YYYY-MM-DD

---

#### OT002：Contract（合同）

**基本信息**：
```yaml
Object Type: Contract
Display Name: 合同
Description: 与业主或供应商签订的具有法律效力的协议，定义了甲乙双方的权责
Classification: Master
Source Type: 行业通用知识 + 企业业务素材
```

**核心属性**：
| 属性名 | 数据类型 | 业务含义 | 约束 | 来源 |
|-------|---------|---------|------|------|
| contract_key | string | 合同唯一标识 | PK | 系统生成 |
| contract_code | string | 合同编码 | UK, NOT NULL | 企业业务素材 |
| contract_name | string | 合同名称 | NOT NULL | 企业业务素材 |
| contract_content | string | 合同内容摘要 | - | 企业业务素材 |
| contract_amount | decimal(18,2) | 合同金额 | ≥0 | 企业业务素材 |
| tax_rate | decimal(5,4) | 税率 | [0, 0.13] | 企业业务素材 |
| payment_ratio | decimal(5,4) | 付款比例 | [0, 1] | 企业业务素材 |
| sign_date | date | 签订日期 | NOT NULL | 企业业务素材 |
| valid_period | int | 有效期限(天) | >0 | 企业业务素材 |
| contract_type_key | string | 合同类型标识 | FK→dim_contract_type, NOT NULL | 行业通用知识 |
| party_a_key | string | 甲方标识 | FK→dim_owner | 企业业务素材 |
| party_b_key | string | 乙方标识 | FK→dim_contractor | 企业业务素材 |
| settlement_status_key | string | 结算状态标识 | FK→dim_settlement_status | 企业业务素材 |

**外键属性**：
| 属性名 | 关联维度表 | 关系说明 |
|-------|-----------|---------|
| contract_type_key | dim_contract_type | 合同类型分类 |
| party_a_key | dim_owner | 合同甲方（业主） |
| party_b_key | dim_contractor | 合同乙方（承包商） |
| settlement_status_key | dim_settlement_status | 结算办理状态 |

**派生属性**：
| 属性名 | 计算规则 | 数据类型 | 业务含义 |
|-------|---------|---------|---------|
| total_payment | Σ(Payment.payment_amount) WHERE contract_key = ? | decimal(18,2) | 累计付款 |
| payment_ratio_actual | total_payment / contract_amount | decimal(5,4) | 实际付款比例 |
| retention_amount | contract_amount × 质保金比例 | decimal(18,2) | 质保金金额 |
| payable_amount | contract_amount - total_payment | decimal(18,2) | 应付余额 |

**业务规则**：
- **计算规则**：
  - CR005：付款比例 = total_payment / contract_amount
  - CR006：质保金金额 = contract_amount × 质保金比例（通常5%-10%）
- **约束条件**：
  - CC004：累计付款 ≤ 合同金额 × 付款比例（BR-C001）
  - CC005：税率 ∈ {0, 0.03, 0.09, 0.13}
- **勾稽关系**：
  - RR001：含税金额 = 不含税金额 × (1 + 税率)（CR-I013）
- **状态流转**：
  - BR-S002：签订 → 执行 → 完成 → 结算 → 归档

---

#### OT003：TargetCost（目标成本）

**基本信息**：
```yaml
Object Type: TargetCost
Display Name: 目标成本
Description: 项目的目标成本基准，用于成本控制参照
Classification: Transaction
Source Type: 企业业务素材
```

**核心属性**：
| 属性名 | 数据类型 | 业务含义 | 约束 | 来源 |
|-------|---------|---------|------|------|
| target_cost_key | string | 目标成本唯一标识 | PK | 系统生成 |
| project_key | string | 项目标识 | FK→Project, NOT NULL | 企业业务素材 |
| target_amount | decimal(18,2) | 目标成本金额 | ≥0 | 企业业务素材 |
| direct_cost | decimal(18,2) | 直接成本 | ≥0 | 企业业务素材 |
| indirect_cost | decimal(18,2) | 间接成本 | ≥0 | 企业业务素材 |
| financial_cost | decimal(18,2) | 财务成本 | ≥0 | 企业业务素材 |
| tax_amount | decimal(18,2) | 税金 | ≥0 | 企业业务素材 |
| management_fee | decimal(18,2) | 管理费 | ≥0 | 企业业务素材 |
| contingency | decimal(18,2) | 不可预见费 | ≥0 | 企业业务素材 |
| created_date | date | 创建日期 | NOT NULL | 企业业务素材 |

**外键属性**：
| 属性名 | 关联Object | 关系说明 |
|-------|-----------|---------|
| project_key | Project | 目标成本归属项目 |

**派生属性**：
| 属性名 | 计算规则 | 数据类型 | 业务含义 |
|-------|---------|---------|---------|
| cost_variance | target_amount - actual_cost | decimal(18,2) | 成本偏差额 |
| cost_variance_rate | cost_variance / target_amount | decimal(5,4) | 成本偏差率 |
| cost_structure_direct | direct_cost / target_amount | decimal(5,4) | 直接成本占比 |
| cost_structure_indirect | indirect_cost / target_amount | decimal(5,4) | 间接成本占比 |

**业务规则**：
- **计算规则**：
  - CR007：成本偏差额 = target_amount - actual_cost
  - CR008：成本偏差率 = cost_variance / target_amount
- **约束条件**：
  - CC006：目标成本金额 = 直接成本 + 间接成本 + 财务成本 + 税金 + 管理费 + 不可预见费
  - CC007：成本偏差率 > 5% 时触发黄色预警，>10%触发红色预警（QR-C001）
- **勾稽关系**：
  - RR002：目标成本 = 直接成本 + 间接成本 + 财务成本 + 税金 + 管理费 + 不可预见费

---

### 2.2 产值域 Object Type

#### OT004：ProjectOutput（产值）

**基本信息**：
```yaml
Object Type: ProjectOutput
Display Name: 项目产值
Description: 已完成的工程量对应的金额，体现收入确认
Classification: Transaction
Source Type: 企业业务素材
企业特有规则: ER002（产值双轨制）
```

**核心属性**：
| 属性名 | 数据类型 | 业务含义 | 约束 | 来源 |
|-------|---------|---------|------|------|
| output_key | string | 产值唯一标识 | PK | 系统生成 |
| project_key | string | 项目标识 | FK→Project, NOT NULL | 企业业务素材 |
| date_key | string | 日期标识 | FK→dim_date, NOT NULL | 行业通用知识 |
| confirmed_amount | decimal(18,2) | 已确认产值 | ≥0 | 企业业务素材 |
| unconfirmed_amount | decimal(18,2) | 待确认产值 | ≥0 | 企业业务素材 |
| total_amount | decimal(18,2) | 总产值 | ≥0 | 企业业务素材 |
| confirm_date | date | 确认日期 | - | 企业业务素材 |
| progress_rate | decimal(5,4) | 进度比例 | [0, 1] | 企业业务素材 |
| period | string | 统计周期 | {月度, 季度, 年度} | 企业业务素材 |

**外键属性**：
| 属性名 | 关联Object/维度表 | 关系说明 |
|-------|------------------|---------|
| project_key | Project | 产值归属项目 |
| date_key | dim_date | 产值发生日期 |

**派生属性**：
| 属性名 | 计算规则 | 数据类型 | 业务含义 |
|-------|---------|---------|---------|
| confirm_ratio | confirmed_amount / total_amount | decimal(5,4) | 产值确权比 |
| cumulative_output | Σ(ProjectOutput.total_amount) WHERE project_key = ? | decimal(18,2) | 累计产值 |
| tax_amount | total_amount / (1 + tax_rate) × tax_rate | decimal(18,2) | 销项税额 |

**业务规则**：
- **计算规则**：
  - CR009：总产值 = 已确认产值 + 待确认产值（产值双轨制ER002）
  - CR010：产值确权比 = confirmed_amount / total_amount
- **约束条件**：
  - CC008：总产值 = 已确认产值 + 待确认产值（勾稽关系）
  - CC009：产值确权比 ≥ 85%为正常，<80%触发红色预警（BR-C005）
- **勾稽关系**：
  - RR003：总产值 = 已确认产值 + 待确认产值（CR-I004）
  - RR004：含税产值 = 不含税产值 × (1 + 税率)（CR-I013）

---

### 2.3 成本域 Object Type

#### OT005：ProjectCost（成本）

**基本信息**：
```yaml
Object Type: ProjectCost
Display Name: 项目成本
Description: 项目实施过程中发生的各项费用
Classification: Transaction
Source Type: 企业业务素材
企业特有规则: ER003（成本三级分类）
```

**核心属性**：
| 属性名 | 数据类型 | 业务含义 | 约束 | 来源 |
|-------|---------|---------|------|------|
| cost_key | string | 成本唯一标识 | PK | 系统生成 |
| project_key | string | 项目标识 | FK→Project, NOT NULL | 企业业务素材 |
| date_key | string | 日期标识 | FK→dim_date, NOT NULL | 行业通用知识 |
| cost_subject_key | string | 成本科目标识 | FK→dim_cost_subject, NOT NULL | 企业业务素材 |
| cost_category_key | string | 成本分类标识 | FK→dim_cost_category | 企业业务素材 |
| confirmed_amount | decimal(18,2) | 已确认成本 | ≥0 | 企业业务素材 |
| unconfirmed_amount | decimal(18,2) | 待确认成本 | ≥0 | 企业业务素材 |
| total_amount | decimal(18,2) | 总成本 | ≥0 | 企业业务素材 |
| occur_date | date | 发生日期 | NOT NULL | 企业业务素材 |
| responsible_department_key | string | 责任部门标识 | FK→dim_department | 企业业务素材 |
| contract_key | string | 合同标识 | FK→Contract | 企业业务素材 |
| supplier_key | string | 供应商标识 | FK→dim_supplier | 企业业务素材 |
| subcontractor_key | string | 分包商标识 | FK→dim_subcontractor | 企业业务素材 |

**外键属性**：
| 属性名 | 关联Object/维度表 | 关系说明 |
|-------|------------------|---------|
| project_key | Project | 成本归属项目 |
| cost_subject_key | dim_cost_subject | 成本科目（四级结构54010104:1） |
| cost_category_key | dim_cost_category | 成本分类（直接/间接/财务/税金） |
| contract_key | Contract | 成本关联合同 |
| supplier_key | dim_supplier | 成本关联供应商 |
| subcontractor_key | dim_subcontractor | 成本关联分包商 |

**派生属性**：
| 属性名 | 计算规则 | 数据类型 | 业务含义 |
|-------|---------|---------|---------|
| cost_rigidity | confirmed_amount / total_amount | decimal(5,4) | 成本刚性度 |
| cumulative_cost | Σ(ProjectCost.total_amount) WHERE project_key = ? | decimal(18,2) | 累计成本 |
| cost_structure_ratio | 按科目汇总 / 累计成本 | decimal(5,4) | 成本结构占比 |
| material_cost_ratio | 材料成本 / 直接成本 | decimal(5,4) | 材料成本占比（应50%-65%） |
| labor_cost_ratio | 人工成本 / 直接成本 | decimal(5,4) | 人工成本占比（应20%-30%） |
| machinery_cost_ratio | 机械成本 / 直接成本 | decimal(5,4) | 机械成本占比（应8%-12%） |

**业务规则**：
- **计算规则**：
  - CR011：总成本 = 已确认成本 + 待确认成本
  - CR012：成本刚性度 = confirmed_amount / total_amount
  - CR013：材料成本占比 = 材料成本 / 直接成本
- **约束条件**：
  - CC010：总成本 = 已确认成本 + 待确认成本（勾稽关系）
  - CC011：成本刚性度 ≥ 95%为正常，<90%触发红色预警（BR-C004）
  - CC012：材料成本占比应在50%-65%之间，超出范围触发预警（QR-C003）
  - CC013：人工成本占比应在20%-30%之间，超出范围触发预警（QR-C004）
  - CC014：成本科目必须符合四级结构编码规则（ER003）
- **勾稽关系**：
  - RR005：总成本 = 已确认成本 + 待确认成本（CR-I003）
  - RR006：直接成本 = 人工成本 + 材料成本 + 机械成本 + 其他直接费

---

### 2.4 资金域 Object Type

#### OT006：Payment（付款）

**基本信息**：
```yaml
Object Type: Payment
Display Name: 付款
Description: 向供应商或分包商支付款项的记录
Classification: Transaction
Source Type: 企业业务素材
```

**核心属性**：
| 属性名 | 数据类型 | 业务含义 | 约束 | 来源 |
|-------|---------|---------|------|------|
| payment_key | string | 付款唯一标识 | PK | 系统生成 |
| contract_key | string | 合同标识 | FK→Contract, NOT NULL | 企业业务素材 |
| date_key | string | 日期标识 | FK→dim_date, NOT NULL | 行业通用知识 |
| payment_amount | decimal(18,2) | 付款金额 | ≥0 | 企业业务素材 |
| payment_method | string | 付款方式 | {银行转账, 承兑汇票, 现金} | 企业业务素材 |
| payment_type_key | string | 付款类型标识 | FK→dim_fund_type | 企业业务素材 |
| payment_status_key | string | 付款状态标识 | FK→dim_payment_status | 企业业务素材 |
| cumulative_ratio | decimal(5,4) | 累计付款比例 | [0, 1] | 企业业务素材 |
| supplier_key | string | 供应商标识 | FK→dim_supplier | 企业业务素材 |
| subcontractor_key | string | 分包商标识 | FK→dim_subcontractor | 企业业务素材 |

**外键属性**：
| 属性名 | 关联Object/维度表 | 关系说明 |
|-------|------------------|---------|
| contract_key | Contract | 付款归属合同 |
| payment_type_key | dim_fund_type | 资金类型（工程款/保证金/借款） |
| payment_status_key | dim_payment_status | 付款状态（已确认/待确认/已支付） |
| supplier_key | dim_supplier | 付款对象（供应商） |
| subcontractor_key | dim_subcontractor | 付款对象（分包商） |

**派生属性**：
| 属性名 | 计算规则 | 数据类型 | 业务含义 |
|-------|---------|---------|---------|
| cumulative_payment | Σ(Payment.payment_amount) WHERE contract_key = ? | decimal(18,2) | 累计付款 |
| payment_ratio_actual | cumulative_payment / contract_amount | decimal(5,4) | 实际付款比例 |
| retention_amount | contract_amount × 质保金比例 - 已返还质保金 | decimal(18,2) | 未返还质保金 |

**业务规则**：
- **计算规则**：
  - CR014：累计付款比例 = cumulative_payment / contract_amount
- **约束条件**：
  - CC015：累计付款 ≤ 合同金额 × 付款比例（BR-C001）
  - CC016：付款时必须暂扣质保金（通常5%-10%）（BR-C002）
  - CC017：分包付款 ≤ 业主收款 × 付款比例（背靠背条款）（BR-C003）
- **状态流转**：
  - BR-S003：申请 → 审批中 → 已批准 → 支付中 → 已支付 → 完成

---

#### OT007：Receipt（收款）

**基本信息**：
```yaml
Object Type: Receipt
Display Name: 收款
Description: 从业主收到的款项记录
Classification: Transaction
Source Type: 企业业务素材
```

**核心属性**：
| 属性名 | 数据类型 | 业务含义 | 约束 | 来源 |
|-------|---------|---------|------|------|
| receipt_key | string | 收款唯一标识 | PK | 系统生成 |
| project_key | string | 项目标识 | FK→Project, NOT NULL | 企业业务素材 |
| date_key | string | 日期标识 | FK→dim_date, NOT NULL | 行业通用知识 |
| receipt_amount | decimal(18,2) | 收款金额 | ≥0 | 企业业务素材 |
| receipt_method | string | 收款方式 | {银行转账, 承兑汇票, 现金} | 企业业务素材 |
| receipt_type_key | string | 收款类型标识 | FK→dim_fund_type | 企业业务素材 |
| overdue_days | int | 逾期天数 | ≥0 | 企业业务素材 |
| owner_key | string | 业主标识 | FK→dim_owner | 企业业务素材 |

**外键属性**：
| 属性名 | 关联Object/维度表 | 关系说明 |
|-------|------------------|---------|
| project_key | Project | 收款归属项目 |
| receipt_type_key | dim_fund_type | 资金类型（工程款/保证金/借款） |
| owner_key | dim_owner | 收款来源（业主） |

**派生属性**：
| 属性名 | 计算规则 | 数据类型 | 业务含义 |
|-------|---------|---------|---------|
| cumulative_receipt | Σ(Receipt.receipt_amount) WHERE project_key = ? | decimal(18,2) | 累计收款 |
| collection_ratio | cumulative_receipt / confirmed_output | decimal(5,4) | 收款率 |
| overdue_amount | 按逾期天数计算的应收金额 | decimal(18,2) | 逾期金额 |

**业务规则**：
- **计算规则**：
  - CR015：收款率 = cumulative_receipt / confirmed_output
- **约束条件**：
  - CC018：收款率 ≥ 80%为正常，<60%触发红色预警（BR-C006）
  - CC019：逾期天数 > 90天触发预警（QR-F008）
- **状态流转**：
  - BR-S004：开票 → 挂账 → 收款 → 核销 → 完成

---

#### OT008：CashFlow（现金流）

**基本信息**：
```yaml
Object Type: CashFlow
Display Name: 现金流
Description: 项目资金的流入流出记录
Classification: Transaction
Source Type: 企业业务素材
企业特有规则: ER001（资金月度批复）
```

**核心属性**：
| 属性名 | 数据类型 | 业务含义 | 约束 | 来源 |
|-------|---------|---------|------|------|
| cashflow_key | string | 现金流唯一标识 | PK | 系统生成 |
| project_key | string | 项目标识 | FK→Project, NOT NULL | 企业业务素材 |
| date_key | string | 日期标识 | FK→dim_date, NOT NULL | 行业通用知识 |
| inflow_amount | decimal(18,2) | 流入金额 | ≥0 | 企业业务素材 |
| outflow_amount | decimal(18,2) | 流出金额 | ≥0 | 企业业务素材 |
| balance | decimal(18,2) | 结余 | - | 企业业务素材 |
| fund_type_key | string | 资金类型标识 | FK→dim_fund_type | 企业业务素材 |
| flow_direction | string | 流向 | {流入, 流出} | 企业业务素材 |
| approval_status | string | 审批状态 | {已批复, 待批复, 未批复} | 企业业务素材 |
| approval_month | string | 批复月份 | YYYY-MM格式 | 企业业务素材 |

**外键属性**：
| 属性名 | 关联Object/维度表 | 关系说明 |
|-------|------------------|---------|
| project_key | Project | 现金流归属项目 |
| fund_type_key | dim_fund_type | 资金类型分类 |

**派生属性**：
| 属性名 | 计算规则 | 数据类型 | 业务含义 |
|-------|---------|---------|---------|
| net_cashflow | inflow_amount - outflow_amount | decimal(18,2) | 现金流净额 |
| cumulative_balance | Σ(net_cashflow) WHERE project_key = ? | decimal(18,2) | 累计结余 |
| monthly_cashflow | 按月汇总的现金流 | decimal(18,2) | 月度现金流 |

**业务规则**：
- **计算规则**：
  - CR016：现金流净额 = inflow_amount - outflow_amount
- **约束条件**：
  - CC020：现金流净额 < 0（净流出）时触发预警（QR-F006）
  - CC021：连续3个月净流出时发送红色预警
  - CC022：资金计划必须按月度批复（ER001）
- **勾稽关系**：
  - RR007：现金流净额 = 流入 - 流出（CR-I008）

---

### 2.5 风险域 Object Type

#### OT009：Risk（风险）

**基本信息**：
```yaml
Object Type: Risk
Display Name: 风险
Description: 可能影响项目目标实现的不确定因素
Classification: Analytical
Source Type: 行业通用知识 + 企业业务素材
企业特有规则: ER004（风险三色预警）
```

**核心属性**：
| 属性名 | 数据类型 | 业务含义 | 约束 | 来源 |
|-------|---------|---------|------|------|
| risk_key | string | 风险唯一标识 | PK | 系统生成 |
| project_key | string | 项目标识 | FK→Project, NOT NULL | 企业业务素材 |
| risk_name | string | 风险名称 | NOT NULL | 企业业务素材 |
| risk_description | string | 风险描述 | - | 企业业务素材 |
| risk_type | string | 风险类型 | {成本风险, 进度风险, 资金风险, 质量风险, 安全风险} | 企业业务素材 |
| risk_level | string | 风险等级 | {高, 中, 低} | 企业业务素材 |
| probability | decimal(5,4) | 发生概率 | [0, 1] | 企业业务素材 |
| impact | decimal(18,2) | 影响金额 | ≥0 | 企业业务素材 |
| response_measure | string | 应对措施 | - | 企业业务素材 |
| risk_status | string | 风险状态 | {识别, 评估, 处置, 监控, 关闭} | 企业业务素材 |
| warning_level_key | string | 预警级别标识 | FK→dim_warning_level | 企业业务素材 |

**外键属性**：
| 属性名 | 关联Object/维度表 | 关系说明 |
|-------|------------------|---------|
| project_key | Project | 风险归属项目 |
| warning_level_key | dim_warning_level | 预警级别（绿/黄/红） |

**派生属性**：
| 属性名 | 计算规则 | 数据类型 | 业务含义 |
|-------|---------|---------|---------|
| risk_score | probability × impact | decimal(18,2) | 风险评分 |
| risk_exposure | Σ(RiskEvent.impact_amount) WHERE risk_key = ? | decimal(18,2) | 风险敞口 |
| risk_level_calculated | 根据risk_score划分 | string | 计算风险等级 |

**业务规则**：
- **计算规则**：
  - CR017：风险评分 = probability × impact
- **约束条件**：
  - CC023：风险等级根据评分划分（高>100万，中50-100万，低<50万）
- **预警规则**：
  - ER004：风险三色预警（绿色=低风险，黄色=中风险，红色=高风险）
- **状态流转**：
  - 识别 → 评估 → 处置 → 监控 → 关闭

---

#### OT010：AlertRule（预警规则）

**基本信息**：
```yaml
Object Type: AlertRule
Display Name: 预警规则
Description: 触发预警的条件和规则
Classification: Master
Source Type: 企业业务素材
```

**核心属性**：
| 属性名 | 数据类型 | 业务含义 | 约束 | 来源 |
|-------|---------|---------|------|------|
| rule_key | string | 规则唯一标识 | PK | 系统生成 |
| rule_code | string | 规则编码 | UK, NOT NULL | 企业业务素材 |
| rule_name | string | 规则名称 | NOT NULL | 企业业务素材 |
| alert_condition | string | 触发条件 | NOT NULL | 企业业务素材 |
| threshold_setting | string | 阈值设置 | - | 企业业务素材 |
| alert_level | string | 预警级别 | {绿色, 黄色, 红色} | 企业业务素材 |
| notification_target | string | 通知对象 | - | 企业业务素材 |
| rule_priority | int | 规则优先级 | [1, 10] | 企业业务素材 |
| related_object | string | 关联对象类型 | - | 企业业务素材 |

**业务规则**：
- **预警规则示例**：
  - QR-C001：成本偏差率 > 5% 时触发黄色预警
  - QR-F002：收款率 < 80% 时触发黄色预警
  - BR-C004：成本刚性度 < 95% 时触发黄色预警
  - BR-C005：产值确权比 < 85% 时触发黄色预警

---

#### OT011：AlertRecord（预警记录）

**基本信息**：
```yaml
Object Type: AlertRecord
Display Name: 预警记录
Description: 预警触发记录
Classification: Transaction
Source Type: 企业业务素材
```

**核心属性**：
| 属性名 | 数据类型 | 业务含义 | 约束 | 来源 |
|-------|---------|---------|------|------|
| alert_key | string | 预警唯一标识 | PK | 系统生成 |
| rule_key | string | 规则标识 | FK→AlertRule, NOT NULL | 企业业务素材 |
| project_key | string | 项目标识 | FK→Project | 企业业务素材 |
| alert_date | date | 预警日期 | NOT NULL | 企业业务素材 |
| alert_level | string | 预警级别 | {绿色, 黄色, 红色} | 企业业务素材 |
| alert_content | string | 预警内容 | NOT NULL | 企业业务素材 |
| handling_status | string | 处理状态 | {未处理, 处理中, 已处理} | 企业业务素材 |
| handler | string | 处理人 | - | 企业业务素材 |
| handle_date | date | 处理日期 | - | 企业业务素材 |

**外键属性**：
| 属性名 | 关联Object/维度表 | 关系说明 |
|-------|------------------|---------|
| rule_key | AlertRule | 预警归属规则 |
| project_key | Project | 预警归属项目 |

---

## 三、阶段一成果覆盖率检查

### 3.1 核心实体覆盖率

| 阶段一实体 | 本设计Object Type | 覆盖情况 | 说明 |
|-----------|------------------|---------|------|
| Project (E001) | Project (OT001) | ✅ 完全覆盖 | 包含所有核心属性：project_type, project_category, business_model等 |
| Contract (E002) | Contract (OT002) | ✅ 完全覆盖 | 包含合同类型、甲乙双方、结算状态等 |
| TargetCost (E005) | TargetCost (OT003) | ✅ 完全覆盖 | 包含直接成本、间接成本、财务成本等 |
| ProjectOutput (E014) | ProjectOutput (OT004) | ✅ 完全覆盖 | 包含产值双轨制（ER002） |
| ProjectCost (E015) | ProjectCost (OT005) | ✅ 完全覆盖 | 包含成本三级分类（ER003） |
| Payment (E016) | Payment (OT006) | ✅ 完全覆盖 | 包含分包付款约束等 |
| Receipt (E017) | Receipt (OT007) | ✅ 完全覆盖 | 包含收款率预警等 |
| CashFlow (E020) | CashFlow (OT008) | ✅ 完全覆盖 | 包含资金月度批复（ER001） |
| Risk (E041) | Risk (OT009) | ✅ 完全覆盖 | 包含风险三色预警（ER004） |
| AlertRule (E049) | AlertRule (OT010) | ✅ 完全覆盖 | 包含预警规则定义 |
| AlertRecord (E050) | AlertRecord (OT011) | ✅ 完全覆盖 | 包含预警触发记录 |

### 3.2 维度表覆盖率

| 阶段一维度表 | 本设计使用情况 | 覆盖情况 | 说明 |
|-------------|---------------|---------|------|
| dim_project_category | ✅ 用于project_type_key, project_category_key | ✅ 完全覆盖 | 支持EPC/PPP/房建/市政等分类 |
| dim_project_status | ✅ 用于project_status_key | ✅ 完全覆盖 | 支持项目生命周期状态 |
| dim_cost_subject | ✅ 用于cost_subject_key | ✅ 完全覆盖 | 四级成本科目结构 |
| dim_cost_category | ✅ 用于cost_category_key | ✅ 完全覆盖 | 直接/间接/财务/税金分类 |
| dim_client | ✅ 用于client_key, client_system | ✅ 完全覆盖 | 大客户标识、客户体系 |
| dim_cooperation | ✅ 用于business_model_key | ✅ 完全覆盖 | 直营/联营/合伙模式 |
| dim_region | ✅ 用于region_key | ✅ 完全覆盖 | 地区层级分析 |
| dim_organization | ✅ 用于organization_key | ✅ 完全覆盖 | 组织层级分析 |
| dim_fund_type | ✅ 用于payment_type_key, receipt_type_key | ✅ 完全覆盖 | 资金类型分类 |
| dim_payment_status | ✅ 用于payment_status_key | ✅ 完全覆盖 | 付款状态 |
| dim_settlement_status | ✅ 用于settlement_status_key | ✅ 完全覆盖 | 结算状态 |
| dim_warning_level | ✅ 用于warning_level_key | ✅ 完全覆盖 | 红绿黄灯预警 |

### 3.3 企业特有规则覆盖率

| 企业特有规则 | 本设计使用情况 | 覆盖情况 | 说明 |
|-------------|---------------|---------|------|
| ER001：资金月度批复 | ✅ 体现在CashFlow的approval_month属性 | ✅ 完全覆盖 | 资金计划按月度批复 |
| ER002：产值双轨制 | ✅ 体现在ProjectOutput的confirmed_amount/unconfirmed_amount | ✅ 完全覆盖 | 产值分为已确认和待确认 |
| ER003：成本三级分类 | ✅ 体现在ProjectCost的cost_subject_key（四级结构） | ✅ 完全覆盖 | 主控费用→分项费用→明细费用 |
| ER004：风险三色预警 | ✅ 体现在Risk和AlertRule的alert_level | ✅ 完全覆盖 | 绿/黄/红三级预警 |

### 3.4 冲突检查结果

**检查内容**：
1. ✅ 无重复属性定义
2. ✅ 无冲突的业务规则
3. ✅ 无冗余的维度引用
4. ✅ 无矛盾的数据标准
5. ✅ 所有外键关系一致

---

## 四、Object Type 总览

### 4.1 Object Type 清单

| 编号 | Object Type | Display Name | Classification | 关键业务规则 |
|-----|------------|-------------|---------------|-------------|
| OT001 | Project | 项目 | Master | CR001-CR004, CC001-CC003, 含project_type/project_category |
| OT002 | Contract | 合同 | Master | CR005-CR006, CC004-CC005, BR-S002 |
| OT003 | TargetCost | 目标成本 | Transaction | CR007-CR008, CC006-CC007 |
| OT004 | ProjectOutput | 产值 | Transaction | CR009-CR010, CC008-CC009, ER002 |
| OT005 | ProjectCost | 成本 | Transaction | CR011-CR013, CC010-CC014, ER003 |
| OT006 | Payment | 付款 | Transaction | CR014, CC015-CC017, BR-S003 |
| OT007 | Receipt | 收款 | Transaction | CR015, CC018-CC019, BR-S004 |
| OT008 | CashFlow | 现金流 | Transaction | CR016, CC020-CC022, ER001 |
| OT009 | Risk | 风险 | Analytical | CR017, CC023, ER004 |
| OT010 | AlertRule | 预警规则 | Master | 预警规则库 |
| OT011 | AlertRecord | 预警记录 | Transaction | 预警触发记录 |

### 4.2 Object Type 分类统计

| 分类 | 数量 | 说明 |
|------|------|------|
| Master | 3个 | Project、Contract、AlertRule |
| Transaction | 7个 | TargetCost、ProjectOutput、ProjectCost、Payment、Receipt、CashFlow、AlertRecord |
| Analytical | 1个 | Risk |

---

## 五、下一步工作

### 5.1 待完成工作

根据《040-本体设计方法.md》，Object Type设计完成后，需要进行：

1. **Link Type设计**（步骤2）
   - 基于业务关系清单（122条关系）设计Link Type
   - 定义关系类型（归属、包含、关联、计算）
   - 定义关系基数（1:1、1:N、N:M）

2. **Action Type设计**（步骤3）
   - 基于流程与动作清单（25个流程+30个动作）设计Action Type
   - 定义动作触发条件
   - 定义动作执行主体

3. **业务规则定义**（步骤4）
   - 详细定义计算规则
   - 详细定义勾稽关系
   - 详细定义约束条件
   - 详细定义数据标准

### 5.2 输出到下一阶段

本文档将作为以下工作的输入：
- Link Type设计文档
- Action Type设计文档
- 业务规则定义文档
- 本体设计确认文档

---

## 六、版本记录

| 版本 | 日期 | 更新内容 |
|-----|------|---------|
| V1.0 | 2026-06-12 | 初始版本，设计11个核心Object Type |
| V2.0 | 2026-06-12 | 全面优化，补充遗漏的维度属性，增加阶段一成果覆盖率检查，确保设计完整性 |

---

**设计人**：系统自动生成  
**设计时间**：2026年6月12日  
**适用项目**：潘达工程-商务成本智能决策体系