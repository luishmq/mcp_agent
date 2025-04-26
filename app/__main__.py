"""Main entry point for MCP chatbot."""

import asyncio
import logging

from app.chat.session import ChatSession
from app.config.config import Configuration
from app.llm.client import LLMClient
from app.server.server import Server


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", handlers=[
        logging.StreamHandler(),
    ]
)


async def main() -> None:
    """Initialize and run the chat session."""
    config = Configuration()
    server_config = config.load_config("servers_config.json")
    logger.info("Loaded server configuration: %s", server_config)
    servers = [
        Server(name, srv_config)
        for name, srv_config in server_config["mcpServers"].items()
    ]
    llm_client = LLMClient(config.llm_api_key)
    chat_session = ChatSession(servers, llm_client)
    await chat_session.start()


if __name__ == "__main__":
    asyncio.run(main())