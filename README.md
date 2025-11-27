<div align="center">
  <img width="250" height="250" alt="Flix API Logo" src="https://github.com/user-attachments/assets/440f8f65-1f9e-4a9a-98e7-1cfd1a73f8e6" />
</div>

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
- 📄 **Pagination**: Custom pagination with configurable page size (10 items per page, max 50)
- 🤖 **AI-Powered Description Suggestions**: Generate movie descriptions using OpenAI GPT models via adapter pattern

## 🧰 Technologies

### Backend
- **Python 3.13**
- **Django 5.2.1** - Web framework
- **Django REST Framework 3.16.0** - REST API framework
- **Django REST Framework Simple JWT 5.5.0** - JWT authentication
- **OpenAI** - AI integration for description generation

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

Copy the `.env.example` file to `.env` and fill in the values:

```bash
cp .env.example .env
```

Then edit the `.env` file with your actual values. See `.env.example` for all available environment variables. Here are the main required variables:

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

# OpenAI (for AI description suggestions)
OPENAI_API_KEY=your-openai-api-key-here
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
- `GET /api/v1/movies/` - List all movies (paginated)
- `POST /api/v1/movies/` - Create a new movie
  - Optional: `ai_description=true` to generate description with AI
- `GET /api/v1/movies/{uuid}/` - Get movie details
- `PATCH /api/v1/movies/{uuid}/` - Update a movie
  - Optional: `ai_description=true` to regenerate description with AI
- `DELETE /api/v1/movies/{uuid}/` - Delete a movie
- `GET /api/v1/movies/stats/` - Movie statistics
- `POST /api/v1/movies/suggest-description/` - Get AI-generated description suggestion for a movie

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

### Pagination

All list endpoints support pagination with the following query parameters:
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 10, max: 50)

Example:
```bash
curl -X GET "http://localhost:8000/api/v1/movies/?page=2&page_size=20" \
  -H "Authorization: Bearer your-token-here"
```

### AI Description Suggestions

Generate movie descriptions using OpenAI:

