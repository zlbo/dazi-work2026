# DRAP 数据源 Cookbook

> runtime-apps 自包含版。内联文件资产见 [inline-data-source.md](./inline-data-source.md)。

---

## 1. 铁律

- 子应用 **只读** 宿主预拉的 `datasets[key]`，或 SDK `refetch` / `invokeDataSource`。
- **禁止** 在子应用内 `fetch` 搭子 API。
- 改 `manifest.json` 后必须 **`upload --activate`**。

---

## 2. kind 速查

| kind | 数据从哪来 | manifest 关键字段 |
|------|------------|-------------------|
| `static` | manifest 内联或 zip 内 JSON | `data` 或 `static_file` |
| `sql_template` | 空间「已保存查询」 | `template_id`、`arguments`、`limit` |
| `script_entry` | 空间「已发布 DaziScript」 | `script_id`、`entry`、`arguments` |
| `ontology_function` | 本体函数 | `function_id`、`object_type_code`、`arguments` |
| `ontology_semantic` | 语义聚合 | `object_type_code`、`metric_request` |
| `cube_query` | Cube / 语义层 | `measures`、`dimensions`、`filters` |
| `sql_asset`（Phase E1+） | `drap-assets/sql/*.sql` | `source`、`arguments`、`limit` |
| `script_asset`（Phase E1+） | `drap-assets/python/*.py` | `source`、`entry`、`arguments` |

---

## 3. static（模板默认）

```json
{
  "key": "kpi",
  "kind": "static",
  "data": {
    "columns": ["label", "value", "unit"],
    "rows": [
      { "label": "营收", "value": 1000, "unit": "万" }
    ]
  }
}
```

---

## 4. sql_template（生产主路径）

**空间前置**：在数据空间创建并保存查询，记下 **query_id**。

```json
{
  "key": "detail",
  "kind": "sql_template",
  "template_id": "qry_production_detail_001",
  "arguments": { "plant_id": "P01" },
  "limit": 500
}
```

空间 policy 须包含 `sql_template` 等 kind；无权限时 `fetch-data-sources` 报 `kind not allowed`（见 [faq.md](./faq.md)）。

---

## 5. script_entry

**空间前置**：发布 DaziScript，返回 `{ columns, data }`。

```json
{
  "key": "kpi",
  "kind": "script_entry",
  "script_id": "scr_month_pl_kpi",
  "entry": "main",
  "arguments": { "year": 2026 }
}
```

---

## 6. ontology_function / ontology_semantic

```json
{
  "key": "kpi",
  "kind": "ontology_function",
  "function_id": "fc02.fn.month_pl_budget_kpi",
  "object_type_code": "FinPLMonthFact",
  "arguments": { "year": 2026, "month": 5 }
}
```

```json
{
  "key": "kpi",
  "kind": "ontology_semantic",
  "object_type_code": "FinPLMonthFact",
  "metric_request": {
    "measures": ["revenue", "profit"],
    "dimensions": [],
    "filters": []
  }
}
```

`permissions` 须含 `ontology_function:...` 或对应语义声明（VS Code 保存时可自动合并）。

---

## 7. cube_query

```json
{
  "key": "sales",
  "kind": "cube_query",
  "measures": ["Sales.amount"],
  "dimensions": ["Sales.region"],
  "limit": 200
}
```

---

## 8. sql_asset / script_asset（Phase E，文件资产）

SQL 写在 `drap-assets/sql/kpi.sql`，manifest：

```json
{
  "key": "kpi",
  "kind": "sql_asset",
  "source": "drap-assets/sql/kpi.sql",
  "arguments": {},
  "limit": 100
}
```

Python 写在 `drap-assets/python/kpi.py`：

```python
def main(params):
    return {
        "columns": ["label", "value", "unit"],
        "data": [{"label": "产量", "value": 100, "unit": "件"}],
        "row_count": 1,
    }
```

```json
{
  "key": "kpi",
  "kind": "script_asset",
  "source": "drap-assets/python/kpi.py",
  "entry": "main",
  "arguments": {}
}
```

**本地预览（E2，须 `auth login`）**：

```powershell
dazi-app preview sql kpi --cwd apps/my-app
dazi-app preview script kpi --params '{}'
dazi-app preview all
dazi-app test --key kpi
dazi-app asset list          # 推荐；旧名 drap-assets ls
dazi-app asset new-sql kpi2
```

测试夹具：`drap-assets/tests/<key>.params.json` + `<key>.expected.json`（对比列名与行数）。

---

## 9. 问数 vs 页模式

| 场景 | 主数据来源 |
|------|------------|
| 问数主区 | 宿主 `message` → `useResultDataset()` |
| 页模式 | `fetch-data-sources` → `useDataset(key)` |
| Chat 应用页模式预览 | manifest `static` 回退 |

---

## 10. permissions 与 policy

| data_sources 使用 | permissions 示例 |
|-------------------|------------------|
| 任意（需空间） | `dataspace:space__0519` |
| ontology_function | `ontology_function:fc02.fn.xxx` |
| cube_query | `cube:Sales` |

空间 `allowed_data_source_kinds` 须包含所用 kind。

---

## 11. 改 manifest 后必做

```powershell
pnpm run dazi-app -- manifest validate --scan-src
pnpm run dazi-app -- upload --cwd . --space <spaceId> --activate
```

Network 验收：`POST .../fetch-data-sources` 对应 key 的 `meta.ok === true`。
