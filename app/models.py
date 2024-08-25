from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class McqTestResult(db.Model):
    __tablename__ = 'mcq_test_results'

    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    student_number = db.Column(db.String)
    available_marks = db.Column(db.Integer)
    obtained_marks = db.Column(db.Integer)
    scanned_on = db.Column(db.DateTime)

    def to_dict(self):
        scanned_on = datetime.fromisoformat(self.scanned_on)

        return {
            'id': self.id,
            'test_id': self.test_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'student_number': self.student_number,
            'available_marks': self.available_marks,
            'obtained_marks': self.obtained_marks,
            'scanned_on': scanned_on
        }
