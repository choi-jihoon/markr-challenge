import xml.etree.ElementTree as ET
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
