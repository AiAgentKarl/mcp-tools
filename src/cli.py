"""mcp-tools — CLI Toolkit für MCP-Server Entwicklung."""

import argparse
import json
import os
import sys
import textwrap


def cmd_create(args):
    """Neues MCP-Server-Projekt scaffolden."""
    name = args.name
    slug = name.lower().replace(" ", "-").replace("_", "-")
    pkg_name = f"{slug}-mcp-server"
    module_name = slug.replace("-", "_")
    project_dir = os.path.join(os.getcwd(), slug)

    if os.path.exists(project_dir):
        print(f"Error: Directory '{slug}' already exists.")
        sys.exit(1)

    print(f"Creating MCP server project: {pkg_name}")

    # Verzeichnisstruktur erstellen
    os.makedirs(os.path.join(project_dir, "src", "tools"), exist_ok=True)
    os.makedirs(os.path.join(project_dir, "src", "clients"), exist_ok=True)

    # __init__.py Dateien
    for d in ["src", "src/tools", "src/clients"]:
        with open(os.path.join(project_dir, d, "__init__.py"), "w") as f:
            pass

    # pyproject.toml
    pyproject = textwrap.dedent(f"""\
    [build-system]
    requires = ["hatchling"]
    build-backend = "hatchling.build"

    [project]
    name = "{pkg_name}"
    version = "0.1.0"
    description = "MCP Server for {name}"
    readme = "README.md"
    license = {{text = "MIT"}}
    requires-python = ">=3.10"
    dependencies = [
        "mcp>=1.0.0",
        "httpx>=0.27.0",
        "pydantic>=2.0.0",
    ]

    [project.scripts]
    {slug}-server = "src.server:main"

    [tool.hatch.build.targets.wheel]
    packages = ["src"]
    """)
    with open(os.path.join(project_dir, "pyproject.toml"), "w") as f:
        f.write(pyproject)

    # server.py
    server_py = textwrap.dedent(f"""\
    \"\"\"MCP Server for {name}.\"\"\"

    from mcp.server.fastmcp import FastMCP

    from src.tools.main_tools import register_tools

    mcp = FastMCP(
        "{name} MCP Server",
        instructions="MCP Server for {name}.",
    )

    register_tools(mcp)


    def main():
        mcp.run(transport="stdio")


    if __name__ == "__main__":
        main()
    """)
    with open(os.path.join(project_dir, "src", "server.py"), "w") as f:
        f.write(server_py)

    # tools/main_tools.py
    tools_py = textwrap.dedent(f"""\
    \"\"\"Tools for {name} MCP Server.\"\"\"

    from mcp.server.fastmcp import FastMCP


    def register_tools(mcp: FastMCP):

        @mcp.tool()
        async def hello(name: str = "World") -> dict:
            \"\"\"A simple hello tool to verify the server works.

            Args:
                name: Name to greet
            \"\"\"
            return {{"message": f"Hello, {{name}}! {name} MCP Server is running."}}
    """)
    with open(os.path.join(project_dir, "src", "tools", "main_tools.py"), "w") as f:
        f.write(tools_py)

    # README.md
    readme = textwrap.dedent(f"""\
    # {name} MCP Server

    MCP Server for {name}.

    ## Installation

    ```bash
    pip install {pkg_name}
    ```

    ## Usage with Claude Code

    ```json
    {{
      "mcpServers": {{
        "{slug}": {{
          "command": "uvx",
          "args": ["{pkg_name}"]
        }}
      }}
    }}
    ```

    ## Development

    ```bash
    pip install -e .
    python -m src.server
    ```

    ## License

    MIT
    """)
    with open(os.path.join(project_dir, "README.md"), "w") as f:
        f.write(readme)

    # .gitignore
    gitignore = textwrap.dedent("""\
    __pycache__/
    *.pyc
    .venv/
    *.egg-info/
    dist/
    build/
    .env
    keys.env
    .mcp.json
    """)
    with open(os.path.join(project_dir, ".gitignore"), "w") as f:
        f.write(gitignore)

    print(f"[OK] Project created in ./{slug}/")
    print(f"")
    print(f"Next steps:")
    print(f"  cd {slug}")
    print(f"  pip install -e .")
    print(f"  python -m src.server")
    print(f"")
    print(f"Add your tools in src/tools/main_tools.py")


def cmd_list(args):
    """Installierte MCP-Server aus .mcp.json anzeigen."""
    config_path = os.path.join(os.getcwd(), ".mcp.json")
    if not os.path.exists(config_path):
        print("No .mcp.json found in current directory.")
        return

    with open(config_path) as f:
        config = json.load(f)

    servers = config.get("mcpServers", {})
    if not servers:
        print("No MCP servers configured.")
        return

    print(f"[LIST] {len(servers)} MCP server(s) configured:\n")
    for name, cfg in servers.items():
        cmd = cfg.get("command", "?")
        server_args = cfg.get("args", [])
        print(f"  {name}")
        print(f"    Command: {cmd} {' '.join(server_args)}")
        if cfg.get("env"):
            env_keys = list(cfg["env"].keys())
            print(f"    Env vars: {', '.join(env_keys)}")
        print()


