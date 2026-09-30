from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .ai import get_ai_provider
from .db import get_db, init_db
from .models import Patient, Visit
from .schemas import PatientCreate, PatientOut, VisitCreate, VisitOut

app = FastAPI(
    title="Cloud Telemedicine API",
    version="1.0.0",
    description="Educational telemedicine cloud infrastructure demo.",
)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/health")
def health():
    return {"status": "ok", "service": "telemedicine-api"}


@app.get("/metrics")
def metrics():
    # Lightweight demo endpoint; CloudWatch/Prometheus integration can replace this.
    return {"service": "telemedicine-api", "status": "healthy"}


@app.post("/patients", response_model=PatientOut, status_code=201)
def create_patient(payload: PatientCreate, db: Session = Depends(get_db)):
    patient = Patient(display_name=payload.display_name)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


@app.get("/patients/{patient_id}", response_model=PatientOut)
def get_patient(patient_id: str, db: Session = Depends(get_db)):
    patient = db.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@app.post("/visits", response_model=VisitOut, status_code=201)
def create_visit(payload: VisitCreate, db: Session = Depends(get_db)):
    if not db.get(Patient, payload.patient_id):
        raise HTTPException(status_code=404, detail="Patient not found")

    visit = Visit(patient_id=payload.patient_id, notes=payload.notes)
    db.add(visit)
    db.commit()
    db.refresh(visit)
    return visit


@app.get("/visits/{visit_id}", response_model=VisitOut)
def get_visit(visit_id: str, db: Session = Depends(get_db)):
    visit = db.get(Visit, visit_id)
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    return visit


@app.post("/visits/{visit_id}/summary", response_model=VisitOut)
def summarize_visit(visit_id: str, db: Session = Depends(get_db)):
    visit = db.get(Visit, visit_id)
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")

    visit.ai_summary = get_ai_provider().summarize(visit.notes)
    db.commit()
    db.refresh(visit)
    return visit
