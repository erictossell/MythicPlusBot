# Builder stage
FROM python:3.11-slim as builder
WORKDIR /usr/src/app
RUN pip install poetry
COPY pyproject.toml poetry.lock* ./
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /usr/src/app
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*
COPY . .
CMD ["python", "-m", "bot"]
