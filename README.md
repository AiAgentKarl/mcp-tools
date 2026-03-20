# mcp-tools ⚡

CLI toolkit for MCP server development — create, manage, search and publish Model Context Protocol servers.

## Installation

```bash
pip install mcp-tools
```

## Commands

### Create a new MCP server

```bash
mcp-tools create weather
```

Generates a complete project with server, tools, config, README and .gitignore — ready to develop.

### Search the server catalog

```bash
mcp-tools search crypto
mcp-tools search health
mcp-tools search infrastructure
```

### Add a server to your project

```bash
mcp-tools add solana --package solana-mcp-server
mcp-tools add weather --package openmeteo-mcp-server
```

### List configured servers

```bash
mcp-tools list
```

### Remove a server

```bash
mcp-tools remove weather
```

## What it generates

```
my-server/
├── src/
│   ├── server.py          # FastMCP server entry point
│   ├── tools/
│   │   └── main_tools.py  # Your tool definitions
│   └── clients/           # API clients
├── pyproject.toml          # Package config with entry points
├── README.md
└── .gitignore
```

## License

MIT
