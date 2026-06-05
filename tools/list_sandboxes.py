from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from declaw import Sandbox


class ListSandboxesTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage]:
        api_key = self.runtime.credentials["declaw_api_key"]
        domain = self.runtime.credentials.get("declaw_domain") or None

        data = Sandbox.list(api_key=api_key, domain=domain)
        sandboxes = data.get("sandboxes", [])

        yield self.create_json_message(
            {
                "count": len(sandboxes),
                "sandboxes": [
                    {
                        "sandbox_id": s.get("sandbox_id"),
                        "template": s.get("template_id"),
                        "name": s.get("name"),
                        "state": s.get("state"),
                    }
                    for s in sandboxes
                ],
            }
        )
