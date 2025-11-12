# Governance & Human Oversight

The Intelligent Negotiation Framework embeds governance at multiple layers to ensure responsible automation.

## Human-in-the-Loop Controls
- All negotiated counter-offers expose rationale and SHAP explanations for buyer review.
- `services.rl_agent.buyer_approval` allows manual approval or override before executing contractual changes.
- Streamlit dashboard highlights outstanding approvals and compliance alerts.

## Policy & Audit
- Activity logs emit structured events through the standard logging configuration (`config/logging.yaml`).
- Optional MLflow integration records experiment metadata when `ENABLE_MLFLOW=1`.
- Drift monitoring computes population stability index (PSI) and logs warnings when thresholds exceed `config/settings.yaml` values.

## Data Lifecycle
- Demo data stored in SQLite; swap adapters for production warehouses with retention policies.
- Transcripts persisted without PII. Redaction utilities strip personal identifiers prior to storage.
- Access to secrets managed through environment variables loaded via `.env` (never commit secrets).

## Compliance Alignment
- Red team checks (see `config/prompts/red_team_checks.md`) enforce refusal behaviour for risky requests.
- GDPR principles addressed through data minimisation, auditability, and right-to-delete hooks in `data_store.py`.
- Security posture described in `docs/SECURITY.md` with guidance for hardening deployments.
