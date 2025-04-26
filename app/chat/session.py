import json
import logging
from typing import List

from app.llm.client import LLMClient
from app.server.server import Server


class ChatSession:
    """Orchestrates the interaction between user, LLM, and tools."""

    def __init__(self, servers: List[Server], llm_client: LLMClient) -> None:
        """Initialize chat session.
        
        Args:
            servers: List of MCP servers.
            llm_client: LLM client.
        """
        self.servers: List[Server] = servers
        self.llm_client: LLMClient = llm_client

    async def cleanup_servers(self) -> None:
        """Clean up all servers properly."""
        for server in self.servers:
            try:
                await server.cleanup()
            except Exception as e:
                logging.warning(f"Warning during cleanup of server {server.name}: {e}")

    async def process_llm_response(self, llm_response: str) -> str:
        """Process the LLM response and execute tools if needed.

        Args:
            llm_response: The response from the LLM.

        Returns:
            The result of tool execution or the original response.
        """
        try:
            tool_call = json.loads(llm_response)
            if "tool" in tool_call and "arguments" in tool_call:
                logging.info(f"Executing tool: {tool_call['tool']}")
                logging.info(f"With arguments: {tool_call['arguments']}")

                for server in self.servers:
                    tools = await server.list_tools()
                    if any(tool.name == tool_call["tool"] for tool in tools):
                        try:
                            result = await server.execute_tool(
                                tool_call["tool"], tool_call["arguments"]
                            )

                            if isinstance(result, dict) and "progress" in result:
                                progress = result["progress"]
                                total = result["total"]
                                percentage = (progress / total) * 100
                                logging.info(
                                    f"Progress: {progress}/{total} ({percentage:.1f}%)"
                                )

                            return f"Tool execution result: {result}"
                        except Exception as e:
                            error_msg = f"Error executing tool: {str(e)}"
                            logging.error(error_msg)
                            return error_msg

                return f"No server found with tool: {tool_call['tool']}"
            return llm_response
        except json.JSONDecodeError:
            return llm_response

    async def start(self) -> None:
        """Main chat session handler."""
        try:
            for server in self.servers:
                try:
                    await server.initialize()
                except Exception as e:
                    logging.error(f"Failed to initialize server: {e}")
                    await self.cleanup_servers()
                    return

            all_tools = []
            for server in self.servers:
                tools = await server.list_tools()
                all_tools.extend(tools)

            tools_description = "\n".join([tool.format_for_llm() for tool in all_tools])

            system_message = (
                "Você é um assistente útil com acesso às seguintes ferramentas:\n\n"
                f"{tools_description}\n"
                "Escolha a ferramenta apropriada com base na pergunta do usuário. "
                "Se nenhuma ferramenta for necessária, responda diretamente.\n\n"
                "IMPORTANTE: Quando precisar usar uma ferramenta, responda APENAS com o "
                "objeto JSON no formato exato abaixo, nada mais:\n"
                "{\n"
                '    "tool": "nome-da-ferramenta",\n'
                '    "arguments": {\n'
                '        "nome-do-argumento": "valor"\n'
                "    }\n"
                "}\n\n"
                "Após receber a resposta de uma ferramenta:\n"
                "1. Transforme os dados brutos em uma resposta natural, de forma conversacional\n"
                "2. Mantenha as respostas concisas, porém informativas\n"
                "3. Foque nas informações mais relevantes\n"
                "4. Use o contexto apropriado da pergunta do usuário\n"
                "5. Evite simplesmente repetir os dados brutos\n\n"
                "Utilize apenas as ferramentas explicitamente definidas acima."
            )

            messages = [{"role": "system", "content": system_message}]

            while True:
                user_input = input("You: ").strip()
                if user_input.lower() in {"quit", "exit"}:
                    print("Tchau!")
                    break

                messages.append({"role": "user", "content": user_input})
                llm_resp = self.llm_client.get_response(messages)
                print(f"Assistant: {llm_resp}")

                tool_resp = await self.process_llm_response(llm_resp)

                # se tool_resp é diferente, preciso fazer follow-up
                if tool_resp != llm_resp:
                    messages.extend(
                        [
                            {"role": "assistant", "content": llm_resp},
                            {"role": "system", "content": tool_resp},
                        ]
                    )
                    follow_up = self.llm_client.get_response(messages)
                    print(f"Assistant: {follow_up}")
                    messages.append({"role": "assistant", "content": follow_up})
                else:
                    messages.append({"role": "assistant", "content": llm_resp})

        finally:
            await self.cleanup_servers()