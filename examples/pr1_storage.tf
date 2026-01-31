# terraform/storage.tf
resource "aws_s3_bucket" "app_logs" {
  bucket = "myapp-logs-prod"

  tags = {
    Environment = "production"
    Team        = "platform"
  }
}
