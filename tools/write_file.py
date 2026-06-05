from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from declaw import Sandbox


class WriteFileTool(Tool):
    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage]:
        api_key = self.runtime.credentials["declaw_api_key"]
        domain = self.runtime.credentials.get("declaw_domain") or None

        sandbox_id = tool_parameters["sandbox_id"]
        path = tool_parameters["path"]
        content = tool_parameters["content"]

        sbx = Sandbox.connect(sandbox_id, api_key=api_key, domain=domain)
        sbx.files.write(path, content)

        yield self.create_json_message({"written": True, "path": path})
