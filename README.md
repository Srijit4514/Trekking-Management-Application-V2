# Trekking Management Application V2

A role-based trekking management system with a Flask backend and a Vue 3 frontend. The app supports three user types: administrators, staff members, and trekkers/users.

## Features by Role

### Admin
- View the full dashboard with trek, user, staff, booking, and revenue metrics.
- Create, edit, delete treks and search user, staff, treks.
- Add staff accounts and send login credentials by email.
- Assign or unassign staff to treks.
- Activate or deactivate user accounts.
- Download trek booking reports as PDF.

### Staff
- View only the treks assigned to them.
- See all bookings for assigned treks.
- Update trek slots and trek status.
- Mark completed treks and automatically complete booked reservations.

### User / Trekker
- Register and log in.
- Browse open treks with filters for location, difficulty, and duration.
- Book available treks.
- View booking history and payment status.
- Update profile details and password.

## Tech Stack

### Backend
- Python 3.11
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- Flask-CORS
- Celery
- Redis
- Gunicorn
- FPDF for PDF report generation

### Frontend
- Vue 3
- Vite
- Vue Router
- Axios
- Bootstrap 5
- Chart.js / vue-chartjs

## Setup

https://github.com/user-attachments/assets/0f8d6ab5-67fa-495d-b757-ed9908f05019

### 1. Clone the repository

```bash
git clone https://github.com/23f3000592/trekking-management-application-V2.git
cd trekking-management-application-V2
```

### 2. Configure the backend environment

Create a `.env` file in the project root for the required values:

```env
SQLALCHEMY_DATABASE_URI
JWT_SECRET_KEY
FRONTEND_URL
ADMIN_USERNAME
ADMIN_PASSWORD
REDIS_URL
SMTP_SERVER
SMTP_PORT
SENDER_EMAIL
SENDER_PASSWORD
```

The backend creates the database tables on startup and also creates a default admin account if one does not exist.

### 3. Install backend dependencies

```bash
cd backend
python -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate 
pip install -r requirements.txt
```

### 4. Install frontend dependencies

```bash
cd ..\frontend
npm install
```

## Run the Project

### Run the application locally

Open two terminals.

Run the backend:

```bash
cd backend
docker compose up --build
```
This starts the Flask app, Redis, and a Celery worker.

Run the frontend:

```bash
cd frontend
npm run dev
```

The app expects the backend at `http://127.0.0.1:5001`, and the frontend typically runs on `http://localhost:5173`.


## Project Structure

```text
trekking-management-application-V2/
├── backend/
│   ├── app.py                  # Flask app entry point
│   ├── auth.py                 # Authentication routes
│   ├── modules.py              # SQLAlchemy models
│   ├── tasks.py                # Celery tasks
│   ├── admin/                  # Admin blueprint and logic
│   ├── staff/                  # Staff blueprint and logic
│   ├── user/                   # User blueprint and logic
│   ├── Dockerfile              # Backend container image
│   ├── docker-compose.yml      # Backend, Redis, Celery stack
│   └── requirements.txt        # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── main.js             # Vue app bootstrap
│   │   ├── App.vue             # Main layout
│   │   ├── router/             # Client-side routes
│   │   ├── services/           # API helper layer
│   │   └── views/              # Pages and role dashboards
│   ├── package.json            # Frontend dependencies and scripts
│   └── vite.config.js          # Vite configuration
└── README.md
```

## Notes

- The frontend API helper is configured to call `http://127.0.0.1:5001`.
- Admin, staff, and user dashboards are route-based and protected by JWT role claims.
- Celery is used to send staff credential emails asynchronously.
