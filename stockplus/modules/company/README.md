# Company Application

This application manages companies, company addresses, and company-related functionality.

## Clean Architecture

This application follows the principles of Clean Architecture, which separates the code into layers with clear dependencies:

```
company/
├── domain/              # Domain layer - Business rules and entities
│   ├── models.py        # Domain models
│   └── exceptions.py    # Domain exceptions
├── application/         # Application layer - Use cases and business logic
│   ├── interfaces.py    # Repository interfaces
│   └── services.py      # Application services
├── infrastructure/      # Infrastructure layer - Technical details
│   └── repositories.py  # Repository implementations
└── interfaces/          # Interface layer - User interfaces
    ├── serializers.py   # API serializers
    └── views/           # API views
        ├── company.py   # Company views
        └── address.py   # Company address views
```

## Layers

### Domain Layer

The domain layer contains the business rules and entities. It is independent of any framework or infrastructure concerns.

- **Models**: Domain models like `Company` and `CompanyAddress`
- **Exceptions**: Domain-specific exceptions

### Application Layer

The application layer contains the use cases and business logic. It depends on the domain layer but is independent of the infrastructure and interface layers.

- **Interfaces**: Repository interfaces that define the contract for data access
- **Services**: Application services that implement the business logic

### Infrastructure Layer

The infrastructure layer contains the technical details. It depends on the domain and application layers.

- **Repositories**: Repository implementations that use Django ORM to access the database

### Interface Layer

The interface layer contains the user interfaces. It depends on the application layer but is independent of the infrastructure layer.

- **Serializers**: API serializers that convert between domain models and JSON
- **Views**: API views that handle HTTP requests and responses

## Benefits

This architecture provides several benefits:

- **Separation of concerns**: Each layer has a clear responsibility
- **Testability**: The domain and application layers can be tested without the infrastructure and interface layers
- **Flexibility**: The infrastructure and interface layers can be changed without affecting the domain and application layers
- **Maintainability**: The code is easier to understand and maintain
