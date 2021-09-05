# Creating the Kinesis Stream as a producer for both Firehose
resource "aws_kinesis_stream" "kinesis_stream" {
  name             = local.kinesis_data_streams_name
  shard_count      = var.shard_count
  retention_period = var.retention_period
}

# Creating the Firehose whose delivers the raw data to s3.
resource "aws_kinesis_firehose_delivery_stream" "stream_raw_data" {
  name        = "firehose-raw-data"
  destination = "extended_s3"

  kinesis_source_configuration {
    kinesis_stream_arn = aws_kinesis_stream.kinesis_stream.arn
    role_arn           = aws_iam_role.firehose_role.arn
  }

  extended_s3_configuration {
    role_arn        = aws_iam_role.firehose_role.arn
    bucket_arn      = aws_s3_bucket.raw_bucket.arn
    buffer_interval = var.buffer_interval

  }
}

resource "aws_kinesis_firehose_delivery_stream" "stream_clean_data" {
  name        = "firehose-clean-data"
  destination = "extended_s3"

  kinesis_source_configuration {
    kinesis_stream_arn = aws_kinesis_stream.kinesis_stream.arn
    role_arn           = aws_iam_role.firehose_role.arn
  }

  extended_s3_configuration {
    role_arn        = aws_iam_role.firehose_role.arn
    bucket_arn      = aws_s3_bucket.clean_bucket.arn
    buffer_interval = var.buffer_interval

    processing_configuration {
      enabled = "true"

      processors {
        type = "Lambda"

        parameters {
          parameter_name  = "LambdaArn"
          parameter_value = "${aws_lambda_function.preprocess_firehose_lambda.arn}:$LATEST"
        }
      }
    }
  }
}