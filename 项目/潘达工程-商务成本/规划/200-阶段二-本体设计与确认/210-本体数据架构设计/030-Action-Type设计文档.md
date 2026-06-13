# Action Type 设计文档（V1.0）

> **版本**：V1.0  
> **创建日期**：2026年6月12日  
> **适用范围**：潘达工程-商务成本智能决策体系  
> **前置成果**：《Object Type设计文档.md》、《Link Type设计文档.md》、《流程与动作清单.md》  
> **依据规范**：《040-本体设计方法.md》§五「Action Type 设计」  
> **工作阶段**：阶段二 - 本体设计与确认（Step 3：Action Type设计）

---

## 一、设计原则与方法

### 1.1 设计原则

> **引用**：《040-本体设计方法.md》§五.1「设计原则」

**核心原则**：
- **动作语义明确**：Action Type命名清晰表达业务操作含义
- **触发条件明确**：明确定义动作触发的业务条件
- **执行主体明确**：指定动作的执行角色或组织
- **权限控制明确**：定义执行动作所需的权限
- **可追溯性**：每个Action Type关联到阶段一的动作编号

### 1.2 Action Type 分类

| 动作类型 | 说明 | 特征 | 示例 |
|---------|------|------|------|
| **审批类 (Approval)** | 需要多级审批的业务动作 | 涉及审批流程，有状态流转 | ContractApproval |
| **业务操作类 (Business)** | 直接的业务操作 | 实时执行，无复杂审批 | CostCollection |
| **系统类 (System)** | 系统自动触发的动作 | 定时或事件触发，无需人工干预 | AlertTrigger |
| **查询分析类 (Query)** | 数据查询和分析操作 | 只读操作，不修改数据 | ReportGenerate |

### 1.3 设计流程

1. 基于流程与动作清单识别核心动作
2. 定义Action Type名称和业务含义
3. 指定触发实体和结果实体
4. 定义触发条件和执行主体
5. 关联到阶段一动作编号

---

## 二、核心 Action Type 设计

### 2.1 审批类动作

#### AT001：ContractApproval（合同审批）

```yaml
Action Type: ContractApproval
Display Name: 合同审批
Description: 对合同进行审核和批准，包括起草、审核、法务审批、领导审批等环节
Category: 审批类
Source Action: A001
Trigger Entity: Contract
Result Entity: Contract
Trigger Condition: 合同状态 = '待审批'
Execution Subject: 合同审批人、法务人员、领导
Permission Required: 合同审批权限
Related Process: P006（合同审批流程）
```

**业务规则**：
- 审批流程：起草→审核→法务审批→领导审批→签订→归档
- 关联诀窍：CM001（合同条款隐藏风险识别）

---

#### AT002：PaymentApproval（付款审批）

```yaml
Action Type: PaymentApproval
Display Name: 付款审批
Description: 对付款申请进行审核和批准
Category: 审批类
Source Action: A002
Trigger Entity: Payment
Result Entity: Payment
Trigger Condition: 付款状态 = '待审批' AND 累计付款 ≤ 合同金额 × 付款比例
Execution Subject: 财务人员、审批领导
Permission Required: 付款审批权限
Related Process: P016（付款审批流程）
```

**业务规则**：
- 付款时必须暂扣质保金（通常5%-10%）
- 分包付款 ≤ 业主收款 × 付款比例（背靠背条款）

---

#### AT003：BudgetApproval（预算审批）

```yaml
Action Type: BudgetApproval
Display Name: 预算审批
Description: 对项目预算进行审核和批准
Category: 审批类
Source Action: A003
Trigger Entity: Budget
Result Entity: Budget
Trigger Condition: 预算状态 = '待审批'
Execution Subject: 预算管理员、审批领导
Permission Required: 预算审批权限
Related Process: P010（预算编制流程）
```

---

#### AT004：ChangeApproval（变更审批）

```yaml
Action Type: ChangeApproval
Display Name: 变更审批
Description: 对设计变更或现场签证进行审核和批准
Category: 审批类
Source Action: A004
Trigger Entity: ChangeOrder
Result Entity: ChangeOrder
Trigger Condition: 变更状态 = '待审批'
Execution Subject: 项目工程师、成本工程师、审批领导
Permission Required: 变更审批权限
Related Process: P004（项目变更流程）、P012（变更签证流程）
```

**业务规则**：
- 变更发生后72小时内必须提出签证（CV001）
- 变更价款计算需遵循优先级规则（CV002）

---

#### AT005：SettlementApproval（结算审批）

