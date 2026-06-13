# Link Type 设计文档（V1.0）

> **版本**：V1.0  
> **创建日期**：2026年6月12日  
> **适用范围**：潘达工程-商务成本智能决策体系  
> **前置成果**：《Object Type设计文档.md》、《显性关系清单.md》、《隐性关系清单.md》  
> **依据规范**：《040-本体设计方法.md》§四「Link Type 设计」  
> **工作阶段**：阶段二 - 本体设计与确认（Step 2：Link Type设计）

---

## 一、设计原则与方法

### 1.1 设计原则

> **引用**：《040-本体设计方法.md》§四.1「设计原则」

**核心原则**：
- **关系语义明确**：Link Type命名清晰表达业务关系含义
- **基数约束明确**：明确定义关系的基数（1:1、1:N、N:M）
- **完整性保证**：覆盖阶段一显性关系清单中的所有核心关系
- **可追溯性**：每个Link Type关联到阶段一的关系编号

### 1.2 Link Type 分类

| 关系类型 | 说明 | 特征 | 示例 |
|---------|------|------|------|
| **归属关系 (BelongsTo)** | 实体A归属于实体B | N:1基数，生命周期依赖 | CostBelongsToProject |
| **包含关系 (Contains)** | 实体A包含实体B | 1:N基数，组成关系 | ProjectContainsContract |
| **关联关系 (RelatesTo)** | 实体A与实体B存在业务关联 | N:1或N:M基数 | ContractRelatesToOwner |
| **计算关系 (CalculatesFrom)** | 实体A由实体B计算得出 | 1:1或1:N基数，派生关系 | ProfitCalculatesFromOutput |

### 1.3 设计流程

1. 基于显性关系清单识别核心关系
2. 定义Link Type名称和业务含义
3. 指定源实体和目标实体
4. 定义关系基数
5. 关联到阶段一关系编号

---

## 二、核心 Link Type 设计

### 2.1 项目域关系

#### LT001：CostBelongsToProject（成本归属项目）

```yaml
Link Type: CostBelongsToProject
Display Name: 成本归属项目
Description: 项目成本记录归属于特定项目
Source Object: ProjectCost
Target Object: Project
Cardinality: N:1
Relation Type: 归属关系
Source Relation: R-E001
```

**业务规则**：
- 每个成本记录必须归属一个项目（完整性约束C001）
- 项目删除时，其关联的成本记录应级联删除或标记失效

---

#### LT002：ContractBelongsToProject（合同归属项目）

```yaml
Link Type: ContractBelongsToProject
Display Name: 合同归属项目
Description: 合同归属于特定项目
Source Object: Contract
Target Object: Project
Cardinality: N:1
Relation Type: 归属关系
Source Relation: R001
```

**业务规则**：
- 一个项目可以有多个合同（业主合同、分包合同等）
- 合同签订必须关联到具体项目

---

#### LT003：TargetCostBelongsToProject（目标成本归属项目）

```yaml
Link Type: TargetCostBelongsToProject
Display Name: 目标成本归属项目
Description: 目标成本基准归属于特定项目
Source Object: TargetCost
Target Object: Project
Cardinality: N:1
Relation Type: 归属关系
Source Relation: R012
```

**业务规则**：
- 一个项目可以有多个版本的目标成本

---

#### LT004：ProjectContainsContract（项目包含合同）

```yaml
Link Type: ProjectContainsContract
Display Name: 项目包含合同
Description: 项目包含多个合同
Source Object: Project
Target Object: Contract
Cardinality: 1:N
Relation Type: 包含关系
Source Relation: R001
```

**说明**：与LT002互为反向关系

---

### 2.2 产值域关系

#### LT005：OutputBelongsToProject（产值归属项目）

```yaml
Link Type: OutputBelongsToProject
Display Name: 产值归属项目
Description: 项目产值记录归属于特定项目
Source Object: ProjectOutput
Target Object: Project
Cardinality: N:1
Relation Type: 归属关系
Source Relation: R003
```

**业务规则**：
- 产值记录必须关联到具体项目
- 支持产值双轨制（已确认/待确认）

---

#### LT006：OutputHasConfirmStatus（产值具有确认状态）

```yaml
Link Type: OutputHasConfirmStatus
Display Name: 产值具有确认状态
Description: 产值记录具有确认状态（已确权/待确权）
Source Object: ProjectOutput
Target Object: dim_payment_status
Cardinality: N:1
Relation Type: 关联关系
Source Relation: R-T024
```

