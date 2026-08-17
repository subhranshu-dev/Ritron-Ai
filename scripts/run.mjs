import { rm } from "node:fs/promises";
import { spawn } from "node:child_process";

const task = process.argv[2] ?? "";

/** @param {string} command @param {string[]} args */
function execute(command, args) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, {
      stdio: "inherit",
      shell: process.platform === "win32",
    });
    child.on("error", reject);
    child.on("exit", (code, signal) => {
      if (code === 0) {
        resolve(undefined);
        return;
      }
      reject(
        new Error(
          `${command} exited with ${code ?? signal ?? "an unknown status"}`,
        ),
      );
    });
  });
}

const commands = {
  dev: () => execute("uv", ["run", "uvicorn", "ritron_api.main:app"]),
  build: async () => {
    await execute("pnpm", ["exec", "tsc", "--noEmit"]);
    await execute("uv", ["build"]);
    await execute("cargo", ["build", "--workspace"]);
  },
  test: () => execute("uv", ["run", "pytest"]),
  "test:unit": () => execute("uv", ["run", "pytest", "apps/api/tests/unit"]),
  "test:integration": () =>
    execute("uv", [
      "run",
      "pytest",
      "apps/api/tests/integration",
      "-m",
      "integration",
    ]),
  "test:e2e": () =>
    execute("uv", ["run", "pytest", "apps/api/tests/e2e", "-m", "e2e"]),
  lint: async () => {
    await execute("pnpm", ["exec", "eslint", "."]);
    await execute("uv", ["run", "ruff", "check", "."]);
    await execute("cargo", ["clippy", "--workspace", "--", "-D", "warnings"]);
  },
  format: async () => {
    await execute("pnpm", ["exec", "prettier", "--write", "."]);
    await execute("uv", ["run", "ruff", "format", "."]);
    await execute("cargo", ["fmt", "--all"]);
  },
  "format:check": async () => {
    await execute("pnpm", ["exec", "prettier", "--check", "."]);
    await execute("uv", ["run", "ruff", "format", "--check", "."]);
    await execute("cargo", ["fmt", "--all", "--check"]);
  },
  typecheck: async () => {
    await execute("pnpm", ["exec", "tsc", "--noEmit"]);
    await execute("uv", ["run", "mypy"]);
  },
  check: async () => {
    await commands["format:check"]();
    await commands.lint();
    await commands.typecheck();
    await commands.test();
    await commands.build();
  },
  clean: async () => {
    await Promise.all(
      [
        "dist",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "coverage",
        "target",
      ].map((path) => rm(path, { force: true, recursive: true })),
    );
  },
};

if (!(task in commands)) {
  throw new Error(`Unknown RITRON command: ${task ?? "(none)"}`);
}

await commands[/** @type {keyof typeof commands} */ (task)]();
