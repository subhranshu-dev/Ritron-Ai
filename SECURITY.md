# Security Policy

## Reporting

Do not report security issues in public tickets. Until a dedicated reporting
channel is published, report them privately to the project maintainers through
the organization’s approved internal channel.

## Foundation controls

- `.env` files are ignored; `.env.example` uses blank placeholders only.
- API responses use safe error messages and do not expose tracebacks or paths.
- Structured logging redacts common credential field names.
- CI scans tracked files for secrets and audits Python and Node dependencies.
- Future desktop secrets must use OS-managed secure storage, never frontend bundles.

Security controls are expanded in Step 09; this foundation does not implement a
permission engine or tool-execution sandbox.
