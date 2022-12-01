# Super OrgContact

This is the backend application of the Super OrgContact project.

Access to frontend: [Super OrgContact frontend](https://mcoelho-people.web.app).

It uses MongoDB Atlas database. Please, follow the **.env_sample** file.

You will need a **web application credentials (JSON file)** from a project at Goodle Could Platform GCP. Once you get it, just insert in your **.env** file.

## Project setup
```
poetry config --local virtualenvs.in-project true
```
```
poetry install
```

### Compiles and hot-reloads for development
```
poetry run flask run
```

