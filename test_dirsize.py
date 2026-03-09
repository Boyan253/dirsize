import dirsize


def test_human_readable_units():
    assert dirsize.human(512) == "512 B"
    assert dirsize.human(2048) == "2.0 KB"
    assert dirsize.human(5 * 1024 ** 3) == "5.0 GB"

def test_parse_size_round_trip():
    assert dirsize.parse_size("10MB") == 10 * 1024 ** 2
    assert dirsize.parse_size("1.5GB") == int(1.5 * 1024 ** 3)
    assert dirsize.parse_size("0") == 0


def test_top_sorts_descending():
    sizes = {"a": 1, "b": 30, "c": 2}
    assert [p for p, _ in dirsize.top(sizes, 2)] == ["b", "c"]

def test_top_respects_minimum():
    sizes = {"a": 1, "b": 30}
    assert dirsize.top(sizes, 10, min_bytes=5) == [("b", 30)]


def test_scan_counts_files(tmp_path):
    (tmp_path / "one.txt").write_text("hello", encoding="utf-8")
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "two.txt").write_text("world!", encoding="utf-8")
    files, dirs = dirsize.scan(str(tmp_path))
    assert len(files) == 2
    assert dirs[str(tmp_path)] == 11
