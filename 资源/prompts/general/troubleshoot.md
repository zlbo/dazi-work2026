# 提示词：问题排查

**提示词 ID**: `general/troubleshoot`  
**场景**: 分析搭子平台错误

---

以下是遇到的错误，请帮助排查。

## 错误信息

```
{{error_message}}
```

## 环境信息

```powershell
# 在 dazi-work 根目录运行
.\scripts\doctor-cli.ps1
.\scripts\dazi.ps1 doctor
.\scripts\dazi.ps1 env
.\scripts\dazi.ps1 auth whoami
```

环境输出：
```
{{env_output}}
```

## 排查步骤

请按以下顺序排查：

1. **认证问题**：401/403 错误
2. **网络问题**：连接超时/DNS 解析失败
3. **配置问题**：`dazi.serverUrl` / `DAZI_BASE_URL` 配置错误
4. **版本问题**：CLI 与平台 API 版本不兼容
5. **权限问题**：空间/资源访问权限不足

给出具体的修复命令和步骤。
