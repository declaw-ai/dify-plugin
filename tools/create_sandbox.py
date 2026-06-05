from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from declaw import Sandbox
from declaw.security import SecurityPolicy, PIIConfig, InjectionDefenseConfig, AuditConfig


class CreateSandboxTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage]:
        api_key = self.runtime.credentials["declaw_api_key"]
        domain = self.runtime.credentials.get("declaw_domain") or None

        template = tool_parameters.get("template", "base")
        timeout = int(tool_parameters.get("timeout", 300))
        preset = tool_parameters.get("security_preset", "standard")
        allowed_domains_str = tool_parameters.get("allowed_domains", "")

        kwargs: dict[str, Any] = {
            "template": template,
            "timeout": timeout,
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

        yield self.create_json_message(
            {
                "sandbox_id": sbx.sandbox_id,
                "template": template,
                "timeout": timeout,
                "security_preset": preset,
            }
        )
