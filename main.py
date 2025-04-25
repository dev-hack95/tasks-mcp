from fastmcp import FastMCP
from src.servers.tasks import tasks

mcp = FastMCP(name="Main")
mcp.mount("tasks", tasks)

if __name__ == "__main__":
    mcp.run(transport="sse", host='0.0.0.0', port=9001)
