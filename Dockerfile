FROM python:3.9

WORKDIR /app

COPY . /app

ENV FLASK_APP=markr
ENV FLASK_ENV=production
ENV SQLALCHEMY_ECHO=True

EXPOSE 8000

RUN pip install -r requirements.txt

COPY init_db.py /app/

# CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]
CMD ["sh", "-c", "python init_db.py && flask run --host=0.0.0.0 --port=8000"]
