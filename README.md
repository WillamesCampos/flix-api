# 🎬 Flix API

> **🇧🇷 Portuguese Version Available**: [README_ptBR.md](README_ptBR.md)

RESTful API built with Django and Django REST Framework for managing movies, actors, genres, and reviews. The project was developed following Django best practices, with modular architecture, comprehensive tests, and CI/CD configured.

## 📋 Table of Contents

- [About the Project](#-about-the-project)
- [Features](#-features)
- [Technologies](#-technologies)
- [Prerequisites](#-prerequisites)
- [Installation and Setup](#-installation-and-setup)
- [Usage](#-usage)
- [Makefile Commands](#-makefile-commands)
- [Testing](#-testing)
- [Project Structure](#-project-structure)
- [Deployment](#-deployment)
- [Challenges and Solutions](#-challenges-and-solutions)
- [Contributing](#-contributing)
- [Author](#-author)

## 🎯 About the Project

Flix API is a complete backend application for managing a movie catalog. The project was developed as part of learning API development with Django REST Framework, implementing advanced concepts such as:

- JWT Authentication
- Custom permissions based on models
- Serializers with complex validations
- Automated tests with high coverage
- Complex database migrations
- Service-based architecture
- Integration with multiple databases (PostgreSQL and MongoDB)

## 🚀 Features

### Complete CRUD
- ✅ **Movies**: Complete movie management with relationships to actors and genres
- ✅ **Actors**: CRUD for actors with nationality and birthdate information
- ✅ **Genres**: Movie category management
- ✅ **Reviews**: Rating system with scores and comments

### Special Features
- 📊 **Movie Statistics**: Dedicated endpoint for aggregated statistics
- 📥 **CSV Import**: Django commands to import actors and movies via CSV files
  - See [Actor CSV Format](instructions/import_csv/actors.md)
  - See [Movie CSV Format](instructions/import_csv/movies.md)
- 🔐 **JWT Authentication**: Complete authentication system with tokens
- 🛡️ **Permission System**: Granular permissions based on models and actions

## 🧰 Technologies

### Backend
- **Python 3.13**
- **Django 5.2.1** - Web framework
- **Django REST Framework 3.16.0** - REST API framework
- **Django REST Framework Simple JWT 5.5.0** - JWT authentication

### Database
- **PostgreSQL** - Main relational database
- **MongoDB** - NoSQL database (for logs and non-relational data)

### Development Tools
- **Poetry** - Dependency management
- **Pytest** - Testing framework
- **Ruff** - Code linter and formatter
- **Factory Boy** - Test fixtures creation
- **Coverage** - Test coverage analysis

### DevOps
- **Docker** - Application containerization
- **Docker Compose** - Container orchestration
- **GitHub Actions** - CI/CD

## 📦 Prerequisites

Before starting, you need to have installed on your machine:

- **Python 3.11+**
- **Poetry** ([Installation](https://python-poetry.org/docs/#installation))
- **Docker** and **Docker Compose** ([Installation](https://docs.docker.com/get-docker/))
- **Git**

## 🔧 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/WillamesCampos/flix-api.git
cd flix-api
```

### 2. Configure environment variables

Create a `.env` file in the project root with the following variables:

```env
# Django
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=DEV
ALLOWED_HOSTS=*

# PostgreSQL
POSTGRES_DB=flix_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-postgres-password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# MongoDB
MONGO_INITDB_ROOT_USERNAME=root
MONGO_INITDB_ROOT_PASSWORD=your-mongo-password
MONGO_INITDB_DATABASE=flix_logs
MONGO_URI=mongodb://root:your-mongo-password@mongo:27017/flix_logs?authSource=admin
```

### 3. Install dependencies

```bash
poetry install
```

### 4. Run with Docker (Recommended)

```bash
# Build and start containers
make up-build

# Or start in background
make up-d

# Run migrations
make migrate
```

### 5. Or run locally

```bash
# Start only the database
make dev-db
make dev-mongo

# Run migrations
python manage.py migrate

# Create a superuser (optional)
python manage.py createsuperuser

# Start the server
make run-dev
```

The API will be available at `http://localhost:8000`

## 📖 Usage

### Authentication

First, obtain a JWT token:

```bash
curl -X POST http://localhost:8000/api/v1/authentication/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your-username",
    "password": "your-password"
  }'
```

Use the returned token in subsequent requests:

```bash
curl -X GET http://localhost:8000/api/v1/movies/ \
  -H "Authorization: Bearer your-token-here"
```

### Main Endpoints

#### Movies
- `GET /api/v1/movies/` - List all movies
- `POST /api/v1/movies/` - Create a new movie
- `GET /api/v1/movies/{uuid}/` - Get movie details
- `PATCH /api/v1/movies/{uuid}/` - Update a movie
- `DELETE /api/v1/movies/{uuid}/` - Delete a movie
- `GET /api/v1/movies/stats/` - Movie statistics

#### Actors
- `GET /api/v1/actors/` - List all actors
- `POST /api/v1/actors/` - Create a new actor
- `GET /api/v1/actors/{uuid}/` - Get actor details
- `PATCH /api/v1/actors/{uuid}/` - Update an actor
- `DELETE /api/v1/actors/{uuid}/` - Delete an actor

#### Genres
- `GET /api/v1/genres/` - List all genres
- `POST /api/v1/genres/` - Create a new genre
- `GET /api/v1/genres/{uuid}/` - Get genre details
- `PATCH /api/v1/genres/{uuid}/` - Update a genre
- `DELETE /api/v1/genres/{uuid}/` - Delete a genre

#### Reviews
- `GET /api/v1/reviews/` - List all reviews
- `POST /api/v1/reviews/` - Create a new review
- `GET /api/v1/reviews/{uuid}/` - Get review details
- `PATCH /api/v1/reviews/{uuid}/` - Update a review
- `DELETE /api/v1/reviews/{uuid}/` - Delete a review

### CSV Import Commands

#### Import Actors

```bash
python manage.py import_actors path/to/file.csv
```

For the CSV file format, see [instructions/import_csv/actors.md](instructions/import_csv/actors.md)

#### Import Movies

```bash
python manage.py import_movies path/to/file.csv
```

For the CSV file format, see [instructions/import_csv/movies.md](instructions/import_csv/movies.md)

## 🛠️ Makefile Commands

The project has a complete Makefile to facilitate development. Run `make help` to see all available commands.

### Docker

```bash
make up              # Start all Docker services
make up-d            # Start all Docker services in background
make up-build         # Build and start Docker services
make down             # Stop and remove Docker services
make logs             # Show Docker services logs
make build            # Build Docker image
make build-image      # Build Docker image for publishing
make push             # Publish Docker image to registry
make dev-db           # Start only database in background
make dev-mongo        # Start only MongoDB in background
make destroy-db       # Stop and remove database container
make destroy-web      # Stop and remove web application container
```

### Django

```bash
make migrate          # Run Django migrations (Docker)
make makemigrations   # Create new Django migrations (Docker)
make run              # Start Django development server (Docker)
make run-dev          # Start Django development server (local)
make shell            # Open Django shell (Docker)
make shell-dev        # Open Django shell (local)
```

### Testing

```bash
make test             # Run tests and generate coverage report
make test-docker      # Run tests inside Docker container
make coverage         # Show coverage report
make coverage-html    # Generate HTML coverage report
```

### Linting and Formatting

```bash
make lint             # Check code with ruff
make fix              # Fix issues found by ruff
make format           # Format code with ruff
```

## 🧪 Testing

The project has a complete test suite with high code coverage.

### Run Tests

```bash
# Run all tests
make test

# Run tests with more verbosity
pytest -vvv

# Run tests for a specific app
pytest movies/tests/

# Run a specific test
pytest movies/tests/test_views.py::TestMoviesAPI::test_create_movie_success
```

### Code Coverage

The project maintains a minimum coverage of 75%. To view the report:

```bash
make coverage        # Terminal report
make coverage-html   # HTML report in htmlcov/
```

## 📂 Project Structure

```
flix-api/
├── actors/              # Actors App
│   ├── management/      # Custom Django commands
│   ├── migrations/      # Database migrations
│   ├── tests/          # App tests
│   ├── models.py       # Data models
│   ├── serializers.py  # API serializers
│   ├── views.py        # API views
│   └── urls.py         # App routes
├── genres/             # Genres App
├── movies/              # Movies App
│   └── services/        # Business services
├── reviews/            # Reviews App
├── authentication/     # JWT Authentication
├── core/               # Shared base models
├── app/                # Main settings
│   ├── settings.py     # Django settings
│   ├── permissions.py  # Custom permissions
│   └── urls.py         # Main URLs
├── logs/               # Logging system
├── conftest.py         # Pytest configuration
├── docker-compose.yml  # Docker Compose configuration
├── Dockerfile          # Docker image
├── Makefile           # Automated commands
├── pyproject.toml     # Poetry configuration
└── README.md          # This file
```

### Architecture

The project follows a modular architecture where each Django app is responsible for a specific domain:

- **Separation of concerns**: Each app has its own business logic
- **Base models**: Use of `BaseModel` for common fields (UUID, timestamps, auditing)
- **Services**: Complex business logic isolated in service classes
- **Permissions**: Centralized and reusable permission system

## 🚀 Deployment

### Docker Hub

The project is configured for automatic publishing to Docker Hub through GitHub Actions.

```bash
# Build image for production
make build-image TAG=v1.0.0

# Publish to Docker Hub
make push TAG=v1.0.0
```

### GitHub Actions

The project has configured workflows for:

- **Quality Assurance**: Runs lint and tests on Pull Requests
- **Docker Image Release**: Publishes Docker images when tags are created
- **Publish**: Complete validation and publishing pipeline

### Production Environment Variables

Make sure to configure the following variables in the production environment:

```env
DEBUG=False
DJANGO_SECRET_KEY=strong-secret-key
ALLOWED_HOSTS=your-domain.com
# ... other variables
```

## 🎓 Challenges and Solutions

### 1. Migration from ID to UUID as Primary Key

**Challenge**: Migrate all models from `id` (BigAutoField) to `uuid` (UUIDField) as primary key, maintaining data integrity and relationships.

**Solution**:
- Creation of sequential migrations that remove the `id` field and add `uuid`
- Implementation of `BaseModel` with UUID as default PK
- Special migration for ManyToMany intermediate table (`movies_movie_actors`)
- Update of all tests and serializers to use `uuid` instead of `id`

**Lessons Learned**:
- In production, it would be necessary to create a manual mapping table
- Safer approach: create UUID as unique field first, then migrate gradually
- Always backup before complex structural migrations

### 2. ManyToMany Intermediate Table

**Challenge**: The intermediate table `movies_movie_actors` maintained `bigint` references while models used UUID.

**Solution**:
- Creation of migration that removes old constraints
- Table cleanup (in development)
- Recreation of columns with UUID type
- Recreation of all constraints and foreign keys

### 3. Custom Permission System

**Challenge**: Implement a granular permission system based on models and actions.

**Solution**:
- Creation of `GlobalDefaultPermission` that checks Django default permissions
- Integration with Django groups and permissions system
- Reuse in all views through `permission_classes`

### 4. High Coverage Testing

**Challenge**: Maintain test coverage above 75% with meaningful tests.

**Solution**:
- Use of `Factory Boy` to create test fixtures
- Creation of `BaseAPITest` for reusable API tests
- Unit tests for models, serializers, and services
- Integration tests for views and endpoints

### 5. CI/CD with GitHub Actions

**Challenge**: Configure complete CI/CD pipeline with tests, lint, and image publishing.

**Solution**:
- Separate workflows for QA and publishing
- Test execution in isolated environment with PostgreSQL
- Automatic Docker image publishing to Docker Hub
- Quality validation before publishing

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Standards

- Follow the code style defined by Ruff
- Run `make lint` and `make format` before committing
- Maintain test coverage above 75%
- Write tests for new features

## 👤 Author

**Willames Campos**

- GitHub: [@WillamesCampos](https://github.com/WillamesCampos)
- Email: willwjccampos@gmail.com

## 🙏 Acknowledgments

- Django and Django REST Framework for excellent documentation
- Python/Django community for support
- All maintainers of the open-source libraries used

---

⭐ If this project was useful to you, consider giving it a star on the repository!
