"""
MCP Server for Obsidian Vault - P1 Project
Exposes 3 tools: search_notes, get_daily_note, list_recent_notes
"""
import os
import json
from pathlib import Path
from datetime import datetime, timedelta

# Configuration: set your vault path
VAULT_PATH = os.environ.get("VAULT_PATH", os.path.expanduser("~/Documents/obsidian-vault"))


class ObsidianVault:
    """Simple Obsidian vault reader without MCP dependency."""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        if not self.vault_path.exists():
            raise FileNotFoundError(f"Vault not found: {vault_path}")

    def search_notes(self, query: str, max_results: int = 10) -> list[dict]:
        """Search vault notes by content keyword."""
        results = []
        query_lower = query.lower()
        for md_file in self.vault_path.rglob("*.md"):
            try:
                content = md_file.read_text(encoding="utf-8")
                if query_lower in content.lower():
                    lines = content.split("\n")
                    matches = [i for i, line in enumerate(lines) if query_lower in line.lower()]
                    for match_line_idx in matches[:3]:
                        start = max(0, match_line_idx - 2)
                        end = min(len(lines), match_line_idx + 3)
                        context = "\n".join(lines[start:end])
                        results.append({
                            "file": str(md_file.relative_to(self.vault_path)),
                            "line": match_line_idx + 1,
                            "context": context,
                        })
            except Exception:
                continue
        return sorted(results, key=lambda r: r["file"])[:max_results]

    def get_daily_note(self, date_str: str) -> dict | None:
        """Get daily note for a specific date (YYYY-MM-DD format)."""
        date = datetime.strptime(date_str, "%Y-%m-%d")
        # Common Obsidian daily note patterns
        patterns = [
            f"daily/{date_str}.md",
            f"日记/{date_str}.md",
            f"Daily/{date_str}.md",
            f"{date_str}.md",
        ]
        for pattern in patterns:
            filepath = self.vault_path / pattern
            if filepath.exists():
                return {
                    "file": pattern,
                    "date": date_str,
                    "content": filepath.read_text(encoding="utf-8")[:5000],
                }
        return None

    def list_recent_notes(self, days: int = 7, category: str | None = None) -> list[dict]:
        """List recently modified notes, optionally filtered by category folder."""
        cutoff = datetime.now() - timedelta(days=days)
        results = []
        for md_file in self.vault_path.rglob("*.md"):
            if category and category not in str(md_file.relative_to(self.vault_path)):
                continue
            mtime = datetime.fromtimestamp(md_file.stat().st_mtime)
            if mtime > cutoff:
                results.append({
                    "file": str(md_file.relative_to(self.vault_path)),
                    "modified": mtime.isoformat(),
                    "size_kb": round(md_file.stat().st_size / 1024, 1),
                })
        return sorted(results, key=lambda r: r["modified"], reverse=True)[:20]


# FastMCP-compatible tool definitions (simplified without actual MCP import)
TOOLS = {
    "search_notes": {
        "description": "Search Obsidian vault notes by keyword",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search keyword"},
                "max_results": {"type": "integer", "default": 10},
            },
            "required": ["query"],
        },
    },
    "get_daily_note": {
        "description": "Get daily note for a specific date",
        "inputSchema": {
            "type": "object",
            "properties": {
                "date": {"type": "string", "description": "Date in YYYY-MM-DD format"},
            },
            "required": ["date"],
        },
    },
    "list_recent_notes": {
        "description": "List recently modified notes",
        "inputSchema": {
            "type": "object",
            "properties": {
                "days": {"type": "integer", "default": 7},
                "category": {"type": "string", "description": "Filter by folder (optional)"},
            },
        },
    },
}


def main():
    """Demo: test all 3 tools standalone."""
    vault = ObsidianVault(VAULT_PATH)
    print(f"Vault: {VAULT_PATH}")
    print(f"Tools available: {list(TOOLS.keys())}\n")

    # Test search_notes
    print("=== search_notes('RAG') ===")
    for r in vault.search_notes("RAG", max_results=3):
        print(f"  {r['file']}:{r['line']}")

    # Test list_recent_notes
    print("\n=== list_recent_notes(7) ===")
    for r in vault.list_recent_notes(7)[:5]:
        print(f"  {r['file']} ({r['size_kb']}KB, {r['modified'][:10]})")

    # Test get_daily_note
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"\n=== get_daily_note('{today}') ===")
    note = vault.get_daily_note(today)
    if note:
        print(f"  Found: {note['file']} ({len(note['content'])} chars)")
    else:
        print("  No daily note found for today.")


if __name__ == "__main__":
    main()