```bash
# Get a description suggestion for a movie
curl -X POST http://localhost:8000/api/v1/movies/suggest-description/ \
  -H "Authorization: Bearer your-token-here" \
  -H "Content-Type: application/json" \
  -d '{"movie_uuid": "movie-uuid-here"}'

# Or create/update a movie with AI description
curl -X POST http://localhost:8000/api/v1/movies/ \
  -H "Authorization: Bearer your-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Inception",
    "ai_description": true
  }'
```

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
make up-build        # Build and start Docker services
make down            # Stop and remove Docker services
make logs            # Show Docker services logs
make build           # Build Docker image
make build-image     # Build Docker image for publishing
make push            # Publish Docker image to registry
make dev-db          # Start only database in background
make dev-mongo       # Start only MongoDB in background
make dev-celery      # Start only Celery worker in background
make dev             # Start development services (db, mongo, celery)
make destroy-db      # Stop and remove database container
make destroy-web     # Stop and remove web application container
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
├── apps/
│   ├── actors/              # Actors App
│   │   ├── management/      # Custom Django commands
│   │   ├── migrations/      # Database migrations
│   │   ├── services/        # Business services
│   │   ├── tests/           # App tests
│   │   ├── models.py        # Data models
│   │   ├── serializers.py   # API serializers
│   │   ├── views.py         # API views
│   │   └── urls.py          # App routes
│   ├── genres/              # Genres App
│   ├── movies/              # Movies App
│   │   ├── mixins/          # Reusable mixins
│   │   │   ├── audit_entity_mixin.py
│   │   │   └── movie_suggestor_description_mixin.py
│   │   ├── services/        # Business services
│   │   │   ├── import_service.py
│   │   │   ├── movie_suggestor_description_service.py
│   │   │   └── stats_service.py
│   │   ├── management/      # Custom Django commands
│   │   └── tests/           # App tests
│   ├── reviews/             # Reviews App
│   │   ├── services/        # Business services
│   │   ├── signals.py       # Django signals
│   │   └── tasks.py         # Celery tasks
│   ├── authentication/      # JWT Authentication
│   ├── core/                # Shared utilities
│   │   ├── adapters/        # Adapter pattern implementations
│   │   │   └── ai_adapters/ # AI service adapters
│   │   │       ├── base.py  # Abstract adapter interface
│   │   │       └── open_ai_adapter.py
│   │   ├── services/        # Shared services
│   │   └── models.py        # Base models
│   └── logs/                # Logging system
├── app/                     # Main settings
│   ├── settings.py          # Django settings
│   ├── permissions.py       # Custom permissions
│   ├── pagination.py        # Custom pagination
│   ├── decorators.py        # Request logging decorators
│   ├── celery.py            # Celery configuration
│   └── urls.py              # Main URLs
├── infrastructure/          # Docker configuration
│   ├── docker-compose.yml
│   ├── Dockerfile
│   └── Dockerfile.celery
├── conftest.py              # Pytest configuration
├── Makefile                 # Automated commands
├── pyproject.toml          # Poetry configuration
└── README.md               # This file
```

### Architecture

The project follows a modular architecture where each Django app is responsible for a specific domain:

- **Separation of concerns**: Each app has its own business logic
- **Base models**: Use of `BaseModel` for common fields (UUID, timestamps, auditing)
- **Services**: Complex business logic isolated in service classes
- **Permissions**: Centralized and reusable permission system
- **Mixins**: Reusable behavior through mixin classes (e.g., `MovieSuggestorDescriptionMixin`)
- **Adapter Pattern**: AI service integration through adapter pattern for flexibility and testability

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

### 6. Asynchronous Tasks with Celery and Redis

**Challenge**: Implement email notifications when reviews are created without blocking the API response.

**Solution**:
- **Celery** for asynchronous task execution
- **Redis** as message broker between Django and Celery workers
- **Django Signals** to automatically trigger tasks when reviews are created
- Separate Docker containers for web application and Celery worker

**Key Learnings**:
- Celery must be initialized in `app/celery.py` and imported in `app/__init__.py`
- Use `@shared_task` decorator for reusable tasks
- Always pass serializable data to Celery tasks (UUIDs as strings, not objects)
- Use entrypoint scripts to wait for dependencies (Postgres, Redis) before starting

### 7. Docker Compose Orchestration

**Challenge**: Coordinate multiple services (Django, PostgreSQL, MongoDB, Redis, Celery) with proper dependencies and initialization order.

**Solution**:
- Use Docker Compose to define all services in one file
- Implement health checks for databases
- Create entrypoint scripts that wait for dependencies
- Use named volumes for data persistence

**Key Learnings**:
- `depends_on` ensures services start in order, but doesn't wait for them to be ready
- Use entrypoint scripts with `nc` (netcat) to check if services are actually ready
- Use service names for inter-service communication (`flix_db`, `redis`, not `localhost`)
- Always use `exec` for the final command in entrypoint scripts to ensure proper signal handling

### 8. AI Integration with Adapter Pattern

**Challenge**: Integrate OpenAI for generating movie descriptions while maintaining flexibility to switch AI providers and testability.

**Solution**:
- **Adapter Pattern**: Created abstract `AIAgentAdapter` interface in `apps/core/adapters/ai_adapters/base.py`
- **Concrete Implementation**: `OpenAIAdapter` implements the interface for OpenAI integration
- **Service Layer**: `MovieSuggestorDescriptionService` uses the adapter, not the concrete implementation
- **Mixin Pattern**: `MovieSuggestorDescriptionMixin` provides reusable methods for views

**Key Learnings**:

**Adapter Pattern Benefits**:
- **Flexibility**: Easy to switch AI providers (OpenAI, Anthropic, etc.) without changing business logic
- **Testability**: Can create mock adapters for testing without API calls
- **Separation of Concerns**: Business logic (service) separated from external API integration (adapter)
- **Dependency Injection**: Views inject the adapter, making dependencies explicit

**Mixin Pattern**:
- **Reusability**: `MovieSuggestorDescriptionMixin` can be used in multiple views
- **Composition over Inheritance**: Mixins allow combining behaviors without deep inheritance hierarchies
- **Single Responsibility**: Each mixin has a focused purpose (description suggestion, audit, etc.)

**Implementation Details**:
- Abstract base class defines the contract (`answer(prompt: str) -> str`)
- Service classes depend on the adapter interface, not concrete implementations
- Views compose mixins and inject adapters through class attributes
- Environment variable `OPENAI_API_KEY` configures the OpenAI adapter

**Best Practices**:
- Always define abstract interfaces for external dependencies
- Use dependency injection to make dependencies explicit and testable
- Keep adapters focused on translation between your domain and external APIs
- Use mixins for cross-cutting concerns that can be shared across views

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
