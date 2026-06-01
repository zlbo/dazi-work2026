# 应用发布管理

**文档 ID**: `app/release-guide`  
**适用**：在 **`dazi-work` 根**通过 `.\scripts\dazi.ps1 app …` 管理发布；`--cwd` 指向 `项目/app_<名>/apps/<app_id>/`。

场景实践：[主要财务指标复杂报表开发实践](./主要财务指标复杂报表开发实践.md)（模板 `financial-indicators-complex-report`）。

```powershell
cd D:\path\to\dazi-work

# 查看某应用的发布版本
.\scripts\dazi.ps1 app release list <app-id> --cwd 项目/app_<名>/apps/<app-id>
```

扩展 **构建并发布** 会调用同一套 API；发布目标由 `dazi.serverUrl` / `~/.dazi/auth.json` 决定（见 §333）。

## 查看发布版本

```powershell
.\scripts\dazi.ps1 app release list <app-id> --cwd 项目/app_<名>/apps/<app-id>
```

## 激活指定版本

```powershell
.\scripts\dazi.ps1 app release activate <app-id> --semver 1.2.0 --cwd 项目/app_<名>/apps/<app-id>
```

## 撤回版本

```powershell
.\scripts\dazi.ps1 app release revoke <app-id> --semver 1.2.0 --cwd 项目/app_<名>/apps/<app-id>
```

## 版本号规范

遵循 semver：`MAJOR.MINOR.PATCH`

- **MAJOR**：不兼容的 API 变更
- **MINOR**：向下兼容的功能新增
- **PATCH**：向下兼容的问题修正

## 资源管理

```powershell
.\scripts\dazi.ps1 app asset list --cwd 项目/app_<名>/apps/<app-id>
.\scripts\dazi.ps1 app asset new-sql --cwd 项目/app_<名>/apps/<app-id>
.\scripts\dazi.ps1 app asset new-script --cwd 项目/app_<名>/apps/<app-id>
```

> **说明**：亦可在应用项目根使用 `pnpm run dazi-app -- release list …` 等等价命令，但需先配置 `DAZI_BUNDLED_DIR`；推荐统一使用 `.\scripts\dazi.ps1 app`。
