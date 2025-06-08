import React from "react";

const DebugCard: React.FC = () => {
  return (
    <div
      style={{
        background: "white",
        padding: "20px",
        margin: "20px",
        border: "2px solid red",
        borderRadius: "8px",
      }}
    >
      <h3 style={{ margin: "0 0 10px 0" }}>Debug Test</h3>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "20px",
          border: "1px solid blue",
          padding: "10px",
        }}
      >
        <span
          style={{
            background: "#f0f0f0",
            padding: "5px 10px",
            borderRadius: "4px",
          }}
        >
          Team Logo
        </span>
        <span
          style={{
            fontWeight: "bold",
            fontSize: "16px",
            color: "#333",
            border: "1px solid green",
            padding: "5px",
            minWidth: "100px",
            whiteSpace: "nowrap",
          }}
        >
          Manchester United
        </span>
        <span
          style={{
            fontSize: "24px",
            fontWeight: "bold",
            background: "#f8f9fa",
            padding: "10px",
            borderRadius: "8px",
            minWidth: "40px",
            textAlign: "center",
          }}
        >
          3
        </span>
      </div>

      <div style={{ marginTop: "10px" }}>
        <p>
          Team name should display horizontally:{" "}
          <strong>Manchester United</strong>
        </p>
        <p>
          If you see characters displayed vertically (M a n c h e s t e r),
          there's a CSS issue.
        </p>
      </div>
    </div>
  );
};

export default DebugCard;
