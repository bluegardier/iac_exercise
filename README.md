![Passing Status](https://github.com/bluegardier/iac_exercise/actions/workflows/github-ci.yml/badge.svg)

# PicPay' Technical Challenge: MLOps

The focus of this challenge is to build up a data pipeline architecture on AWS using Terraform. At the end of this process, we should be able to fetch a structured table from s3 to train a machine learning model.

Regarding the machine learning problem, it's a regression type problem that aims to estimates the **ibu** (International Bitterness Units) of a beer.
### Data Dependencies
We are using the following Data Source:

| Source | Description |
|--------|-------------|
|[Punk API](https://punkapi.com/documentation/v2)| Info about a number of artisanal beers.|------------|

### Column Inputs
| Column | Type | Description |
|--------|------|-------------|
|id|int|Beer's ID|
|name|str|Beer's Name|
|abv|float|The Beer's alcohol by volume|
|ibu|float|The Beer's international bittering unit|
|target_fg|float|The Beer's final gravity|
|target_og|float|The Beer's original gravity|
|ebc|float|A modern brew system to specify beer color|
|srm|float|Likewise the ebc, it's measure the beer color |
|ph|float| The Beer's ph|

## Repository Structure
- ```terraform```: The terraform configuration to create the required architecure. See the ```Installation``` section for more details.

- ```analysis```:  A Jupyter Notebook demonstration on how the data created through the pipeline, was used to train a machine learning model.

- ```iac_exercise```: The project modules.

- ```tests```: The project's test directory.

## Installation
Run the command below on the root directory to install the proper dependencies.

```
pip install .
```

To replicate the architecture, a few steps are required before running it.
Its necessary to set your **AWS_ACCESS_KEY_ID**, **AWS_SECRET_ACCESS_KEY** and **REGION_NAME** as environment variables for account replication.

```
export AWS_ACCESS_KEY_ID="anaccesskey"
export AWS_SECRET_ACCESS_KEY="asecretkey"
export AWS_DEFAULT_REGION="yourregion"
```

The second step is to zip the lambda functions so that they can be uploaded properly into your AWS account.
```
cd terraform
cd lambda
zip fetch_data_from_api.zip fetch_data_from_api.py
zip preprocess_data.zip preprocess_data.py
```

## Usage

From the root directory, run the commands below:

```
cd terraform
terraform apply --auto-approve
```




