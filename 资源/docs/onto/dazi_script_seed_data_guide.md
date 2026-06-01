# DaziScript 灌数脚本编写指南

**文档 ID**: `onto/dazi-script-seed-data-guide`  
**适用**: dazi-vscode v3 + ClickHouse 数据空间

> **用途**：约定工作区内「一次性 / 可重复执行」的造数、补数、历史回填脚本的写法，供人与 LLM 统一遵循。  
> SDK API 见 **[dazi_script_sdk_reference](./dazi_script_sdk_reference.md)**；目录与发布见 **[本体脚本编写指南](./本体脚本编写指南.md)**。

---

## 1. 什么是灌数脚本

**灌数脚本**指在**已存在表结构**（或同脚本内先 DDL）的前提下，向当前空间写入**演示数据、回归数据、历史样本**的 DaziScript。

### 1.1 放置位置（v3）

| 类型 | 推荐路径 |
|------|----------|
| **项目内开发** | `<工作区根>/项目/onto_<项目名>/脚本/<名称>.py` |
| **参考示例** | `资源/examples/onto/setup/`（初始化+灌数一体）、`资源/examples/onto/function/`（分析函数，非灌数专篇） |

- `space_id` 以 **`项目/onto_<项目名>/README.md`** 为准（扩展「新建项目」时已绑定）。
- 侧栏 **帮助 → 📎 示例 → 下载所有示例**，或：`.\scripts\dazi.ps1 examples sync` → `资源/examples/`。
- 须定义 **`main()`**，**不要**写 `if __name__ == "__main__":`。

> 不再使用 `spaces/<space_id>/editorial/scripts/setup/` 作为 v3 本地约定路径。

---

## 2. 硬约束（违反易导致联调失败）

### 2.1 ClickHouse：`INSERT ... VALUES` 与注释

- **`VALUES` 与各元组之间禁止 SQL 行注释 `--`**。常见报错：`CANNOT_PARSE_INPUT_ASSERTION_FAILED`、`Code: 27`。
- **允许**：在**整条** `INSERT` **之前**写注释；或拆成多条 `INSERT`。
- **推荐**：大批量灌数用 **`s.sql.insert_rows(table, rows)`**（`rows` 为 `list[dict]`）。

### 2.2 幂等与可重复执行

- 先 `query_one` / `count()` 判断已有数据，满足阈值则**跳过**或**仅补差额**。
- 「清空再灌」须**显式开关**（如 `--force`），**默认**不破坏已有数据。

### 2.3 数据质量

- 枚举字段勿含多余空格；`Date` / `DateTime` 与表定义、SDK 规整规则一致。

### 2.4 输出与验收

- 关键步骤 `output.print`；结束可用 `output.success(...)`。
- 机器解析约定：`__JSON_SUMMARY__` + JSON（与回归脚本一致）。

---

## 3. 推荐模式对照

| 场景 | 推荐做法 |
|------|----------|
| 少量固定行 | 单条 `INSERT ... VALUES`，元组间**无**行间 `--`；或拆多条 `INSERT` |
| 多批次、多行 | **`s.sql.insert_rows`** + Python 生成 `list[dict]` |
| 需读 SQL 文件 | 注释写在 **INSERT 块上方**（Python 侧），不要塞进 `VALUES` 中间 |

---

## 4. 示例：`insert_rows`（推荐）

将 `space_id`、表名、列名替换为项目 README 与规划文档中的真实值。表须已存在（或在本脚本前文 DDL 创建）。

```python
"""示例：按空间灌入演示数据（幂等 + insert_rows）

放置：项目/onto_<项目名>/脚本/demo_seed.py
space_id：见项目 README.md
"""

import json


def main():
    space_id = "space__your_id_here"  # 与 README 一致
    table = "your_fact_table"
    s = space.get(space_id)

    try:
        n = int(s.sql.query_one(f"SELECT count() FROM {table}") or 0)
    except Exception:
        n = 0
    if n > 0:
        output.print(f"{table} 已有 {n} 行，跳过灌数")
        return

    rows = [
        {"id": "row_001", "name": "样例A", "metric_value": 100.5, "biz_date": "2025-01-10"},
        {"id": "row_002", "name": "样例B", "metric_value": 200.0, "biz_date": "2025-01-11"},
    ]

    inserted = s.sql.insert_rows(table, rows)
    output.print(f"已插入 {inserted} 行")
    output.success("灌数完成")
    output.print("__JSON_SUMMARY__" + json.dumps(
        {"ok": True, "table": table, "inserted": inserted},
        ensure_ascii=True,
        default=str,
    ))
```

---

## 5. 示例：单条 `execute` + `VALUES`

```python
def main():
    s = space.get("space__your_id_here")
    if int(s.sql.query_one("SELECT count() FROM your_fact_table WHERE id = 'row_001'") or 0) > 0:
        output.print("已存在，跳过")
        return

    s.sql.execute(
        """
        INSERT INTO your_fact_table VALUES
        ('row_001', '样例A', 100.5, toDate('2025-01-10')),
        ('row_002', '样例B', 200.0, toDate('2025-01-11'))
        """
    )
    output.success("灌数完成")
```

---

## 6. 发布与执行（dazi-vscode）

在工作区根目录（`--space` 与项目 README 一致）：

```bash
# 预检
.\scripts\dazi.ps1 onto script publish-preview 项目/onto_<项目名>/脚本/demo_seed.py --space <space-id>

# 发布到平台（data_script / 初始化脚本）
.\scripts\dazi.ps1 onto script publish 项目/onto_<项目名>/脚本/demo_seed.py --space <space-id>

# 若已入库且已知 script-id，可在平台侧执行；或通过 Onto 侧栏运行
.\scripts\dazi.ps1 onto script run --script-id <script-id> --space <space-id> --params '{}'
```

**参考完整初始化+灌数**：复制 `资源/examples/onto/setup/profit_ontology_init.py` 到 `项目/.../脚本/` 后按空间改 `space_id` 与表名，再发布执行。

> **已废弃**：`dazi-agent run --file "spaces/.../editorial/..."` — 请改用上表 `.\scripts\dazi.ps1 onto script publish` / `function run`。

---

## 7. 相关文档

- [DaziScript SDK 参考](./dazi_script_sdk_reference.md)
- [本体脚本编写指南](./本体脚本编写指南.md)
- [本体脚本编写指南](./本体脚本编写指南.md)
- [本体规划指南](./本体规划指南.md)
