# Declaw Plugin for Dify

Secure sandbox execution for AI agents in [Dify](https://dify.ai). Run AI agents and their tools in Firecracker microVMs with network policies, PII scanning, prompt injection defense, and audit logging.

## Tools

| Tool | Description |
|------|-------------|
| `create_sandbox` | Create a secure sandbox with configurable security policies |
| `run_command` | Execute a shell command inside a sandbox |
| `read_file` | Read a file from a sandbox |
| `write_file` | Write a file to a sandbox |
| `list_files` | List directory contents in a sandbox |
| `kill_sandbox` | Destroy a sandbox |
| `list_sandboxes` | List all active sandboxes |

## Setup

1. Install the plugin from the Dify Marketplace
2. Configure your Declaw API key (get one at [declaw.ai](https://declaw.ai))
3. Optionally set a custom API domain for on-prem deployments

## Security Presets

When creating a sandbox, choose a security preset:

- **none** — No guardrails. Full internet access.
- **standard** (default) — PII scanning + audit logging.
- **strict** — PII + injection defense + audit + network deny-all.

Pass `allowed_domains` (comma-separated) to restrict outbound traffic to specific domains.

## Templates

8 built-in templates: `base`, `python`, `node`, `code-interpreter`, `ai-agent`, `mcp-server`, `web-dev`, `devops`.

## Links

- [Declaw](https://declaw.ai)
- [Documentation](https://docs.declaw.ai)
- [GitHub](https://github.com/declaw-ai/dify-plugin)
- [Privacy Policy](./PRIVACY.md)

## License

Apache-2.0
