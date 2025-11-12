# Data Dictionary

## BOM Records
| Field | Type | Description |
| --- | --- | --- |
| material | string | Material name as provided by supplier |
| composition | string | Blend or material composition |
| gsm | float | Grams per square meter, converted to numeric |
| process | string | Manufacturing process (weaving, dyeing, etc.) |
| unit_cost | float | Cost per unit (default currency USD) |
| moq | int | Minimum order quantity |
| lead_time | int | Lead time in days |

## Market Signals
| Field | Type | Description |
| date | date | Observation date |
| commodity | string | Commodity name |
| price_usd | float | Commodity price in USD |
| pair | string | FX currency pair |
| rate | float | Exchange rate benchmark |

## Negotiation Transcripts
| Field | Type | Description |
| session_id | string | Unique negotiation session identifier |
| buyer | string | Buying organization |
| supplier | string | Supplier partner |
| messages | list[dict] | Ordered conversation turns |
| outcome | string | Final negotiation state (accepted, pending, etc.) |

## Feature Store (Demo)
| Field | Type | Description |
| product_id | string | SKU or BOM identifier |
| supplier_id | string | Supplier unique identifier |
| similarity_score | float | Graph similarity to historical parts |
| benchmark_delta | float | Difference vs market benchmark |
| last_offer_delta | float | Variation from previous supplier offer |
