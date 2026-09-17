# ajaxace

## Hostinger MCP servers

`.mcp.json` wires up six Hostinger MCP servers (hosting, domains, DNS, billing, reach,
ecommerce) so Claude Code can manage this project's Hostinger account directly —
provisioning, DNS records, invoices, storefront, etc.

### Setup

1. Get an API token from your Hostinger account (hPanel → API).
2. Export it in your shell before starting Claude Code — do **not** paste it into
   `.mcp.json` itself:

   ```bash
   export HOSTINGER_API_TOKEN="your-real-token"
   ```

   `.mcp.json` references `${HOSTINGER_API_TOKEN}`, which Claude Code expands from
   your environment at startup, so the token never gets committed to this repo.
3. The `command` is set to `npx.cmd`, which is the correct launcher for Windows
   (cmd.exe/PowerShell) environments. On macOS/Linux, change `npx.cmd` to `npx` in
   `.mcp.json` before use.

### Servers

| Server | Purpose |
| --- | --- |
| `hostinger-hosting` | Manage hosting plans, subscriptions, resources |
| `hostinger-domains` | Manage domain registrations, renewals, transfers |
| `hostinger-dns` | Manage DNS zones and records |
| `hostinger-billing` | View/manage invoices and billing |
| `hostinger-reach` | Manage Hostinger Reach (email marketing) |
| `hostinger-ecommerce` | Manage Hostinger ecommerce/storefront |
