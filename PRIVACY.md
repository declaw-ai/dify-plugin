# Declaw Dify Plugin — Privacy Policy

## Data Collection

This plugin does **not** collect any personal data. It acts as a connector between Dify and the Declaw API.

## Data Transmission

When you use this plugin, the following data is sent to Declaw's API (`api.declaw.ai` or your configured on-prem domain):

- **API Key**: Your Declaw API key (stored securely by Dify, transmitted over HTTPS)
- **Commands and file content**: Any commands you execute or files you read/write are sent to the Declaw API to be processed inside an isolated sandbox
- **Sandbox metadata**: Template selection, timeout, and security policy configuration

## Data Storage

Declaw does not persist command output or file content after a sandbox is destroyed. Sandboxes are ephemeral and automatically cleaned up after the configured timeout.

For Declaw's full privacy policy, see: https://declaw.ai/privacy
