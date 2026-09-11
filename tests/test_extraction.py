from pathlib import Path

import pytest

from app.providers.document_extractors.extractors import ExtractionError, get_extractor


def test_txt_extractor_reads_content(tmp_path):
    p = tmp_path / "sample.txt"
    p.write_text("Hello DocuMind")
    result = get_extractor("txt").extract(p)
    assert result == [(None, "Hello DocuMind")]


def test_txt_extractor_rejects_empty_file(tmp_path):
    p = tmp_path / "empty.txt"
    p.write_text("")
    with pytest.raises(ExtractionError):
        get_extractor("txt").extract(p)


def test_md_uses_plain_text_extractor(tmp_path):
    p = tmp_path / "sample.md"
    p.write_text("# Title\n\nBody text")
    result = get_extractor("md").extract(p)
    assert "Title" in result[0][1]


def test_unsupported_extension_raises():
    with pytest.raises(ExtractionError):
        get_extractor("exe")
