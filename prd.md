Here's a detailed Product Requirements Document (PRD) for the AI Agent to understand and create the project. The tasks are divided into smaller, manageable steps for better clarity:

### Product Requirements Document (PRD)

---

### **1. Project Overview**
Design and implement a web-based task management system for a small project management company, enabling streamlined task tracking and management with a backend in Python (Django) and frontend in HTML, CSS (TailwindCSS), and JavaScript.

---

### **2. Features and Functionalities**
1. **UI Design (Responsive)**
    - Design a responsive layout that adjusts to different screen sizes (desktop, tablet, mobile).
    - Use TailwindCSS for styling.
    - Include a landing page and a functional navbar.

2. **User Authentication (Login/Register)**
    - Implement user authentication with login and registration functionality.
    - Include user roles (Standard User and Admin).
    - Admins should have access to full CRUD operations (create, read, update, delete) for tasks.
    - Standard users should have the ability to view and add new tasks.

3. **Task Management**
    - Allow users to create, update, insert, and delete tasks.
    - Admin can perform full CRUD operations, while standard users can only view and add tasks.
    - Each task should have:
        - Title
        - Description
        - Due date
        - Priority (High, Medium, Low)
        - Status (Started, In-Progress, Completed)
    - Tasks should be categorized into different projects.
    - Implement a CRUD interface for tasks.

4. **User Roles (Standard User and Admin)**
    - Standard User: Can view tasks, add new tasks, and view projects.
    - Admin: Can manage users, tasks, projects, and roles.

5. **Database Design**
    - Create models for:
        - **User** (Employee and Project Manager)
        - **Project**
        - **Task** (with states: Started, In-Progress, Completed)
        - **Team** (Comprises Employees)
    - Use SQLite as the database for the Django app.
    - Implement necessary relationships (e.g., one-to-many between Project and Tasks).

6. **Testing**
    - Test user authentication.
    - Test CRUD operations on tasks (for both Admin and Standard users).
    - Ensure proper database relationships are maintained.

7. **Deployment**
    - Deploy the application on a platform of your choice (e.g., Heroku, AWS, DigitalOcean).

---

### **3. Breakdown into Smaller Tasks**


#### **Task 0: Set Up Development Environment**
- **Sub-task 0.1**: Create a Python virtual environment for the project.
    - Command: `python312 -m venv venv`
- **Sub-task 0.2**: Activate the virtual environment.
    - On Windows: `.\venv\Scripts\activate`
    - On macOS/Linux: `source venv/bin/activate`
- **Sub-task 0.3**: Install the necessary dependencies.
    - Install Django: `pip install django`
    - Install TailwindCSS for integration with Django (if using Django-Tailwind): `pip install django-tailwind`
    - Create a `requirements.txt` file for easy dependency management: `pip freeze > requirements.txt`
- **Sub-task 0.4**: Initialize a new Django project.
    - Command: `django-admin startproject task_manager`
- **Sub-task 0.5**: Create a Django app within the project to handle task management.
    - Command: `python manage.py startapp tasks`


#### **Task 1: UI Design (Responsive)**
- **Sub-task 1.1**: Create a layout for the landing page.
- **Sub-task 1.2**: Design a navbar that includes links for login/register and task management (for both Admin and Standard Users).
- **Sub-task 1.3**: Make the layout responsive using TailwindCSS (mobile-first approach).
- **Sub-task 1.4**: Design the task list page (with filters based on task status).
- **Sub-task 1.5**: Design the task creation form with input fields for title, description, due date, priority, and status.

#### **Task 2: User Authentication**
- **Sub-task 2.1**: Implement user registration form (using Django’s authentication system).
- **Sub-task 2.2**: Implement login form.
- **Sub-task 2.3**: Define roles for Standard User and Admin in the database.
- **Sub-task 2.4**: Set permissions for different user roles (Standard User can only add/view tasks, Admin has full CRUD capabilities).

#### **Task 3: Task Management**
- **Sub-task 3.1**: Implement CRUD operations for tasks for Admin users.
- **Sub-task 3.2**: Implement the task viewing and adding functionality for Standard Users.
- **Sub-task 3.3**: Create a form for task creation, including fields for task title, description, due date, priority, and status.
- **Sub-task 3.4**: Implement task editing and deleting features for Admin.
- **Sub-task 3.5**: Implement task categorization into different projects.

#### **Task 4: Database Design**
- **Sub-task 4.1**: Create the User model with fields for username, password, role, and any necessary fields.
- **Sub-task 4.2**: Design the Project model.
- **Sub-task 4.3**: Design the Task model with fields for title, description, due date, priority, status, and a foreign key relationship with Projects.
- **Sub-task 4.4**: Create the Team model with a many-to-many relationship to the User model.

#### **Task 5: Testing**
- **Sub-task 5.1**: Write test cases for user authentication (register and login).
- **Sub-task 5.2**: Write test cases for CRUD operations on tasks.
- **Sub-task 5.3**: Test role-based access control (admin and standard user permissions).
- **Sub-task 5.4**: Test the task filtering and sorting functionalities.

#### **Task 6: Deployment**
- **Sub-task 6.1**: Set up deployment on a platform (e.g., Heroku or AWS).
- **Sub-task 6.2**: Configure the database for production.
- **Sub-task 6.3**: Deploy the app and test on the deployed platform.

---

### **4. Technology Stack**
- **Backend**: Python (Django)
- **Frontend**: HTML, CSS (TailwindCSS), JavaScript
- **Database**: SQLite (default in Django)
- **Deployment**: Heroku or AWS (choose based on preference)

---

### **5. Deliverables**
1. Complete web-based task management system with user authentication and role-based task management.
2. Responsive UI design with TailwindCSS.
3. All necessary database models and relationships.
4. Unit and integration tests for the system.
5. Deployed application on a chosen platform.

---

By following this detailed PRD, the AI Agent can tackle each task step by step, ensuring that each feature and functionality is correctly implemented and tested before proceeding to the next.