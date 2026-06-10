# 从文件上传管理实现复杂报表（主要财务指标）

完整实践见：**[`dazi/docs/app/主要财务指标复杂报表开发实践.md`](../../../../docs/app/主要财务指标复杂报表开发实践.md)**

## 步骤

1. 在管理端上传 Excel（如「单一分析表2026.xlsx」）→ **原生摘录** → **报表布局**（规则或 AI）
2. VS Code **拉取到本地资源** → 得到 `报表布局.json`
3. **App: 绑定复杂报表设计稿** → 写入 `manifest.report_design.managed_file_id`
4. 同步 `src/fixtures/generated/reportLayout.json`（**仅叶子列**）与 `reportRows.json`
5. **App: 写入 layout 快照**（发布用）→ `layout_snapshot`
6. Cursor `@报表布局.json` + `.ai/report-intent.md` → 按需改 `MainPage.tsx` / `reportLayout.ts`
7. `pnpm run dev` 验收 → `pnpm run build` → **构建并上传激活**
