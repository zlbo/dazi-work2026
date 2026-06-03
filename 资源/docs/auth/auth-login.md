# 认证登录

**文档 ID**: `auth/auth-login`

## 登录方式

### Token 登录（推荐 CI/CD）

```bash
dazi auth set-token --token "eyJ..."
```

Token 存储在 `~/.dazi/auth.json`，可在多个项目间共享。

### 用户名密码登录

```bash
dazi auth login --username your@email.com --password yourpassword
```

### 验证登录状态

```bash
dazi auth whoami
```

## 多环境支持

通过环境变量切换服务器：

```powershell
$env:DAZI_BASE_URL = "https://staging.dazi.tech"
dazi auth whoami
```

或在 `.env` 文件中配置：

```
DAZI_BASE_URL=https://your-dazi-server.com
DAZI_AGENT_API_TOKEN=eyJ...
```
