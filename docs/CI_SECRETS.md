# CI / Secrets Guidance

Recommended GitHub Secrets (Repository settings → Secrets → Actions):

- DATABASE_URL        (e.g. postgres://user:pass@host:5432/dbname)
- DOCKERHUB_TOKEN     (if you push images)
- DOCKERHUB_USERNAME
- AWS_ACCESS_KEY_ID   (if deploying)
- AWS_SECRET_ACCESS_KEY
- GITHUB_TOKEN        (auto provided; avoid overriding)
- SENTRY_DSN          (optional, for error monitoring)
- VAULT_ADDR / VAULT_TOKEN (if using Hashicorp Vault)

Best practices:
1. Store secrets only in GitHub Secrets or a managed secret store (HashiCorp Vault, AWS Secrets Manager).
2. Do not check secrets into repository or .env files.
3. Enable secret rotation policy in your organisation.
4. Limit access: least-privilege for deploy keys and tokens.