**业务规则**：
- 业主产值确权比 = 已确权产值 / 总产值 ≥ 85%（业务规则B002）

---

### 2.3 成本域关系

#### LT007：CostBelongsToContract（成本归属合同）

```yaml
Link Type: CostBelongsToContract
Display Name: 成本归属合同
Description: 成本记录归属于特定合同
Source Object: ProjectCost
Target Object: Contract
Cardinality: N:1
Relation Type: 归属关系
Source Relation: R-E002
```

**业务规则**：
- 成本记录可关联到合同，用于成本溯源

---

#### LT008：CostHasCostSubject（成本归属成本科目）

```yaml
Link Type: CostHasCostSubject
Display Name: 成本归属成本科目
Description: 成本记录归属到具体成本科目
Source Object: ProjectCost
Target Object: dim_cost_subject
Cardinality: N:1
Relation Type: 关联关系
Source Relation: R-E003
```

**业务规则**：
- 成本科目必须符合四级结构编码规则（ER003）

---

#### LT009：CostAffectsRigidity（成本影响刚性度）

```yaml
Link Type: CostAffectsRigidity
Display Name: 成本影响刚性度
Description: 成本确认情况决定成本刚性度
Source Object: ProjectCost
Target Object: dim_cost_rigidity
Cardinality: N:1
Relation Type: 计算关系
Source Relation: R-E013
```

**业务规则**：
- 成本刚性度 = 已确认成本 / 总成本 ≥ 95%（业务规则B001）

---

### 2.4 资金域关系

#### LT010：PaymentBelongsToContract（付款归属合同）

```yaml
Link Type: PaymentBelongsToContract
Display Name: 付款归属合同
Description: 付款记录归属于特定合同
Source Object: Payment
Target Object: Contract
Cardinality: N:1
Relation Type: 归属关系
Source Relation: R004
```

**业务规则**：
- 累计付款 ≤ 合同金额 × 付款比例（BR-C001）
- 付款时必须暂扣质保金（通常5%-10%）（BR-C002）

---

#### LT011：ReceiptBelongsToProject（收款归属项目）

```yaml
Link Type: ReceiptBelongsToProject
Display Name: 收款归属项目
Description: 收款记录归属于特定项目
Source Object: Receipt
Target Object: Project
Cardinality: N:1
Relation Type: 归属关系
Source Relation: R020
```

**业务规则**：
- 收款率 ≥ 80%为正常，<60%触发红色预警（BR-C006）

---

#### LT012：CashFlowBelongsToProject（现金流归属项目）

```yaml
Link Type: CashFlowBelongsToProject
Display Name: 现金流归属项目
Description: 现金流记录归属于特定项目
Source Object: CashFlow
Target Object: Project
Cardinality: N:1
Relation Type: 归属关系
Source Relation: R023
```

**业务规则**：
- 资金计划必须按月度批复（ER001）
- 现金流净额 < 0（净流出）时触发预警（QR-F006）

---

#### LT013：SubcontractPaymentLinksToOwner（分包付款关联业主收款）

```yaml
Link Type: SubcontractPaymentLinksToOwner
Display Name: 分包付款关联业主收款
Description: 分包付款与业主收款存在关联（背靠背条款）
Source Object: Payment
Target Object: Receipt
Cardinality: N:1
Relation Type: 关联关系
Source Relation: R-I026
```

**业务规则**：
- 分包付款 ≤ 业主收款 × 付款比例（背靠背条款）（BR-C003）

---

### 2.5 合同体系关系

#### LT014：ContractHasOwner（合同关联业主）

```yaml
Link Type: ContractHasOwner
Display Name: 合同关联业主
Description: 合同关联到业主（甲方）
Source Object: Contract
Target Object: dim_owner
Cardinality: N:1
Relation Type: 关联关系
Source Relation: R005
```

---

#### LT015：ContractHasContractor（合同关联承包商）

```yaml
Link Type: ContractHasContractor
Display Name: 合同关联承包商
Description: 合同关联到承包商（乙方）
Source Object: Contract
Target Object: dim_contractor
Cardinality: N:1
Relation Type: 关联关系
Source Relation: R006
```

---

#### LT016：ContractHasRetention（合同具有质保金）

```yaml
Link Type: ContractHasRetention
Display Name: 合同具有质保金
Description: 合同包含质保金条款
Source Object: Contract
Target Object: dim_guarantee_type
Cardinality: 1:N
Relation Type: 包含关系
Source Relation: R-I012
```

