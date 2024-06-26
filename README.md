# Contextual Logging

[![CICD](https://github.com/u-ways/contextual-logging/actions/workflows/CICD.yml/badge.svg)](https://github.com/u-ways/contextual-logging/actions/workflows/CICD.yml)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Python: 3.12](https://img.shields.io/badge/python-3.12-008be1.svg)](https://www.python.org/downloads/release/python-3110/)
[![Linter: Flake8](https://img.shields.io/badge/linter-Flake8-008be1.svg)](https://flake8.pycqa.org/en/latest/)
[![Style: Black](https://img.shields.io/badge/style-Black-000.svg)](https://github.com/psf/black)

A logging interface to address your observability requirements.

## Background

Contextual Logging is a Python package that provides you with much-needed flexibility and control over your logs. It
allows you to attach contextual information to your logs, so you can easily trace and debug issues in your application.

The key features are:

- **Global Context**: Attach log attributes to all logger calls regardless of the logger instance.
- **Local Context**: Attach log attributes to a specific logger instance.
- **YAML Support**: Configure your loggers (including standard Python loggers) using a YAML file.
- **JSON Formatter**: Format your logs in JSON for easy parsing and analysis.
- **Transit log processing**: Process log attribute at the global level during transit before they are written to the
  log handler to further breakdown the log data.

## Contributing

If you have any suggestions or improvements, feel free to open a PR or an issue. The build and development process has
been made to be as seamless as possible, so you can easily run and test your changes locally before submitting a PR.

We ask for adequate test coverage and adherence to the project's code quality standards. This includes running the
tests, formatter, and linter before submitting a PR. You can run the following command to ensure your changes are in
line with the project standards:

```bash
make check-code-quality
```

### Prerequisites

- [Python](https://www.python.org/downloads/): The project is built with Python 3.12.
- [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer): The dependency management tool of
  choice for this project.
- [Docker](https://docs.docker.com/engine/install/): For containerisation support, so it can be completely built and run
  in an isolated environment.
- [Make](https://www.gnu.org/software/make/): For running common tasks such as installing dependencies, building the
  project, running tests, etc.

### Environment Setup

Before opening the project in your IDE, I highly recommend running the following recipe:

```shell
make setup-project
```

This will create your Poetry's virtual environment, install the project's dependencies, set up the code quality
pre-commit hook, and configure your IDE (VSCode and PyCharm) as appropriate.

### Code Quality

The project is configured with a set of tools to ensure code quality. You can run the following commands to check for

- Linting issues:

    ```bash
    make check-lint
    ```

- Formatting issues:

    ```bash
    make check-format
    ```

You can also setup your IDE to use Black as the code formatter:

- Visual Studio Code: [Formatter extension for Visual Studio Code using the Black formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)
- PyCharm: [Reformat Python code with Black](https://www.jetbrains.com/help/pycharm/reformat-and-rearrange-code.html#format-python-code-with-black)

On top of that, you can enable a code quality pre-commit hook:

```bash
make enable-code-quality-pre-commit-hook
```

This will ensure that the code quality checks are run before every commit.

### Containerisation Support (Docker)

You can also run the project using Docker. Our Dockerfile is a multi-stage build based on the official slimmed down
Python image. It's divided into the following stages:

| Layer | Name         | Description                                                                                                                                |
|-------|--------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| 1     | PYTHON-BASE  | Configures the base image environment variables.                                                                                           |
| 2     | BUILDER-BASE | Installs Poetry, and then loads the project dependencies with caching enabled.                                                             |
| 3     | DEVELOPMENT  | Relies on the `BUILDER-BASE` to pull in the dependencies, as such this layer focus on testing and running the project in development mode. |

This enables you to build and run the project in an isolated environment with all the dependencies and configurations
bundled together without diverging image builds when you switch between development and production environments.

Here are some commands to get you started:

```bash
make test-app-docker
```

To check for code quality issues:

```bash
make check-format-docker
make check-lint-docker
```

___