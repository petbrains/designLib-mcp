from __future__ import annotations
import argparse
import os

from designlib_mcp.server import build_server


def main() -> None:
    parser = argparse.ArgumentParser(prog="designlib-mcp")
    parser.add_argument("--http", action="store_true",
                        help="Run over HTTP (streamable-http) instead of stdio")
    parser.add_argument("--host", default="0.0.0.0",
                        help="HTTP bind host (default: 0.0.0.0)")
    parser.add_argument("--port", type=int,
                        default=int(os.getenv("PORT", "8000")),
                        help="HTTP port (default: $PORT or 8000)")
    args = parser.parse_args()

    mcp = build_server()
    use_http = args.http or os.getenv("DESIGNLIB_TRANSPORT", "").lower() == "http"
    if use_http:
        mcp.run(transport="http", host=args.host, port=args.port)
    else:
        mcp.run()


if __name__ == "__main__":
    main()
