# 工作区 v3 规范

**文档 ID**: `guides/workspace-v3`  
**适用版本**: dazi-vscode v3.0+  
**最后更新**: 2026-05-28（应用项目 `项目/app_*`）

## 目录结构（搭子工作区，如 dazi-work）

```text
<workspace>/
├── 项目/
│   ├── onto_<名称>/          ← 本体项目（规划、脚本、快速启动）
│   └── app_<名称>/           ← ★ 应用项目 = DRAP monorepo（sdk、templates、apps）
├── 资源/                     ← 帮助文档、提示词等（dazi docs sync）
├── scripts/                  ← dazi.ps1、doctor-cli（终端 CLI 包装）
├── tools/dazi-clis/          ← 可选：离线 bundled CLI 副本
└── （可选）runtime-apps/     ← 兼容旧布局；可与 项目/app_* 并存
```

> v3.1+ **推荐**在 `项目/app_<名称>/` 下维护 DRAP，由扩展「新建应用项目」生成。详见 [§331](../../docs/331-应用项目多项目与组件重构.md)。

## 目录说明

| 路径 | 对应 CLI | 用途 |
|------|----------|------|
| `项目/onto_<名称>/` | `.\scripts\dazi.ps1 onto ...` | 本体规划、脚本、发布 |
| `项目/app_<名称>/` | `pnpm run dazi-app -- ...`（在应用项目根） | DRAP monorepo；组件在 `apps/<app_id>/` |
| `项目/app_<名称>/apps/<app_id>/` | 同上 + `--cwd apps/<app_id>` | 单个应用组件源码 |
| `资源/docs/` | `.\scripts\dazi.ps1 docs ...` | 同步后的内置文档 |
| `scripts/` | `.\scripts\dazi.ps1 ...` | 本体/流程/鉴权/数据（非 DRAP） |
| `~/.dazi/auth.json` | 共享 | 登录凭据（扩展与 CLI 共用） |

## 扩展侧栏对应

| 侧栏 | 工作区路径 |
|------|------------|
| 本体 | `项目/onto_*` |
| App 应用 | `项目/app_*`（monorepo）→ `apps/<app_id>` |
| 数据资源 | 平台数据空间（非目录） |

## v2 → v3 目录映射

| v2 | v3（搭子工作区） |
|----|----------------|
| `ontology/` | `项目/onto_*` |
| `runtime-apps/apps/*` | `项目/app_*/apps/*`（推荐）或 `<ws>/runtime-apps/apps/*`（兼容） |
| `.dazi-agent/auth.json` | `~/.dazi/auth.json` |

## 相关文档

- [§331 应用项目多项目与组件重构](../../docs/331-应用项目多项目与组件重构.md)
- [§333 本轮扩展总结](../../docs/333-dazi-vscode应用项目多项目与本轮优化总结.md)
- [CLI 调用约定](./cli-invocation.md)
