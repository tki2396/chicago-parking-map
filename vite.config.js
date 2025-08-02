import { defineConfig } from "vite";

export default defineConfig({
  root: ".",
  base: "/chicago-parking-map/",
  build: {
    outDir: "dist",
    emptyOutDir: true,
  },
  server: {
    open: "/index.html",
  },
});
