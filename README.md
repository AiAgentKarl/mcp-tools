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


---

## More MCP Servers by AiAgentKarl

| Category | Servers |
|----------|---------|
| 🔗 Blockchain | [Solana](https://github.com/AiAgentKarl/solana-mcp-server) |
| 🌍 Data | [Weather](https://github.com/AiAgentKarl/weather-mcp-server) · [Germany](https://github.com/AiAgentKarl/germany-mcp-server) · [Agriculture](https://github.com/AiAgentKarl/agriculture-mcp-server) · [Space](https://github.com/AiAgentKarl/space-mcp-server) · [Aviation](https://github.com/AiAgentKarl/aviation-mcp-server) · [EU Companies](https://github.com/AiAgentKarl/eu-company-mcp-server) |
| 🔒 Security | [Cybersecurity](https://github.com/AiAgentKarl/cybersecurity-mcp-server) · [Policy Gateway](https://github.com/AiAgentKarl/agent-policy-gateway-mcp) · [Audit Trail](https://github.com/AiAgentKarl/agent-audit-trail-mcp) |
| 🤖 Agent Infra | [Memory](https://github.com/AiAgentKarl/agent-memory-mcp-server) · [Directory](https://github.com/AiAgentKarl/agent-directory-mcp-server) · [Hub](https://github.com/AiAgentKarl/mcp-appstore-server) · [Reputation](https://github.com/AiAgentKarl/agent-reputation-mcp-server) |
| 🔬 Research | [Academic](https://github.com/AiAgentKarl/crossref-academic-mcp-server) · [LLM Benchmark](https://github.com/AiAgentKarl/llm-benchmark-mcp-server) · [Legal](https://github.com/AiAgentKarl/legal-court-mcp-server) |

[→ Full catalog (40+ servers)](https://github.com/AiAgentKarl)

## License

MIT
