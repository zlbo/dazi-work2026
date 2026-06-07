# DRAP 子应用 UI 规范（精简版）

> 子应用嵌入搭子主站，**视觉与交互必须与宿主一致**。  
> 实现方式：只用 `@dazi/app-sdk-ui` + `useAppearance()`，勿自建设计系统。

---

## 1. 颜色（禁止自造品牌色）

| 用途 | 色值 / 类名 |
|------|-------------|
| 主色 Tech Blue | `#1677FF` · `text-tech-blue` / `bg-tech-blue` |
| 成功 | `#00B42A` · `text-success-green` |
| 警告 | `#FF7D00` · `text-warn-yellow` |
| 错误 | `#F53F3F` · 错误条 / 文案 |

背景、卡片、边框、文字深浅色值由 SDK / `useAppearance()` 提供，**禁止**在组件里写死 `#fff` / `#000`。

---

## 2. 排版

| 层级 | 建议类名 |
|------|----------|
| 页面标题 | `text-xl font-bold` |
| 区块标题 | `text-base font-bold` |
| 正文 | `text-sm` ~ `text-base` |
| 辅助说明 | `text-xs text-gray-500`（暗色用 SDK 次要色） |

中文为主；字体由宿主/SDK 注入，子应用不要 `@font-face` 或替换全局字体。

---

## 3. 布局与间距

- 页面壳：`PageLayout`（标题、内边距由 SDK 统一）
- 卡片：`rounded-lg` 或 `rounded-xl`，`shadow-sm`（普通）/ `shadow-md`（重点 KPI）
- 栅格间距：常用 `gap-4`（16px）；KPI 墙示例：`grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4`
- 最小支持宽度：**1366px**；大屏 **1920px** 下 KPI/表格勿过度拉伸

---

## 4. 核心组件（只用 SDK）

| 场景 | 组件 |
|------|------|
| KPI 指标 | `KpiCard` |
| 趋势 | `TrendChart` / `LineChart` |
| 明细表 | `DataGrid` |
| 筛选 | `FilterBar` |
| 页壳 | `PageLayout` |

**禁止**：直接 `import echarts`、`import antd` 做图表/表单（图表走 SDK 封装）。

---

## 5. 状态（必须可感知）

| 状态 | 要求 |
|------|------|
| loading | 骨架屏或 SDK `Skeleton`，禁止白屏 |
| empty | 明确文案，如「暂无数据」 |
| error | 展示 `meta.error` 或数据集 `error`，勿静默失败 |

问数场景：`useResultDataset()`；页模式：`useDataset(key)`，loading/error 同样处理。

---

## 6. 深色模式

- 通过 `useAppearance()` 跟随宿主 `light` / `dark` / `system`
- 所有背景、边框、文字使用 SDK 变量或带 `dark:` 的 Tailwind 类
- 自测：在主站切换深色后打开 `/runtime-apps/<appId>` 验收

---

## 7. 禁止项（与平台铁律一致）

- 裸 `fetch` / `axios` 调搭子 API
- 修改 `window` / `globalThis`
- 子应用内自建侧边栏、顶栏（布局由宿主提供）
- 硬编码浅色/深色配色

修改 UI 前请先读 `.ai/overview.md` 与 `AGENTS.md`。
