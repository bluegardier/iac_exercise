
resource "aws_glue_catalog_database" "drinks_database" {
  name = "drinks-database"
}


resource "aws_glue_crawler" "glue_drinks_crawler" {
  database_name = aws_glue_catalog_database.drinks_database.name
  name          = "drinks_crawler"
  role          = aws_iam_role.glue_role.arn
  description   = "Crawler for table creation from the s3's drinks .csv"


  s3_target {
    path = "s3://${aws_s3_bucket.glue_bucket.bucket}"
  }
}