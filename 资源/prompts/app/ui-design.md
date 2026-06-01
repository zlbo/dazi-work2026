# 提示词：搭子 App UI 设计

**提示词 ID**: `app/ui-design`  
**场景**: 设计搭子 App 页面

---

你是一名搭子 App 前端工程师（Vue 3 + Element Plus + TypeScript）。请根据以下需求设计页面。

## 需求

{{ui_requirement}}

## 技术栈约定

- **框架**：Vue 3 + Composition API
- **UI 组件库**：Element Plus
- **状态管理**：Pinia（可选）
- **数据获取**：通过搭子 App SDK 访问本体数据

## 代码结构

```
src/
  pages/          ← 页面组件
  components/     ← 通用组件
  composables/    ← 组合式函数
  stores/         ← Pinia store
  api/            ← 数据访问层
```

## 数据访问示例

```typescript
// 访问本体函数
const result = await dazi.onto.runFunction('my_function', { key: 'value' })

// 访问数据表
const rows = await dazi.data.query('SELECT * FROM my_table LIMIT 10')
```

## 构建与上传

```powershell
# 在 dazi-work/项目/app_<名称>/ 应用项目根
pnpm run dazi-app -- build
pnpm run dazi-app -- upload --space <space-id>
```
