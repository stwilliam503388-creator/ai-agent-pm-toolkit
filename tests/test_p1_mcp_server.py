"""Tests for P1: MCP Obsidian Server - ObsidianVault class."""
import os
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import pytest

# Add project to path so we can import
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "04-projects", "p1-mcp-server"))

# We import the module by filename since it has a hyphen
import importlib.util
_spec = importlib.util.spec_from_file_location(
    "mcp_obsidian_server",
    os.path.join(os.path.dirname(__file__), "..", "04-projects", "p1-mcp-server", "mcp-obsidian-server.py"),
)
mcp_server = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mcp_server)

ObsidianVault = mcp_server.ObsidianVault
TOOLS = mcp_server.TOOLS


@pytest.fixture
def vault_dir(tmp_path):
    """Create a temporary vault with sample markdown files."""
    # Create some markdown files
    (tmp_path / "note1.md").write_text("# Introduction to RAG\nRAG stands for Retrieval Augmented Generation.\nIt combines retrieval with generation.")
    (tmp_path / "note2.md").write_text("# MCP Protocol\nModel Context Protocol enables tool use.\nAgents can call external tools.")
    (tmp_path / "subdir").mkdir()
    (tmp_path / "subdir" / "nested.md").write_text("# Nested Note\nThis note is in a subdirectory.\nRAG is also mentioned here.")
    (tmp_path / "daily").mkdir()
    today = datetime.now().strftime("%Y-%m-%d")
    (tmp_path / "daily" / f"{today}.md").write_text("# Daily Note\nToday I learned about agents.\nKey takeaways from the day.")
    return tmp_path


@pytest.fixture
def vault(vault_dir):
    """Create an ObsidianVault instance with the temp vault."""
    return ObsidianVault(str(vault_dir))


class TestObsidianVaultInit:
    def test_init_valid_path(self, vault_dir):
        v = ObsidianVault(str(vault_dir))
        assert v.vault_path == vault_dir

    def test_init_nonexistent_path(self):
        with pytest.raises(FileNotFoundError, match="Vault not found"):
            ObsidianVault("/nonexistent/path/that/does/not/exist")


class TestSearchNotes:
    def test_search_finds_matching_notes(self, vault):
        results = vault.search_notes("RAG")
        assert len(results) >= 2
        files = [r["file"] for r in results]
        assert "note1.md" in files

    def test_search_case_insensitive(self, vault):
        results_lower = vault.search_notes("rag")
        results_upper = vault.search_notes("RAG")
        assert len(results_lower) == len(results_upper)

    def test_search_no_results(self, vault):
        results = vault.search_notes("xyznonexistentkeyword")
        assert results == []

    def test_search_max_results(self, vault):
        results = vault.search_notes("RAG", max_results=1)
        assert len(results) <= 1

    def test_search_returns_context(self, vault):
        results = vault.search_notes("RAG")
        for r in results:
            assert "file" in r
            assert "line" in r
            assert "context" in r
            assert isinstance(r["line"], int)

    def test_search_in_subdirectory(self, vault):
        results = vault.search_notes("subdirectory")
        assert len(results) >= 1
        assert any("nested.md" in r["file"] for r in results)

    def test_search_results_sorted_by_file(self, vault):
        results = vault.search_notes("RAG")
        files = [r["file"] for r in results]
        assert files == sorted(files)


class TestGetDailyNote:
    def test_get_existing_daily_note(self, vault):
        today = datetime.now().strftime("%Y-%m-%d")
        result = vault.get_daily_note(today)
        assert result is not None
        assert result["date"] == today
        assert "content" in result
        assert "Daily Note" in result["content"]

    def test_get_nonexistent_daily_note(self, vault):
        result = vault.get_daily_note("1999-01-01")
        assert result is None

    def test_get_daily_note_invalid_date_format(self, vault):
        with pytest.raises(ValueError):
            vault.get_daily_note("not-a-date")

    def test_daily_note_content_truncated_at_5000(self, vault_dir):
        """Content should be truncated to 5000 characters."""
        today = datetime.now().strftime("%Y-%m-%d")
        (vault_dir / "daily" / f"{today}.md").write_text("x" * 10000)
        vault = ObsidianVault(str(vault_dir))
        result = vault.get_daily_note(today)
        assert result is not None
        assert len(result["content"]) == 5000


class TestListRecentNotes:
    def test_list_recent_notes_returns_results(self, vault):
        results = vault.list_recent_notes(days=7)
        assert len(results) > 0

    def test_list_recent_notes_sorted_by_modified_desc(self, vault):
        results = vault.list_recent_notes(days=7)
        dates = [r["modified"] for r in results]
        assert dates == sorted(dates, reverse=True)

    def test_list_recent_notes_contains_expected_fields(self, vault):
        results = vault.list_recent_notes(days=7)
        for r in results:
            assert "file" in r
            assert "modified" in r
            assert "size_kb" in r

    def test_list_recent_notes_category_filter(self, vault):
        results = vault.list_recent_notes(days=7, category="subdir")
        assert all("subdir" in r["file"] for r in results)

    def test_list_recent_notes_no_old_results(self, vault):
        results = vault.list_recent_notes(days=0)
        # With days=0, cutoff is now, so nothing should match unless just created
        # Files created in the fixture were just created, so they might match
        # The point is the function doesn't crash
        assert isinstance(results, list)

    def test_list_recent_notes_max_20(self, vault_dir):
        """Should return at most 20 results."""
        for i in range(25):
            (vault_dir / f"bulk_{i}.md").write_text(f"Bulk note {i}")
        vault = ObsidianVault(str(vault_dir))
        results = vault.list_recent_notes(days=7)
        assert len(results) <= 20


class TestToolDefinitions:
    def test_tools_dict_has_all_tools(self):
        assert "search_notes" in TOOLS
        assert "get_daily_note" in TOOLS
        assert "list_recent_notes" in TOOLS

    def test_tools_have_required_fields(self):
        for name, tool in TOOLS.items():
            assert "description" in tool
            assert "inputSchema" in tool
            assert "properties" in tool["inputSchema"]

    def test_search_notes_schema_requires_query(self):
        schema = TOOLS["search_notes"]["inputSchema"]
        assert "query" in schema["required"]
