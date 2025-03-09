# Task Manager - Django Project

A comprehensive task management system built with Django and TailwindCSS. Features include project management, task tracking, team collaboration, and role-based access control.

## Features

- User Authentication & Role-based Access Control
- Project Management
- Task Management with Priority & Status Tracking
- Team Collaboration
- Responsive UI with Dark Mode Support
- Modern UI with TailwindCSS and Flowbite Components

## Prerequisites

- Python 3.12 or higher
- pip (Python package manager)
- Node.js and npm (for TailwindCSS)

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd TrelloClone
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # Linux/MacOS
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Node Dependencies**
   ```bash
   npm install
   ```

5. **Initialize Database**
   ```bash
   python manage.py migrate
   ```

6. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```
   When prompted:
   - Enter your desired username
   - Enter your email address (optional)
   - Enter and confirm your password
     Note: The password won't be visible as you type
   
   Example:
   ```
   Username: admin
   Email address: admin@example.com
   Password: 
   Password (again):
   Superuser created successfully.
   ```

7. **Configure Superuser as Admin**
   ```bash
   # Run the custom management command to make the superuser an admin
   python manage.py fix_user_profiles --username admin
   ```
   Replace 'admin' with your superuser's username if different.

   Alternatively, you can:
   1. Log in to the Django admin panel at `http://localhost:8000/admin`
   2. Click on "User profiles" under the Tasks section
   3. Find your superuser's profile
   4. Change the role from "Standard User" to "Admin"
   5. Click "Save"

8. **Build TailwindCSS**
   ```bash
   # Development (with watch mode)
   npm run watch

   # Production build
   npm run build
   ```

9. **Run Development Server**
   ```bash
   python manage.py runserver
   ```
   The application will be available at `http://localhost:8000`

### Important URLs

- Main Application: `http://localhost:8000`
- Admin Panel: `http://localhost:8000/admin`
- Task List: `http://localhost:8000/tasks`
- Project List: `http://localhost:8000/projects`

## Development

### Running TailwindCSS in Development Mode

```bash
npm run dev
```

This will start TailwindCSS in watch mode, automatically rebuilding the CSS when you make changes.

### Database Migrations

When making changes to models:

```bash
python manage.py makemigrations
python manage.py migrate
```

## User Roles

1. **Admin Users**
   - Can create and manage projects
   - Can create, update, and delete tasks
   - Have access to all projects and tasks
   - Can manage team members

2. **Standard Users**
   - Can view projects they are members of
   - Can create tasks
   - Can update and delete their own tasks
   - Can view tasks assigned to them

## Project Structure

```
TrelloClone/
├── manage.py
├── requirements.txt
├── package.json
├── task_manager/          # Project settings
├── tasks/                 # Main application
│   ├── models.py         # Database models
│   ├── views.py          # View logic
│   ├── urls.py          # URL routing
│   └── templates/       # HTML templates
├── static/               # Static files
│   └── src/             # TailwindCSS source
└── templates/            # Base templates
```

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
