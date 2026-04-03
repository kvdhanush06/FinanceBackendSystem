# Finance Data Processing and Access Control Backend

A robust and clean backend API for a finance dashboard, built with FastAPI, PostgreSQL, and SQLAlchemy.

## Features

- **User & Role Management**: Register, login, and manage user roles (Viewer, Analyst, Admin).
- **Financial Records CRUD**: Full management of income and expenses with descriptions, categories, and dates.
- **Filtering**: Advanced filtering of records by date range, category, and type.
- **Dashboard Summaries**: Summary metrics including total income, total expenses, net balance, category breakdown, and monthly trends.
- **Role-Based Access Control (RBAC)**: Securely enforced permissions based on user roles.
  - **Viewer**: Can view high-level dashboard summaries and recent activity.
  - **Analyst**: Can view individual records, category insights, and trends.
  - **Admin**: Full control over all records and user accounts.
- **Automated API Docs**: Built-in interactive Swagger UI available at `/docs`.

## Technology Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python)
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
- **Authentication**: JWT (JSON Web Tokens) with `python-jose`
- **Security**: Password hashing with `passlib[bcrypt]`
- **Validation**: `Pydantic`

## Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL (Local or Hosted)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/kvdhanush06/FinanceBackendSystem.git
   cd FinanceBackendSystem
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Create a `.env` file in the root directory based on `.env.example`:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/finance_db
   SECRET_KEY=your-generate-secret-key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

### Running Locally

```bash
uvicorn app.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

### API Documentation

Once the server is running, you can access the interactive Swagger documentation at:
- **Swagger UI**: `http://127.0.0.1:8000/docs`

## Assumptions & Trade-offs

1. **Admin Initialization**: The very first user to register on a fresh database is automatically assigned the `Admin` role. Subsequent users default to `Viewer`.
2. **Global Records**: Financial records are currently managed globally for the dashboard, though each record tracks which user created it.
3. **Data Integrity**: Financial amounts are stored as floats for simplicity in this assignment, though `Decimal` would be preferred for high-precision production financial systems.
4. **Soft Delete**: To keep the implementation clean and focused on the core requirements, a standard "Hard Delete" was implemented for users and records.

## License

This project is submitted as an internship assignment.
