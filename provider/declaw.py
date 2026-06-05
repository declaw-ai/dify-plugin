from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from declaw import Sandbox


class DeclawProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        api_key = credentials.get("declaw_api_key", "")
        domain = credentials.get("declaw_domain") or None

        if not api_key:
            raise ToolProviderCredentialValidationError("Declaw API key is required")

        try:
            sbx = Sandbox.create(
                template="base",
                timeout=30,
                api_key=api_key,
                domain=domain,
            )
            result = sbx.commands.run("echo ok")
            sbx.kill()
            if result.exit_code != 0:
                raise Exception("sandbox command failed")
        except ToolProviderCredentialValidationError:
            raise
        except Exception as e:
            raise ToolProviderCredentialValidationError(
                f"Failed to validate Declaw credentials: {e}"
            )
