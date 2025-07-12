# Contributing to CodeCrusher

**Author:** Martin Pfeffer (c) 2025  
**License:** MIT

Thank you for your interest in contributing to CodeCrusher! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Git
- Basic understanding of web application security
- Familiarity with penetration testing concepts

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/pepperonas/codecrusher.git
   cd codecrusher
   ```

2. **Setup Development Environment**
   ```bash
   ./scripts/setup.sh
   pip install -r requirements-dev.txt
   ```

3. **Install Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

## 🎯 How to Contribute

### 🐛 Bug Reports

1. **Search existing issues** first
2. **Use the bug report template**
3. **Include detailed reproduction steps**
4. **Provide environment information**
5. **Never include sensitive data** in public issues

### 💡 Feature Requests

1. **Check if feature exists** in latest version
2. **Use the feature request template**
3. **Explain the use case** and benefits
4. **Consider security implications**
5. **Ensure ethical usage** alignment

### 🔧 Code Contributions

#### Exploit Modules
When adding new exploit modules:

```python
# src/exploits/new_category/new_exploit.py
class NewExploit:
    """
    Description of the exploit
    
    Author: Your Name
    Security Category: [Injection/Auth/XSS/etc]
    Target: [Specific vulnerable app or general]
    """
    
    def __init__(self, api, browser=None):
        self.api = api
        self.browser = browser
        self.logger = logging.getLogger(__name__)
        
    def exploit_vulnerability_name(self) -> Dict[str, Any]:
        """
        Challenge: Specific Challenge Name
        Exploit: Brief description of technique
        """
        self.logger.info("Exploiting: Vulnerability Name")
        
        # Implementation here
        
        return {
            'success': True/False,
            'challenge': 'Challenge Name',
            'payload': 'Used payload',
            'result': 'Additional data'
        }
```

#### Documentation
- Add educational content explaining the vulnerability
- Include mitigation strategies
- Provide real-world examples
- Reference OWASP guidelines

## 📋 Development Guidelines

### Code Style

1. **Python Code**
   - Follow PEP 8
   - Use type hints
   - Add docstrings to all public methods
   - Maximum line length: 127 characters

2. **Naming Conventions**
   ```python
   # Functions and variables
   def exploit_sql_injection():
   vulnerability_found = True
   
   # Classes
   class SQLInjectionExploit:
   
   # Constants
   MAX_RETRY_ATTEMPTS = 3
   ```

3. **Comments and Documentation**
   ```python
   def exploit_method(self) -> Dict[str, Any]:
       """
       Challenge: Name of the challenge
       Exploit: Brief explanation of the technique used
       
       Returns:
           Dict containing success status and results
       """
   ```

### Testing

1. **Unit Tests**
   ```bash
   pytest tests/test_new_module.py -v
   ```

2. **Integration Tests**
   ```bash
   pytest tests/integration/ -v
   ```

3. **Security Tests**
   ```bash
   bandit -r src/
   ```

### Git Workflow

1. **Branch Naming**
   ```bash
   feature/add-xss-exploits
   bugfix/fix-sql-injection-parser
   docs/update-setup-guide
   security/improve-input-validation
   ```

2. **Commit Messages**
   ```bash
   feat: add stored XSS exploitation module
   fix: resolve SQL injection payload encoding issue
   docs: update installation instructions
   security: add input validation for user payloads
   ```

3. **Pull Request Process**
   - Create descriptive PR title
   - Fill out PR template completely
   - Ensure all tests pass
   - Update documentation if needed
   - Request review from maintainers

## 🔒 Security Guidelines

### Ethical Considerations

**✅ DO:**
- Test only against authorized targets
- Include educational content
- Promote defensive security
- Follow responsible disclosure
- Add appropriate warnings

**❌ DON'T:**
- Create tools for malicious purposes
- Include real credentials or secrets
- Target unauthorized systems
- Ignore legal implications
- Skip ethical considerations

### Code Security

1. **Input Validation**
   ```python
   def validate_url(url: str) -> bool:
       """Validate URL format and allowed schemes"""
       if not url.startswith(('http://', 'https://')):
           return False
       return True
   ```

2. **Secret Management**
   ```python
   # ❌ Don't do this
   api_key = "hardcoded-secret"
   
   # ✅ Do this
   api_key = os.environ.get('API_KEY')
   ```

3. **Error Handling**
   ```python
   try:
       result = dangerous_operation()
   except Exception as e:
       # Don't expose sensitive information
       self.logger.error(f"Operation failed: {type(e).__name__}")
       return {'success': False, 'error': 'Operation failed'}
   ```

## 📚 Documentation Standards

### Code Documentation
- All public methods must have docstrings
- Include parameter types and return types
- Explain the purpose and security implications
- Provide usage examples

### Educational Content
- Explain the vulnerability being exploited
- Include OWASP references where applicable
- Provide mitigation strategies
- Add real-world context

### README Updates
- Keep installation instructions current
- Update feature lists when adding capabilities
- Maintain example usage sections
- Include troubleshooting information

## 🧪 Testing Your Contributions

### Local Testing
```bash
# Run all tests
pytest tests/ -v --cov=src

# Test specific module
pytest tests/test_injection.py -v

# Security scan
bandit -r src/

# Code style check
black --check src/
flake8 src/
```

### Manual Testing
```bash
# Test against OWASP Juice Shop
docker run -d -p 3000:3000 bkimminich/juice-shop
python src/main.py --target http://localhost:3000 --category new_category
```

## 🎯 Areas Needing Contributions

### High Priority
- [ ] XSS exploitation modules
- [ ] Access control testing
- [ ] Advanced authentication bypasses
- [ ] API security testing
- [ ] Mobile app security features

### Medium Priority
- [ ] Additional report formats
- [ ] Performance optimizations
- [ ] Browser compatibility improvements
- [ ] Docker containerization
- [ ] CI/CD pipeline enhancements

### Documentation
- [ ] Video tutorials
- [ ] Advanced usage guides
- [ ] Security best practices
- [ ] Integration examples
- [ ] Troubleshooting guides

## 🏆 Recognition

Contributors will be:
- Listed in [AUTHORS](AUTHORS) file
- Mentioned in release notes
- Credited in relevant documentation
- Recognized in the project README

## 📞 Getting Help

- **Discord:** [CodeCrusher Community](#)
- **Email:** martin.pfeffer@codecrusher.dev
- **Issues:** Use GitHub issues for bugs/features
- **Security:** Email privately for security concerns

## ⚖️ Legal Considerations

By contributing, you:
- Grant MIT license rights to your contributions
- Confirm your code is original or properly licensed
- Acknowledge the educational purpose of this project
- Agree to the project's ethical use guidelines

---

**Thank you for helping make CodeCrusher better!** 💥

*Together we can build the most comprehensive web security testing framework for education and authorized testing.*