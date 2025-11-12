# Metrics & KPIs

## Negotiation Outcomes
- **Cycle Time Reduction**: Average negotiation time vs baseline manual process.
- **Cost Savings %**: (Baseline quote - final agreed price) / baseline quote.
- **Sustainability Compliance Rate**: Percentage of negotiations meeting ESG thresholds.

## Model Health
- **BOM Parser Accuracy**: % of fields correctly extracted (via spot checks or labeled set).
- **NER F1 Score**: Micro/macro averages for material and process tags.
- **Graph Similarity Precision@k**: Accuracy of recommended similar BOMs.
- **RL Reward Trend**: Rolling mean reward per episode; monitor for regressions.

## Explainability & Governance
- **SHAP Stability**: Variation in top contributing features over time.
- **Human Override Rate**: Frequency of buyer overrides; triggers retraining pipeline when high.
- **Drift PSI**: Feature drift for cost, lead time, and similarity metrics.

## Operational Metrics
- **API Latency (p95)**: Derived from FastAPI logs or APM tooling.
- **Throughput**: Negotiation steps processed per minute.
- **Error Rate**: 4xx/5xx counts segmented by endpoint.
