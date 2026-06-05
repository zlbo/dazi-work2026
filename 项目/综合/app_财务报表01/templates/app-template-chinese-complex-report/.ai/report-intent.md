# 中国式复杂报表 · 页面意图

## 数据源

- 主数据集 key：`report_data`（`useDataset("report_data")`）
- 设计稿：`manifest.report_design.managed_file_id` → 文件上传管理侧车 `报表布局.json`（RLIR）

## UI

- 使用 `@dazi/app-sdk-ui` 的 **`ComplexReport`**，禁止手写百列 `<table>`
- 布局以 RLIR 为准；改表头请更新 Excel → 平台「报表布局」→ 拉取 bundle → 绑定 manifest

## 本地 AI 上下文

拉取后在工作区 `资源/files/<名>_<id>/`：

- `原生解析.md`
- `表结构.json`（Flow 扁平表，可选）
- `报表布局.json`（本报表必选）
