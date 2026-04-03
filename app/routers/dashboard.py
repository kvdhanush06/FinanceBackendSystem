from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import List

from app.database import get_db
from app.models import User, UserRole, FinancialRecord, RecordType
from app.schemas import SummaryResponse, CategorySummary, TrendItem, RecordResponse
from app.dependencies import role_required, get_current_user


router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/summary", response_model=SummaryResponse)
def get_summary(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """
    Get a high-level summary of the finances.
    Accessible to all logged-in users (Viewer, Analyst, Admin).
    """
    income = db.query(func.sum(FinancialRecord.amount)).filter(FinancialRecord.type == RecordType.income).scalar() or 0.0
    expenses = db.query(func.sum(FinancialRecord.amount)).filter(FinancialRecord.type == RecordType.expense).scalar() or 0.0
    
    return {
        "total_income": income,
        "total_expenses": expenses,
        "net_balance": income - expenses
    }


@router.get("/category-summary", response_model=List[CategorySummary])
def get_category_summary(
    db: Session = Depends(get_db),
    user: User = Depends(role_required([UserRole.analyst, UserRole.admin]))
):
    """
    Get totals broken down by category.
    Accessible to Analysts and Admins.
    """
    results = db.query(
        FinancialRecord.category,
        func.sum(FinancialRecord.amount).label("total")
    ).group_by(FinancialRecord.category).all()
    
    return [{"category": r.category, "total": r.total} for r in results]


@router.get("/recent", response_model=List[RecordResponse])
def get_recent_activity(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """
    Get the last 10 financial entries.
    Accessible to all users.
    """
    return db.query(FinancialRecord).order_by(FinancialRecord.created_at.desc()).limit(10).all()


@router.get("/trends", response_model=List[TrendItem])
def get_trends(
    db: Session = Depends(get_db),
    user: User = Depends(role_required([UserRole.analyst, UserRole.admin]))
):
    """
    Get monthly trends for income and expenses.
    Accessible to Analysts and Admins.
    """
    # Grouping by month and type
    trends_query = db.query(
        func.to_char(FinancialRecord.date, 'YYYY-MM').label("month"),
        FinancialRecord.type,
        func.sum(FinancialRecord.amount).label("total")
    ).group_by("month", FinancialRecord.type).order_by("month").all()
    
    # Restructuring the flat query result into TrendItem list
    trends_dict = {}
    for r in trends_query:
        if r.month not in trends_dict:
            trends_dict[r.month] = {"month": r.month, "income": 0.0, "expense": 0.0}
        
        if r.type == RecordType.income:
            trends_dict[r.month]["income"] = r.total
        else:
            trends_dict[r.month]["expense"] = r.total
            
    return list(trends_dict.values())
