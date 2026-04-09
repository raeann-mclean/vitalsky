from flask import Blueprint, request, jsonify
from app import db
from app.models.record import MedicalRecord

records_bp = Blueprint("records", __name__)

@records_bp.route("/patient/<patient_id>", methods=["GET"])
def get_records(patient_id):
    records = MedicalRecord.query.filter_by(patient_id=patient_id).all()
    return jsonify([r.to_dict() for r in records]), 200

@records_bp.route("/<record_id>", methods=["GET"])
def get_record(record_id):
    record = MedicalRecord.query.get_or_404(record_id)
    return jsonify(record.to_dict()), 200

@records_bp.route("/", methods=["POST"])
def create_record():
    data = request.get_json()
    required = ["patient_id", "record_type", "title"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing required fields"}), 400

    record = MedicalRecord(
        patient_id=data["patient_id"],
        record_type=data["record_type"],
        title=data["title"],
        content=data.get("content"),
        s3_key=data.get("s3_key"),
        created_by=data.get("created_by"),
    )
    db.session.add(record)
    db.session.commit()
    return jsonify(record.to_dict()), 201

@records_bp.route("/<record_id>", methods=["DELETE"])
def delete_record(record_id):
    record = MedicalRecord.query.get_or_404(record_id)
    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "Record deleted"}), 200