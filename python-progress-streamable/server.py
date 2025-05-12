import signal
from typing import Literal
from pydantic import Field
from mcp.server.fastmcp import FastMCP, Context
import argparse
import time
import os
import anyio


mcp = FastMCP("sample_mcp", port=3005, debug=True)


@mcp.tool()
async def mcp_sleep(
    context: Context,
    seconds: int = Field(default=1, description="等待时间（单位秒），默认1秒"),
) -> str:
    """Sleep 工具"""
    if seconds <= 0:
        raise Exception(f"seconds必须大于0")

    if seconds > 1000:
        raise Exception(f"seconds最多1000")

    for i in range(seconds):
        # 模拟进度更新
        print(f"sleeping {i+1}/{seconds} seconds")
        # 每秒钟更新一次进度
        await context.session.send_log_message(
            level="info",
            data=f"Notification {i+1}/{seconds}",
            logger="mcp_sleep",
            related_request_id=context.request_id,
        )
        # 等待1秒
        await anyio.sleep(1)

    return f"sleeped {seconds} seconds"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--transport",
        type=str,
        default="stdio",
        help="stdio/sse/streamable-http (default: stdio)",
    )  # Add transport argument
    args = parser.parse_args()

    transport = args.transport
    print(f"transport: {transport}")

    mcp.run(transport=transport)  # Use the parsed transport argument


def signal_handler(signal, frame):
    print("Ctrl-C break")
    os._exit(0)
    return


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    main()
