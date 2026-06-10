# Flow 开发标准操作程序（SOP）- 临时版本

> **状态**：待架构师确认  
> **创建日期**：2026-06-10  
> **更新日期**：2026-06-10  
> **适用范围**：dazi-flow 流程开发

---

## 一、开发前检查清单（必须完成才能开始写代码）

### 1.1 数据源信息收集
- [ ] 查看数据源表结构文档（`资源/datasources/数据源名/表名.md`）
- [ ] 确认数据源 `connectionId`（字符串类型，如 `"duckdb__建工成本01"`）
- [ ] 记录所有字段名称和数据类型
- [ ] 确认数据量级（预估行数）

### 1.2 目标表信息收集
- [ ] 查看本体模型表定义（`资源/dataspaces/space__panda_construction/表名.md`）
- [ ] 确认目标表字段映射关系
- [ ] 确认数据写入方式（追加/覆盖/合并）
- [ ] 注意：数据源表不一定包含目标表的所有字段，需合理处理缺失字段

### 1.3 流程设计确认
- [ ] 绘制流程图（节点类型和连接关系）
- [ ] 确认每个节点的输入输出变量名
- [ ] 确认节点类型（`database-source`、`python-script`、`dataspace-sink` 等）

### 1.4 参考示例查看
- [ ] 查看 `flow-example/flow.json` 中的正确配置
- [ ] 查看示例节点的 `code.*` 文件
- [ ] 确认平台规范要求

---

## 二、节点开发规范

### 2.1 数据读取节点（`database-source`）
**配置要点**：
```json
{
"type": "database-source",
"connectionId": "duckdb__建工成本01",  // 字符串类型，必须与数据源文档一致
"output_variable_name": "output_raw_data",
"queryConfig": {
    "tableName": "tb_project_income_outcome_summary",
    "selectedFields": ["id", "project_id", "year", "month", ...],
    "useAliases": true,
    "distinct": false,
    "rowLimit": 200000,
    "filters": []
},
"tableName": "tb_project_income_outcome_summary"
}
```

**常见错误**：
- ❌ 使用 `dataSourceId`（数字ID，已验证不可用）
- ❌ 使用 `code.sql`（必须使用 `queryConfig`）
- ❌ 字段名拼写错误（必须与表结构文档一致）

### 2.2 Python 转换节点（`python-script`）
**配置要点**：
```python
# 必须定义 result_df 作为输出变量
import pandas as pd

df = get_variable("input_data")

# 字段映射必须使用实际字段名
result_df = df.copy()

# 类型转换：确保使用 Python 原生类型
result_df['amount'] = df['amount'].fillna(0.0).tolist()
result_df['count'] = df['count'].fillna(0).astype(int).tolist()
```

**常见错误**：
- ❌ 使用 `validated_df` 而不是 `result_df`
- ❌ 字段名假设（必须先查看表结构）
- ❌ 输出 numpy 类型数据（需转换为 Python 原生类型）

### 2.3 数据写入节点（`dataspace-sink`）
**配置要点**：
```json
{
"type": "dataspace-sink",
"spaceId": "space__panda_construction",
"tableName": "fact_project_output",
"writeMode": "append",
"input_variable_name": "validated_output_data"
}
```

**注意**：**必须有数据写入节点，否则数据不会落地到本体模型表**

---

## 三、开发流程

### 3.1 按顺序执行
1. **信息收集** → 完成检查清单
2. **流程设计** → 绘制节点和连接
3. **节点开发** → 按节点类型编写代码
4. **逐节点测试** → `node push` → `node-exec` → `variable pull`
5. **全流程测试** → 运行完整流程
6. **数据验证** → 检查数据是否落地到目标表

### 3.2 测试验证步骤
```powershell
# 1. 推送代码
dazi flow node push --node <node_uuid> --dir "流程目录"

# 2. 单节点测试
dazi flow run node-exec --node <node_uuid> --dir "流程目录" --json

# 3. 验证输出变量
dazi flow variable pull --name <variable_name> --dir "流程目录"

# 4. 全流程测试
dazi flow run flow-exec --dir "流程目录" --type debug

# 5. 检查数据是否落地（查询目标表）
```

