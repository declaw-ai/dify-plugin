from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from declaw import Sandbox
from declaw.security import (
    AuditConfig,
    InjectionDefenseConfig,
    PIIConfig,
    SecurityPolicy,
)

# language -> (template, source file path, run command)
LANGUAGE_CONFIG = {
    "python": ("python", "/home/user/main.py", "python3 /home/user/main.py"),
    "javascript": ("node", "/home/user/main.js", "node /home/user/main.js"),
}


class RunCodeTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage]:
        api_key = self.runtime.credentials["declaw_api_key"]
        domain = self.runtime.credentials.get("declaw_domain") or None

        code = tool_parameters["code"]
        language = tool_parameters.get("language", "python")
        timeout = int(tool_parameters.get("timeout", 30))
        preset = tool_parameters.get("security_preset", "standard")
        allowed_domains_str = tool_parameters.get("allowed_domains", "")
        output_files_str = tool_parameters.get("output_files", "")

        if language not in LANGUAGE_CONFIG:
            raise ValueError(
                f"Unsupported language '{language}'. Use 'python' or 'javascript'."
            )
        template, file_path, run_cmd = LANGUAGE_CONFIG[language]

        # Give the sandbox enough lifetime to create, run, and download results.
        kwargs: dict[str, Any] = {
            "template": template,
            "timeout": timeout + 120,
            "api_key": api_key,
        }
        if domain:
            kwargs["domain"] = domain

        if preset != "none":
            kwargs["security"] = SecurityPolicy(
                pii=PIIConfig(enabled=True),
                injection_defense=InjectionDefenseConfig(enabled=(preset == "strict")),
                audit=AuditConfig(enabled=True),
            )

        if allowed_domains_str:
            domains = [d.strip() for d in allowed_domains_str.split(",") if d.strip()]
            if domains:
                kwargs["network"] = {"allow_out": domains}
        elif preset == "strict":
            kwargs["network"] = {"deny_out": ["0.0.0.0/0"]}

        sbx = Sandbox.create(**kwargs)
        try:
            sbx.files.write(file_path, code)
            result = sbx.commands.run(run_cmd, timeout=timeout)

            output: dict[str, Any] = {
                "exit_code": result.exit_code,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "language": language,
            }

            if output_files_str:
                files_out: dict[str, str] = {}
                for path in [p.strip() for p in output_files_str.split(",") if p.strip()]:
                    try:
                        files_out[path] = sbx.files.read(path)
                    except Exception as e:  # noqa: BLE001 - report per-file, don't fail the run
                        files_out[path] = f"ERROR: {e}"
                if files_out:
                    output["output_files"] = files_out

            yield self.create_json_message(output)
        finally:
            # Ephemeral sandbox — always tear down, even on error.
            try:
                sbx.kill()
            except Exception:  # noqa: BLE001
                pass
