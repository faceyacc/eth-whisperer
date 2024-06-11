FROM python:3.10.3-slim-buster

# install poetry
RUN pip install poetry

WORKDIR /app

# copy trade_producer to container
COPY . /app

# install poetry dependencies
RUN poetry install

# run trade_producer
CMD ["poetry", "run", "python", "src/main.py"]
