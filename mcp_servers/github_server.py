"""
GitHub MCP Server
Provides GitHub integration for code and documentation management
"""
import json
from typing import Any, Dict, List
from mcp.server import Server
from mcp.types import Tool, TextContent


class GitHubMCPServer:
    """MCP Server for GitHub operations"""

    def __init__(self):
        self.server = Server("github-server")
        self._register_tools()

    def _register_tools(self):
        """Register available tools"""

        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            return [
                Tool(
                    name="search_repositories",
                    description="Search GitHub repositories",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query"
                            },
                            "language": {
                                "type": "string",
                                "description": "Filter by programming language"
                            },
                            "max_results": {
                                "type": "integer",
                                "description": "Maximum number of results",
                                "default": 10
                            }
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="get_repository_info",
                    description="Get detailed information about a repository",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "owner": {
                                "type": "string",
                                "description": "Repository owner"
                            },
                            "repo": {
                                "type": "string",
                                "description": "Repository name"
                            }
                        },
                        "required": ["owner", "repo"]
                    }
                ),
                Tool(
                    name="get_file_content",
                    description="Get content of a file from a repository",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "owner": {
                                "type": "string",
                                "description": "Repository owner"
                            },
                            "repo": {
                                "type": "string",
                                "description": "Repository name"
                            },
                            "path": {
                                "type": "string",
                                "description": "File path in repository"
                            },
                            "branch": {
                                "type": "string",
                                "description": "Branch name",
                                "default": "main"
                            }
                        },
                        "required": ["owner", "repo", "path"]
                    }
                ),
                Tool(
                    name="list_repository_files",
                    description="List files in a repository directory",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "owner": {
                                "type": "string",
                                "description": "Repository owner"
                            },
                            "repo": {
                                "type": "string",
                                "description": "Repository name"
                            },
                            "path": {
                                "type": "string",
                                "description": "Directory path",
                                "default": ""
                            }
                        },
                        "required": ["owner", "repo"]
                    }
                ),
                Tool(
                    name="search_code",
                    description="Search for code across GitHub",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Code search query"
                            },
                            "language": {
                                "type": "string",
                                "description": "Filter by language"
                            }
                        },
                        "required": ["query"]
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            if name == "search_repositories":
                return await self._search_repositories(arguments)
            elif name == "get_repository_info":
                return await self._get_repository_info(arguments["owner"], arguments["repo"])
            elif name == "get_file_content":
                return await self._get_file_content(
                    arguments["owner"],
                    arguments["repo"],
                    arguments["path"],
                    arguments.get("branch", "main")
                )
            elif name == "list_repository_files":
                return await self._list_repository_files(
                    arguments["owner"],
                    arguments["repo"],
                    arguments.get("path", "")
                )
            elif name == "search_code":
                return await self._search_code(arguments)
            else:
                raise ValueError(f"Unknown tool: {name}")

    async def _search_repositories(self, params: Dict[str, Any]) -> List[TextContent]:
        """Search GitHub repositories"""
        try:
            from github import Github
            import os

            # GitHub token from environment
            token = os.getenv("GITHUB_TOKEN")
            g = Github(token) if token else Github()

            query = params["query"]
            if "language" in params:
                query += f" language:{params['language']}"

            repos = g.search_repositories(query=query)

            results = []
            for repo in repos[:params.get("max_results", 10)]:
                results.append({
                    "name": repo.full_name,
                    "description": repo.description,
                    "url": repo.html_url,
                    "stars": repo.stargazers_count,
                    "language": repo.language
                })

            return [TextContent(type="text", text=json.dumps(results, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error searching repositories: {str(e)}")]

    async def _get_repository_info(self, owner: str, repo: str) -> List[TextContent]:
        """Get repository information"""
        try:
            from github import Github
            import os

            token = os.getenv("GITHUB_TOKEN")
            g = Github(token) if token else Github()

            repository = g.get_repo(f"{owner}/{repo}")

            info = {
                "name": repository.full_name,
                "description": repository.description,
                "url": repository.html_url,
                "stars": repository.stargazers_count,
                "forks": repository.forks_count,
                "language": repository.language,
                "topics": repository.get_topics(),
                "default_branch": repository.default_branch
            }

            return [TextContent(type="text", text=json.dumps(info, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error getting repository info: {str(e)}")]

    async def _get_file_content(self, owner: str, repo: str, path: str, branch: str = "main") -> List[TextContent]:
        """Get file content from repository"""
        try:
            from github import Github
            import os
            import base64

            token = os.getenv("GITHUB_TOKEN")
            g = Github(token) if token else Github()

            repository = g.get_repo(f"{owner}/{repo}")
            file_content = repository.get_contents(path, ref=branch)

            if isinstance(file_content, list):
                return [TextContent(type="text", text="Path is a directory, not a file")]

            content = base64.b64decode(file_content.content).decode('utf-8')
            return [TextContent(type="text", text=content)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error getting file content: {str(e)}")]

    async def _list_repository_files(self, owner: str, repo: str, path: str = "") -> List[TextContent]:
        """List files in repository directory"""
        try:
            from github import Github
            import os

            token = os.getenv("GITHUB_TOKEN")
            g = Github(token) if token else Github()

            repository = g.get_repo(f"{owner}/{repo}")
            contents = repository.get_contents(path)

            if not isinstance(contents, list):
                contents = [contents]

            files = []
            for content in contents:
                files.append({
                    "name": content.name,
                    "path": content.path,
                    "type": content.type,
                    "size": content.size
                })

            return [TextContent(type="text", text=json.dumps(files, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error listing files: {str(e)}")]

    async def _search_code(self, params: Dict[str, Any]) -> List[TextContent]:
        """Search for code across GitHub"""
        try:
            from github import Github
            import os

            token = os.getenv("GITHUB_TOKEN")
            g = Github(token) if token else Github()

            query = params["query"]
            if "language" in params:
                query += f" language:{params['language']}"

            code_results = g.search_code(query=query)

            results = []
            for code in code_results[:10]:
                results.append({
                    "repository": code.repository.full_name,
                    "path": code.path,
                    "url": code.html_url
                })

            return [TextContent(type="text", text=json.dumps(results, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error searching code: {str(e)}")]

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
    server = GitHubMCPServer()
    server.run()
