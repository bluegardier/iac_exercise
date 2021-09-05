terraform {
  required_version = ">= 0.12"
}


provider "aws" {
}

data "aws_caller_identity" "current" {}