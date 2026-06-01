# 从文件上传管理实现复杂报表

1. 在管理端上传 Excel → **原生摘录** → **报表布局**（规则或 AI）
2. VS Code **拉取到本地资源** → 得到 `报表布局.json`
3. **App: 绑定复杂报表设计稿** → 写入 `manifest.report_design`
4. **App: 同步报表 binding 与 SQL 草稿** → `binding` + `drap-assets/sql/report_data_projection.sql`
5. Cursor `@报表布局.json` + 本目录 `report-intent.md` → 改 `src/pages/MainPage.tsx`
6. `pnpm run dev` → `构建并上传激活`
