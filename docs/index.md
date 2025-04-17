# EOSC Data Transfer Client

Welcome to the documentation for the **EOSC Data Transfer Client** — a Python wrapper for interacting with the [EOSC Data Transfer Service](https://data-transfer.service.eosc-beyond.eu/swagger-ui/).

This client provides a simple and structured way to:

- Submit new transfer jobs
- Query status of transfer jobs
- Cancel jobs
- Retrieve specific metadata fields
- Search through previous transfers
- Digital Object Indetifier (DIO) parsing

It is built on top of the [requests](https://docs.python-requests.org/en/latest/) library and uses Pydantic models for robust data validation.

## Features

- Easy integration with the EOSC Data Transfer API
- Pydantic models for request/response validation
- Wrapper functions for common endpoints
- Clear error handling with custom exceptions
- Lightweight and dependency minimal
- Unit tested and ready for CI/CD pipelines

---

## Documentation Contents

- [Getting Started](getting-started.md)
- [API Reference](reference/)

---

Looking to just send a file? Head to the [Getting Started](getting-started.md) guide.

