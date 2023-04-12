# syntax = docker/dockerfile:1
# This Dockerfile uses multi-stage build to customize DEV and PROD images:
# https://docs.docker.com/develop/develop-images/multistage-build/

FROM python:3.10.10-slim-bullseye AS base_build

LABEL maintainer="stevenengland"
LABEL vendor="stevenengland"

# `DJANGO_ENV` arg is used to make prod / dev builds:
ARG DJANGO_ENV \
  # Needed for fixing permissions of files created by Docker:
  UID=1000 \
  GID=1000


ENV DJANGO_ENV=${DJANGO_ENV} \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  # pip:
  PIP_NO_CACHE_DIR=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=1 \
  PIP_DEFAULT_TIMEOUT=100 \
  PIP_ROOT_USER_ACTION=ignore

SHELL ["/bin/bash", "-eo", "pipefail", "-c"]

WORKDIR /photogrepo

RUN groupadd -g "${GID}" -r photogrepo && \
    useradd -d '/photogrepo' -g photogrepo -l -r -u "${UID}" photogrepo && \
    chown photogrepo:photogrepo -R '/photogrepo'

COPY --chown=photogrepo:photogrepo ./app/ ./app/
COPY --chown=photogrepo:photogrepo ./config/ ./config/
COPY --chown=photogrepo:photogrepo ./requirements/ ./requirements/
COPY --chown=photogrepo:photogrepo ./scripts/ ./scripts/

COPY [ \
  "manage.py", \
  "./" \
]

# System deps (we don't use exact versions because it is hard to update them,
# pin when needed):
# hadolint ignore=DL3008
RUN \
    apt-get update && apt-get upgrade -y && \
    apt-get install --no-install-recommends -y \
      bash \
      curl \
      postgresql-client \
      tini \
      wait-for-it && \
    tini --version && \
# Python deps
    python -m venv ./.venv && \
    ./.venv/bin/pip install --upgrade pip && \
    ./.venv/bin/pip install -r ./requirements/base.txt && \
    if [ "$DJANGO_ENV" != "production" ]; \
        then ./.venv/bin/pip install -r ./requirements/dev.txt ; \
    fi && \
# Cleaning cache:
    apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false && \
    apt-get clean -y && rm -rf /var/lib/apt/lists/* \
# Permissions & mods
    chmod -R +x ./scripts

# This is a special case. We need to run this script as an entry point:
COPY ./docker/entrypoint.sh ./docker-entrypoint.sh

# Setting up proper permissions:
RUN chmod +x './docker-entrypoint.sh' \
  # Replacing line separator CRLF with LF for Windows users:
  && sed -i 's/\r$//g' './docker-entrypoint.sh'

# Extend the PATH
ENV PATH="/photogrepo/scripts:/photogrepo/.venv/bin:$PATH"

# Running as non-root user:
USER photogrepo

# We customize how our app is loaded with the custom entrypoint:
CMD ["/usr/bin/tini", "--", "./docker-entrypoint.sh"]

# Test build stage
FROM base_build as development_build

WORKDIR /photogrepo

# Pure testing dependencies
COPY --chown=photogrepo:photogrepo ./tests/ ./tests/
COPY [ \
  "setup.cfg", \
  ".yamllint.yml", \
  "pyproject.toml", \
  "./" \
]

# Additional check dependencies (e.g. to be able to lint all files in repo)
COPY --chown=photogrepo:photogrepo ./.github/ ./.github/
COPY --chown=photogrepo:photogrepo ./docker/ ./docker/
COPY --chown=photogrepo:photogrepo ./docs/ ./docs/
COPY --chown=photogrepo:photogrepo ./tools/ ./tools/
COPY [ \
  ".pre-commit-config.yaml", \
  "docker-compose*", \
  "./" \
]
