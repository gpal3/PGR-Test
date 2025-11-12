# Contributing Guide

We welcome contributions to the AI-Driven Intelligent Negotiation Framework. To keep a high-quality codebase, please follow the steps below.

1. **Fork & Branch**: Fork the repository and create a feature branch (`feature/my-enhancement`).
2. **Setup**: Run `make setup` to install dependencies and set up pre-commit hooks.
3. **Coding Standards**:
   - Use type hints throughout the Python codebase.
   - Keep modules small and cohesive; prefer dependency injection for services.
   - Run `make format` and `make lint` before committing.
4. **Testing**: Ensure `make test` passes with coverage ≥ 70%.
5. **Documentation**: Update relevant docs in `docs/` and the `CHANGELOG.md` entry under the "Unreleased" section.
6. **Pull Request**: Provide a clear description, reference related issues, and include screenshots for UI changes when possible.

Thank you for helping build responsible procurement automation!