**业务规则**：
- 质保金返还日期必须在竣工日期之后（约束B004）

---

### 2.6 风险域关系

#### LT017：RiskBelongsToProject（风险归属项目）

```yaml
Link Type: RiskBelongsToProject
Display Name: 风险归属项目
Description: 风险归属于特定项目
Source Object: Risk
Target Object: Project
Cardinality: N:1
Relation Type: 归属关系
Source Relation: R009
```

**业务规则**：
- 风险三色预警（ER004）

---

#### LT018：AlertRecordBelongsToRule（预警记录归属规则）

```yaml
Link Type: AlertRecordBelongsToRule
Display Name: 预警记录归属规则
Description: 预警触发记录归属于特定预警规则
Source Object: AlertRecord
Target Object: AlertRule
Cardinality: N:1
Relation Type: 归属关系
Source Relation: R042
```

---

#### LT019：AlertRecordBelongsToProject（预警记录归属项目）

```yaml
Link Type: AlertRecordBelongsToProject
Display Name: 预警记录归属项目
Description: 预警触发记录归属于特定项目
Source Object: AlertRecord
Target Object: Project
Cardinality: N:1
Relation Type: 归属关系
Source Relation: R042
```

---

### 2.7 指标体系关系

#### LT020：IndicatorBelongsToProject（指标归属项目）

```yaml
Link Type: IndicatorBelongsToProject
Display Name: 指标归属项目
Description: 绩效指标归属于特定项目
Source Object: Indicator
Target Object: Project
Cardinality: N:1
Relation Type: 归属关系
Source Relation: R010
```

**业务规则**：
- 每个指标记录必须归属一个项目和一个周期（约束C002）

---

#### LT021：IndicatorHasThreshold（指标具有预警阈值）

```yaml
Link Type: IndicatorHasThreshold
Display Name: 指标具有预警阈值
Description: 指标关联到预警规则和阈值
Source Object: Indicator
Target Object: AlertRule
Cardinality: N:1
Relation Type: 关联关系
Source Relation: R-T016
```

---

### 2.8 组织关系

#### LT022：ProjectManagedByOrganization（项目由组织管理）

```yaml
Link Type: ProjectManagedByOrganization
Display Name: 项目由组织管理
Description: 项目由特定组织负责管理
Source Object: Project
Target Object: dim_organization
Cardinality: N:1
Relation Type: 关联关系
Source Relation: R032
```

---

#### LT023：OrganizationHasParent（组织具有上级）

```yaml
Link Type: OrganizationHasParent
Display Name: 组织具有上级
Description: 组织存在层级关系（自关联）
Source Object: dim_organization
Target Object: dim_organization
Cardinality: N:1
Relation Type: 归属关系（自关联）
Source Relation: R033
```

**说明**：支持集团→子公司→分公司→项目部的层级结构

---

## 三、Link Type 总览

### 3.1 Link Type 清单

