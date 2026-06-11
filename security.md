# Security Policy

## Supported Versions

Security updates are applied to the active development branch of this project.

## Reporting a Vulnerability

Please do not open public issues for security vulnerabilities.

To report a vulnerability, contact the project maintainers privately with:

- A clear description of the issue
- Steps to reproduce the issue
- The affected files, endpoints, or configuration
- Any logs or screenshots that help explain the risk

The maintainers will review the report and respond as soon as possible.

## Security Guidelines

- Do not commit real secrets, API keys, passwords, tokens, or private keys.
- Use `.env.example` as a template and keep real `.env` files local.
- Change default `SECRET_KEY` and `JWT_SECRET` values before production use.
- Restrict `CORS_ORIGINS` and `TRUSTED_HOSTS` for deployed environments.
- Use HTTPS in production.
- Rotate credentials immediately if they are exposed.

