import React from "react";
import { useAppearance } from "@dazi/app-sdk-runtime";
import { Card, PageLayout } from "@dazi/app-sdk-ui";

export function MainPage() {
  const appearance = useAppearance();

  return (
    <PageLayout title="采购单维护" appearance={appearance}>
      <Card title="采购单（演示表单）">
        <div style={{ display: "grid", gap: 12, maxWidth: 480 }}>
          <label style={{ display: "grid", gap: 4, fontSize: 13 }}>
            供应商
            <input readOnly value="示例供应商有限公司" style={{ padding: 8, borderRadius: 6, border: "1px solid #e5e7eb" }} />
          </label>
          <label style={{ display: "grid", gap: 4, fontSize: 13 }}>
            物料
            <input readOnly value="原料 A-100" style={{ padding: 8, borderRadius: 6, border: "1px solid #e5e7eb" }} />
          </label>
          <label style={{ display: "grid", gap: 4, fontSize: 13 }}>
            数量
            <input readOnly value="500" style={{ padding: 8, borderRadius: 6, border: "1px solid #e5e7eb" }} />
          </label>
          <p style={{ fontSize: 12, color: "#6b7280" }}>
            演示模板：提交 Action 请在本体函数绑定后扩展（禁止裸 fetch）。
          </p>
        </div>
      </Card>
    </PageLayout>
  );
}
