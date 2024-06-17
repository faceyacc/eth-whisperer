FROM python:3.10.3-slim-buster

# install poetry
RUN pip install poetry==1.8.3

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

# install poetry dependencies
RUN poetry install

# copy trade_producer to container
COPY . /app

# set PYTHONPATH to include the src directory
ENV PYTHONPATH="${PYTHONPATH}:/app/src"

# run trade_producer
CMD ["poetry", "run", "python", "src/main.py"]
