variable "cloudwatch_schedule_trigger" {
  type        = string
  default     = "rate(5 minutes)"
  description = "The time interval which triggers the lambda function."
}

variable "shard_count" {
  type        = number
  default     = 1
  description = "Number of shards the Data Stream will have."
}


variable "retention_period" {
  type        = number
  default     = 24
  description = "Number of hours the Data Stream persist the data."
}

variable "runtime" {
  type        = string
  default     = "python3.8"
  description = "Lambda's programming language."
}

variable "region" {
  description = "The AWS region we want this bucket to live in."
  default     = "sa-east-1"
}

variable "buffer_interval" {
  description = "The interval in seconds Firehose sends data to S3."
  default     = 60
}

variable "lambda_timeout" {
  description = "Seconds until lambda returns a timeout."
  default     = 60
}

variable "glue_bucket_name" {
  description = "Seconds until lambda returns a timeout."
  default     = "bgardier-glue-bucket"
}

variable "clean_bucket_name" {
  description = "Seconds until lambda returns a timeout."
  default     = "bgardier-clean-bucket"
}

variable "raw_bucket_name" {
  description = "Seconds until lambda returns a timeout."
  default     = "bgardier-raw-bucket"
}