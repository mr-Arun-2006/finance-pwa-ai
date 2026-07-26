# Contributing Guide

We welcome contributions! Please follow these guidelines.

## Code Standards

### TypeScript
- Use strict mode
- Type all function parameters and returns
- Use interfaces for objects
- 80 character line limit

### Python
- Follow PEP 8
- Use type hints
- Document functions with docstrings
- Test coverage minimum: 80%

### Commits

Format: `<type>(<scope>): <subject>`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style
- `refactor`: Refactoring
- `test`: Tests
- `chore`: Build/dependencies

Example:
```
feat(transactions): add CSV import feature
fix(budget): correct spending calculation
docs(setup): update installation guide
```

## Pull Request Process

1. Fork repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -am 'feat: new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Open Pull Request

## Testing

### Backend

```bash
cd backend
npm test
```

### Frontend

```bash
cd frontend
npm test
```

### ML Models

```bash
cd ml-models
pytest tests/
```

## Code Review

Reviewers will check:
- Code quality
- Test coverage
- Documentation
- Performance
- Security

## License

MIT License - see LICENSE file
