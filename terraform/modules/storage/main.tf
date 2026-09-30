resource "aws_s3_bucket" "records" {
  bucket_prefix = "${var.name}-records-"
}

resource "aws_s3_bucket_public_access_block" "records" {
  bucket = aws_s3_bucket.records.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_server_side_encryption_configuration" "records" {
  bucket = aws_s3_bucket.records.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}
