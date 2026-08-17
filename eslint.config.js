import js from "@eslint/js";
import tseslint from "typescript-eslint";

export default [
  { ignores: [".venv/**", "dist/**", "node_modules/**", "target/**"] },
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    files: ["scripts/**/*.mjs"],
    languageOptions: {
      globals: {
        process: "readonly",
      },
      parserOptions: {
        project: "./tsconfig.json",
        tsconfigRootDir: import.meta.dirname,
      },
    },
  },
];