---

## 四、常见错误排查

### 4.1 "数据连接不存在"
**原因**：使用了错误的数据源标识  
**解决**：使用 `connectionId`（字符串类型），值必须与数据源文档一致

### 4.2 "字段不存在"
**原因**：字段名拼写错误或假设字段名  
**解决**：查看表结构文档，使用实际字段名

### 4.3 "Code did not define 'result_df'"
**原因**：Python 节点没有定义 `result_df`  
**解决**：将输出变量命名为 `result_df`

### 4.4 数据没有落地到目标表
**原因**：缺少 `dataspace-sink` 数据写入节点  
**解决**：添加数据写入节点，配置 `spaceId` 和 `tableName`

### 4.5 "object of type 'numpy.float64' has no len()"
**原因**：Python 节点输出了 numpy 类型数据  
**解决**：使用 `tolist()` 转换为 Python 原生类型

### 4.6 "Unrecognized column 'xxx' in table"
**原因**：输出字段与目标表不匹配  
**解决**：确保只输出目标表中存在的字段

---

## 五、数据落地规范

### 5.1 必须包含的节点
- [ ] 数据读取节点（`database-source`）
- [ ] 数据转换节点（`python-script`）
- [ ] 数据质量检查节点（`python-script`）
- [ ] **数据写入节点（`dataspace-sink`）← 关键！**

### 5.2 数据写入节点配置
```json
{
"type": "dataspace-sink",
"label": "写入产值数据",
"spaceId": "space__panda_construction",
"tableName": "fact_project_output",  // 目标表名
"writeMode": "append",  // 追加模式
"input_variable_name": "validated_output_data"
}
```

### 5.3 字段映射注意事项
- 数据源表可能不包含目标表的所有字段
- 缺失字段可设置默认值（如 `0.0`、`''`、`0`）
- 字段类型必须与目标表一致

---

## 六、文档参考

- `资源/docs/flow/flows-guide.md` - 流程开发指南
- `资源/docs/flow/node-code-guide.md` - 节点代码指南
- `项目/潘达工程-商务成本/流程/flows/flow-example/` - 正确示例
- `资源/datasources/数据源名/表名.md` - 数据源表结构
- `资源/dataspaces/space__panda_construction/表名.md` - 本体模型表定义

---

## 七、已验证的正确配置示例

### 7.1 database-source 节点
```json
{
"id": "database-source-output",
"data": {
    "label": "读取产值数据",
    "type": "database-source",
    "connectionId": "duckdb__建工成本01",
    "output_variable_name": "output_raw_data",
    "queryConfig": {
    "tableName": "tb_project_income_outcome_summary",
    "selectedFields": ["id", "project_id", "year", "month", "code", "name", "project_amount", "company_amount", "total", "remark", "status", "create_time", "create_by", "update_time", "update_by"],
    "useAliases": true,
    "distinct": false,
    "rowLimit": 200000,
    "filters": []
    },
    "tableName": "tb_project_income_outcome_summary"
}
}
```

### 7.2 dataspace-sink 节点
```json
{
"id": "dataspace-sink-output",
"data": {
    "label": "写入产值数据",
    "type": "dataspace-sink",
    "spaceId": "space__panda_construction",
    "tableName": "fact_project_output",
    "writeMode": "append",
    "input_variable_name": "validated_output_data"
}
}
```

---

## 八、待确认事项（提交给架构师）

1. **数据源标识**：平台应使用 `connectionId` 还是 `dataSourceId`？
2. **文档更新**：是否需要更新 `资源/datasources/` 目录下的连接配置文档？
3. **数据写入规范**：`dataspace-sink` 节点的标准配置是什么？
4. **类型转换**：是否需要在平台层面自动处理 numpy 类型转换？
5. **错误提示**：是否需要优化平台错误提示？

---

**记录人**：开发团队  
**记录时间**：2026-06-10  
**更新时间**：2026-06-10  
**状态**：待架构师确认