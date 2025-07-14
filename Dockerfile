# 🧱 Builder stage
FROM python:3.13-slim

ENV POETRY_VERSION=1.8.2
ENV PATH="/root/.local/bin:$PATH"

# Установим system-зависимости
RUN apt-get update && apt-get install -y curl build-essential

# Установим Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

COPY . .

RUN poetry install --no-root

RUN chmod +x start.sh

CMD ["./start.sh"]