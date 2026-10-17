# Top-level task runner. Each task folder provides its own Makefile with
# setup / test / lint targets; folders without a Makefile are skipped.
FOLDERS := common rig-calib street-detector tracker edge-runtime pan-tilt \
           robustness gnss-free-nav thermal cat-deterrent
ACTIVE  := $(strip $(foreach d,$(FOLDERS),$(if $(wildcard $(d)/Makefile),$(d))))

.PHONY: env setup test lint test-hooks $(ACTIVE)

# Python environment: uv venv at .venv with the shared package and dev tools
env:
	uv venv --python 3.12 --allow-existing
	uv pip install -e "common/[dev]"

test-hooks:
	python -m pytest -q .claude/hooks/tests

setup test lint:
	@if [ -z "$(ACTIVE)" ]; then echo "no task folders with a Makefile yet"; fi
	@for d in $(ACTIVE); do echo "==> $$d: $@"; $(MAKE) -C $$d $@ || exit 1; done
	@if [ "$@" = "test" ]; then $(MAKE) test-hooks; fi
