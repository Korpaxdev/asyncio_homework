FROM python:alpine

ENV PYTHONUNBUFFERED = 1
ENV PYTHONDONTWRITEBYCODE = 1

WORKDIR /app

COPY poetry.lock pyproject.toml ./
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction

COPY . .

CMD python main.py