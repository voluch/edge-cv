# Top-level task runner. Each task folder provides its own Makefile with
# setup / test / lint targets; folders without a Makefile are skipped.
FOLDERS := common rig-calib street-detector tracker edge-runtime pan-tilt \
           robustness gnss-free-nav thermal cat-deterrent
ACTIVE  := $(strip $(foreach d,$(FOLDERS),$(if $(wildcard $(d)/Makefile),$(d))))

.PHONY: setup test lint $(ACTIVE)

setup test lint:
	@if [ -z "$(ACTIVE)" ]; then echo "no task folders with a Makefile yet"; fi
	@for d in $(ACTIVE); do echo "==> $$d: $@"; $(MAKE) -C $$d $@ || exit 1; done
