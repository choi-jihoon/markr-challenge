from flask import Flask
from .config import Configuration
from .models import db
from .api import test_results

app = Flask(__name__)
app.config.from_object(Configuration)
app.register_blueprint(test_results.bp)
db.init_app(app)
