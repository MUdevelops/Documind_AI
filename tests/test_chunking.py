from app.utils.chunking import chunk_pages


def test_chunk_pages_respects_size_and_overlap():
    text = "A" * 2000
    chunks = chunk_pages([(1, text)], chunk_size=800, overlap=150)
    assert len(chunks) >= 2
    assert all(len(c.text) <= 800 for c in chunks)
    assert chunks[0].page_number == 1


def test_chunk_pages_skips_empty_pages():
    chunks = chunk_pages([(1, "   "), (2, "real content here")], chunk_size=800, overlap=150)
    assert len(chunks) == 1
    assert chunks[0].page_number == 2


def test_chunk_pages_indexes_sequentially():
    chunks = chunk_pages([(1, "x" * 1000), (2, "y" * 1000)], chunk_size=400, overlap=50)
    indices = [c.index for c in chunks]
    assert indices == list(range(len(chunks)))
