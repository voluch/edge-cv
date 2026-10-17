from ecv_common import Detection, FrameRecord, Track, read_jsonl, write_jsonl


def make_record() -> FrameRecord:
    return FrameRecord(
        1234,
        1739000000123456789,
        [Detection("car", 0.91, (412, 233, 520, 301))],
        [Track(17, "car", (410, 231, 519, 300), (12.4, 3.1), 34.2)],
    )


def test_roundtrip_line():
    r = make_record()
    assert FrameRecord.from_json(r.to_json()) == r


def test_roundtrip_file(tmp_path):
    p = tmp_path / "x.jsonl"
    write_jsonl(p, [make_record(), FrameRecord(1235, 1)])
    out = list(read_jsonl(p))
    assert len(out) == 2 and out[0] == make_record() and out[1].dets == []


def test_optional_track_fields_omitted():
    t = Track(1, "cat", (0, 0, 1, 1))
    assert "speed_kmh" not in t.to_dict() and "ground_xy_m" not in t.to_dict()


def test_matches_documented_format():
    line = make_record().to_json()
    assert line.startswith('{"frame":1234,"t_ns":1739000000123456789,"dets":[{"cls":"car"')
