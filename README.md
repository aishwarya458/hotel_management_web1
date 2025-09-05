# hotel_management_web1
A Django-based hotel booking platform.
This project allows users to search and book hotels and vendors to manage their hotel listings.

✨ Features
👤 User Features

Register, Login, and Logout

Search hotels by name

View hotel details

Responsive UI with Bootstrap

Email and OTP based authentication



🏪 Vendor Features

Vendor Registration and Login

Add and manage hotels

Upload hotel details with amenities

Manage hotel listings

Email and OTP based authentication




⚙️ Tech Stack

Backend: Django (Python)

Frontend: HTML, CSS, Bootstrap, JavaScript

Database: MySQL

Other: AJAX for dynamic loading

🛠️ Installation & Setup
1. Clone the repo
git clone https://github.com/your-username/oyo_clone.git
cd oyo_clone



3. Create a virtual environment
python -m venv venv


Activate it:

Windows (PowerShell):

venv\Scripts\activate


Mac/Linux:

source venv/bin/activate



3. Install dependencies
pip install -r requirements.txt



4. Configure Database

Update your settings.py with MySQL credentials:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'oyo_clone_db',
        'USER': 'root',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


5.Configure Messages
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email'
EMAIL_HOST_PASSWORD = 'email_password'


6. Run Migrations
python manage.py makemigrations
python manage.py migrate


8. Create Superuser
python manage.py createsuperuser

9. Run Server
python manage.py runserver


Now open 👉 http://127.0.0.1:8000/


<img width="1902" height="837" alt="image" src="https://github.com/user-attachments/assets/06b27f18-a67a-424f-b094-c65f911786b2" />
<img width="853" height="645" alt="image" src="https://github.com/user-attachments/assets/0bf01fd8-8fb7-49d5-afda-584bda9ef542" />
<img width="1782" height="920" alt="image" src="https://github.com/user-attachments/assets/32ae0364-a907-48da-b0cf-f5ac0dee47d1" />




