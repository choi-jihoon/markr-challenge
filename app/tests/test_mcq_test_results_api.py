import pytest
import logging
from flask import json
from app import app, db, McqTestResult

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()

            db.session.add(McqTestResult(test_id='1234',
                                         first_name='Virginia',
                                         last_name='Woolf',
                                         student_number='123456789',
                                         obtained_marks=80,
                                         available_marks=100))
            db.session.add(McqTestResult(test_id='1234',
                                         first_name='Mary',
                                         last_name='Shelley',
                                         student_number='987654321',
                                         obtained_marks=70,
                                         available_marks=100))
            db.session.add(McqTestResult(test_id='1234',
                                         first_name='Emily',
                                         last_name='Dickinson',
                                         student_number='246810',
                                         obtained_marks=90,
                                         available_marks=100))
            db.session.commit()

        yield client
        with app.app_context():
            db.drop_all()

@pytest.fixture
def valid_xml():
    return """<?xml version="1.0" encoding="UTF-8"?>
    <mcq-test-results>
        <mcq-test-result scanned-on="2017-12-04T12:12:10+11:00">
            <first-name>Jane</first-name>
            <last-name>Austen</last-name>
            <student-number>521585128</student-number>
            <test-id>1234</test-id>
            <summary-marks available="20" obtained="13" />
        </mcq-test-result>
    </mcq-test-results>"""

@pytest.fixture
def invalid_xml():
    return """<?xml version="1.0" encoding="UTF-8"?>
    <mcq-test-results>
        <!-- Missing mcq-test-result element -->
    </mcq-test-results>"""

def test_post_test_result_valid(client, valid_xml):
    response = client.post('/import', data=valid_xml, content_type='text/xml')
    assert response.status_code == 201
    assert json.loads(response.data)['message'] == 'Data saved successfully'

    # Verify data was saved to the database
    result = McqTestResult.query.filter_by(student_number='521585128').first()
    assert result is not None
    assert result.first_name == 'Jane'
    assert result.last_name == 'Austen'
    assert result.student_number == '521585128'
    assert result.test_id == '1234'
    assert result.available_marks == 20
    assert result.obtained_marks == 13

def test_post_test_result_invalid(client, invalid_xml):
    response = client.post('/import', data=invalid_xml, content_type='text/xml')
    assert response.status_code == 400
    assert json.loads(response.data)['error'] == 'Invalid XML format'


def test_get_aggregate_with_data(client):
    response = client.get('/results/1234/aggregate')
    data = response.json

    assert response.status_code == 200
    assert data["count"] == 3
    assert data["mean"] == 80.0
    assert data["p25"] == 75.0
    assert data["p50"] == 80.0
    assert data["p75"] == 85.0


def test_get_aggregate_without_data(client):
    response = client.get('/results/empty_test_id/aggregate')
    assert json.loads(response.data)['message'] == 'No test scores to aggregate.'
