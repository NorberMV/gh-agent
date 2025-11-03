import json
from pathlib import Path


def read_config(config_file: Path):
    """Read the MCP config JSON."""
    print(f"Reading the file at: {config_file}")

    with open(config_file, "r", encoding="utf-8") as fh:
        config = json.load(fh)

    servers = config.get("mcpServers")
    # Optionally add default transports if missing
    for name, server in servers.items():
        if "command" in server and "transport" not in server:
            server["transport"] = "stdio"
        # Only set default transport for URL-based servers if not explicitly set
        if "url" in server and "transport" not in server:
            server["transport"] = "streamable_http"

    return servers