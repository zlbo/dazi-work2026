# Onto 内置示例

`dazi examples sync` 后位于 **`资源/examples/onto/`**。每个子目录是**完整本体单元**（与业务 `ontos/<实现>/` 同构）：

```text
<示例名>/
├── README.md
├── plans/          ← ★ 规划正文（真理源）
├── setup/          ← init、seed、category_mount
└── functions/      ← 本体函数 + test_arguments
```

**规划 / 脚本前**：须至少阅读 **一个** 示例的 `README.md` + `plans/*.md`。索引见 **`index.yaml`** / **`index.json`**（`dazi examples onto list`）。

## 示例一览

| 目录 | 域 | 规划（plans/） | 函数数 |
|------|-----|----------------|--------|
| [销售示例](./销售示例/) | 销售、订单、渠道 | `规划示例_产品销售本体规划方案.md` | 7 |
| [利润示例](./利润示例/) | GL、科目、预实 | `规划示例_利润分析本体方案.md` | 7 |
| [设备运营](./设备运营/) | 设备、OEE、停机 | `化工设备运营分析本体方案.md` | 11 |

> 规划正文仅在 `examples/onto/<示例>/plans/`；`dazi examples onto show <id> --plan`。

## 复制到业务项目

```text
资源/examples/onto/<示例>/setup/*       → 项目/<业务>/本体/ontos/<实现>/setup/
资源/examples/onto/<示例>/functions/*   → 项目/<业务>/本体/ontos/<实现>/functions/
```

规划须在本项目 **`plans/` 独立撰写**；示例 `plans/` 仅供只读对照（见快速启动 §0）。

## 模板与工具

| 路径 | 说明 |
|------|------|
| [_templates/ontology_function_template.py](./_templates/ontology_function_template.py) | 新建函数结构模板 |
| [_templates/onto_preflight.ps1](./_templates/onto_preflight.ps1) | 函数数 / publish-preview 门禁 |

```powershell
dazi examples onto list
dazi examples onto suggest 设备 OEE
dazi examples onto show equip-ops --plan
dazi examples list --category onto
dazi examples show onto/readme
```

侧栏 **帮助 → 示例** 可按 `onto-销售-函数`、`onto-设备运营-函数` 等分类浏览。
