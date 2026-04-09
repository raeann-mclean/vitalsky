from app import db
from datetime import datetime, timezone
import uuid

class MedicalRecord(db.Model):
    __tablename__ = "medical_records"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = db.Column(db.String(36), db.ForeignKey("patients.id"), nullable=False)
    record_type = db.Column(db.String(50), nullable=False)  # e.g. lab_result, prescription, note
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text)
    s3_key = db.Column(db.String(500))  # path to PHI document in S3/localstack
    created_by = db.Column(db.String(100))  # provider name or ID
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "record_type": self.record_type,
            "title": self.title,
            "content": self.content,
            "s3_key": self.s3_key,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat(),
        }