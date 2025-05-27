This is the Django REST API backend for the healthcare appointment scheduling system. It supports user authentication (OAuth2), doctor and patient profiles, appointment booking, and role-based permissions.



## 🚀 Setup Instructions

### 1. Clone the Repository

git https://github.com/Antonymegar/healthcarebackend.git
cd healthcare_system_backend

### 2. Create and Activate a Virtual Environment
python -m venv env
source env/bin/activate       # On Windows: env\Scripts\activate

### 3.Install Dependencies
pip install -r requirements.txt

### 4.Configure Environment Variables
DATABASE_URL=postgres://username:password@host:port/dbname
SECRET_KEY=your-secret-key

### 5. Apply Migrations
python manage.py migrate

### 6. Create a Superuser
python manage.py createsuperuser

### 7. Run the Server
python manage.py runserver

## Swagger Documentation
http://localhost:8000/swagger/

## Endpoints 
| Endpoint                  | Method | Description                           |
| ------------------------- | ------ | ------------------------------------- |
| `/api/appointments/`      | GET    | List appointments for logged-in user  |
| `/api/appointments/`      | POST   | Create new appointment (patient only) |
| `/api/appointments/<id>/` | PATCH  | Cancel (patient) or Complete (doctor) |
| `/api/doctors/`           | GET    | List available doctors                |
| `/api/user-profile/`      | GET    | Return current user profile           |
| `/swagger/`               | GET    | View API documentation                |

## DataBase Schema
![Database](https://github.com/user-attachments/assets/c1f01551-82a6-4d8c-b1b9-99d08d0dadb2)
