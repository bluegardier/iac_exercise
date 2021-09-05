resource "aws_s3_bucket" "raw_bucket" {
  bucket = "bgardier-raw-bucket"
  acl    = "private"

  versioning {
    enabled = true
  }
}

resource "aws_s3_bucket" "clean_bucket" {
  bucket = "bgardier-clean-bucket"
  acl    = "private"

  versioning {
    enabled = true
  }
}


resource "aws_s3_bucket_public_access_block" "raw_restriction" {
    bucket = aws_s3_bucket.raw_bucket.id
    block_public_acls = true
    block_public_policy = true
    ignore_public_acls = true
    restrict_public_buckets = true
}

resource "aws_s3_bucket_public_access_block" "clean_restriction" {
    bucket = aws_s3_bucket.clean_bucket.id
    block_public_acls = true
    block_public_policy = true
    ignore_public_acls = true
    restrict_public_buckets = true
}