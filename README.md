# Eventorize API

## Introduction
The Eventorize API is the backend service powering the Eventorize platform, a comprehensive event management solution. Built with FastAPI, this API provides the core functionalities needed to manage users, events, tickets, and more. The API is designed for high performance, scalability, and ease of integration, making it a reliable backbone for both the Eventorize frontend and any third-party applications.

This repository contains all the backend logic, database interactions, and API endpoints necessary to support the full range of features offered by the Eventorize platform.



## Features

- **User Authentication and Authorization**: Implements secure user authentication using JWT, ensuring that all endpoints are protected and user sessions are securely managed.
- **Event Management**: Provides endpoints to create, update, delete, and retrieve events. This includes managing event details, schedules, and associated venues.
- **Ticketing System**: Handles all ticketing operations, including issuing, validating, and managing tickets for events. Supports multiple ticket types and pricing options.
- **User Profiles**: Allows users to manage their profiles, view their registered events, and access their tickets through secure API calls.
- **Analytics and Reporting**: Offers data endpoints for retrieving analytics related to events, such as attendance numbers, ticket sales, and user engagement metrics.
- **RESTful API Design**: Follows RESTful principles, making it easy to integrate with various frontend applications and third-party services.
- **Comprehensive Documentation**: Auto-generated API documentation with FastAPI's integrated Swagger and ReDoc, providing developers with detailed information on how to interact with the API.
- **Scalable and Extensible**: Built with scalability in mind, using asynchronous programming to handle high traffic and offering easy extension for future features.

## Getting Started

### Prerequisites

- [Python](https://www.python.org/)
- [Pip](https://pip.pypa.io/en/stable/installation/)
- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### Cloning the Repository
First, clone the repository from GitLab and navigate into the project directory:
```bash
git clone https://github.com/ellyx13/eventorize-api.git
cd eventorize-api
```

### Setting Up the Environment
1. Create a folder named `.env`:
```bash
mkdir .env
```

2. Create a file named `dev.env` inside the `.env` folder and fill it with the following content. You can get the `SECRET_KEY` from [this link](https://8gwifi.org/jwsgen.jsp) by selecting `HS512` and clicking "Generate JWS Keys". Then, copy the `SharedSecret`:
```plaintext
environment=dev
app_database_name=app
database_url=mongodb://db?retryWrites=true

# Authentication 
SECRET_KEY={ENTER_YOUR_SECRET_KEY}
ALGORITHM="HS512"
DEFAULT_ADMIN_EMAIL={ENTER_YOUR_DEFAULT_EMAIL}
DEFAULT_ADMIN_PASSWORD={ENTER_YOUR_DEFAULT_PASSWORD}
```

3. Create a file named `test.env` inside the `.env` folder, and add the following content:
```plaintext
ENVIRONMENT=test
database_url=mongodb://db-test?retryWrites=true
```

### Install pre-commit
1. Download [pre-commit](https://pre-commit.com/):
```bash
pip install pre-commit
```
2. Install pre-commit
```
pre-commit install
```

### Running on Linux

To start the project on a Linux machine:

1. Open your terminal.
2. Navigate to the project directory.
3. Run the following command to make the script executable and start the Docker containers:
```bash
chmod +x bin/linux/start.sh
bin/linux/start.sh
```

### Running on Windows

To start the project on a Windows machine:

1. Open Command Prompt or PowerShell.
2. Navigate to the project directory.
3. Run the following command to start the Docker containers:
```cmd
bin\windows\start.bat
```

This script will build and start the Docker containers for the FastAPI application and MongoDB database.

### Accessing the API
Once the containers are up and running, you can access the FastAPI application by navigating to:

```
http://localhost:8005
```

You can explore the automatically generated API documentation at:

- Swagger UI: [http://localhost:8005/docs](http://localhost:8005/docs)
- ReDoc: [http://localhost:8005/redoc](http://localhost:8005/redoc)

### Stopping the Project

To stop the Docker containers, use the following commands based on your operating system:

#### Linux & Windows

Press `Ctrl + C`

This will stop and remove the containers, networks, and volumes created by Docker Compose.
