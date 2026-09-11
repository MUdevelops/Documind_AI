# Security Policy

If you discover a security vulnerability, please do **not** open a public
issue. Instead, email the maintainers directly (see repository contact) with:

- A description of the vulnerability and its impact
- Steps to reproduce
- Any suggested fix

We aim to acknowledge reports within 5 business days. Please allow us
reasonable time to address the issue before public disclosure.

## Scope notes

- Never commit `.env`, API keys, or database credentials.
- Report any per-user data isolation bypass (one user accessing another
  user's documents, chunks, or conversations) as high severity.
