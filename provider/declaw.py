from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from declaw import Sandbox
from declaw.exceptions import AuthenticationException


class DeclawProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        api_key = credentials.get("declaw_api_key", "")
        domain = credentials.get("declaw_domain") or None

        if not api_key:
            raise ToolProviderCredentialValidationError("Declaw API key is required")

        # Validate against a lightweight authenticated endpoint (list sandboxes)
        # instead of booting a microVM — faster, cheaper, and not subject to
        # cold-boot timeouts.
        try:
            Sandbox.list(api_key=api_key, domain=domain, limit=1)
        except AuthenticationException as e:
            raise ToolProviderCredentialValidationError(
                f"Invalid Declaw API key: {e}"
            )
        except Exception as e:
            raise ToolProviderCredentialValidationError(
                f"Failed to validate Declaw credentials: {e}"
            )
