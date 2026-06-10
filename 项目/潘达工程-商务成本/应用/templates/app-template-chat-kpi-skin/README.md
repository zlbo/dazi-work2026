# @dazi/app-template-chat-kpi-skin

DRAP **聊天问数 KPI 皮肤**（`mount.type=chat_result`）。

## 能力

- 仅消费宿主注入的 `message` 数据集（首行）
- 自动从数值列生成最多 4 张 `KpiCard`（无趋势图、无明细表）
- 生产入口 `prod-entry`：按 `window.__MICRO_APP_NAME__` 注册 `mount/unmount`，支持同会话多消息多实例

## 本地开发

```bash
cd templates/app-template-chat-kpi-skin
pnpm install   # 或在 monorepo 根目录 pnpm install
pnpm dev       # http://localhost:5182
```

## 发布到 Registry

```bash
pnpm run build
pnpm -C ../.. run dazi-app -- upload --space <space_id> --activate --changelog "chat-kpi-skin 0.1.0"
```

## 脚手架

```bash
pnpm -C ../.. run dazi-app -- init chat-kpi-skin --space space__0519 --app-id chat-kpi-skin
```

默认 manifest 已是 `chat_result`；也可用 `--profile chat-result`（与默认等价）。

## 聊天绑定

在管理端 **DRAP 聊天绑定** 将目标 `ontology_function_id` 指向本应用的 `app_id`（上传后的 Registry `app_id`）。
