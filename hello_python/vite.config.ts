import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  build: {
    lib: {
      entry: path.resolve(__dirname, "src/index.tsx"),
      name: "@madfish/hello_python",
      formats: ["umd"],
      fileName: () => "index.umd.js",
    },
    rollupOptions: {
      external: ["react", "react-dom", "@fiftyone/plugins"],
      output: {
        globals: {
          react: "React",
          "react-dom": "ReactDOM",
          "@fiftyone/plugins": "plugins",
        },
      },
    },
  },
});
