FROM python:3.11

RUN addgroup --system app && adduser --system --group app

WORKDIR /app/

RUN apt-get update && apt-get -y upgrade

COPY ./pyproject.toml ./poetry.lock* /app/

RUN chown -R app:app /app/

RUN pip install --upgrade pip && pip install poetry
RUN poetry config virtualenvs.create false

ARG INSTALL_DEV=true

RUN bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --only main ; fi"

COPY . /app

USER app

CMD uvicorn main:app --host 0.0.0.0 --port 80