```yaml
Action Type: SettlementApproval
Display Name: 结算审批
Description: 对项目或合同结算进行审核和批准
Category: 审批类
Source Action: A005
Trigger Entity: Settlement
Result Entity: Settlement
Trigger Condition: 结算状态 = '待审批'
Execution Subject: 结算专员、审计人员、审批领导
Permission Required: 结算审批权限
Related Process: P016（付款审批流程）、P021（竣工结算流程）
```

---

#### AT006：ProjectApproval（项目审批）

```yaml
Action Type: ProjectApproval
Display Name: 项目审批
Description: 对项目立项进行审核和批准
Category: 审批类
Source Action: A006
Trigger Entity: Project
Result Entity: Project
Trigger Condition: 项目状态 = '待审批'
Execution Subject: 项目审批人、领导
Permission Required: 项目审批权限
Related Process: P001（项目立项流程）
```

**业务规则**：
- 关联规则：BR-E004（资金月度批复）

---

#### AT007：BidSubmission（投标提交）

```yaml
Action Type: BidSubmission
Display Name: 投标提交
Description: 提交投标文件参与项目竞标
Category: 审批类
Source Action: A007
Trigger Entity: BidActivity
Result Entity: BidActivity
Trigger Condition: 投标文件编制完成
Execution Subject: 投标专员、商务经理
Permission Required: 投标权限
Related Process: P002（项目投标流程）
```

---

#### AT008：TargetCostApproval（目标成本审批）

```yaml
Action Type: TargetCostApproval
Display Name: 目标成本审批
Description: 对目标成本进行审核和批准
Category: 审批类
Source Action: A008
Trigger Entity: TargetCost
Result Entity: TargetCost
Trigger Condition: 目标成本状态 = '待审批'
Execution Subject: 成本工程师、审批领导
Permission Required: 成本审批权限
Related Process: P009（目标成本制定流程）
```

**业务规则**：
- 关联规则：QR-C001（目标成本计算）

---

#### AT009：SectionDivision（标段划分）

```yaml
Action Type: SectionDivision
Display Name: 标段划分
Description: 对大型项目进行标段划分
Category: 审批类
Source Action: A009
Trigger Entity: Section
Result Entity: Section
Trigger Condition: 项目中标后
Execution Subject: 项目策划人员、审批领导
Permission Required: 项目管理权限
Related Process: P014（标段划分流程）
```

---

#### AT010：SectionSettlement（标段结算）

```yaml
Action Type: SectionSettlement
Display Name: 标段结算
Description: 对标段进行结算审核和批准
Category: 审批类
Source Action: A010
Trigger Entity: Settlement
Result Entity: Settlement
Trigger Condition: 标段完工
Execution Subject: 结算专员、审批领导
Permission Required: 结算审批权限
Related Process: P015（标段结算流程）
```

---

### 2.2 业务操作类动作

#### AT011：CostCollection（成本归集）

```yaml
Action Type: CostCollection
Display Name: 成本归集
Description: 收集和录入项目成本数据，进行成本归集入账
Category: 业务操作类
Source Action: A011
Trigger Entity: ProjectCost
Result Entity: ProjectCost
Trigger Condition: 发生成本费用
Execution Subject: 成本会计、项目成本员
Permission Required: 成本录入权限
Related Process: P011（成本归集流程）
```

---

#### AT012：ReceiptConfirmation（收款确认）

```yaml
Action Type: ReceiptConfirmation
Display Name: 收款确认
Description: 确认收到业主款项并进行入账核销
Category: 业务操作类
Source Action: A012
Trigger Entity: Receipt
Result Entity: Receipt
Trigger Condition: 收到款项
Execution Subject: 财务人员
Permission Required: 财务权限
Related Process: P017（收款确认流程）
```

**业务规则**：
- 收款率 ≥ 80%为正常，<60%触发红色预警

---

#### AT013：InvoiceVerify（发票验证）

```yaml
Action Type: InvoiceVerify
Display Name: 发票验证
Description: 验证供应商开具的发票真实性和合规性
Category: 业务操作类
Source Action: A013
Trigger Entity: Invoice
Result Entity: Invoice
Trigger Condition: 收到发票
Execution Subject: 财务人员
Permission Required: 财务权限
```

---

#### AT014：FundTransfer（资金划转）

```yaml
Action Type: FundTransfer
Display Name: 资金划转
Description: 执行资金的转入转出操作
Category: 业务操作类
Source Action: A014
Trigger Entity: CashFlow
Result Entity: CashFlow
Trigger Condition: 付款审批通过
Execution Subject: 资金管理人员
Permission Required: 资金管理权限
```

