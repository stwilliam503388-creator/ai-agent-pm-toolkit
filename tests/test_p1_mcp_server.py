"""P1 MCP Obsidian Server 测试 — ObsidianVault 类的完整单元测试。

被测对象
--------
04-projects/p1-mcp-server/mcp-obsidian-server.py
  - ObsidianVault 类：search_notes / get_daily_note / list_recent_notes
  - TOOLS 字典：FastMCP 兼容的工具 schema 定义

运行方式
--------
    # 在项目根目录执行全部 P1 测试
    pytest tests/test_p1_mcp_server.py -v

    # 只运行搜索相关测试
    pytest tests/test_p1_mcp_server.py::TestSearchNotes -v

    # 只运行某一条用例
    pytest tests/test_p1_mcp_server.py::TestGetDailyNote::test_daily_note_content_truncated_at_5000 -v

测试策略
--------
- 使用 pytest 的 tmp_path fixture 在临时目录下创建模拟 Obsidian vault 结构
  （包括 note1.md、note2.md、subdir/nested.md、daily/{today}.md）
- 不依赖真实 Obsidian 安装或文件系统
- 由于源文件名含连字符 (mcp-obsidian-server.py)，使用 importlib 动态导入

依赖
----
- pytest (pip install pytest)
- 无其他外部依赖
"""
import os
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import pytest

# 源文件名含连字符，不能直接 import，需要用 importlib 动态加载
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "04-projects", "p1-mcp-server"))

import importlib.util
_spec = importlib.util.spec_from_file_location(
    "mcp_obsidian_server",
    os.path.join(os.path.dirname(__file__), "..", "04-projects", "p1-mcp-server", "mcp-obsidian-server.py"),
)
mcp_server = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mcp_server)

ObsidianVault = mcp_server.ObsidianVault
TOOLS = mcp_server.TOOLS


# =====================================================================
# Fixtures — 构造测试用的临时 Obsidian vault 目录
# =====================================================================

@pytest.fixture
def vault_dir(tmp_path):
    """创建一个含有示例 Markdown 文件的临时 vault 目录。

    目录结构:
        tmp_path/
        ├── note1.md          — 包含 "RAG" 关键词
        ├── note2.md          — 包含 "MCP" 关键词
        ├── subdir/
        │   └── nested.md     — 子目录中的笔记，也含 "RAG"
        └── daily/
            └── {today}.md    — 今日的 Daily Note
    """
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
    """基于临时目录创建 ObsidianVault 实例，供各测试方法直接使用。"""
    return ObsidianVault(str(vault_dir))


class TestObsidianVaultInit:
    """ObsidianVault 构造函数测试 — 验证路径校验逻辑。"""

    def test_init_valid_path(self, vault_dir):
        """合法路径应成功创建实例，vault_path 指向该目录。"""
        v = ObsidianVault(str(vault_dir))
        assert v.vault_path == vault_dir

    def test_init_nonexistent_path(self):
        """不存在的路径应抛出 FileNotFoundError。"""
        with pytest.raises(FileNotFoundError, match="Vault not found"):
            ObsidianVault("/nonexistent/path/that/does/not/exist")


class TestSearchNotes:
    """search_notes() 方法测试 — 按关键词在 vault 中搜索笔记内容。

    验证点：
    - 关键词匹配：能在多个文件中找到包含关键词的行
    - 大小写不敏感：search("rag") 和 search("RAG") 应返回相同数量的结果
    - 无结果处理：不存在的关键词返回空列表
    - max_results 截断：结果数量不超过指定上限
    - 上下文窗口：每条结果包含匹配行前后各 2 行的上下文
    - 子目录搜索：能递归搜索子目录中的 .md 文件
    - 排序：结果按文件名字母序排列
    """

    def test_search_finds_matching_notes(self, vault):
        """搜索 "RAG" 应至少匹配 note1.md 和 subdir/nested.md。"""
        results = vault.search_notes("RAG")
        assert len(results) >= 2
        files = [r["file"] for r in results]
        assert "note1.md" in files

    def test_search_case_insensitive(self, vault):
        """搜索应不区分大小写 —— "rag" 和 "RAG" 结果数量相同。"""
        results_lower = vault.search_notes("rag")
        results_upper = vault.search_notes("RAG")
        assert len(results_lower) == len(results_upper)

    def test_search_no_results(self, vault):
        """搜索不存在的关键词应返回空列表。"""
        results = vault.search_notes("xyznonexistentkeyword")
        assert results == []

    def test_search_max_results(self, vault):
        """max_results=1 时最多只返回 1 条结果。"""
        results = vault.search_notes("RAG", max_results=1)
        assert len(results) <= 1

    def test_search_returns_context(self, vault):
        """每条结果应包含 file（文件名）、line（行号）、context（上下文片段）。"""
        results = vault.search_notes("RAG")
        for r in results:
            assert "file" in r
            assert "line" in r
            assert "context" in r
            assert isinstance(r["line"], int)

    def test_search_in_subdirectory(self, vault):
        """应能递归搜索子目录中的笔记。"""
        results = vault.search_notes("subdirectory")
        assert len(results) >= 1
        assert any("nested.md" in r["file"] for r in results)

    def test_search_results_sorted_by_file(self, vault):
        """搜索结果应按文件路径字母序排列。"""
        results = vault.search_notes("RAG")
        files = [r["file"] for r in results]
        assert files == sorted(files)


