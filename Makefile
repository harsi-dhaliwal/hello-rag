# ---- config ---------------------------------------------------------------
PIP_COMPILE ?= pip-compile
PIP_SYNC    ?= pip-sync

PROD_IN     ?= requirements.in
DEV_IN      ?= requirements-dev.in
PROD_LOCK   ?= requirements.txt
DEV_LOCK    ?= requirements-dev.txt

# Set HASHES=--generate-hashes to produce hashed lock files
HASHES      ?= --generate-hashes
UNSAFE 		?= --allow-unsafe
# ---- rules ----------------------------------------------------------------
.PHONY: install lock sync upgrade upgrade-pkg help

# Rebuild lockfiles only if inputs changed
$(PROD_LOCK): $(PROD_IN)
	$(PIP_COMPILE) $(HASHES) $(UNSAFE) $< -o $@

# Dev is constrained by prod; rebuild when either changes
$(DEV_LOCK): $(DEV_IN) $(PROD_LOCK)
	$(PIP_COMPILE) $(HASHES) $(UNSAFE) $< -o $@

# Compile lock files (no install)
lock: $(PROD_LOCK) $(DEV_LOCK)

# Install exactly the pinned versions (compile first if needed)
install: lock
	$(PIP_SYNC) $(PROD_LOCK) $(DEV_LOCK)

# Sync without compiling (assumes locks are up to date)
sync:
	$(PIP_SYNC) $(PROD_LOCK) $(DEV_LOCK)

# Upgrade everything to latest compatible versions, then install
upgrade:
	$(PIP_COMPILE) $(HASHES) --upgrade $(PROD_IN) -o $(PROD_LOCK)
	$(PIP_COMPILE) $(HASHES) --upgrade $(DEV_IN)  -o $(DEV_LOCK)
	$(MAKE) sync

# Upgrade just one package: make upgrade-pkg PKG=openai
upgrade-pkg:
	@test -n "$(PKG)" || (echo "Usage: make upgrade-pkg PKG=<name>"; exit 2)
	$(PIP_COMPILE) $(HASHES) --upgrade-package $(PKG) $(PROD_IN) -o $(PROD_LOCK)
	$(PIP_COMPILE) $(HASHES) $(DEV_IN) -o $(DEV_LOCK)
	$(MAKE) sync

help:
	@echo "Targets:"
	@echo "  install       Compile locks (if needed) and pip-sync"
	@echo "  lock          Compile requirements.txt and requirements-dev.txt"
	@echo "  sync          pip-sync exactly to lock files"
	@echo "  upgrade       Re-lock everything to latest compatible versions"
	@echo "  upgrade-pkg   Upgrade a single package (PKG=name)"
	@echo "Hints: use HASHES=--generate-hashes to produce hash-pinned locks"
