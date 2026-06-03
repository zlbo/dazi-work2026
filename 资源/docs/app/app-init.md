# 应用初始化

**文档 ID**: `app/app-init`  
**适用**：搭子 v3 · 应用项目 `项目/app_<名称>/`

## 推荐：扩展创建

| 场景                     | 操作                                                                 |
| ------------------------ | -------------------------------------------------------------------- |
| 新建 monorepo + 首个组件 | 侧栏 **新建项目** → **应用项目** → **新建应用项目**                  |
| 已有项目加组件           | **新建项目** → **在已有项目下新建组件**，或 `dazi.app.component.new` |

生成目录：`项目/app_<名称>/apps/<app_id>/`（含 `manifest.json`、`src/`、`drap-assets/` 等）。

## CLI：从模板创建

**推荐**：在 **`dazi-work` 根目录**执行 `dazi app …`（脚本会自动设置 `DAZI_BUNDLED_DIR`，避免「未找到 bundled CLI」）：

```powershell
cd D:\path\to\dazi-work

# 从模板创建（--dir 相对 dazi-work 根）
dazi app init <template-id> --space <space-id> --dir 项目/app_<名>/apps/<app-id>

# 查看可用模板（含平台「转为应用模板」的动态模板）
dazi app templates list --remote
```

**可选**：在**应用项目根**（`项目/app_<名称>/`，含 `sdk/`、`templates/`）使用 `pnpm run dazi-app -- …`。若报「未找到 bundled CLI」，需将 `DAZI_BUNDLED_DIR` 指向扩展或 `tools/dazi-clis` 下的 `bundled/clis`，或改用上方 `dazi app`。

`template-id` 对应 `templates/app-template-*` 目录短名（如 `alarm-center` → `app-template-alarm-center`）。

## 创建后目录结构

```text
项目/app_<名称>/
├── sdk/、templates/、cli/
└── apps/<app-id>/
    ├── manifest.json      # 权威声明（upload 后进 Registry DB）
    ├── src/
    ├── drap-assets/
    ├── package.json
    └── AGENTS.md
```

## 清单要点

`manifest.json` 定义应用与平台的绑定关系，常用字段：

| 字段             | 说明                       |
| ---------------- | -------------------------- |
| `appId`          | Registry 全局唯一 ID       |
| `permissions`    | 至少 `dataspace:<spaceId>` |
| `data_sources[]` | 数据集 key + kind          |
| `mount`          | `page` 或 `chat_result`    |

扩展 **配置 manifest 数据源**（`dazi.app.editDataSources`）可图形化编辑 `data_sources`。

## 验证清单

```powershell
# 在 dazi-work 根
dazi app manifest validate --cwd 项目/app_<名>/apps/<app-id> --scan-src
```

## 相关文档

- [build-upload](./build-upload.md)
- 应用项目内 [quickstart](../../bundled/templates/runtime-apps-project/docs/quickstart.md)（复制到工作区后的 monorepo）
