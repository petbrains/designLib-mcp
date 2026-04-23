FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY src/ ./src/

RUN pip install --no-cache-dir -e .

ENV PORT=8000 \
    DESIGNLIB_TRANSPORT=http \
    PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["designlib-mcp"]
