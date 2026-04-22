from __future__ import annotations
from designlib_mcp.server import build_server


def main() -> None:
    mcp = build_server()
    mcp.run()


if __name__ == "__main__":
    main()
