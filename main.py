import asyncio
import logging

from app.chat.session import ChatSession
from app.config.config import Configuration
from app.llm.client import LLMClient
from app.server.server import Server


logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.StreamHandler()],
)

async def main() -> None:
    cfg = Configuration()

    server_cfg = cfg.load_config("servers_config.json")
    servers = [
        Server(name, srv_cfg)
        for name, srv_cfg in server_cfg["mcpServers"].items()
    ]

    llm_client = LLMClient(cfg.llm_api_key)
    chat = ChatSession(servers, llm_client)
    await chat.start()


if __name__ == "__main__":
    asyncio.run(main())