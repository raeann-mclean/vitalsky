resource "aws_sqs_queue" "jobs" {
  name                       = "${var.name}-jobs"
  message_retention_seconds  = 86400
  visibility_timeout_seconds = 60
}
