"""
Web Search MCP Server
Provides web search and content extraction capabilities
"""
import json
from typing import Any, Dict, List
import requests
from bs4 import BeautifulSoup
from mcp.server import Server
from mcp.types import Tool, TextContent


class WebSearchMCPServer:
    """MCP Server for web search operations"""

    def __init__(self):
        self.server = Server("websearch-server")
        self._register_tools()

    def _register_tools(self):
        """Register available tools"""

        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            return [
                Tool(
                    name="search_web",
                    description="Search the web for information",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query"
                            },
                            "num_results": {
                                "type": "integer",
                                "description": "Number of results to return",
                                "default": 5
                            }
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="extract_content",
                    description="Extract text content from a web page",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "URL of the web page"
                            }
                        },
                        "required": ["url"]
                    }
                ),
                Tool(
                    name="extract_links",
                    description="Extract all links from a web page",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "URL of the web page"
                            }
                        },
                        "required": ["url"]
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            if name == "search_web":
                return await self._search_web(
                    arguments["query"],
                    arguments.get("num_results", 5)
                )
            elif name == "extract_content":
                return await self._extract_content(arguments["url"])
            elif name == "extract_links":
                return await self._extract_links(arguments["url"])
            else:
                raise ValueError(f"Unknown tool: {name}")

    async def _search_web(self, query: str, num_results: int = 5) -> List[TextContent]:
        """
        Search the web (using DuckDuckGo HTML)
        Note: For production, consider using proper search APIs
        """
        try:
            # Simple DuckDuckGo HTML search
            url = f"https://html.duckduckgo.com/html/?q={query}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            results = []
            for result in soup.find_all('div', class_='result')[:num_results]:
                title_elem = result.find('a', class_='result__a')
                snippet_elem = result.find('a', class_='result__snippet')

                if title_elem:
                    results.append({
                        'title': title_elem.get_text(strip=True),
                        'url': title_elem.get('href', ''),
                        'snippet': snippet_elem.get_text(strip=True) if snippet_elem else ''
                    })

            return [TextContent(type="text", text=json.dumps(results, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error searching web: {str(e)}")]

    async def _extract_content(self, url: str) -> List[TextContent]:
        """Extract text content from a web page"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Get text content
            text = soup.get_text()

            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)

            return [TextContent(type="text", text=text[:10000])]  # Limit to 10k chars
        except Exception as e:
            return [TextContent(type="text", text=f"Error extracting content: {str(e)}")]

    async def _extract_links(self, url: str) -> List[TextContent]:
        """Extract all links from a web page"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            links = []
            for link in soup.find_all('a', href=True):
                href = link['href']
                text = link.get_text(strip=True)
                if href.startswith('http'):
                    links.append({'url': href, 'text': text})

            return [TextContent(type="text", text=json.dumps(links, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error extracting links: {str(e)}")]

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
    server = WebSearchMCPServer()
    server.run()
