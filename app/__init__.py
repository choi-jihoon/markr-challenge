import os
from flask import Flask
from .config import Configuration, ConfigTest
from .models import db, McqTestResult
from .api import mcq_test_results

app = Flask(__name__)

if os.environ.get('FLASK_ENV') == 'production':
    app.config.from_object(Configuration)
else:
    app.config.from_object(ConfigTest)

app.register_blueprint(mcq_test_results.bp)
db.init_app(app)
