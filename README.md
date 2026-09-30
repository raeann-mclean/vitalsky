# ⋆｡ﾟ☁︎｡⋆𓂃 ོ☼𓂃 Cloud Telemedicine Infrastructure 𓂃｡ﾟ☁︎｡⋆𓂃 ོ☼｡ﾟ⋆

Vital Sky is a cloud/DevOps project that simulates an ultra secure telemedicine platform on AWS!

> **Important:** This is a simulation/student project!! It is not intended for real patient data, production healthcare use, or HIPAA compliance certification.

## What this infra demonstrates

- AWS cloud architecture and networking
- Infrastructure as Code with Terraform
- Containerized Python API with Docker
- Multi-tier architecture: edge → API → data/async/AI
- Private subnets for application and database workloads
- IAM least-privilege design
- Secrets Manager for database credentials
- S3 for encrypted object storage
- SQS for asynchronous jobs
- PostgreSQL/RDS persistence
- CloudWatch logs and alarms
- WAF protection in front of the public application
- GitHub Actions CI/CD
- Unit/integration-style API tests
- Security scanning with Trivy
- AI-assisted visit summarization with a provider interface
- Local/mock AI mode so the project can be demonstrated without cloud AI spend
- Health checks and structured JSON logging

## Architecture

```text
                         Internet
                            |
                     CloudFront / WAF
                            |
                       Public ALB
                            |
                    +-------+-------+
                    |   API / ECS   |
                    | FastAPI       |
                    | Docker        |
                    +---+-------+---+
                        |       |
                  HTTPS |       | SQS
                        |       v
                        |   Async Worker
                        |       |
                        |       +----> AI service
                        |
                        +----> RDS PostgreSQL
                        |
                        +----> S3 encrypted objects

        Private subnets:
        - ECS API
        - ECS Worker
        - RDS PostgreSQL

        Observability:
        CloudWatch Logs + Metrics + Alarms

        Delivery:
        GitHub -> Actions -> tests/security scan -> build -> deploy
```

## Repo structure

```text
.
├── services/
│   ├── records/              # Flask records API (patients + medical records)
│   │   ├── app/
│   │   ├── migrations/
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── telemedicine/         # FastAPI telemedicine API (patients, visits, AI summaries)
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── config.py
│   │   │   ├── db.py
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── ai.py
│   │   │   └── worker.py
│   │   ├── tests/
│   │   │   └── test_api.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── appointments/         # scaffold
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── versions.tf
│   └── modules/
│       ├── vpc/              # VPC, public/private/db subnets, IGW, routes
│       ├── security/         # API + DB security groups
│       ├── rds/              # PostgreSQL (encrypted, private)
│       ├── ecs/              # ECR repo + CloudWatch log group
│       ├── messaging/        # SQS jobs queue
│       └── storage/          # encrypted, private S3 bucket
├── scripts/
│   └── init-multiple-dbs.sh
├── docs/
│   ├── architecture.md
│   └── interview-notes.md
├── .github/workflows/ci.yml
├── docker-compose.yml
└── .env.example
```

## Local demo

Requirements: Python 3.12+, Docker, Docker Compose.

```bash
cp .env.example .env
docker compose up --build
```

Telemedicine API (FastAPI) — http://localhost:8000:
- `GET /health`
- `POST /patients`
- `GET /patients/{patient_id}`
- `POST /visits`
- `GET /visits/{visit_id}`
- `POST /visits/{visit_id}/summary`
- `GET /metrics`

Records API (Flask) — http://localhost:5001:
- `GET /api/patients/`
- `POST /api/patients/`
- `GET|PUT|DELETE /api/patients/{patient_id}`
- `POST /api/records/`
- `GET /api/records/patient/{patient_id}`
- `GET|DELETE /api/records/{record_id}`

Example:

```bash
curl http://localhost:8000/health
```

Create a simulated patient:

```bash
curl -X POST http://localhost:8000/patients \
  -H "Content-Type: application/json" \
  -d '{"display_name":"Demo Patient"}'
```

Create a visit:

```bash
curl -X POST http://localhost:8000/visits \
  -H "Content-Type: application/json" \
  -d '{"patient_id":"<PATIENT_ID>","notes":"Demo visit: patient reports mild seasonal symptoms."}'
```

Generate an AI-style summary:

```bash
curl -X POST http://localhost:8000/visits/<VISIT_ID>/summary
```

The default local AI provider is a deterministic mock. This keeps the demo free.

## AWS deployment

The Terraform configuration is intentionally designed as a portfolio architecture rather than a production healthcare deployment.

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

Before applying, review:

- AWS region
- instance/service sizing
- estimated monthly cost
- IAM permissions
- security groups
- deletion protection settings
- logging retention

Destroy when finished:

```bash
terraform destroy
```

### AI mode

The application has an AI provider interface.

`AI_PROVIDER=mock`:
- free
- deterministic
- ideal for GitHub demos

`AI_PROVIDER=bedrock`:
- intended for an AWS Bedrock implementation
- requires AWS credentials/IAM permissions
- model availability varies by AWS region
- use only synthetic demo text

The important engineering pattern is that the API does not depend directly on one model provider. The provider can be swapped without changing the visit API.

## CI/CD

GitHub Actions runs:

1. Python compile check
2. Ruff linting
3. Pytest
4. Docker build
5. Trivy container scan
6. Terraform formatting and validation

Run the tests the same way CI does:

```bash
cd services/telemedicine
python -m pytest -q
```



For a real deployment pipeline, the next step would be GitHub OIDC → AWS IAM role → ECR → ECS deployment.

