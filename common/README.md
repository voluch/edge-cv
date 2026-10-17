# common/

Shared code used by every task folder: a Python package (`ecv_common`) and a C++17 CMake library (`ecv::common`).

| Module | Python | C++ | Status |
|---|---|---|---|
| `types` | ✓ | ✓ | `Detection`, `Track`, `FrameRecord`; JSON Lines |
| `geometry` | ✓ | ✓ | `Homography` (pixel ↔ ground), OpenCV YAML load/save (Python); undistortion is a stub |
| `metrics` | ✓ | | latency percentiles done; mAP and HOTA/IDF1 are stubs |
| `bench` | ✓ | ✓ | result record, JSONL append, Markdown table (Python) |
| `logging` | ✓ | | JSON log formatter |
| `io.camera`, `io.recorder` | ✓ | | interfaces and a video-file source; Pi camera is a stub |
| `privacy` | ✓ | | stub (face and plate blurring) |

## Use

```bash
# Python (from the repo root)
pip install -e "common/[dev]"
make -C common test

# C++ (from a task folder's CMakeLists.txt)
add_subdirectory(${CMAKE_SOURCE_DIR}/../common common)   # adjust the path
target_link_libraries(my_target PRIVATE ecv::common)
```

## Data format (JSON Lines, one record per frame)

```json
{"frame": 1234, "t_ns": 1739000000123456789, "dets": [{"cls": "car", "score": 0.91, "xyxy": [412, 233, 520, 301]}],
 "tracks": [{"id": 17, "cls": "car", "xyxy": [410, 231, 519, 300], "ground_xy_m": [12.4, 3.1], "speed_kmh": 34.2}]}
```

Changing this format means updating Python, C++ and all users in one commit.
