from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from dotenv import load_dotenv
from pathlib import Path
import asyncio
import os

load_dotenv()

async def main():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing from your .env file")

    project_dir = Path(__file__).resolve().parent.parent

    client = MultiServerMCPClient(
        {
            "MathServer": {
                "command": "python",
                "args": [str(project_dir / "MCP" / "mathserver.py")],
                "transport": "stdio",
            },
            "WeatherServer": {
                "url": "http://localhost:8000/mcp",
                "transport": "streamable-http",
            },
        }
    )

    groq = ChatGroq(
        model="openai/gpt-oss-120b",
        api_key=api_key,
    )

    tools = await client.get_tools()
    print("Available tools:", [tool.name for tool in tools])

    agent = create_agent(
        model=groq,
        tools=tools,
    )

    response_math = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "What is (3 x 5) x 12 + 10?",
                }
            ]
        }
    )
    response_weather = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "What is the current weather in Vadodara?",
                }
            ]
        }
    )



    print("Math Response:", response_math["messages"][-1].content)
    print("Weather Response:", response_weather["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())
