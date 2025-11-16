# Reflection

Key experiences and challenges:
- Modeling: Decided to store `result` in the DB to simplify querying and demonstrate both persisted and computed approaches. The model keeps `a`, `b`, and `op_type` as core inputs and an optional `result`.
- Validation: Used Pydantic `CalculationCreate` to validate inputs (non-zero divisor for Divide, operation enum).
- Factory pattern: Implemented a simple `OperationFactory` to encapsulate Add/Sub/Mul/Divide logic so the code is extensible.
- Testing: Unit tests validate operations and schema validation. Integration test uses a PostgreSQL container (as configured in GitHub Actions workflow) — locally tests run against SQLite in-memory.
- CI/CD: Workflow builds and runs tests, then builds and pushes Docker image on success. Secrets required: `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`.
