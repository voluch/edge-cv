BUILD := build

.PHONY: setup test lint test-py test-cpp

setup:
	pip install -e ".[dev]"

test: test-py test-cpp

test-py:
	python -m pytest -q

# Uses CMake when available, otherwise a plain g++ build (Pi and CI have CMake).
test-cpp:
	@if command -v cmake >/dev/null 2>&1; then \
	  cmake -S . -B $(BUILD) -DCMAKE_BUILD_TYPE=Release && cmake --build $(BUILD) -j && ctest --test-dir $(BUILD) --output-on-failure; \
	else \
	  mkdir -p $(BUILD) && g++ -std=c++17 -Wall -Wextra -Iinclude src_cpp/*.cpp tests_cpp/test_common.cpp -o $(BUILD)/test_common && $(BUILD)/test_common; \
	fi

lint:
	ruff check src tests
