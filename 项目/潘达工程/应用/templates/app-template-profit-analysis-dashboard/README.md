# @dazi/app-template-profit-analysis-dashboard

DRAP 业务场景模板：利润分析看板。

## 快速开始

```bash
cd ..  # 应用项目根（本 README 在 templates/ 子目录时）
pnpm install
pnpm dev:profit-analysis           # 等价于 pnpm --filter @dazi/app-template-profit-analysis-dashboard dev
```

浏览器打开 `http://localhost:5180`，可看到由 `src/fixtures/datasets.ts` 提供的 mock 数据 dashboard。

## 主站宿主加载

```bash
pnpm --filter @dazi/app-template-profit-analysis-dashboard build
# 然后在主站 frontend 启动后访问：
#   http://localhost:3011/runtime-apps-test
#   （会用 vite preview / http-server 起的 dist 作为 micro-app 子应用 URL）
```

## P0 范围

- 单页 `ProfitDashboard`：KPI + 趋势 + 同比表
- mock 数据：`src/fixtures/datasets.ts`
- 真实数据：P1 后由后端 `/api/runtime-apps/apps/{id}/fetch-data-sources` 提供
