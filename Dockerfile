FROM python:3.11-bookworm as builder

ENV PIP_ROOT_USER_ACTION=ignore
ENV BUILD_DIR=/opt/build
ENV TZ=UTC

# Upgrate pip
RUN pip install --upgrade pip

# Copy files and dirictory
COPY fastid $BUILD_DIR/fastid
COPY *.md $BUILD_DIR/
COPY LICENSE $BUILD_DIR/
COPY pyproject.toml $BUILD_DIR/
COPY alembic.ini $BUILD_DIR/
COPY migrations $BUILD_DIR/migrations

WORKDIR $BUILD_DIR/

RUN pip install poetry
RUN poetry config virtualenvs.create false --local
RUN poetry build

FROM python:3.11-bookworm

ENV PIP_ROOT_USER_ACTION=ignore
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV BUILD_DIR=/opt/build
ENV TZ=UTC

LABEL org.opencontainers.image.source=https://github.com/fastid/fastid
LABEL org.opencontainers.image.description="FastID"
LABEL org.opencontainers.image.licenses=MIT

COPY --from=builder $BUILD_DIR/dist/*.tar.gz $BUILD_DIR/

RUN pip install $BUILD_DIR/*.tar.gz
RUN rm -rf $BUILD_DIR

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD curl -f http://localhost:8585/healthcheck/ || exit 1

# Change workdir
WORKDIR /usr/local/lib/python3.12/site-packages

# Change user
USER www-data

# Ports
EXPOSE 8585/tcp

ENTRYPOINT ["uvicorn", "--no-date-header", "--no-server-header", "--no-access-log", "--log-level=error", "--host=0.0.0.0", "--port=8585", "fastid.app:app"]
