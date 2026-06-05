import React from "react";

export interface CardProps {
  title?: string;
  toolbar?: React.ReactNode;
  children: React.ReactNode;
}

export function Card(props: CardProps) {
  return (
    <div className="drap-card">
      {(props.title || props.toolbar) && (
        <div
          className="drap-card__title"
          style={{ display: "flex", justifyContent: "space-between" }}
        >
          <span>{props.title}</span>
          <span>{props.toolbar}</span>
        </div>
      )}
      {props.children}
    </div>
  );
}
