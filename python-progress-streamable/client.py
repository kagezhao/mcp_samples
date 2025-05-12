from mcp.client.session import ClientSession, RequestResponder
from mcp.client.streamable_http import streamablehttp_client
import mcp.types as types
import asyncio


async def message_handler(
    message: (
        RequestResponder[types.ServerRequest, types.ClientResult]
        | types.ServerNotification
        | Exception
    ),
) -> None:
    if isinstance(message, types.ServerNotification):
        print("ServerNotification", message)


async def main():
    server_url = "http://127.0.0.1:3005/mcp"

    async with streamablehttp_client(server_url) as (
        read_stream,
        write_stream,
        get_session_id_callback,
    ):
        async with ClientSession(
            read_stream=read_stream,
            write_stream=write_stream,
            message_handler=message_handler,
        ) as client:
            await client.initialize()

            print(f"calling tool at {server_url}")
            tool_response = await client.call_tool(
                name="mcp_sleep", arguments={"seconds": 5}
            )
            print(f"result:\n{tool_response.content[0].text}")


if __name__ == "__main__":
    asyncio.run(main())
