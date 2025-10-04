import React, { useState } from "react";
import { registerComponent } from "@fiftyone/plugins";

const HelloPanel = () => {
  const [message, setMessage] = useState("Hello World!");

  const handleClick = async () => {
    const result = await fo.operators.execute("@madfish/hello_python/print_me");
    if (result && result.message) {
      setMessage(result.message);
    }
  };

  return (
    <div style={{ padding: "1rem" }}>
      <h2>{message}</h2>
      <button
        style={{
          background: "#4caf50",
          border: "none",
          color: "white",
          padding: "0.5rem 1rem",
          borderRadius: "6px",
          cursor: "pointer",
        }}
        onClick={handleClick}
      >
        Click Me!
      </button>
    </div>
  );
};

registerComponent("@madfish/hello_python.HelloPanel", HelloPanel);
