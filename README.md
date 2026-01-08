# Help Decorah Project Backend part

## ⚙️ Backend Development & API Design
The backend of HelpDecorah serves as the central engine for data management and secure user interactions, built with a focus on scalability and clean architecture.

## Description
Help Decorah is a web application designed and created for the town Decorah. It helps users to sign up to different commutity work and also allows admins to assign work for the community.

## Key Technical Features:

Robust Framework: Developed using Python and the Flask web framework.

Relational Database Management: Designed a relational database schema using SQLAlchemy ORM to manage users, community tasks, and volunteer registrations.

Implemented a many-to-many relationship via a Signup association table, allowing multiple users to register for multiple tasks.

Secure Authentication: * Integrated Google OAuth 2.0 for industry-standard secure user login, utilizing Flask-Login for session management.

Established an Admin Authorization layer based on unique Google IDs to protect sensitive operations like creating or deleting community tasks.

Automated Data Serialization: Leveraged Marshmallow and flask-marshmallow to automatically convert complex database models into JSON format for seamless frontend integration.

Comprehensive REST API Endpoints: Built full CRUD functionality (Create, Read, Update, Delete) for task management.

## Video demonstration user interface:

## Video demonstration admin interface:
