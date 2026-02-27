# ECU Release Pipeline Makefile
# Targets: lint, test, build, release-check, release

PYTHON   ?= python3
ECU_ID   ?= ECU
DIST_DIR  = dist

.PHONY: all lint test build release-check release clean

all: lint test build

# ---------------------------------------------------------------------------
# Lint (reuse project-wide pytest + pylint if available, else no-op)
# ---------------------------------------------------------------------------
lint:
	@echo "[lint] Running pylint on ecu_pipeline.py..."
	$(PYTHON) -m pylint --score=no ecu_pipeline.py || true

# ---------------------------------------------------------------------------
# Unit tests
# ---------------------------------------------------------------------------
test:
	@echo "[test] Running unit tests..."
	$(PYTHON) -m pytest test_ecu_pipeline.py -v

# ---------------------------------------------------------------------------
# Build – create a placeholder binary in dist/
# ---------------------------------------------------------------------------
build: release-check
	@echo "[build] Creating artifact..."
	@mkdir -p $(DIST_DIR)
	@VERSION=$$($(PYTHON) ecu_pipeline.py version) && \
	 ARTIFACT=$$($(PYTHON) ecu_pipeline.py artifact-name $(ECU_ID)) && \
	 echo "ECU software $$VERSION built at $$(date -u +%Y-%m-%dT%H:%M:%SZ)" > $(DIST_DIR)/$$ARTIFACT && \
	 echo "[build] Artifact: $(DIST_DIR)/$$ARTIFACT"

# ---------------------------------------------------------------------------
# Release readiness check
# ---------------------------------------------------------------------------
release-check:
	@echo "[check] Verifying release readiness..."
	$(PYTHON) ecu_pipeline.py check

# ---------------------------------------------------------------------------
# Release – tag and archive dist/
# ---------------------------------------------------------------------------
release: build
	@echo "[release] Packaging artifacts..."
	@VERSION=$$($(PYTHON) ecu_pipeline.py version) && \
	 tar -czf $(DIST_DIR)/$(ECU_ID)_$$VERSION.tar.gz -C $(DIST_DIR) . && \
	 echo "[release] Archive: $(DIST_DIR)/$(ECU_ID)_$$VERSION.tar.gz"

# ---------------------------------------------------------------------------
# Clean
# ---------------------------------------------------------------------------
clean:
	rm -rf $(DIST_DIR) __pycache__ .pytest_cache
