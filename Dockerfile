# syntax=docker/dockerfile:1

FROM python:3.12-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:0.10.12 /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-install-project

COPY src ./src
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-editable \
    && groupadd --system app \
    && useradd --system --gid app --create-home --home-dir /home/app app

USER app

CMD ["starter-app"]
