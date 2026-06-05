# 内联数据源（sql_asset / script_asset）

> 应用内 SQL/Python 写在 `drap-assets/`，manifest 用 `sql_asset` / `script_asset` 引用。  
> 与空间资产（`sql_template` / `script_entry`）可混用。

---

## 1. 目录约定

```text
apps/<app_id>/
├── drap-assets/
│   ├── sql/              # *.sql
│   ├── python/           # *.py，入口默认 main(params)
│   ├── tests/            # 可选：预览/断言夹具
│   └── README.md
├── manifest.json
└── ...
```

---

## 2. manifest 字段

```json
{
  "data_sources": [
    {
      "key": "kpi",
      "kind": "sql_asset",
      "source": "drap-assets/sql/kpi.sql",
      "arguments": { "year": 2026 },
      "limit": 100
    },
    {
      "key": "trend",
      "kind": "script_asset",
      "source": "drap-assets/python/trend.py",
      "entry": "main",
      "arguments": {}
    }
  ]
}
```

| 字段 | 必填 | 说明 |
|------|------|------|
| `source` | ✓ | zip 内相对路径，须在 `drap-assets/` 下 |
| `arguments` | 可选 | SQL 参数；Python 为 `main(params)` 入参 |
| `limit` | sql_asset 可选 | 行数上限，默认 500 |
| `entry` | script_asset 可选 | 入口符号，默认 `main` |

**原则**：短 SQL 也放独立 `.sql` 文件，便于 Git diff 与 IDE 高亮；勿在 manifest 内联 SQL 文本。

---

## 3. Python 脚本约定

```python
def main(params):
    return {
        "columns": ["label", "value", "unit"],
        "data": [{"label": "产量", "value": 100, "unit": "件"}],
        "row_count": 1,
    }
```

返回须含 `columns` 与 `data`（或 `rows`），与 `sql_template` 结果形态一致。

---

## 4. 本地预览与测试

```powershell
pnpm -C ../.. run dazi-app -- preview sql kpi --cwd apps/<app_id>
pnpm -C ../.. run dazi-app -- preview script kpi --cwd apps/<app_id>
pnpm -C ../.. run dazi-app -- preview all --cwd apps/<app_id>
pnpm -C ../.. run dazi-app -- test --key kpi --cwd apps/<app_id>
pnpm -C ../.. run dazi-app -- asset list --cwd apps/<app_id>
# 旧名仍可用：drap-assets ls
```

须已 `auth login`（API 见 [env.md](./env.md)）。

测试夹具：`drap-assets/tests/<key>.params.json` + 可选 `<key>.expected.json`。

---

## 5. 发布注意

- `upload` 会将 `drap-assets/` 打入 zip
- 改 manifest 或资产后须 **`upload --activate`**
- 组件仍只读 `useDataset(key)`，禁止裸 `fetch`

更多 kind 组合见 [data-source-cookbook.md](./data-source-cookbook.md)。
