# ⋆｡ﾟ☁︎｡⋆𓂃 ོ☼𓂃 Cloud Telemedicine Infrastructure 𓂃｡ﾟ☁︎｡⋆𓂃 ོ☼｡ﾟ⋆

Vital Sky is a cloud/DevOps project that simulates an ultra secure telemedicine platform on AWS!

> **Important:** This is a simulation/portfolio project!! It is also still a WIP. It is not intended for real patient data, production healthcare use, or HIPAA compliance certification.

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



## Whats Next?

### Roadmap: Security Hardening

VitalSky's core AWS foundation is in place: the RDS instance is private, and the database only accepts connections from the API's security group. The next phase turns it into a production-style, defense-in-depth deployment suitable for healthcare-style data. YAY!


### Known gaps (in progress)
- API routes don't yet enforce authentication or authorization
- API security group currently allows inbound traffic on port 8000 from `0.0.0.0/0`
- Database credentials are placeholders in Terraform rather than pulled from Secrets Manager
- ECS/Fargate service definition is incomplete

### Target architecture
```
Internet
   ↓
CloudFront + AWS WAF
   ↓
HTTPS Application Load Balancer
   ↓
Cognito authentication (JWT)
   ↓
ECS/Fargate API (private subnet)
   ↓
┌───────────┬───────────┬───────────┐
RDS         S3          SQS
(private)   (private)   (async)
                          ↓
                     AI worker → Amazon Bedrock
```





## Current Sctructure



### Architecture

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

### Planned work

**Identity & access**
- [ ] Amazon Cognito login with JWT validation on every API route
- [ ] Role-based access control (doctor, nurse, admin)
- [ ] Per-patient authorization checks, so a valid token alone can't read any record
- [ ] Audit logging of patient-record access

**Network**
- [ ] CloudFront and AWS WAF in front of an HTTPS Application Load Balancer
- [ ] Restrict ECS ingress to the ALB security group only
- [ ] Complete the ECS/Fargate service in private subnets
- [ ] Only port 443 publicly exposed; no database or application ports reachable from the internet

**Secrets & least privilege**
- [ ] Move RDS credentials into AWS Secrets Manager, retrieved by the ECS task role
- [ ] Scope ECS task IAM roles to only the actions each service needs (no wildcard permissions)

**Data protection**
- [ ] RDS encryption at rest, automated backups, and a Multi-AZ option
- [ ] Private, encrypted S3 storage

**Application hardening**
- [ ] Input validation, request size limits, and rate limiting
- [ ] Secure response headers

**Monitoring & detection**
- [ ] CloudWatch logging and alarms
- [ ] GuardDuty and Security Hub

**AI visit summaries**
- [ ] Async pipeline: SQS queue → worker → Amazon Bedrock
- [ ] Human review required before summaries are saved; no autonomous diagnosis

**CI/CD**
- [ ] GitHub Actions checks for infrastructure-as-code scanning, dependency and container scanning, and tests confirming protected routes reject unauthenticated requests

**Goal:** defense-in-depth security using private AWS networking, WAF, IAM least privilege, managed secrets, authenticated API access, encrypted storage, security scanning, and centralized logging.




