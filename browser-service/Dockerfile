FROM python:3.11-slim AS builder
RUN pip install poetry
COPY pyproject.toml pyproject.toml
COPY eidolon_browser_service/ browser_service/
COPY README.md README.md
RUN poetry build

FROM python:3.11-slim
RUN mkdir dist

# Install playwright since it should be static
ENV PLAYWRIGHT_BROWSERS_PATH=/opt/playwright
COPY poetry.lock dist/poetry.lock

# we could just do playwright first, then install everything afterwards for a more optimal layering
RUN pip install -r dist/poetry.lock
RUN playwright install --with-deps chromium

# Then install poetry project wheel since it will change more frequently
COPY --from=builder dist/*.whl /dist/
RUN pip install /dist/*.whl --no-cache --no-deps

WORKDIR /app
RUN addgroup --system --gid 1001 eidolon && adduser --system --uid 1001 --ingroup eidolon eidolon
USER eidolon
EXPOSE 7468
ENV PYTHONUNBUFFERED=1
#ENTRYPOINT ["fastapi", "run", "eidolon_browser_service", "--port", 7468] todo this is wrong entrypoint for sure