---

#### AT015：GuaranteeIssue（保函开具）

```yaml
Action Type: GuaranteeIssue
Display Name: 保函开具
Description: 申请和开具各类保函（履约、质量、农民工工资等）
Category: 业务操作类
Source Action: A015
Trigger Entity: Guarantee
Result Entity: Guarantee
Trigger Condition: 合同要求
Execution Subject: 法务人员
Permission Required: 法务权限
Related Process: P019（保函管理流程）
```

**业务规则**：
- 关联诀窍：CM003（履约保函管理）

---

#### AT016：RiskAssessment（风险评估）

```yaml
Action Type: RiskAssessment
Display Name: 风险评估
Description: 对识别的风险进行评估和分级
Category: 业务操作类
Source Action: A016
Trigger Entity: Risk
Result Entity: Risk
Trigger Condition: 识别到风险
Execution Subject: 风控人员
Permission Required: 风控权限
Related Process: P023（风险识别流程）
```

**业务规则**：
- 关联规则：BR-E003（风险三色预警）

---

#### AT017：ClaimNegotiate（索赔谈判）

```yaml
Action Type: ClaimNegotiate
Display Name: 索赔谈判
Description: 与业主或供应商进行索赔谈判
Category: 业务操作类
Source Action: A017
Trigger Entity: Claim
Result Entity: Claim
Trigger Condition: 提出索赔申请
Execution Subject: 商务人员
Permission Required: 商务权限
Related Process: P025（索赔处理流程）
```

---

#### AT018：DataExport（数据导出）

```yaml
Action Type: DataExport
Display Name: 数据导出
Description: 导出业务数据为文件格式
Category: 业务操作类
Source Action: A018
Trigger Entity: Report
Result Entity: File
Trigger Condition: 用户请求导出
Execution Subject: 报表用户
Permission Required: 报表权限
```

---

#### AT019：ReportGenerate（报表生成）

```yaml
Action Type: ReportGenerate
Display Name: 报表生成
Description: 生成各类业务分析报表
Category: 业务操作类
Source Action: A019
Trigger Entity: Report
Result Entity: Report
Trigger Condition: 定时或用户请求
Execution Subject: 报表用户、系统自动
Permission Required: 报表权限
```

---

#### AT020：ConfirmOutput（确认产值）【企业特有动作】

```yaml
Action Type: ConfirmOutput
Display Name: 确认产值
Description: 确认项目已完成的工程量对应的产值
Category: 业务操作类
Source Action: A020（企业特有动作）
Trigger Entity: ProjectOutput
Result Entity: ProjectOutput
Trigger Condition: 完成工程量验收
Execution Subject: 商务人员、业主代表
Permission Required: 商务权限
Related Process: P013（成本分析流程）
```

**业务规则**：
- 支持产值双轨制（ER002）：已确认产值 + 待确认产值

---

#### AT021：ApplyChange（申请变更签证）【企业特有动作】

```yaml
Action Type: ApplyChange
Display Name: 申请变更签证
Description: 申请设计变更或现场签证
Category: 业务操作类
Source Action: A021（企业特有动作）
Trigger Entity: ChangeOrder
Result Entity: ChangeOrder
Trigger Condition: 发生变更事项
Execution Subject: 项目工程师
Permission Required: 项目权限
Related Process: P004（项目变更流程）、P012（变更签证流程）
```

**业务规则**：
- 变更发生后72小时内必须提出签证（CV001）

---

#### AT022：FileClaim（提交索赔）【企业特有动作】

```yaml
Action Type: FileClaim
Display Name: 提交索赔
Description: 提交索赔申请
Category: 业务操作类
Source Action: A022（企业特有动作）
Trigger Entity: Claim
Result Entity: Claim
Trigger Condition: 发生索赔事件
Execution Subject: 商务人员
Permission Required: 商务权限
Related Process: P025（索赔处理流程）
```

**业务规则**：
- 关联诀窍：CV004（变更索赔联动）

---

#### AT023：CollectReceivable（催收应收账款）【企业特有动作】

```yaml
Action Type: CollectReceivable
Display Name: 催收应收账款
Description: 对逾期应收账款进行催收
Category: 业务操作类
Source Action: A023（企业特有动作）
Trigger Entity: Receivable
Result Entity: Receivable
Trigger Condition: 应收账款逾期
Execution Subject: 财务人员、商务人员
Permission Required: 财务权限
```

