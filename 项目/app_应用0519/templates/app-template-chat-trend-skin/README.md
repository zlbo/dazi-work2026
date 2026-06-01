# @dazi/app-template-chat-trend-skin

DRAP 聊天问数 **趋势图** 皮肤（`mount.type=chat_result`）。

## 开发

```powershell
cd templates/app-template-chat-trend-skin
pnpm run dev   # 5183
```

## 发布

```powershell
pnpm run build
pnpm -C ../.. run dazi-app -- upload --space <space_id> --activate
```

## init

```powershell
pnpm -C ../.. run dazi-app -- init chat-trend-skin --space space__0519 --app-id chat-trend-skin
```
