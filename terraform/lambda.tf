resource "aws_lambda_function" "data_to_kinesis_lambda" {
  filename      = "${local.lambda_path}/${local.fetch_lambda_func_name}.zip"
  function_name = local.fetch_lambda_func_name
  role          = aws_iam_role.lambda_role_kinesis.arn
  handler       = "${local.fetch_lambda_func_name}.lambda_handler"

  source_code_hash = filebase64sha256("${local.lambda_path}/${local.fetch_lambda_func_name}.zip")

  runtime = var.runtime

}


resource "aws_lambda_function" "preprocess_firehose_lambda" {
  filename      = "${local.lambda_path}/${local.preprocess_lambda_func_name}.zip"
  function_name = local.preprocess_lambda_func_name
  role          = aws_iam_role.lambda_role_firehose.arn
  handler       = "${local.preprocess_lambda_func_name}.lambda_handler"
  timeout       = var.lambda_timeout


  source_code_hash = filebase64sha256("${local.lambda_path}/${local.preprocess_lambda_func_name}.zip")

  runtime = var.runtime

}

