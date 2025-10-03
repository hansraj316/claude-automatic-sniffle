"""
Database MCP Server
Provides SQLite database and vector storage capabilities
"""
import json
import sqlite3
from typing import Any, Dict, List
from pathlib import Path
from mcp.server import Server
from mcp.types import Tool, TextContent


class DatabaseMCPServer:
    """MCP Server for database operations"""

    def __init__(self, db_path: str = "./knowledge_base/research_hub.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.server = Server("database-server")
        self._init_database()
        self._register_tools()

    def _init_database(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Documents table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                source_url TEXT,
                document_type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT
            )
        """)

        # Citations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS citations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER,
                citation_text TEXT NOT NULL,
                citation_type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (document_id) REFERENCES documents(id)
            )
        """)

        # Queries table for Q&A history
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS qa_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                context_docs TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

    def _register_tools(self):
        """Register available tools"""

        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            return [
                Tool(
                    name="store_document",
                    description="Store a document in the database",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "content": {"type": "string"},
                            "source_url": {"type": "string"},
                            "document_type": {"type": "string"},
                            "metadata": {"type": "object"}
                        },
                        "required": ["title", "content"]
                    }
                ),
                Tool(
                    name="search_documents",
                    description="Search for documents by keyword",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"},
                            "limit": {"type": "integer", "default": 10}
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="get_document",
                    description="Get a document by ID",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "document_id": {"type": "integer"}
                        },
                        "required": ["document_id"]
                    }
                ),
                Tool(
                    name="store_citation",
                    description="Store a citation for a document",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "document_id": {"type": "integer"},
                            "citation_text": {"type": "string"},
                            "citation_type": {"type": "string"}
                        },
                        "required": ["citation_text"]
                    }
                ),
                Tool(
                    name="store_qa",
                    description="Store a Q&A interaction",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "question": {"type": "string"},
                            "answer": {"type": "string"},
                            "context_docs": {"type": "string"}
                        },
                        "required": ["question", "answer"]
                    }
                ),
                Tool(
                    name="get_qa_history",
                    description="Get Q&A history",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "limit": {"type": "integer", "default": 20}
                        }
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            if name == "store_document":
                return await self._store_document(arguments)
            elif name == "search_documents":
                return await self._search_documents(arguments["query"], arguments.get("limit", 10))
            elif name == "get_document":
                return await self._get_document(arguments["document_id"])
            elif name == "store_citation":
                return await self._store_citation(arguments)
            elif name == "store_qa":
                return await self._store_qa(arguments)
            elif name == "get_qa_history":
                return await self._get_qa_history(arguments.get("limit", 20))
            else:
                raise ValueError(f"Unknown tool: {name}")

    async def _store_document(self, doc_data: Dict[str, Any]) -> List[TextContent]:
        """Store a document"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO documents (title, content, source_url, document_type, metadata)
                VALUES (?, ?, ?, ?, ?)
            """, (
                doc_data["title"],
                doc_data["content"],
                doc_data.get("source_url"),
                doc_data.get("document_type"),
                json.dumps(doc_data.get("metadata", {}))
            ))

            doc_id = cursor.lastrowid
            conn.commit()
            conn.close()

            return [TextContent(type="text", text=f"Document stored with ID: {doc_id}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error storing document: {str(e)}")]

    async def _search_documents(self, query: str, limit: int = 10) -> List[TextContent]:
        """Search documents by keyword"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, title, content, source_url, document_type
                FROM documents
                WHERE title LIKE ? OR content LIKE ?
                LIMIT ?
            """, (f"%{query}%", f"%{query}%", limit))

            results = []
            for row in cursor.fetchall():
                results.append({
                    "id": row[0],
                    "title": row[1],
                    "content": row[2][:500],  # Truncate content
                    "source_url": row[3],
                    "document_type": row[4]
                })

            conn.close()
            return [TextContent(type="text", text=json.dumps(results, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error searching documents: {str(e)}")]

    async def _get_document(self, document_id: int) -> List[TextContent]:
        """Get a document by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, title, content, source_url, document_type, metadata
                FROM documents WHERE id = ?
            """, (document_id,))

            row = cursor.fetchone()
            if row:
                result = {
                    "id": row[0],
                    "title": row[1],
                    "content": row[2],
                    "source_url": row[3],
                    "document_type": row[4],
                    "metadata": json.loads(row[5]) if row[5] else {}
                }
                conn.close()
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            else:
                conn.close()
                return [TextContent(type="text", text=f"Document {document_id} not found")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error getting document: {str(e)}")]

    async def _store_citation(self, citation_data: Dict[str, Any]) -> List[TextContent]:
        """Store a citation"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO citations (document_id, citation_text, citation_type)
                VALUES (?, ?, ?)
            """, (
                citation_data.get("document_id"),
                citation_data["citation_text"],
                citation_data.get("citation_type")
            ))

            citation_id = cursor.lastrowid
            conn.commit()
            conn.close()

            return [TextContent(type="text", text=f"Citation stored with ID: {citation_id}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error storing citation: {str(e)}")]

    async def _store_qa(self, qa_data: Dict[str, Any]) -> List[TextContent]:
        """Store a Q&A interaction"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO qa_history (question, answer, context_docs)
                VALUES (?, ?, ?)
            """, (
                qa_data["question"],
                qa_data["answer"],
                qa_data.get("context_docs")
            ))

            qa_id = cursor.lastrowid
            conn.commit()
            conn.close()

            return [TextContent(type="text", text=f"Q&A stored with ID: {qa_id}")]
        except Exception as e:
            return [TextContent(type="text", text=f"Error storing Q&A: {str(e)}")]

    async def _get_qa_history(self, limit: int = 20) -> List[TextContent]:
        """Get Q&A history"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT question, answer, context_docs, created_at
                FROM qa_history
                ORDER BY created_at DESC
                LIMIT ?
            """, (limit,))

            results = []
            for row in cursor.fetchall():
                results.append({
                    "question": row[0],
                    "answer": row[1],
                    "context_docs": row[2],
                    "created_at": row[3]
                })

            conn.close()
            return [TextContent(type="text", text=json.dumps(results, indent=2))]
        except Exception as e:
            return [TextContent(type="text", text=f"Error getting Q&A history: {str(e)}")]

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
    server = DatabaseMCPServer()
    server.run()
