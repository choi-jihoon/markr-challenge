# markr-challenge
[Stile Coding Challenge](https://gist.github.com/nick96/fda49ece0de8e64f58d45b03dda9b0c6)

## Key Assumptions
One key assumption I made initially was that each POST request would contain one test result. I added a new route (/imports) for requests with multiple test results. Another assumption I made was that student numbers are unique to each student. This is necessary when checking for rescans.

## Approach
In order to complete this coding challenge, I set up a Flask app with SQLAlchemy and a PostgreSQL database, with Pytest for unit testing. I made use of imported methods to calculate the aggregation data (statistics for mean, NumPy for percentiles) after querying the database to obtain the test results filtered by test-id. The validation in the POST method(s) reject any results with missing information, and also checks if a test result already exists with the same test-id and student-number. If a test does already exist in the database for a student, it will always retain the higher score.

Please see directions below to run locally or on a Docker container.

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

```docker compose build```

```docker compose up```


## Run unit tests
```pytest --log-cli-level=DEBUG --log-cli-format='%(asctime)s - %(levelname)s - %(message)s'```

## Example Requests

### Example POST to /import (one test result)

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

### Example GET (aggregate)

```
curl http://127.0.0.1:8000/results/1234/aggregate
```

### Example POST to /imports (multiple test results)

```
curl -X POST -H 'Content-Type: text/xml+markr' http://127.0.0.1:8000/imports -d @- <<XML
    <mcq-test-results>
        <mcq-test-result scanned-on="2017-12-04T12:12:10+11:00">
            <first-name>KJ</first-name>
            <last-name>Alysander</last-name>
            <student-number>002299</student-number>
            <test-id>9863</test-id>
            <answer question="0" marks-available="1" marks-awarded="1">D</answer>
            <answer question="1" marks-available="1" marks-awarded="1">D</answer>
            <answer question="2" marks-available="1" marks-awarded="1">D</answer>
            <answer question="3" marks-available="1" marks-awarded="0">C</answer>
            <answer question="4" marks-available="1" marks-awarded="1">B</answer>
            <answer question="5" marks-available="1" marks-awarded="0">D</answer>
            <answer question="6" marks-available="1" marks-awarded="0">A</answer>
            <answer question="7" marks-available="1" marks-awarded="1">A</answer>
            <answer question="8" marks-available="1" marks-awarded="1">B</answer>
            <answer question="9" marks-available="1" marks-awarded="1">D</answer>
            <answer question="10" marks-available="1" marks-awarded="1">A</answer>
            <answer question="11" marks-available="1" marks-awarded="1">B</answer>
            <answer question="12" marks-available="1" marks-awarded="0">A</answer>
            <answer question="13" marks-available="1" marks-awarded="0">B</answer>
            <answer question="14" marks-available="1" marks-awarded="1">B</answer>
            <answer question="15" marks-available="1" marks-awarded="1">A</answer>
            <answer question="16" marks-available="1" marks-awarded="1">C</answer>
            <answer question="17" marks-available="1" marks-awarded="0">B</answer>
            <answer question="18" marks-available="1" marks-awarded="1">A</answer>
            <answer question="19" marks-available="1" marks-awarded="0">B</answer>
            <summary-marks available="20" obtained="13" />
        </mcq-test-result>
        <mcq-test-result scanned-on="2017-12-04T12:13:10+11:00">
            <first-name>KJ</first-name>
            <last-name>Jim</last-name>
            <student-number>2300</student-number>
            <test-id>9863</test-id>
            <answer question="0" marks-available="1" marks-awarded="0">C</answer>
            <answer question="1" marks-available="1" marks-awarded="0">B</answer>
            <answer question="2" marks-available="1" marks-awarded="0">D</answer>
            <answer question="3" marks-available="1" marks-awarded="1">A</answer>
            <answer question="4" marks-available="1" marks-awarded="1">C</answer>
            <answer question="5" marks-available="1" marks-awarded="0">C</answer>
            <answer question="6" marks-available="1" marks-awarded="0">C</answer>
            <answer question="7" marks-available="1" marks-awarded="0">B</answer>
            <answer question="8" marks-available="1" marks-awarded="0">C</answer>
            <answer question="9" marks-available="1" marks-awarded="1">C</answer>
            <answer question="10" marks-available="1" marks-awarded="0">C</answer>
            <answer question="11" marks-available="1" marks-awarded="0">B</answer>
            <answer question="12" marks-available="1" marks-awarded="0">B</answer>
            <answer question="13" marks-available="1" marks-awarded="0">B</answer>
            <answer question="14" marks-available="1" marks-awarded="1">B</answer>
            <answer question="15" marks-available="1" marks-awarded="0">C</answer>
            <answer question="16" marks-available="1" marks-awarded="1">C</answer>
            <answer question="17" marks-available="1" marks-awarded="1">A</answer>
            <answer question="18" marks-available="1" marks-awarded="1">C</answer>
            <answer question="19" marks-available="1" marks-awarded="1">D</answer>
            <summary-marks available="20" obtained="8" />
        </mcq-test-result>
        <mcq-test-result scanned-on="2017-12-04T12:14:10+11:00">
            <first-name>Claire</first-name>
            <last-name>Byron</last-name>
            <student-number>2301</student-number>
            <test-id>9863</test-id>
            <answer question="0" marks-available="1" marks-awarded="0">A</answer>
            <answer question="1" marks-available="1" marks-awarded="0">B</answer>
            <answer question="2" marks-available="1" marks-awarded="1">B</answer>
            <answer question="3" marks-available="1" marks-awarded="1">C</answer>
            <answer question="4" marks-available="1" marks-awarded="1">B</answer>
            <answer question="5" marks-available="1" marks-awarded="0">D</answer>
            <answer question="6" marks-available="1" marks-awarded="1">C</answer>
            <answer question="7" marks-available="1" marks-awarded="1">A</answer>
            <answer question="8" marks-available="1" marks-awarded="1">D</answer>
            <answer question="9" marks-available="1" marks-awarded="0">C</answer>
            <answer question="10" marks-available="1" marks-awarded="1">C</answer>
            <answer question="11" marks-available="1" marks-awarded="1">C</answer>
            <answer question="12" marks-available="1" marks-awarded="1">A</answer>
            <answer question="13" marks-available="1" marks-awarded="1">B</answer>
            <answer question="14" marks-available="1" marks-awarded="0">B</answer>
            <answer question="15" marks-available="1" marks-awarded="1">D</answer>
            <answer question="16" marks-available="1" marks-awarded="1">C</answer>
            <answer question="17" marks-available="1" marks-awarded="1">A</answer>
            <answer question="18" marks-available="1" marks-awarded="0">D</answer>
            <answer question="19" marks-available="1" marks-awarded="1">B</answer>
            <summary-marks available="20" obtained="14" />
        </mcq-test-result>
        <mcq-test-result scanned-on="2017-12-04T12:15:10+11:00">
            <first-name>Claire</first-name>
            <last-name>Bob</last-name>
            <student-number>2302</student-number>
            <test-id>9863</test-id>
            <answer question="0" marks-available="1" marks-awarded="0">A</answer>
            <answer question="1" marks-available="1" marks-awarded="0">D</answer>
            <answer question="2" marks-available="1" marks-awarded="0">A</answer>
            <answer question="3" marks-available="1" marks-awarded="0">A</answer>
            <answer question="4" marks-available="1" marks-awarded="1">D</answer>
            <answer question="5" marks-available="1" marks-awarded="1">D</answer>
            <answer question="6" marks-available="1" marks-awarded="1">A</answer>
            <answer question="7" marks-available="1" marks-awarded="0">C</answer>
            <answer question="8" marks-available="1" marks-awarded="1">B</answer>
            <answer question="9" marks-available="1" marks-awarded="0">D</answer>
            <answer question="10" marks-available="1" marks-awarded="0">D</answer>
            <answer question="11" marks-available="1" marks-awarded="0">B</answer>
            <answer question="12" marks-available="1" marks-awarded="1">C</answer>
            <answer question="13" marks-available="1" marks-awarded="1">A</answer>
            <answer question="14" marks-available="1" marks-awarded="0">D</answer>
            <answer question="15" marks-available="1" marks-awarded="1">B</answer>
            <answer question="16" marks-available="1" marks-awarded="1">A</answer>
            <answer question="17" marks-available="1" marks-awarded="0">A</answer>
            <answer question="18" marks-available="1" marks-awarded="0">A</answer>
            <answer question="19" marks-available="1" marks-awarded="0">A</answer>
            <summary-marks available="20" obtained="8" />
        </mcq-test-result>
        <mcq-test-result scanned-on="2017-12-04T12:16:10+11:00">
            <first-name>Stephanie</first-name>
            <last-name>Susan</last-name>
            <student-number>2303</student-number>
            <test-id>9863</test-id>
            <answer question="0" marks-available="1" marks-awarded="0">C</answer>
            <answer question="1" marks-available="1" marks-awarded="0">C</answer>
            <answer question="2" marks-available="1" marks-awarded="0">B</answer>
            <answer question="3" marks-available="1" marks-awarded="0">B</answer>
            <answer question="4" marks-available="1" marks-awarded="1">B</answer>
            <answer question="5" marks-available="1" marks-awarded="1">D</answer>
            <answer question="6" marks-available="1" marks-awarded="1">D</answer>
            <answer question="7" marks-available="1" marks-awarded="1">D</answer>
            <answer question="8" marks-available="1" marks-awarded="1">A</answer>
            <answer question="9" marks-available="1" marks-awarded="1">B</answer>
            <answer question="10" marks-available="1" marks-awarded="0">A</answer>
            <answer question="11" marks-available="1" marks-awarded="0">D</answer>
            <answer question="12" marks-available="1" marks-awarded="1">C</answer>
            <answer question="13" marks-available="1" marks-awarded="1">D</answer>
            <answer question="14" marks-available="1" marks-awarded="1">A</answer>
            <answer question="15" marks-available="1" marks-awarded="0">A</answer>
            <answer question="16" marks-available="1" marks-awarded="1">C</answer>
            <answer question="17" marks-available="1" marks-awarded="0">D</answer>
            <answer question="18" marks-available="1" marks-awarded="1">A</answer>
            <answer question="19" marks-available="1" marks-awarded="0">C</answer>
            <summary-marks available="20" obtained="11" />
        </mcq-test-result>
    </mcq-test-results>
XML
```
