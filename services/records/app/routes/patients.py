from flask import Blueprint, request, jsonify
from app import db
from app.models.patient import Patient

patients_bp = Blueprint("patients", __name__)

@patients_bp.route("/", methods=["GET"])
def get_patients():
    patients = Patient.query.all()
    return jsonify([p.to_dict() for p in patients]), 200

@patients_bp.route("/<patient_id>", methods=["GET"])
def get_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return jsonify(patient.to_dict()), 200

@patients_bp.route("/", methods=["POST"])
def create_patient():
    data = request.get_json()
    required = ["first_name", "last_name", "date_of_birth", "email"]
    if not all(k in data for k in required):
        return jsonify({"error": "Missing required fields"}), 400

    patient = Patient(
        first_name=data["first_name"],
        last_name=data["last_name"],
        date_of_birth=data["date_of_birth"],
        email=data["email"],
        phone=data.get("phone"),
    )
    db.session.add(patient)
    db.session.commit()
    return jsonify(patient.to_dict()), 201

@patients_bp.route("/<patient_id>", methods=["PUT"])
def update_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    data = request.get_json()
    for field in ["first_name", "last_name", "email", "phone"]:
        if field in data:
            setattr(patient, field, data[field])
    db.session.commit()
    return jsonify(patient.to_dict()), 200

@patients_bp.route("/<patient_id>", methods=["DELETE"])
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    db.session.delete(patient)
    db.session.commit()
    return jsonify({"message": "Patient deleted"}), 200