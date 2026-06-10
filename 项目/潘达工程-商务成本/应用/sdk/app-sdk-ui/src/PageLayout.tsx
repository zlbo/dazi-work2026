import React from "react";

export interface PageLayoutProps {
  title: string;
  toolbar?: React.ReactNode;
  children: React.ReactNode;
  appearance?: "light" | "dark";
}

export function PageLayout(props: PageLayoutProps) {
  const cls =
    "drap-page " +
    (props.appearance === "dark" ? "drap-page--dark" : "drap-page--light");
  return (
    <div className={cls}>
      <div className="drap-page__header">
        <div className="drap-page__title">{props.title}</div>
        <div>{props.toolbar}</div>
      </div>
      <div className="drap-page__body">{props.children}</div>
    </div>
  );
}
