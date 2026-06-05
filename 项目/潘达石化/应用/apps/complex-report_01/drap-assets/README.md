# drap-assets · complex-report_01

本目录存放随 DRAP 组件 **zip 一起发布** 的 SQL / Python 资产（Phase E）。

## 目录

| 路径 | 用途 |
|------|------|
| `sql/*.sql` | `sql_asset` 数据源（manifest `source: "drap-assets/sql/..."`） |
| `python/*.py` | `script_asset` 数据源（须实现 `def main(params):` 返回 `{ columns, data }`） |
| `tests/*.json` | 预览测试参数（`dazi-app test`，E2+） |

## manifest 示例

```json
{
  "key": "kpi",
  "kind": "sql_asset",
  "source": "drap-assets/sql/kpi.sql",
  "arguments": {},
  "limit": 100
}
```

## 注意

- 改 SQL/Python 后须 `upload --activate` 才在线上生效
- 预览：`dazi-app preview sql kpi`、`dazi-app test`、`dazi-app drap-assets ls`
- 详见 `docs/data-source-cookbook.md` 与 `docs/inline-data-source.md`
