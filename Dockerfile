
# # Use the official lightweight Python image.
# # https://hub.docker.com/_/python
# COPY . /src/app
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1
# ENV POETRY_VERSION 1.0
# RUN pip install "poetry==$POETRY_VERSION"
# WORKDIR /app
# COPY poetry.lock /app
# COPY pyproject.toml /app
# RUN poetry config virtualenvs.create false \
# && poetry install --no-interaction --no-ansi
# COPY . .
# CMD gunicorn --bind 0.0.0.0:5000 app:app
# FROM python:3.10-slim

# # ENV FLASK_APP=app.py
# # ENV FLASK_ENV=development
# # ENV FLASK_DEBUG=True
# # ENV FLASK_RUN_HOST=0.0.0.0
# # ENV FLASK_RUN_PORT=8080
# # ENV SECRET_KEY=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
# # ENV OAUTHLIB_INSECURE_TRANSPORT=1
# # ENV FRONTEND_URL=https://mcoelho-people.web.app
# # ENV BACKEND_URL=https://mcoelho-people-w5u4ladcda-uc.a.run.app/
# # ENV PORT=8080
# ENV APP_HOME /app
# WORKDIR $APP_HOME
# COPY poetry.lock /app
# COPY pyproject.toml /app
# COPY requirements.txt requirements.txt
# RUN pip3 install -r requirements.txt
# RUN poetry config virtualenvs.create false \
# && poetry install --no-interaction --no-ansi
# # RUN pip3 install gunicorn
# COPY . .
# EXPOSE 8080
# # RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
# # USER appuser

# # CMD [ "python3", "app.py" ]
# CMD [ "poetry", "run", "flask", "run", "--host=0.0.0.0" ]

FROM python:3.10-slim
# COPY . /src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# ENV POETRY_VERSION 1
# RUN pip3 install "poetry==$POETRY_VERSION"
# RUN pip3 install gunicorn
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY poetry.lock /app
COPY pyproject.toml /app
RUN poetry config virtualenvs.create false \
&& poetry install --no-interaction --no-ansi
COPY . .
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
