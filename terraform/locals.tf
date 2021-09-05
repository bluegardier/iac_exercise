locals {
  lambda_path                 = "lambda/"
  fetch_lambda_func_name      = "fetch_data_from_api"
  preprocess_lambda_func_name = "preprocess_data"
  kinesis_data_streams_name   = "kinesis-drinks"
  drinks_endpoint             = "https://api.punkapi.com/v2/beers/random"
  glue_bucket_name            = "bgardier-glue-bucket"
}

