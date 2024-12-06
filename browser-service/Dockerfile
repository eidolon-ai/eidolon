FROM python:3.11-slim AS builder
RUN pip install poetry
COPY poetry.lock pyproject.toml ./
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --without dev --extras server
COPY eidolon_browser_service/ eidolon_browser_service/
COPY README.md ./
RUN poetry build


FROM python:3.11-slim

WORKDIR /app
ENV PLAYWRIGHT_BROWSERS_PATH=/opt/playwright
COPY --from=builder requirements.txt .
RUN pip install -r requirements.txt
RUN playwright install --with-deps chromium
COPY --from=builder dist/*.whl /tmp/eidolon_ai_sdk/
RUN pip install /tmp/eidolon_ai_sdk/*.whl --no-cache --no-deps

# Create non-root user
RUN addgroup --system --gid 1001 eidolon && adduser --system --uid 1001 --ingroup eidolon eidolon
RUN chown -R eidolon:eidolon /app
USER eidolon

ENV PYTHONUNBUFFERED=1

EXPOSE 7468
CMD ["uvicorn", "eidolon_browser_service.main:app", "--host", "0.0.0.0", "--port", "7468"]
