resource "aws_cloudwatch_event_rule" "trigger_rule" {
  name                = "trigger-fetch-data"
  description         = "Trigger lambda function for data fetching."
  schedule_expression = var.cloudwatch_schedule_trigger
}

resource "aws_cloudwatch_event_target" "lambda-func" {
  target_id = "lambda"
  rule      = aws_cloudwatch_event_rule.trigger_rule.name
  arn       = aws_lambda_function.data_to_kinesis_lambda.arn
}

resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.data_to_kinesis_lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.trigger_rule.arn
}  