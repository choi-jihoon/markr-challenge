# markr-challenge

## Run Locally

1. Create a PostgreSQL user and database.

```psql -c "CREATE USER <psql_user> PASSWORD '<password>' CREATEDB;"```

```psql -c "CREATE DATABASE <database> OWNER <psql_user>;"```

2. Create a .env file.

```SECRET_KEY=<your_secret_key>```
```DATABASE_URL=postgresql://<psql_user>:<password>@localhost/<database>```

3. Install dependencies.

```pipenv install```

4. Initialize the database.

```python init_db.py```

5. ```pipenv shell```
6. ```flask run```

## Run on Docker

1. Create a PostgreSQL user and database.

```psql -c "CREATE USER <psql_user> PASSWORD '<password>' CREATEDB;"```

```psql -c "CREATE DATABASE <database> OWNER <psql_user>;"```

2. Create a .env file.

```SECRET_KEY=<your_secret_key>```
```DATABASE_URL_PRODUCTION=postgresql://<psql_user>:<password>@db:5432/<database>```
```POSTGRES_PASSWORD=<password>```

3. Build and run on Docker

```docker compose up```

4. Example POST

```
curl -X POST -H 'Content-Type: text/xml+markr' http://127.0.0.1:8000/import -d @- <<XML
    <mcq-test-results>
        <mcq-test-result scanned-on="2017-12-04T12:12:10+11:00">
            <first-name>Jane</first-name>
            <last-name>Austen</last-name>
            <student-number>521585128</student-number>
            <test-id>1234</test-id>
            <summary-marks available="20" obtained="13" />
        </mcq-test-result>
    </mcq-test-results>
XML
```

5. Example GET (aggregate)

```
curl http://127.0.0.1:8000/results/1234/aggregate
```

Note that the tables in the database will be cleaned up every time the Docker container is restarted. To avoid this, remove running init_db.py from the Dockerfile and initialize the database only if it does not already exist.


## Run unit tests
```pytest --log-cli-level=DEBUG --log-cli-format='%(asctime)s - %(levelname)s - %(message)s'```
