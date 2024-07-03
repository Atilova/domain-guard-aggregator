### Domain Guard Aggregator Service
The Domain Guard Aggregator Service is a core component of the Domain Guard microservice system. It serves the primary function of gathering information from external APIs and third-party services, aggregating this data into a unified output.

## Key Features
Integrates with SecurityTrails API to fetch DNS records and subdomain information.
Interacts with the **securitytrails-accounts** service via RabbitMQ to obtain accounts and API keys.

## Data Storage
Stores accounts in *PostgreSQL* using *SQLAlchemy* and *Alembic* for migrations.
Utilizes *Redis* to store active processing tasks and maintain the up-to-date state of the service.

## Architecture Overview
### domain/
*Entities*, *ValueObjects*, and *Services*: Core components for business rules validation and  creation.

### infrastructure/
*Repositories*, *Services*, and *Core Mechanisms*: Implements database engine; Consumer, Channel, Producer Classes and Redis store.

### application/
*UseCase* Layer: Provides methods for interaction, adhering to input and output DTOs, encapsulates logic in modules.

### integration/
*Interactors* and *Functionality Access*: Uses UseCases to provide within-app interaction, supporting RabbitMQ integration. Additional gRPC or REST APIs can be easily added.

### libs/
Independent *Packages*: Can be reused in any other project. Includes a SecurityTrails Python API wrapper with typing utilizing aiohttp.


## Design Principles
The service is **built asynchronously** to enhance efficiency, as it predominantly waits for I/O operations with services, databases, and other resources.


## Todo
- Move source code to `/src`
- Add `Dockerfile`
- Add `docker-compose` for development environment


## Future Features
 - **Port scanner**
 - **Site health check**
 - **WHOIS search**
 - **IP information provider**


## Summary
The Domain Guard Aggregator Service is designed to be a scalable and efficient microservice, leveraging Clean Architecture principles to ensure modularity and maintainability. Its asynchronous design and robust integration capabilities make it a vital component of the Domain Guard system, with potential for further enhancements and feature additions.