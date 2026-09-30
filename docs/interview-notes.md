# Interview Talking Points

## Why private subnets?

The database should not be directly reachable from the public internet. The API is the controlled entry point.

## Why SQS?

AI inference and notifications can be slow or fail independently. A queue creates a buffer and lets workers retry jobs.

## Why Terraform?

The infrastructure becomes version-controlled, repeatable, reviewable, and easier to recreate.

## Why Docker?

It gives the application a consistent runtime between a developer laptop, CI, and cloud deployment.

## Why GitHub Actions?

It automates quality gates so code is tested and scanned before deployment.

## What would you improve?

1. Replace static database password with Secrets Manager.
2. Use ECS/Fargate with task roles and autoscaling.
3. Put an ALB behind CloudFront/WAF.
4. Add HTTPS certificates with ACM.
5. Use GitHub OIDC instead of AWS access keys.
6. Add distributed tracing with OpenTelemetry.
7. Add Cognito authentication and authorization.
8. Add SQS dead-letter queues.
9. Add database migrations with Alembic.
10. Add AI evaluation and prompt/version tracking.
