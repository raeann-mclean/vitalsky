# Architecture Notes

## Tier 1 — Edge

A production-style implementation would place CloudFront and AWS WAF at the public edge, with an HTTPS load balancer behind it.

Goals:
- TLS
- DDoS/WAF controls
- rate limiting
- centralized edge logging

## Tier 2 — Application

The FastAPI service is containerized and intended to run on ECS/Fargate.

The service is stateless. This means additional containers can be started without copying local application state between them.

## Tier 3 — Data

RDS PostgreSQL stores application records.

S3 stores object-style data such as generated reports or documents.

Both are private and encrypted at rest.

## Async tier

SQS is used to decouple long-running work from API requests.

Example flow:

```text
POST /visits
      |
      v
API stores visit
      |
      v
SQS message
      |
      v
worker
  |       |
  v       v
AI      notification
```

This pattern prevents an AI/model call from making the main API request unnecessarily slow.

## AI engineering angle

The app uses an interface:

```text
AIProvider
  ├── MockAIProvider
  └── BedrockAIProvider
```

This demonstrates provider abstraction, which makes model replacement easier and keeps application code independent from a specific model vendor.

A stronger production version would add:

- prompt versioning
- evaluation datasets
- latency/cost metrics
- model fallback
- PII/PHI redaction
- output validation
- human review
- audit trails
- model monitoring
