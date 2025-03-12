# HR & Payroll Management System

A comprehensive HR and Payroll Management System built with FastAPI (Backend) and Vue.js (Frontend).

## Features

- 👥 Employee Management
- 📊 Department Management
- 💰 Payroll Processing
- ⏰ Attendance Tracking
- 🔐 Role-based Access Control
- 📈 Reports and Analytics

## Tech Stack

### Backend
- FastAPI (Python web framework)
- PostgreSQL (Database)
- SQLAlchemy (ORM)
- Pydantic (Data validation)
- JWT (Authentication)

### Frontend (Coming Soon)
- Vue.js 3
- Tailwind CSS
- Pinia (State management)
- Vue Router
- Axios

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Node.js 16+ (for frontend)

## Setup Instructions

### 1. Database Setup

```bash
# Create and setup PostgreSQL database
psql -U postgres
# Enter your PostgreSQL password when prompted
\i backend/init_db.sql
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your configuration

# Run the application
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

API Documentation will be available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 3. Frontend Setup (Coming Soon)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

## API Endpoints

### Authentication
- POST `/api/v1/auth/login` - User login
- POST `/api/v1/auth/register` - Register new user (Admin only)
- GET `/api/v1/auth/me` - Get current user info

### Employees
- GET `/api/v1/employees` - List employees
- POST `/api/v1/employees` - Create employee
- GET `/api/v1/employees/{id}` - Get employee details
- PUT `/api/v1/employees/{id}` - Update employee
- DELETE `/api/v1/employees/{id}` - Delete employee

### Departments
- GET `/api/v1/departments` - List departments
- POST `/api/v1/departments` - Create department
- GET `/api/v1/departments/{id}` - Get department details
- PUT `/api/v1/departments/{id}` - Update department
- DELETE `/api/v1/departments/{id}` - Delete department
- GET `/api/v1/departments/{id}/employees` - List employees in department

### Payroll
- GET `/api/v1/payroll` - List payroll records
- POST `/api/v1/payroll` - Create payroll record
- GET `/api/v1/payroll/{id}` - Get payroll details
- PUT `/api/v1/payroll/{id}` - Update payroll record
- DELETE `/api/v1/payroll/{id}` - Delete payroll record
- POST `/api/v1/payroll/{id}/process` - Process payroll
- POST `/api/v1/payroll/{id}/pay` - Mark payroll as paid

### Attendance
- GET `/api/v1/employees/{id}/attendance` - List employee attendance
- POST `/api/v1/employees/{id}/attendance` - Create attendance record
- PUT `/api/v1/employees/{id}/attendance/{attendance_id}` - Update attendance
- DELETE `/api/v1/employees/{id}/attendance/{attendance_id}` - Delete attendance

## Default Credentials

After setting up the database, you can login with these default credentials:

```
Username: admin
Password: admin123
```

⚠️ **Important**: Change the default password immediately after first login in production!

## Development

### Code Structure

```
backend/
├── routes/          # API endpoints
├── models.py        # SQLAlchemy models
├── schemas.py       # Pydantic schemas
├── crud.py         # Database operations
├── auth.py         # Authentication logic
├── config.py       # Configuration settings
├── database.py     # Database connection
└── main.py         # Application entry point
```

### Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/hrpayroll
SECRET_KEY=your-secret-key-here
API_V1_PREFIX=/api/v1
CORS_ORIGINS=["http://localhost:3000"]
```

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