class TestGetDailyNote:
    """get_daily_note() 方法测试 — 按日期获取 Daily Note。

    验证点：
    - 存在的日期返回 {file, date, content}
    - 不存在的日期返回 None
    - 非法日期格式抛出 ValueError
    - 长内容截断至 5000 字符
    """

    def test_get_existing_daily_note(self, vault):
        """今天的 Daily Note 存在，应返回完整信息。"""
        today = datetime.now().strftime("%Y-%m-%d")
        result = vault.get_daily_note(today)
        assert result is not None
        assert result["date"] == today
        assert "content" in result
        assert "Daily Note" in result["content"]

    def test_get_nonexistent_daily_note(self, vault):
        """1999-01-01 不存在对应笔记，应返回 None。"""
        result = vault.get_daily_note("1999-01-01")
        assert result is None

    def test_get_daily_note_invalid_date_format(self, vault):
        """非 YYYY-MM-DD 格式的字符串应抛出 ValueError。"""
        with pytest.raises(ValueError):
            vault.get_daily_note("not-a-date")

    def test_daily_note_content_truncated_at_5000(self, vault_dir):
        """超过 5000 字符的笔记内容应被截断至 5000 字符。"""
        today = datetime.now().strftime("%Y-%m-%d")
        (vault_dir / "daily" / f"{today}.md").write_text("x" * 10000)
        vault = ObsidianVault(str(vault_dir))
        result = vault.get_daily_note(today)
        assert result is not None
        assert len(result["content"]) == 5000


class TestListRecentNotes:
    """list_recent_notes() 方法测试 — 列出最近修改过的笔记。

    验证点：
    - 返回最近 N 天内修改的笔记列表
    - 结果按修改时间倒序排列（最新的在前）
    - 每条结果包含 file / modified / size_kb 字段
    - category 参数可按目录名过滤
    - 结果数量上限为 20
    """

    def test_list_recent_notes_returns_results(self, vault):
        """vault 中的文件刚创建，7 天内应有结果。"""
        results = vault.list_recent_notes(days=7)
        assert len(results) > 0

    def test_list_recent_notes_sorted_by_modified_desc(self, vault):
        """结果应按修改时间从新到旧排列。"""
        results = vault.list_recent_notes(days=7)
        dates = [r["modified"] for r in results]
        assert dates == sorted(dates, reverse=True)

    def test_list_recent_notes_contains_expected_fields(self, vault):
        """每条结果应包含 file（路径）、modified（ISO 时间戳）、size_kb（文件大小）。"""
        results = vault.list_recent_notes(days=7)
        for r in results:
            assert "file" in r
            assert "modified" in r
            assert "size_kb" in r

    def test_list_recent_notes_category_filter(self, vault):
        """传入 category="subdir" 时，只返回路径中包含 "subdir" 的笔记。"""
        results = vault.list_recent_notes(days=7, category="subdir")
        assert all("subdir" in r["file"] for r in results)

    def test_list_recent_notes_no_old_results(self, vault):
        """days=0 表示只返回"此刻之后"修改的文件，用于验证不会崩溃。"""
        results = vault.list_recent_notes(days=0)
        assert isinstance(results, list)

    def test_list_recent_notes_max_20(self, vault_dir):
        """创建 25 个文件，结果应被截断至最多 20 条。"""
        for i in range(25):
            (vault_dir / f"bulk_{i}.md").write_text(f"Bulk note {i}")
        vault = ObsidianVault(str(vault_dir))
        results = vault.list_recent_notes(days=7)
        assert len(results) <= 20


class TestToolDefinitions:
    """TOOLS 字典测试 — 验证 FastMCP 兼容的工具 schema 定义是否完整。

    TOOLS 字典定义了 MCP 协议暴露给 Agent 的 3 个工具：
    search_notes / get_daily_note / list_recent_notes
    每个工具需要有 description 和 inputSchema（含 properties）。
    """

    def test_tools_dict_has_all_tools(self):
        """TOOLS 应包含全部 3 个工具名。"""
        assert "search_notes" in TOOLS
        assert "get_daily_note" in TOOLS
        assert "list_recent_notes" in TOOLS

    def test_tools_have_required_fields(self):
        """每个工具定义应包含 description 和 inputSchema.properties。"""
        for name, tool in TOOLS.items():
            assert "description" in tool
            assert "inputSchema" in tool
            assert "properties" in tool["inputSchema"]

    def test_search_notes_schema_requires_query(self):
        """search_notes 的 required 字段应包含 "query"。"""
        schema = TOOLS["search_notes"]["inputSchema"]
        assert "query" in schema["required"]
