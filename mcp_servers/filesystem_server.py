"""
Filesystem MCP Server
Provides file system operations for document management
"""
import os
import json
from pathlib import Path
from typing import Any, Dict, List
from mcp.server import Server
from mcp.types import Tool, TextContent


class FilesystemMCPServer:
    """MCP Server for file system operations"""

    def __init__(self, base_path: str = "./knowledge_base"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.server = Server("filesystem-server")
        self._register_tools()

    def _register_tools(self):
        """Register available tools"""

        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            return [
                Tool(
                    name="read_file",
                    description="Read contents of a file from knowledge base",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Path to file relative to knowledge base"
                            }
                        },
                        "required": ["file_path"]
                    }
                ),
                Tool(
                    name="write_file",
                    description="Write content to a file in knowledge base",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Path to file relative to knowledge base"
                            },
                            "content": {
                                "type": "string",
                                "description": "Content to write to file"
                            }
                        },
                        "required": ["file_path", "content"]
                    }
                ),
                Tool(
                    name="list_files",
                    description="List all files in knowledge base directory",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "directory": {
                                "type": "string",
                                "description": "Directory to list (optional)",
                                "default": "."
                            }
                        }
                    }
                ),
                Tool(
                    name="delete_file",
                    description="Delete a file from knowledge base",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "Path to file to delete"
                            }
                        },
                        "required": ["file_path"]
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            if name == "read_file":
                return await self._read_file(arguments["file_path"])
            elif name == "write_file":
                return await self._write_file(arguments["file_path"], arguments["content"])
            elif name == "list_files":
                directory = arguments.get("directory", ".")
                return await self._list_files(directory)
            elif name == "delete_file":
                return await self._delete_file(arguments["file_path"])
            else:
                raise ValueError(f"Unknown tool: {name}")

    async def _read_file(self, file_path: str) -> List[TextContent]:
        """Read file from knowledge base"""
        try:
            full_path = self.base_path / file_path
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return [TextContent(type="text", text=content)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error reading file: {str(e)}")]

    async def _write_file(self, file_path: str, content: str) -> List[TextContent]:
        """Write file to knowledge base"""
        try:
            full_path = self.base_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return [TextContent(type="text", text=f"Successfully wrote to {file_path}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error writing file: {str(e)}")]

    async def _list_files(self, directory: str = ".") -> List[TextContent]:
        """List files in knowledge base directory"""
        try:
            full_path = self.base_path / directory
            files = [str(f.relative_to(self.base_path)) for f in full_path.rglob("*") if f.is_file()]
            return [TextContent(type="text", text=json.dumps(files, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error listing files: {str(e)}")]

    async def _delete_file(self, file_path: str) -> List[TextContent]:
        """Delete file from knowledge base"""
        try:
            full_path = self.base_path / file_path
            os.remove(full_path)
            return [TextContent(type="text", text=f"Successfully deleted {file_path}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error deleting file: {str(e)}")]

    def run(self):
        """Run the MCP server"""
        import asyncio
        from mcp.server.stdio import stdio_server

        async def main():
            async with stdio_server() as (read_stream, write_stream):
                await self.server.run(
                    read_stream,
                    write_stream,
                    self.server.create_initialization_options()
                )

        asyncio.run(main())


if __name__ == "__main__":
    server = FilesystemMCPServer()
    server.run()