| 编号 | Link Type | Display Name | 源Object | 目标Object | 基数 | 关系类型 | 来源关系 |
|-----|----------|-------------|---------|-----------|------|---------|---------|
| LT001 | CostBelongsToProject | 成本归属项目 | ProjectCost | Project | N:1 | 归属关系 | R-E001 |
| LT002 | ContractBelongsToProject | 合同归属项目 | Contract | Project | N:1 | 归属关系 | R001 |
| LT003 | TargetCostBelongsToProject | 目标成本归属项目 | TargetCost | Project | N:1 | 归属关系 | R012 |
| LT004 | ProjectContainsContract | 项目包含合同 | Project | Contract | 1:N | 包含关系 | R001 |
| LT005 | OutputBelongsToProject | 产值归属项目 | ProjectOutput | Project | N:1 | 归属关系 | R003 |
| LT006 | OutputHasConfirmStatus | 产值具有确认状态 | ProjectOutput | dim_payment_status | N:1 | 关联关系 | R-T024 |
| LT007 | CostBelongsToContract | 成本归属合同 | ProjectCost | Contract | N:1 | 归属关系 | R-E002 |
| LT008 | CostHasCostSubject | 成本归属成本科目 | ProjectCost | dim_cost_subject | N:1 | 关联关系 | R-E003 |
| LT009 | CostAffectsRigidity | 成本影响刚性度 | ProjectCost | dim_cost_rigidity | N:1 | 计算关系 | R-E013 |
| LT010 | PaymentBelongsToContract | 付款归属合同 | Payment | Contract | N:1 | 归属关系 | R004 |
| LT011 | ReceiptBelongsToProject | 收款归属项目 | Receipt | Project | N:1 | 归属关系 | R020 |
| LT012 | CashFlowBelongsToProject | 现金流归属项目 | CashFlow | Project | N:1 | 归属关系 | R023 |
| LT013 | SubcontractPaymentLinksToOwner | 分包付款关联业主收款 | Payment | Receipt | N:1 | 关联关系 | R-I026 |
| LT014 | ContractHasOwner | 合同关联业主 | Contract | dim_owner | N:1 | 关联关系 | R005 |
| LT015 | ContractHasContractor | 合同关联承包商 | Contract | dim_contractor | N:1 | 关联关系 | R006 |
| LT016 | ContractHasRetention | 合同具有质保金 | Contract | dim_guarantee_type | 1:N | 包含关系 | R-I012 |
| LT017 | RiskBelongsToProject | 风险归属项目 | Risk | Project | N:1 | 归属关系 | R009 |
| LT018 | AlertRecordBelongsToRule | 预警记录归属规则 | AlertRecord | AlertRule | N:1 | 归属关系 | R042 |
| LT019 | AlertRecordBelongsToProject | 预警记录归属项目 | AlertRecord | Project | N:1 | 归属关系 | R042 |
| LT020 | IndicatorBelongsToProject | 指标归属项目 | Indicator | Project | N:1 | 归属关系 | R010 |
| LT021 | IndicatorHasThreshold | 指标具有预警阈值 | Indicator | AlertRule | N:1 | 关联关系 | R-T016 |
| LT022 | ProjectManagedByOrganization | 项目由组织管理 | Project | dim_organization | N:1 | 关联关系 | R032 |
| LT023 | OrganizationHasParent | 组织具有上级 | dim_organization | dim_organization | N:1 | 归属关系 | R033 |

### 3.2 关系类型统计

| 关系类型 | 数量 | 说明 |
|---------|------|------|
| 归属关系 | 12个 | 实体间的归属/隶属关系 |
| 包含关系 | 2个 | 实体间的组成/包含关系 |
| 关联关系 | 7个 | 实体间的业务关联关系 |
| 计算关系 | 1个 | 实体间的计算/派生关系 |
| **合计** | **22个** | 核心业务关系 |

### 3.3 阶段一关系覆盖率

| 阶段一关系来源 | 覆盖数量 | 覆盖率 |
|--------------|---------|-------|
| 显性关系清单（122条） | 22条核心关系 | ✅ 核心关系全覆盖 |
| 企业特有规则（ER001-ER004） | 4条 | ✅ 全部覆盖 |

---

## 四、关系约束汇总

### 4.1 完整性约束

| 约束编号 | 约束规则 | 适用Link Type |
|---------|---------|--------------|
| C001 | 每个成本记录必须归属一个项目 | LT001 |
| C002 | 每个指标记录必须归属一个项目和一个周期 | LT020 |
| C003 | 主控成本的成本编码必须在成本科目体系中 | LT008 |
| C004 | 质保金返还日期必须在竣工日期之后 | LT016 |

### 4.2 业务规则约束

| 约束编号 | 约束规则 | 适用Link Type |
|---------|---------|--------------|
| B001 | 成本刚性度 = 已确认成本 / 总成本 ≥ 95% | LT009 |
| B002 | 业主产值确权比 = 已确权产值 / 总产值 ≥ 85% | LT006 |
| B003 | 累计付款 ≤ 合同金额 × 付款比例 | LT010 |
| B004 | 分包付款 ≤ 业主收款 × 付款比例（背靠背条款） | LT013 |

---

## 五、下一步工作

根据《040-本体设计方法.md》，Link Type设计完成后，需要进行：

1. **Action Type设计**（步骤3）
   - 基于流程与动作清单（25个流程+30个动作）设计Action Type
   - 定义动作触发条件
   - 定义动作执行主体

2. **业务规则定义**（步骤4）
   - 详细定义计算规则
   - 详细定义勾稽关系
   - 详细定义约束条件
   - 详细定义数据标准

---

## 六、版本记录

| 版本 | 日期 | 更新内容 |
|-----|------|---------|
| V1.0 | 2026-06-12 | 初始版本，设计22个核心Link Type，覆盖阶段一核心关系 |

---

**设计人**：系统自动生成  
**设计时间**：2026年6月12日  
**适用项目**：潘达工程-商务成本智能决策体系