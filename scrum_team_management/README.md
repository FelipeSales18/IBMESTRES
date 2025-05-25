# Scrum Team Management Application

This is a Django-based application designed for managing SCRUM teams. It provides features for project creation, team management, and role-based access control for Team Leaders and Collaborators.

## Features

- **User Roles**: Different access levels for Team Leaders and Collaborators.
- **Project Management**: Create and manage projects effectively.
- **Team Management**: Organize team members and assign roles.
- **Role-Based Access Control**: Ensure that users have appropriate permissions based on their roles.

## Setup Instructions

1. **Clone the Repository**:
   ```
   git clone <repository-url>
   cd scrum_team_management
   ```

2. **Install Dependencies**:
   Ensure you have Python and pip installed, then run:
   ```
   pip install -r requirements.txt
   ```

3. **Run Migrations**:
   Prepare the database by running:
   ```
   python manage.py migrate
   ```

4. **Create a Superuser**:
   To access the admin panel, create a superuser:
   ```
   python manage.py createsuperuser
   ```

5. **Run the Development Server**:
   Start the server with:
   ```
   python manage.py runserver
   ```

6. **Access the Application**:
   Open your browser and go to `http://127.0.0.1:8000/`.

## Directory Structure

- `manage.py`: Command-line utility for managing the project.
- `requirements.txt`: Lists project dependencies.
- `scrum_team_management/`: Main project directory containing settings and configurations.
- `projects/`: Application for managing projects.
- `teams/`: Application for managing teams.
- `users/`: Application for user management and authentication.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.