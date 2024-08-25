# markr-challenge

1. Create a .env file.

```SECRET_KEY=<your_secret_key>```
```DATABASE_URL=postgresql://markr_app:password@localhost/markr_db```

2. Install dependencies.

```pipenv install```

3. Create a PostgreSQL user and database.

```psql -c "CREATE USER markr_app PASSWORD '<password>' CREATEDB;"```

```psql -c "CREATE DATABASE markr_db OWNER markr_app;"```

4. Initialize the database.

```python init_db.py```

5. ```pipenv shell```
6. ```flask run```


Run unit tests
```pytest --log-cli-level=DEBUG --log-cli-format='%(asctime)s - %(levelname)s - %(message)s'```