**业务规则**：
- 逾期天数 > 90天触发预警

---

#### AT024：ApproveSubcontractSettlement（审批分包结算）【企业特有动作】

```yaml
Action Type: ApproveSubcontractSettlement
Display Name: 审批分包结算
Description: 对分包商的结算申请进行审批
Category: 业务操作类
Source Action: A024（企业特有动作）
Trigger Entity: Settlement
Result Entity: Settlement
Trigger Condition: 分包工程完工
Execution Subject: 结算专员、审批领导
Permission Required: 结算审批权限
Related Process: P016（付款审批流程）
```

---

### 2.3 系统类动作

#### AT025：DataSync（数据同步）

```yaml
Action Type: DataSync
Display Name: 数据同步
Description: 定时或事件触发的数据同步操作
Category: 系统类
Source Action: A025
Trigger Entity: System
Result Entity: System
Trigger Condition: 定时任务或数据变更事件
Execution Subject: 系统自动
Permission Required: 系统权限
```

---

#### AT026：AlertTrigger（预警触发）

```yaml
Action Type: AlertTrigger
Display Name: 预警触发
Description: 当满足预警条件时自动触发预警通知
Category: 系统类
Source Action: A026
Trigger Entity: AlertRule
Result Entity: AlertRecord
Trigger Condition: 指标值超出阈值
Execution Subject: 系统自动
Permission Required: 系统权限
```

**业务规则**：
- 关联规则：ER004（风险三色预警）

---

#### AT027：AuditLog（审计日志）

```yaml
Action Type: AuditLog
Display Name: 审计日志
Description: 记录所有业务操作的审计日志
Category: 系统类
Source Action: A027
Trigger Entity: System
Result Entity: AuditLog
Trigger Condition: 任何业务操作完成
Execution Subject: 系统自动
Permission Required: 系统权限
```

---

#### AT028：StatusChange（状态变更）

```yaml
Action Type: StatusChange
Display Name: 状态变更
Description: 根据流程完成情况自动变更业务实体状态
Category: 系统类
Source Action: A028
Trigger Entity: 各业务实体
Result Entity: 各业务实体
Trigger Condition: 流程节点完成
Execution Subject: 系统自动
Permission Required: 业务权限
```

---

#### AT029：DocumentArchive（文档归档）

```yaml
Action Type: DocumentArchive
Description: 文档归档
Description: 对业务文档进行归档保存
Category: 系统类
Source Action: A029
Trigger Entity: Document
Result Entity: Document
Trigger Condition: 流程结束
Execution Subject: 系统自动或文档管理员
Permission Required: 文档权限
```

---

#### AT030：EscalateRisk（升级风险上报）

```yaml
Action Type: EscalateRisk
Display Name: 升级风险上报
Description: 当红色预警触发时自动升级上报风险
Category: 系统类
Source Action: A030
Trigger Entity: Risk
Result Entity: AlertRecord
Trigger Condition: 红色预警触发
Execution Subject: 系统自动
Permission Required: 风控权限
Related Process: P024（风险处置流程）
```

---

## 三、Action Type 总览

### 3.1 Action Type 清单

