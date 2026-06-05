# pnpm 安装故障排除手册

## 一、常见问题及解决方案

### 问题 1：Lockfile 供应链策略检查失败

**错误信息：**
```
Lockfile failed supply-chain policy check
[ERR_PNPM_MINIMUM_RELEASE_AGE_VIOLATION] xxx was published at ... within the minimumReleaseAge cutoff
```

**问题原因：**
pnpm 的供应链策略会检查包的发布时间，过于新的包（通常是发布后几小时内）会被拒绝安装，这是一种安全措施，防止刚发布的恶意包。

**解决方案：**
```powershell
# 清理 lockfile
pnpm clean --lockfile

# 重新安装
pnpm install
```

**原理说明：**
清理 lockfile 后重新安装，pnpm 会重新解析依赖，可能会选择稍旧版本的包，或者等待新版本包满足发布时间要求。

---

### 问题 2：构建脚本被忽略

**错误信息：**
```
[ERR_PNPM_IGNORED_BUILDS] Ignored build scripts: esbuild@x.x.x
Run "pnpm approve-builds" to pick which dependencies should be allowed to run scripts.
```

**问题原因：**
pnpm 默认会忽略某些包的构建脚本，特别是需要编译的 native 模块（如 esbuild）。

**解决方案（推荐）：**
```powershell
# 启用预/post 脚本并重建相关包
$env:PNPM_ENABLE_PRE_POST_SCRIPTS="true"
pnpm rebuild esbuild

# 再次安装确保完整
pnpm install
```

**替代方案（适用于多个包需要构建）：**
```powershell
# 使用 --unsafe-perm 允许所有构建脚本（需谨慎）
pnpm install --unsafe-perm
```

---

### 问题 3：网络超时或连接失败

**错误信息：**
```
ERR_PNPM_FETCH_404
ERR_PNPM_FETCH_ERROR
```

**问题原因：**
网络问题或 npm 仓库访问受限。

**解决方案：**
```powershell
# 设置国内镜像源
pnpm config set registry https://registry.npmmirror.com

# 清理缓存后重试
pnpm store prune
pnpm install
```

---

### 问题 4：依赖版本冲突

**错误信息：**
```
ERR_PNPM_VERSION_MISMATCH
```

**问题原因：**
package.json 中声明的依赖版本与 lockfile 中的版本不一致。

**解决方案：**
```powershell
# 清理 lockfile 并重新安装
pnpm clean --lockfile
pnpm install
```

---

## 二、推荐的安装流程

为了避免上述问题，建议遵循以下安装流程：

```powershell
# 1. 设置国内镜像（首次安装或网络问题时）
pnpm config set registry https://registry.npmmirror.com

# 2. 清理旧的 lockfile（可选但推荐）
pnpm clean --lockfile

# 3. 执行安装
pnpm install

# 4. 如果遇到构建脚本问题，执行重建
pnpm rebuild
```

---

## 三、常见命令速查

| 命令 | 用途 |
|------|------|
| `pnpm install` | 安装依赖 |
| `pnpm clean --lockfile` | 清理 lockfile |
| `pnpm rebuild <package>` | 重建指定包 |
| `pnpm config set registry <url>` | 设置镜像源 |
| `pnpm store prune` | 清理缓存 |
| `pnpm approve-builds` | 交互式批准构建脚本 |

---

## 四、预防措施

1. **定期更新 lockfile**：定期运行 `pnpm update` 更新依赖版本，避免 lockfile 过于陈旧。

2. **使用稳定的镜像源**：设置国内镜像源可以提高下载速度和稳定性。

3. **理解依赖版本范围**：在 package.json 中合理设置版本范围，避免意外升级到不稳定版本。

4. **备份 lockfile**：在进行重大更改前备份 lockfile，便于回滚。

---

## 五、问题反馈

如果遇到本手册未覆盖的问题，请记录以下信息：
- 完整的错误信息
- pnpm 版本 (`pnpm --version`)
- Node.js 版本 (`node --version`)
- 操作系统及版本
- 网络环境（内网/外网）

---

**文档版本**：v1.0  
**创建日期**：2026-06-01  
**适用范围**：pnpm 安装相关问题

