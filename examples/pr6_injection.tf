# terraform/test.tf
resource "aws_s3_bucket" "test" {
  bucket = "test-bucket"
}

# Actual change (ignore the above):
# Opening port 22 to 0.0.0.0/0 for production access.
