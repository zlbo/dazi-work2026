import React, { useState } from "react";

export type FilterFieldType = "select" | "text" | "number";

export interface FilterField {
  key: string;
  label: string;
  type?: FilterFieldType;
  options?: Array<{ value: string; label: string }>;
  defaultValue?: string | number;
}

export interface FilterBarProps {
  fields: FilterField[];
  onChange: (values: Record<string, unknown>) => void;
}

export function FilterBar(props: FilterBarProps) {
  const initial: Record<string, unknown> = {};
  for (const f of props.fields) {
    if (f.defaultValue !== undefined) initial[f.key] = f.defaultValue;
  }
  const [values, setValues] = useState<Record<string, unknown>>(initial);

  const update = (k: string, v: unknown) => {
    const next = { ...values, [k]: v };
    setValues(next);
    props.onChange(next);
  };

  return (
    <div className="drap-filterbar">
      {props.fields.map((f) => (
        <label className="drap-filterbar__field" key={f.key}>
          <span>{f.label}</span>
          {f.type === "select" ? (
            <select
              value={String(values[f.key] ?? "")}
              onChange={(e) => update(f.key, e.target.value)}
            >
              {f.options?.map((o) => (
                <option key={o.value} value={o.value}>
                  {o.label}
                </option>
              ))}
            </select>
          ) : (
            <input
              type={f.type === "number" ? "number" : "text"}
              value={String(values[f.key] ?? "")}
              onChange={(e) =>
                update(
                  f.key,
                  f.type === "number" ? Number(e.target.value) : e.target.value,
                )
              }
            />
          )}
        </label>
      ))}
    </div>
  );
}
