FROM python:3.10.0-slim-buster

ENV POETRY_VERSION=1.8.3

# Install Poetry
RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

COPY . /app

WORKDIR /app

RUN poetry install 

EXPOSE 5000

# COPY start.sh /app/start.sh

RUN chmod +x /app/start.sh

CMD ["./start.sh"]
