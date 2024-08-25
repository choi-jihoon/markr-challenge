from flask import jsonify

# Check if all information is provided, throw error if any piece is missing
def validate_data(test_result_elem):
    if test_result_elem is None:
        return jsonify({"error": "Invalid XML format"}), 400

    # Extract and validate 'scanned-on'
    scanned_on_str = test_result_elem.get('scanned-on')
    if not scanned_on_str:
        return jsonify({"error": "Missing 'scanned-on' attribute"}), 400

    # Extract and validate 'first-name'
    first_name = test_result_elem.find('first-name')
    if first_name is None or not first_name.text.strip():
        return jsonify({"error": "Missing or empty 'first-name'"}), 400

    # Extract and validate 'last-name'
    last_name = test_result_elem.find('last-name')
    if last_name is None or not last_name.text.strip():
        return jsonify({"error": "Missing or empty 'last-name'"}), 400

    # Extract and validate 'student-number'
    student_number = test_result_elem.find('student-number')
    if student_number is None or not student_number.text.strip():
        return jsonify({"error": "Missing or empty 'student-number'"}), 400

    # Extract and validate 'test-id'
    test_id = test_result_elem.find('test-id')
    if test_id is None or not test_id.text.strip():
        return jsonify({"error": "Missing or empty 'test-id'"}), 400

    # Extract and validate 'summary-marks'
    summary_marks_elem = test_result_elem.find('summary-marks')
    if summary_marks_elem is None:
        return jsonify({"error": "Missing 'summary-marks' element"}), 400

    available_marks_str = summary_marks_elem.get('available')
    obtained_marks_str = summary_marks_elem.get('obtained')

    if not available_marks_str or not obtained_marks_str:
        return jsonify({"error": "Missing 'available' or 'obtained' attribute in 'summary-marks'"}), 400

def find_percentage(obtained, available):
    return (obtained / available) * 100.0
