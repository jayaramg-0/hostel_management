# Hostel Management System

A comprehensive web-based Hostel Management System built with Django and MySQL for college/university hostels. This system provides complete management of student accommodation, attendance, fees, complaints, and more.

## Features

### For Admin
- **Dashboard**: Overview with statistics, charts, and quick actions
- **Student Management**: Add, edit, view, and manage student records
- **Room Management**: Create rooms, assign students, track occupancy
- **Attendance Management**: Mark daily attendance, view reports
- **Visitor Management**: Track visitor check-in/check-out
- **Complaint Management**: View and resolve student complaints
- **Fee Management**: Create fee records, track payments, mark as paid
- **Notice Board**: Post announcements and notices
- **Leave Requests**: Approve/reject student leave applications
- **Reports**: Generate Excel reports for students, fees, attendance

### For Students
- **Dashboard**: Personal overview with room info, fees, attendance
- **Profile**: View and update personal information
- **Attendance**: View personal attendance history
- **Fees**: View fee status and payment history
- **Complaints**: Submit and track complaints
- **Leave Requests**: Apply for leave and view status
- **Notices**: View hostel notices and announcements

## Technology Stack

- **Backend**: Django 5.x
- **Database**: MySQL
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Forms**: Django Crispy Forms with Bootstrap 5
- **Charts**: Chart.js
- **Icons**: Bootstrap Icons
- **Reports**: OpenPyXL (Excel), ReportLab (PDF)

## Installation

### Prerequisites
- Python 3.10+
- MySQL 8.0+
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
cd /path/to/your/projects
git clone <repository-url>
cd hostel_management
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Database
1. Create a MySQL database:
```sql
CREATE DATABASE hostel_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'hostel_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON hostel_db.* TO 'hostel_user'@'localhost';
FLUSH PRIVILEGES;
```

2. Update `hostel_management/settings.py` with your database credentials:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hostel_db',
        'USER': 'hostel_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Step 5: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### Step 7: Run Development Server
```bash
python manage.py runserver
```

Access the application at `http://127.0.0.1:8000`

## Project Structure

```
hostel_management/
├── hostel_management/      # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/               # User authentication & profiles
├── students/               # Student management
├── rooms/                  # Room management
├── attendance/             # Attendance tracking
├── visitors/               # Visitor management
├── complaints/             # Complaint system
├── fees/                   # Fee management
├── notices/                # Notice board
├── leave_requests/         # Leave applications
├── dashboard/              # Dashboard & reports
├── templates/              # HTML templates
├── static/                 # Static files (CSS, JS)
├── media/                  # Uploaded files
├── requirements.txt        # Python dependencies
└── manage.py
```

## User Roles

### Admin
- Full access to all modules
- Can manage students, rooms, fees, attendance
- Can approve/reject leave requests
- Can resolve complaints
- Can generate reports

### Student
- Limited access to personal data
- Can view attendance, fees, room details
- Can submit complaints and leave requests
- Can update profile information

## Default URLs

| URL | Description |
|-----|-------------|
| `/` | Home/Login page |
| `/accounts/login/` | Login |
| `/accounts/register/` | Student registration |
| `/dashboard/` | Admin/Student dashboard |
| `/students/` | Student management |
| `/rooms/` | Room management |
| `/attendance/` | Attendance management |
| `/visitors/` | Visitor management |
| `/complaints/` | Complaints |
| `/fees/` | Fee management |
| `/notices/` | Notice board |
| `/leave/` | Leave requests |
| `/reports/` | Reports (Admin only) |

## Environment Variables

Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_NAME=hostel_db
DATABASE_USER=hostel_user
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=3306
```

## Screenshots

(Add screenshots of your application here)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Developed as a Final Year Project for College/University.

## Support

For support, please create an issue in the repository or contact the development team.
