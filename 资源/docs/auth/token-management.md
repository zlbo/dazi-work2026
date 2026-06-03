# Token 管理

**文档 ID**: `auth/token-management`

## Token 存储

Token 存储在 `~/.dazi/auth.json`，格式：

```json
{
  "token": "eyJ...",
  "serverUrl": "https://your-dazi.example.com",
  "username": "user@example.com",
  "savedAt": "2026-01-01T00:00:00.000Z"
}
```

## 迁移旧版 Token

```bash
# 预览
dazi auth migrate --dry-run

# 执行（从 ~/.dazi-app/auth.json 迁移）
dazi auth migrate
```

## Token 刷新

Token 过期后重新登录，旧 Token 自动覆盖：

```bash
dazi auth login
# 或
dazi auth set-token --token "<new-token>"
```

## 清除 Token

```bash
dazi auth logout
```
