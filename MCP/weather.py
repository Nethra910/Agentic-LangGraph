from mcp.server.fastmcp import FastMCP

mcp = FastMCP("WeatherServer")

@mcp.tool()
async def get_weather(location:str) -> str:
    """
    Get the current weather for a given location.
    """
    return "Gujrat ,vododara 35°C"


if __name__ == "__main__":
    mcp.run(transport="streamable-http")