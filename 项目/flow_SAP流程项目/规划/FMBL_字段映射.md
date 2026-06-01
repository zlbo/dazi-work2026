# SAP FMBL 字段中文映射

供 `sap_flow01` 及后续节点 @ 引用。

| SAP 物理列 | 中文列名 | 说明 |
| --- | --- | --- |
| `/BIC/LOGSYS` | 逻辑系统 | BW 逻辑系统 |
| `CLIENT` | 客户端 | Client |
| `FM_AREA` | 财务管理范围 | FIKRS |
| `DOCYEAR` | 凭证年度 | 预算凭证年度 |
| `DOCNR` | 凭证编号 | 预算录入凭证号 |
| `DOCLN` | 凭证行号 | 行项目号 |
| `RPMAX` | 期间 | Period |
| `FLG_ADDED` | 附加行标识 | |
| `CTEM_CATEGORY` | 承诺项类别 | |
| `FISCYEAR` | 财年 | 筛选 `='2025'` |
| `CEFFYEAR` | 现金生效年度 | |
| `FUND` | 基金 | |
| `BUDGET_PD` | 预算期间 | |
| `FUNDSCTR` | 基金中心 | FISTL |
| `CMMTITEM` | 承诺项 | FM_FIPEX |
| `FUNCAREA` | 功能范围 | |
| `GRANT_NBR` | 资助 | |
| `MEASURE` | 资助项目 | |
| `USERDIM` | 用户维度 | |
| `BUDCAT` | 预算类别 | 样例 `9F` |
| `VALTYPE` | 值类型 | 样例 `B1` |
| `PROCESS` | 预算流程 | 样例 `ENTR` |
| `BUDTYPE` | 预算类型 | 样例 `ND` |
| `TCURR` | 交易货币 | |
| `TVAL01`–`TVAL12` | 交易金额_01月–12月 | 交易币各期金额 |
| `LVAL01`–`LVAL12` | 本币金额_01月–12月 | 本币各期金额 |
| `DISTKEY` | 分配键 | |
| `TEXT50` | 行文本 | |
| `RID` | 行ID | 技术标识 |

**流程变量**

| 节点 | `output_variable_name` |
| --- | --- |
| 读取FMBL_2025预算明细 | `预算明细_2025` |
| 合计1至12月交易金额 | `预算年度交易合计`（含 `交易金额_1至12月合计`、`本币金额_1至12月合计`） |

数据源：`duckdb__ods_budget_expense` · 表 `FMBL` · 详见 `资源/datasources/ods_budget_expense/FMBL.md`。
