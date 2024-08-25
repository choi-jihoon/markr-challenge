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

@pytest.fixture
def missing_first_name():
    return """<?xml version="1.0" encoding="UTF-8"?>
    <mcq-test-results>
        <mcq-test-result scanned-on="2017-12-04T12:12:10+11:00">
            <last-name>Austen</last-name>
            <student-number>521585128</student-number>
            <test-id>1234</test-id>
            <summary-marks available="20" obtained="13" />
        </mcq-test-result>
    </mcq-test-results>"""

@pytest.fixture
def missing_last_name():
    return """<?xml version="1.0" encoding="UTF-8"?>
    <mcq-test-results>
        <mcq-test-result scanned-on="2017-12-04T12:12:10+11:00">
            <first-name>Jane</first-name>
            <student-number>521585128</student-number>
            <test-id>1234</test-id>
            <summary-marks available="20" obtained="13" />
        </mcq-test-result>
    </mcq-test-results>"""

@pytest.fixture
def missing_student_number():
    return """<?xml version="1.0" encoding="UTF-8"?>
    <mcq-test-results>
        <mcq-test-result scanned-on="2017-12-04T12:12:10+11:00">
            <first-name>Jane</first-name>
            <last-name>Austen</last-name>
            <test-id>1234</test-id>
            <summary-marks available="20" obtained="13" />
        </mcq-test-result>
    </mcq-test-results>"""

@pytest.fixture
def missing_test_id():
    return """<?xml version="1.0" encoding="UTF-8"?>
    <mcq-test-results>
        <mcq-test-result scanned-on="2017-12-04T12:12:10+11:00">
            <first-name>Jane</first-name>
            <last-name>Austen</last-name>
            <student-number>521585128</student-number>
            <summary-marks available="20" obtained="13" />
        </mcq-test-result>
    </mcq-test-results>"""

@pytest.fixture
def missing_summary_marks():
    return """<?xml version="1.0" encoding="UTF-8"?>
    <mcq-test-results>
        <mcq-test-result scanned-on="2017-12-04T12:12:10+11:00">
            <first-name>Jane</first-name>
            <last-name>Austen</last-name>
            <student-number>521585128</student-number>
            <test-id>1234</test-id>
        </mcq-test-result>
    </mcq-test-results>"""

@pytest.fixture
def missing_available_marks():
    return """<?xml version="1.0" encoding="UTF-8"?>
    <mcq-test-results>
        <mcq-test-result scanned-on="2017-12-04T12:12:10+11:00">
            <first-name>Jane</first-name>
            <last-name>Austen</last-name>
            <student-number>521585128</student-number>
            <test-id>1234</test-id>
            <summary-marks available="" obtained="13" />
        </mcq-test-result>
    </mcq-test-results>"""

@pytest.fixture
def missing_obtained_marks():
    return """<?xml version="1.0" encoding="UTF-8"?>
    <mcq-test-results>
        <mcq-test-result scanned-on="2017-12-04T12:12:10+11:00">
            <first-name>Jane</first-name>
            <last-name>Austen</last-name>
            <student-number>521585128</student-number>
            <test-id>1234</test-id>
            <summary-marks available="20" obtained="" />
        </mcq-test-result>
    </mcq-test-results>"""

@pytest.fixture
def valid_rescan():
    return """<?xml version="1.0" encoding="UTF-8"?>
    <mcq-test-results>
        <mcq-test-result scanned-on="2017-12-04T12:12:10+11:00">
            <first-name>Virginia</first-name>
            <last-name>Woolf</last-name>
            <student-number>123456789</student-number>
            <test-id>1234</test-id>
            <summary-marks available="100" obtained="98" />
        </mcq-test-result>
    </mcq-test-results>"""

@pytest.fixture
def invalid_rescan():
    return """<?xml version="1.0" encoding="UTF-8"?>
    <mcq-test-results>
        <mcq-test-result scanned-on="2017-12-04T12:12:10+11:00">
            <first-name>Virginia</first-name>
            <last-name>Woolf</last-name>
            <student-number>123456789</student-number>
            <test-id>1234</test-id>
            <summary-marks available="20" obtained="5" />
        </mcq-test-result>
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

def test_post_test_result_missing_first_name(client, missing_first_name):
    response = client.post('/import', data=missing_first_name, content_type='text/xml')
    assert response.status_code == 400
    assert json.loads(response.data)['error'] == "Missing or empty 'first-name'"

def test_post_test_result_missing_last_name(client, missing_last_name):
    response = client.post('/import', data=missing_last_name, content_type='text/xml')
    assert response.status_code == 400
    assert json.loads(response.data)['error'] == "Missing or empty 'last-name'"

def test_post_test_result_missing_student_number(client, missing_student_number):
    response = client.post('/import', data=missing_student_number, content_type='text/xml')
    assert response.status_code == 400
    assert json.loads(response.data)['error'] == "Missing or empty 'student-number'"

def test_post_test_result_missing_test_id(client, missing_test_id):
    response = client.post('/import', data=missing_test_id, content_type='text/xml')
    assert response.status_code == 400
    assert json.loads(response.data)['error'] == "Missing or empty 'test-id'"

def test_post_test_result_missing_summary_marks(client, missing_summary_marks):
    response = client.post('/import', data=missing_summary_marks, content_type='text/xml')
    assert response.status_code == 400
    assert json.loads(response.data)['error'] == "Missing 'summary-marks' element"

def test_post_test_result_missing_available_marks(client, missing_available_marks):
    response = client.post('/import', data=missing_available_marks, content_type='text/xml')
    assert response.status_code == 400
    assert json.loads(response.data)['error'] == "Missing 'available' or 'obtained' attribute in 'summary-marks'"

def test_post_test_result_missing_obtained_marks(client, missing_obtained_marks):
    response = client.post('/import', data=missing_obtained_marks, content_type='text/xml')
    assert response.status_code == 400
    assert json.loads(response.data)['error'] == "Missing 'available' or 'obtained' attribute in 'summary-marks'"

def test_post_valid_rescan(client, valid_rescan):
    response = client.post('/import', data=valid_rescan, content_type='text/xml')
    assert response.status_code == 201
    assert json.loads(response.data)['message'] == 'Data saved successfully'

    # Verify data was updated in the database
    result = McqTestResult.query.filter_by(student_number='123456789').first()
    assert result is not None
    assert result.available_marks == 100
    assert result.obtained_marks == 98

def test_post_invalid_rescan(client, invalid_rescan):
    response = client.post('/import', data=invalid_rescan, content_type='text/xml')
    assert response.status_code == 200
    assert json.loads(response.data)['message'] == 'Unnecessary rescan, no update to database'

    # Verify data was not changed in the database
    result = McqTestResult.query.filter_by(student_number='123456789').first()
    assert result is not None
    assert result.available_marks == 100
    assert result.obtained_marks == 80

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
