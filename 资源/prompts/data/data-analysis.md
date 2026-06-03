# 提示词：数据分析

**提示词 ID**: `data/data-analysis`  
**场景**: 分析数据表内容

---

以下是数据表结构，请帮我分析数据并给出洞察。

## 数据表信息

**表名**: {{table_name}}  
**数据空间**: {{space_name}}

### 字段结构

```
{{table_schema}}
```

### 数据样本（前 10 行）

```
{{data_sample}}
```

## 分析要求

{{analysis_requirement}}

## 参考命令

```bash
# 查看表结构
dazi data table schema <table-id> --space <space-id>

# 采样数据（在 VS Code 侧栏点击表名）
dazi data table sample <table-id> --space <space-id> --rows 20

# 使用 Flow 做批量分析
dazi-flow run start <analysis-flow-id>
```
