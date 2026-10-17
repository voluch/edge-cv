# common/

Shared library (Python `ecv_common` + C++ `ecv::common`). Every other folder depends on it, so changes here are cross-cutting.

## Commands
- Setup: `make setup` (editable install with dev extras)
- Tests: `make test` (pytest + C++ test)
- Lint: `make lint`

## Layout
- `src/ecv_common/` Python modules; `tests/` pytest
- `include/ecv/common/`, `src_cpp/`, `tests_cpp/` C++ library and test
- `CMakeLists.txt` exposes target `ecv::common`

## Local conventions
- The JSON Lines format must stay identical in Python and C++. Change both, plus tests, plus users in other folders, in one commit.
- Python depends on numpy only; OpenCV is an optional extra (`video`). Import it lazily.
- Stubs raise `NotImplementedError` with a clear message; do not return fake values.
- Do not add dependencies without approval.

## Definition of done
- `pip install -e common/` works on laptop, Colab and Pi; C++ builds with CMake on the Pi.
- Unit tests for geometry (pixel → ground → pixel round trip), serialization and metrics.
