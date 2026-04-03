from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.database import get_db
from app.models import User, UserRole, FinancialRecord, RecordType
from app.schemas import RecordResponse, RecordCreate, RecordUpdate
from app.dependencies import role_required


router = APIRouter(prefix="/records", tags=["Records"])


@router.post("/", response_model=RecordResponse)
def create_record(
    record_in: RecordCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(role_required([UserRole.admin]))
):
    """Admin-only endpoint to create a new financial record."""
    new_record = FinancialRecord(
        **record_in.dict(),
        created_by=admin.id
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record


@router.get("/", response_model=List[RecordResponse])
def list_records(
    db: Session = Depends(get_db),
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    category: Optional[str] = Query(None),
    type: Optional[RecordType] = Query(None),
    user: User = Depends(role_required([UserRole.analyst, UserRole.admin]))
):
    """List financial records with optional filtering. Accessible to Analysts and Admins."""
    query = db.query(FinancialRecord)
    
    if start_date:
        query = query.filter(FinancialRecord.date >= start_date)
    if end_date:
        query = query.filter(FinancialRecord.date <= end_date)
    if category:
        query = query.filter(FinancialRecord.category.ilike(f"%{category}%"))
    if type:
        query = query.filter(FinancialRecord.type == type)
        
    return query.all()


@router.get("/{record_id}", response_model=RecordResponse)
def get_record(
    record_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(role_required([UserRole.analyst, UserRole.admin]))
):
    """Retrieve details of a specific financial record. Accessible to Analysts and Admins."""
    record = db.query(FinancialRecord).filter(FinancialRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record


@router.put("/{record_id}", response_model=RecordResponse)
def update_record(
    record_id: int,
    record_update: RecordUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(role_required([UserRole.admin]))
):
    """Admin-only endpoint to update an existing financial record."""
    db_record = db.query(FinancialRecord).filter(FinancialRecord.id == record_id).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    update_data = record_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_record, key, value)
    
    db.commit()
    db.refresh(db_record)
    return db_record


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_record(
    record_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(role_required([UserRole.admin]))
):
    """Admin-only endpoint to permanently delete a financial record."""
    db_record = db.query(FinancialRecord).filter(FinancialRecord.id == record_id).first()
    if not db_record:
        raise HTTPException(status_code=404, detail="Record not found")
    
    db.delete(db_record)
    db.commit()
    return None
