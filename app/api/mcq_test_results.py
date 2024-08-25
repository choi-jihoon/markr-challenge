import xml.etree.ElementTree as ET
import statistics
import numpy as np
from datetime import datetime
from flask import Blueprint, request, jsonify
from app.models import db, McqTestResult

bp = Blueprint("mcq_test_results", __name__, url_prefix="")

@bp.route("/")
def index():
    return "Test Results!"

@bp.route("/import", methods=["POST"])
def post_test_result():
    xml_data = request.data.decode('utf-8')
    root = ET.fromstring(xml_data)

    test_result_elem = root.find('mcq-test-result')
    if test_result_elem is None:
        return jsonify({"error": "Invalid XML format"}), 400

    scanned_on_str = test_result_elem.get('scanned-on')
    scanned_on = datetime.fromisoformat(scanned_on_str)

    first_name = test_result_elem.find('first-name').text
    last_name = test_result_elem.find('last-name').text
    student_number = test_result_elem.find('student-number').text
    test_id = test_result_elem.find('test-id').text
    summary_marks_elem = test_result_elem.find('summary-marks')
    available_marks = int(summary_marks_elem.get('available'))
    obtained_marks = int(summary_marks_elem.get('obtained'))

    result = McqTestResult(
        scanned_on=scanned_on,
        first_name=first_name,
        last_name=last_name,
        student_number=student_number,
        test_id=test_id,
        available_marks=available_marks,
        obtained_marks=obtained_marks
    )

    db.session.add(result)
    db.session.commit()

    return jsonify({"message": "Data saved successfully"}), 201


@bp.route("/results/<string:test_id>/aggregate")
def get_aggregate(test_id):
    # first get all tests with test_id
    tests_query = McqTestResult.query.filter(McqTestResult.test_id == test_id).all()

    # validate there's data to aggregate
    if not tests_query:
        return jsonify({"message": "No test scores to aggregate."})
    
    tests_json = {'tests': [test.to_dict() for test in tests_query]}

    scores = [find_percentage(test['obtained_marks'], test['available_marks']) for test in tests_json['tests']]
    mean = statistics.mean(scores)
    count = len(scores)
    p25 = np.percentile(scores, 25)
    p50 = np.percentile(scores, 50)
    p75 = np.percentile(scores, 75)

    return {
        "mean": mean,
        "count": count,
        "p25": p25,
        "p50": p50,
        "p75": p75
    }

def find_percentage(obtained, available):
    return (obtained / available) * 100.0
