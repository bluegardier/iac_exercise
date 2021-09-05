resource "aws_iam_role" "lambda_role_kinesis" {
  name = "trigger-data-fetching"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_policy" "lambda_policy_kinesis" {
  name = "lambda-trigger-kinesis"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Effect   = "Allow"
        Resource = "*"
      },
      {
        "Effect" : "Allow",
        "Action" : "kinesis:*",
        "Resource" : "*"
      }

    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_data_kinesis_attach" {
  role       = aws_iam_role.lambda_role_kinesis.name
  policy_arn = aws_iam_policy.lambda_policy_kinesis.arn
}



resource "aws_iam_role" "lambda_role_firehose" {
  name = "preprocessing-data"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
}

resource "aws_iam_policy" "lambda_policy_firehose" {
  name = "preprocess-data-firehose"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        "Effect" : "Allow",
        "Action" : [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents",
          "s3-object-lambda:WriteGetObjectResponse"
        ],
        "Resource" : "*"
      },
      {

        "Effect" : "Allow",
        "Action" : "s3:*",
        "Resource" : "*"

      },
      {
        "Action" : [
          "firehose:*"
        ],
        "Effect" : "Allow",
        "Resource" : "*"

      }

    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_data_firehose_attach" {
  role       = aws_iam_role.lambda_role_firehose.name
  policy_arn = aws_iam_policy.lambda_policy_firehose.arn
}






resource "aws_iam_role" "firehose_role" {
  name = "firehose_stream_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "firehose.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy" "firehose_raw_policy" {
  name = "test_policy"
  role = aws_iam_role.firehose_role.id

  policy = jsonencode(
    {
      "Version" : "2012-10-17",
      "Statement" : [
        {
          "Sid" : "",
          "Effect" : "Allow",
          "Action" : [
            "glue:GetTable",
            "glue:GetTableVersion",
            "glue:GetTableVersions"
          ],
          "Resource" : "*"
        },
        {
          "Sid" : "",
          "Effect" : "Allow",
          "Action" : [
            "s3:AbortMultipartUpload",
            "s3:GetBucketLocation",
            "s3:GetObject",
            "s3:ListBucket",
            "s3:ListBucketMultipartUploads",
            "s3:PutObject"
          ],
          "Resource" : "*"
        },
        {
          "Sid" : "",
          "Effect" : "Allow",
          "Action" : [
            "lambda:InvokeFunction",
            "lambda:GetFunctionConfiguration"
          ],
          "Resource" : "*"
        },
        {
          "Effect" : "Allow",
          "Action" : [
            "kms:GenerateDataKey",
            "kms:Decrypt"
          ],
          "Resource" : "*",
          "Condition" : {
            "StringEquals" : {
              "kms:ViaService" : "s3.${var.region}.amazonaws.com"
            },
            "StringLike" : {
              "kms:EncryptionContext:aws:s3:arn" : [
                "arn:aws:s3:::%FIREHOSE_POLICY_TEMPLATE_PLACEHOLDER%/*"
              ]
            }
          }
        },
        {
          "Sid" : "",
          "Effect" : "Allow",
          "Action" : [
            "logs:PutLogEvents"
          ],
          "Resource" : "*"
        },
        {
          "Sid" : "",
          "Effect" : "Allow",
          "Action" : [
            "kinesis:DescribeStream",
            "kinesis:GetShardIterator",
            "kinesis:GetRecords",
            "kinesis:ListShards"
          ],
          "Resource" : "*"
        },
        {
          "Effect" : "Allow",
          "Action" : [
            "kms:Decrypt"
          ],
          "Resource" : "*",
          "Condition" : {
            "StringEquals" : {
              "kms:ViaService" : "kinesis.${var.region}.amazonaws.com"
            },
            "StringLike" : {
              "kms:EncryptionContext:aws:kinesis:arn" : "arn:aws:kinesis:${var.region}:${data.aws_caller_identity.current.account_id}:stream/${local.kinesis_data_streams_name}"
            }
          }
        }
      ]
    }
  )

}