| 编号 | Action Type | Display Name | 类别 | 触发实体 | 来源动作 | 关联流程 |
|-----|------------|-------------|------|---------|---------|---------|
| AT001 | ContractApproval | 合同审批 | 审批类 | Contract | A001 | P006 |
| AT002 | PaymentApproval | 付款审批 | 审批类 | Payment | A002 | P016 |
| AT003 | BudgetApproval | 预算审批 | 审批类 | Budget | A003 | P010 |
| AT004 | ChangeApproval | 变更审批 | 审批类 | ChangeOrder | A004 | P004, P012 |
| AT005 | SettlementApproval | 结算审批 | 审批类 | Settlement | A005 | P016, P021 |
| AT006 | ProjectApproval | 项目审批 | 审批类 | Project | A006 | P001 |
| AT007 | BidSubmission | 投标提交 | 审批类 | BidActivity | A007 | P002 |
| AT008 | TargetCostApproval | 目标成本审批 | 审批类 | TargetCost | A008 | P009 |
| AT009 | SectionDivision | 标段划分 | 审批类 | Section | A009 | P014 |
| AT010 | SectionSettlement | 标段结算 | 审批类 | Settlement | A010 | P015 |
| AT011 | CostCollection | 成本归集 | 业务操作类 | ProjectCost | A011 | P011 |
| AT012 | ReceiptConfirmation | 收款确认 | 业务操作类 | Receipt | A012 | P017 |
| AT013 | InvoiceVerify | 发票验证 | 业务操作类 | Invoice | A013 | - |
| AT014 | FundTransfer | 资金划转 | 业务操作类 | CashFlow | A014 | - |
| AT015 | GuaranteeIssue | 保函开具 | 业务操作类 | Guarantee | A015 | P019 |
| AT016 | RiskAssessment | 风险评估 | 业务操作类 | Risk | A016 | P023 |
| AT017 | ClaimNegotiate | 索赔谈判 | 业务操作类 | Claim | A017 | P025 |
| AT018 | DataExport | 数据导出 | 业务操作类 | Report | A018 | - |
| AT019 | ReportGenerate | 报表生成 | 业务操作类 | Report | A019 | - |
| AT020 | ConfirmOutput | 确认产值 | 业务操作类 | ProjectOutput | A020* | P013 |
| AT021 | ApplyChange | 申请变更签证 | 业务操作类 | ChangeOrder | A021* | P004, P012 |
| AT022 | FileClaim | 提交索赔 | 业务操作类 | Claim | A022* | P025 |
| AT023 | CollectReceivable | 催收应收账款 | 业务操作类 | Receivable | A023* | - |
| AT024 | ApproveSubcontractSettlement | 审批分包结算 | 业务操作类 | Settlement | A024* | P016 |
| AT025 | DataSync | 数据同步 | 系统类 | System | A025 | - |
| AT026 | AlertTrigger | 预警触发 | 系统类 | AlertRule | A026 | - |
| AT027 | AuditLog | 审计日志 | 系统类 | System | A027 | - |
| AT028 | StatusChange | 状态变更 | 系统类 | 各业务实体 | A028 | - |
| AT029 | DocumentArchive | 文档归档 | 系统类 | Document | A029 | - |
| AT030 | EscalateRisk | 升级风险上报 | 系统类 | Risk | A030 | P024 |

> 注：带*号的为企业特有动作（A020-A024）

### 3.2 Action Type 分类统计

| 类别 | 数量 | 说明 |
|------|------|------|
| 审批类 | 10个 | 合同审批、付款审批、预算审批等 |
| 业务操作类 | 14个 | 成本归集、收款确认、风险评估等（含5个企业特有动作） |
| 系统类 | 6个 | 数据同步、预警触发、审计日志等 |
| **合计** | **30个** | 覆盖所有核心业务动作 |

### 3.3 阶段一成果覆盖率

| 阶段一成果 | 覆盖数量 | 覆盖率 |
|-----------|---------|-------|
| 动作清单（30个） | 30个 | ✅ 100% 覆盖 |
| 企业特有动作（5个） | 5个 | ✅ 100% 覆盖 |
| 业务流程（25个） | 12个核心流程 | ✅ 核心流程覆盖 |

---

## 四、权限与角色映射

### 4.1 角色权限矩阵

| 角色 | 可执行动作 |
|------|-----------|
| 项目经理 | ProjectApproval, ChangeApproval, SectionDivision |
| 商务经理 | ContractApproval, BidSubmission, ClaimNegotiate, ConfirmOutput, FileClaim |
| 成本工程师 | TargetCostApproval, CostCollection, ChangeApproval |
| 财务人员 | PaymentApproval, ReceiptConfirmation, InvoiceVerify, FundTransfer, CollectReceivable |
| 法务人员 | ContractApproval, GuaranteeIssue |
| 风控人员 | RiskAssessment, EscalateRisk |
| 结算专员 | SettlementApproval, SectionSettlement, ApproveSubcontractSettlement |
| 系统管理员 | DataSync, AuditLog |

---

## 五、下一步工作

根据《040-本体设计方法.md》，Action Type设计完成后，需要进行：

1. **业务规则定义**（步骤4）
   - 详细定义计算规则
   - 详细定义勾稽关系
   - 详细定义约束条件
   - 详细定义数据标准

2. **本体设计确认**（步骤5）
   - 确认Object Type、Link Type、Action Type设计
   - 验证与阶段一成果的一致性
   - 形成本体设计确认文档

---

## 六、版本记录

| 版本 | 日期 | 更新内容 |
|-----|------|---------|
| V1.0 | 2026-06-12 | 初始版本，设计30个核心Action Type，覆盖阶段一全部动作清单 |

---

**设计人**：系统自动生成  
**设计时间**：2026年6月12日  
**适用项目**：潘达工程-商务成本智能决策体系