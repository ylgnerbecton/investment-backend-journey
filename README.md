# Financial Investment Project

## Overview

The Financial Investment Project is a service centered around financial investments, allowing users to manage assets, users, orders, and more. We are committed to solid design principles such as Domain-Driven Design (DDD) and Onion Architecture, ensuring a robust and well-organized structure.

## Key Technologies

* [FastAPI](https://fastapi.tiangolo.com/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [Pydantic](https://pydantic-docs.helpmanual.io/)
* [Uvicorn](https://www.uvicorn.org/)
* [Alembic](https://alembic.sqlalchemy.org/en/latest/)
* [MySQL](https://www.mysql.com/)
* [Docker](https://www.docker.com/)

## Project Architecture

The application is structured using Domain-Driven Design (DDD) and Onion Architecture. The directory structure is organized as follows:

```tree
├── alembic
│    └── versions
├── src
│    ├── application
│    │    ├── adapters
│    │    ├── errors
│    │    │    └── exceptions.py
│    │    ├── extensions
│    │    └── helpers
│    │        └── https_models.py
│    ├── config.py
│    ├── domain
│    │    ├── interfaces.py
│    │    ├── models
│    │    │    ├── asset.py
│    │    │    ├── transaction.py
│    │    │    └── user.py
│    │    └── services
│    │        ├── asset.py
│    │        ├── service.py
│    │        ├── transaction.py
│    │        └── user.py
│    ├── infrastructure
│    │    ├── db
│    │    │    ├── base.py
│    │    │    ├── base_class.py
│    │    │    └── database.py
│    │    ├── repositories
│    │    │    ├── asset.py
│    │    │    ├── repository.py
│    │    │    ├── transaction.py
│    │    │    └── user.py
│    │    └── schemas
│    │        ├── asset.py
│    │        ├── response.py
│    │        ├── transaction.py
│    │        └── user.py
│    ├── main.py
│    └── presentation
│        └── views
│            ├── asset.py
│            ├── auth.py
│            ├── base.py
│            ├── healthz.py
│            ├── transaction.py
│            └── user.py
└── tests
    └── presentation
        └── test_user.py

```

For more insights on the roles of each layer, consult our [Architecture Documentation](https://github.com/ylgnerbecton/investment-backend-journey/wiki/Architecture).

## Getting Started

### Running the Application with Docker

This application initializes three Docker images:

- **app_financial_investment**: Docker image of the FastApi application.
- **db_financial_investment**: Docker image for the MySQL database.

Follow the steps below to get the application up and running:

1. Create a local `.env` file by copying the contents of `sample.env`:
```bash
cp example.env .env
```

2. Launch the application using Docker:
```bash
make start-build
```

### Using the Application

1. When the application is up and running through Docker, access the available services via the Swagger UI:
    http://localhost:8010/docs/

2. Use the API structure to fetch the information:

```
  curl -X 'POST' \
  'http://localhost:8010/api/v1/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{}'
```

### Running Unit Tests

Execute the unit tests with the following command:

```bash
make test
```

### Endpoints:

#### Asset
- `GET` /asset/trends *(Retrieving the Top 5 Most Frequently Traded Assets)*
- `GET` /asset *(Retrieve All Resources)*
- `POST` /asset *(Create Resource)*
- `GET` /asset/{uuid} *(Retrieve Resource By Uuid)*
- `PUT` /asset/{uuid} *(Update Resource)*
- `DELETE` /asset/{uuid} *(Delete Resource)*

#### User
- `GET` /user *(Retrieve All Resources)*
- `POST` /user *(Create Resource)*
- `GET` /user/{uuid} *(Retrieve Resource By Uuid)*
- `PUT` /user/{uuid} *(Update Resource)*
- `DELETE` /user/{uuid} *(Delete Resource)*
- `GET` /user/position/{uuid} *(Retrieving Client's Financial Balance and Total Net Worth)*

#### Order
- `GET` /order *(Retrieve All Resources)*
- `POST` /order *(Create Purchase Order Processing)*
- `GET` /order/{uuid} *(Retrieve Resource By Uuid)*
- `PUT` /order/{uuid} *(Update Resource)*
- `DELETE` /order/{uuid} *(Delete Resource)*

#### Health
- `GET` /healthz *(Health Check)*
- `GET` /readiness *(Readiness Check)*
- `POST` /spb/events *(Transfer Event)*

