# Super OrgContact

## Description

This is the backend application of the Super OrgContact project.

It is running on Google Cloud Run [Backend URL](https://superorgcontact-3fufpf5spq-rj.a.run.app), and you can get access by the frontend on firebase. 

Access to frontend: [Super OrgContact frontend](https://superorgcontactfirebase.web.app/).

**Important** Unfortunatelly, it is not possible to get access right now, because of app verification issues. But it will be fixed soon!

For running locally, please follow this instructions:

It uses **MongoDB Atlas** database. Please, follow the **.env_sample** file.

You will need:
- Create a database at MongoDB Atlas and insert the MONGO_URI and database name in **.env**;
- an **installed application credentials (JSON file)** from a project at Goodle Could Platform GCP;
- Enable **People Api**;
- Once you get it, just insert in your **.env** file, just like the .env_sample.

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

