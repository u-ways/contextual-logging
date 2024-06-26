################################################################################################
# Project Makefile
#
# This Makefile is split into three sections:
#   - Application: for building, testing, and publishing the project.
#   - Development: for formatting, linting, and other development tasks.
#   - Docker: for building, running, and publishing Docker images.
#
# We write our rule names in the following format: [verb]-[noun]-[noun], e.g. "build-app".
#
# Variables ####################################################################################

APP_VERSION?=DEV-SNAPSHOT
APP_NAME?=contextual-logging

PROJECT_ROOT:=$(CURDIR)

IMAGE_ID?=$(APP_NAME):$(APP_VERSION)

# PHONY #########################################################################################
#
# The .PHONY directive in a Makefile is used to declare phony targets. A phony target is one
# that is not associated with a file. It's a way of telling make that the target is not a real
# file, but a name for a recipe to be executed.
#
# Without .PHONY, if a file with the same name as the recipe/target is created in the directory,
# make will not execute the recipe because it sees that a file with that name already exists and
# is therefore 'up to date'.
#
# Therefore, please append .PHONY for all targets that are not associated with a file.

.PHONY: setup-project clean-app test-app require-poetry install-poetry install-dependencies update-dependencies lock-dependencies format-code lint-code check-format check-lint check-code-quality require-docker test-app-docker check-format-docker check-lint-docker enable-code-quality-pre-commit-hook

# Application ##################################################################################

clean-app: require-poetry
	@echo "Cleaning application (e.g. cache, build files)..."
	@poetry run pyclean -v $(PROJECT_ROOT)/src $(PROJECT_ROOT)/tests

test-app: install-dependencies
	@echo "Testing application..."
	@poetry run pytest -v $(PROJECT_ROOT)/tests

# Development ##################################################################################

setup-project: require-poetry install-dependencies enable-code-quality-pre-commit-hook
	@echo "Setting up your IDE..."
	@mkdir -p $(PROJECT_ROOT)/.idea
	@cp $(PROJECT_ROOT)/.ide/contextual-logging.iml $(PROJECT_ROOT)/.idea/contextual-logging.iml
	@mkdir -p $(PROJECT_ROOT)/.vscode
	@cp $(PROJECT_ROOT)/.ide/settings.json $(PROJECT_ROOT)/.vscode/settings.json

require-poetry:
	@echo "Checking for Poetry..."
	@command -v poetry >/dev/null 2>&1 || (echo "Poetry is required. Please install via 'make install-poetry'." && exit 1)

install-poetry:
	@echo "Installing Poetry..."
	@curl -sSL https://install.python-poetry.org | python3 -

install-dependencies: require-poetry
	@echo "Installing dependencies..."
	@poetry --directory=$(PROJECT_ROOT) install

update-dependencies: require-poetry
	@echo "Updating dependencies..."
	@poetry --directory=$(PROJECT_ROOT) update

lock-dependencies: require-poetry
	@echo "Locking dependencies..."
	@poetry --directory=$(PROJECT_ROOT) lock

format-code: require-poetry
	@echo "Formatting application..."
	@poetry run black $(PROJECT_ROOT)/src $(PROJECT_ROOT)/tests

lint-code: require-poetry
	@echo "Linting application..."
	@poetry run flake8 $(PROJECT_ROOT)/src $(PROJECT_ROOT)/tests

check-format: require-poetry
	@echo "Checking application formatting..."
	@poetry run black --check $(PROJECT_ROOT)/src $(PROJECT_ROOT)/tests

check-lint: require-poetry
	@echo "Checking application linting..."
	@poetry run flake8 --show-source --statistics --count $(PROJECT_ROOT)/src $(PROJECT_ROOT)/tests

check-code-quality: check-format check-lint

enable-code-quality-pre-commit-hook:
	@echo "Enabling pre-commit hook..."
	@ln -sf $(PROJECT_ROOT)/.hooks/pre-commit $(PROJECT_ROOT)/.git/hooks/pre-commit

# Docker #######################################################################################

require-docker:
	@echo "Checking for Docker..."
	@command -v docker >/dev/null 2>&1 || (echo "Docker is required. Please install via 'make install-docker'." && exit 1)

test-app-docker: require-docker
	@echo "Testing application... (Containerised)"
	@$(call build_docker_image,development)
	@$(call run_docker_dev_mount,poetry run pytest -v /app/tests)

check-format-docker: require-docker
	@echo "Checking application formatting... (Containerised)"
	@$(call build_docker_image,development)
	@$(call run_docker_dev_mount,poetry run black --check /app/src /app/tests)

check-lint-docker: require-docker
	@echo "Checking application linting... (Containerised)"
	@$(call build_docker_image,development)
	@$(call run_docker_dev_mount,poetry run flake8 --show-source --statistics --count /app/src /app/tests)

# Functions ####################################################################################

define build_docker_image
	@echo "Building Docker image for target: $(1)"
	@docker build --target $(1) --build-arg APP_VERSION=$(APP_VERSION) --build-arg APP_NAME=$(APP_NAME) -t $(IMAGE_ID) .
endef

define run_docker_dev_mount
	@docker run $(2) \
		-v $(PROJECT_ROOT)/src:/app/src \
		-v $(PROJECT_ROOT)/tests:/app/tests \
		-v $(PROJECT_ROOT)/pyproject.toml:/app/pyproject.toml \
		-v $(PROJECT_ROOT)/poetry.lock:/app/poetry.lock \
		--rm --name $(APP_NAME)-toolchain-dev $(IMAGE_ID) $(1)
endef

# IDE ##########################################################################################