def cmd_add(args):
    """MCP-Server zur .mcp.json hinzufügen."""
    config_path = os.path.join(os.getcwd(), ".mcp.json")

    if os.path.exists(config_path):
        with open(config_path) as f:
            config = json.load(f)
    else:
        config = {"mcpServers": {}}

    name = args.name
    package = args.package or f"{name}-mcp-server"

    config["mcpServers"][name] = {
        "command": "uvx",
        "args": [package],
    }

    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    print(f"[OK] Added '{name}' to .mcp.json (package: {package})")


def cmd_remove(args):
    """MCP-Server aus .mcp.json entfernen."""
    config_path = os.path.join(os.getcwd(), ".mcp.json")

    if not os.path.exists(config_path):
        print("No .mcp.json found.")
        return

    with open(config_path) as f:
        config = json.load(f)

    name = args.name
    if name in config.get("mcpServers", {}):
        del config["mcpServers"][name]
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
        print(f"[OK] Removed '{name}' from .mcp.json")
    else:
        print(f"Server '{name}' not found in .mcp.json")


def cmd_search(args):
    """MCP-Server im Katalog suchen."""
    query = args.query.lower()

    # Eingebauter Katalog (Top-Server)
    catalog = [
        ("solana-mcp-server", "Solana blockchain, DeFi, wallet, token prices", "Crypto"),
        ("openmeteo-mcp-server", "Weather, forecasts, air quality, climate data", "Weather"),
        ("agriculture-mcp-server", "FAO crop data, soil, food nutrition", "Science"),
        ("germany-mcp-server", "German government data, Destatis, registers", "Government"),
        ("space-mcp-server", "NASA, asteroids, Mars rover, ISS tracking", "Science"),
        ("aviation-mcp-server", "Flight tracking, airports, airlines", "Transport"),
        ("eu-company-mcp-server", "EU company data, filings, LEI lookup", "Business"),
        ("cybersecurity-mcp-server", "CVE vulnerabilities, threat intel", "Security"),
        ("medical-data-mcp-server", "WHO data, drugs, clinical trials", "Health"),
        ("crossref-academic-mcp-server", "180M+ papers, citations, DOI lookup", "Science"),
        ("legal-court-mcp-server", "3M+ court decisions, case law", "Legal"),
        ("llm-benchmark-mcp-server", "LLM comparison, benchmarks, pricing", "AI"),
        ("agent-memory-mcp-server", "Persistent memory for agents", "Infrastructure"),
        ("agent-context-optimizer-mcp", "Context window optimization", "Infrastructure"),
        ("x402-mcp-server", "Micropayments for agents", "Infrastructure"),
        ("agent-reputation-mcp-server", "Trust scores for agents", "Infrastructure"),
        ("hive-mind-mcp-server", "Collective decision-making", "Infrastructure"),
    ]

    results = [
        (name, desc, cat)
        for name, desc, cat in catalog
        if query in name.lower() or query in desc.lower() or query in cat.lower()
    ]

    if not results:
        print(f"No servers found for '{args.query}'")
        return

    print(f"[SEARCH] Found {len(results)} server(s):\n")
    for name, desc, cat in results:
        print(f"  [{cat}] {name}")
        print(f"    {desc}")
        print(f"    Install: mcp-tools add {name.replace('-mcp-server', '')} --package {name}")
        print()


def main():
    parser = argparse.ArgumentParser(
        prog="mcp-tools",
        description="CLI toolkit for MCP server development",
    )
    subparsers = parser.add_subparsers(dest="command")

    # create
    create_parser = subparsers.add_parser("create", help="Create a new MCP server project")
    create_parser.add_argument("name", help="Server name (e.g. 'weather' or 'my-data')")

    # list
    subparsers.add_parser("list", help="List configured MCP servers from .mcp.json")

    # add
    add_parser = subparsers.add_parser("add", help="Add an MCP server to .mcp.json")
    add_parser.add_argument("name", help="Server name")
    add_parser.add_argument("--package", help="PyPI package name (default: {name}-mcp-server)")

    # remove
    remove_parser = subparsers.add_parser("remove", help="Remove an MCP server from .mcp.json")
    remove_parser.add_argument("name", help="Server name to remove")

    # search
    search_parser = subparsers.add_parser("search", help="Search MCP server catalog")
    search_parser.add_argument("query", help="Search query")

    args = parser.parse_args()

    if args.command == "create":
        cmd_create(args)
    elif args.command == "list":
        cmd_list(args)
    elif args.command == "add":
        cmd_add(args)
    elif args.command == "remove":
        cmd_remove(args)
    elif args.command == "search":
        cmd_search(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
