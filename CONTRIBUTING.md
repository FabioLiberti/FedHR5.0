# Contributing to FedHR5.0

First off, thank you for considering contributing to FedHR5.0! 🎉 

As our framework is currently accompanying a paper under review, we have specific guidelines for contributions during this phase.

## 🚧 Current Status

**Note**: FedHR5.0 is currently in a limited release phase while our paper undergoes peer review. We welcome feedback and discussions, but major contributions will be accepted after the review process is complete.

## 📋 How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, please include:

- **Clear descriptive title**
- **Steps to reproduce**
- **Expected behavior**
- **Actual behavior**
- **System information** (OS, Python version, PyTorch version)
- **Minimal reproducible example**

### 💡 Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, provide:

- **Use case** - Why is this enhancement needed?
- **Expected behavior** - How should it work?
- **Alternative solutions** - What other approaches did you consider?
- **Additional context** - Screenshots, diagrams, or mockups

### 🔬 Research Collaborations

We're particularly interested in collaborations on:

- **Privacy mechanisms** - Novel differential privacy techniques
- **Fairness metrics** - Cross-cultural fairness evaluation
- **Scalability** - Optimization for 100+ organizations
- **Industry applications** - Adapting to new sectors beyond manufacturing

Contact the principal investigator at author1@university.edu for research collaborations.

## 🛠️ Development Process

### Setting Up Your Environment

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/FedHR5.0.git
   cd FedHR5.0
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

5. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Code Style

We follow PEP 8 with the following specifications:

- **Line length**: 88 characters (Black default)
- **Imports**: Sorted with `isort`
- **Docstrings**: Google style
- **Type hints**: Required for public APIs

Example:
```python
def federated_average(
    models: List[torch.nn.Module], 
    weights: Optional[List[float]] = None
) -> torch.nn.Module:
    """
    Perform federated averaging of model parameters.
    
    Args:
        models: List of local models to average.
        weights: Optional weights for weighted averaging.
        
    Returns:
        Averaged global model.
        
    Raises:
        ValueError: If models list is empty.
    """
    if not models:
        raise ValueError("Cannot average empty model list")
    
    # Implementation here
    pass
```

### Testing

- Write tests for any new functionality
- Maintain test coverage above 80%
- Run tests before submitting:
  ```bash
  pytest tests/ -v --cov=src --cov-report=html
  ```

### Documentation

- Update docstrings for API changes
- Update README.md if adding new features
- Add examples for new functionality
- Update CHANGELOG.md

## 📝 Pull Request Process

1. **Branch naming**: `feature/description` or `fix/description`
2. **Commits**: Use conventional commits (e.g., `feat:`, `fix:`, `docs:`)
3. **PR description**: Use our template and link related issues
4. **Tests**: Ensure all tests pass
5. **Review**: Wait for at least one maintainer review

### PR Checklist

- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] No merge conflicts

## 🔒 Security

**IMPORTANT**: Do not commit any real employee data or organizational information. All data in examples must be synthetic.

If you discover a security vulnerability, please email security@university.edu instead of using the issue tracker.

## 📜 Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, sex characteristics, gender identity and expression, level of experience, education, socio-economic status, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Expected Behavior

- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior

- Harassment of any kind
- Discriminatory language or actions
- Publishing others' private information
- Other conduct inappropriate for a professional setting

## 📄 License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

## 🙏 Recognition

Contributors will be acknowledged in:
- The project README
- Future publications (for significant contributions)
- The project website (coming soon)

## 📞 Questions?

Feel free to:
- Open a [Discussion](https://github.com/yourusername/FedHR5.0/discussions)
- Contact the maintainers
- Join our [Slack channel](#) (coming soon)

---

Thank you for helping make FedHR5.0 better! 🚀