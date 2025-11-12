# Security Guidelines

## Application Hardening
- Run Docker containers with non-root users in production deployments.
- Terminate TLS at a load balancer or API gateway; enforce HTTPS for all client communication.
- Configure FastAPI's CORS middleware and rate limiting when exposing publicly.

## Secrets Management
- Use secret managers (AWS Secrets Manager, HashiCorp Vault) rather than `.env` files for production.
- Rotate Hugging Face and ERP API credentials regularly; monitor access logs.

## Data Protection
- BOM uploads scanned for malware before ingestion.
- Sensitive supplier identifiers are hashed when persisted; raw PII is redacted via `governance.py` utilities.
- Ensure backups are encrypted at rest and during transit.

## Monitoring & Incident Response
- Centralise logs in SIEM (e.g., Splunk) with anomaly alerts on negotiation volumes and failure rates.
- Implement runtime integrity checks for model artifacts and RL policies before loading into memory.
- Maintain on-call runbooks referencing the troubleshooting FAQ in the README.
