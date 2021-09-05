import json
import boto3
import urllib3


STREAM_NAME = "kinesis-drinks"
DRINKS_ENDPOINT = "https://api.punkapi.com/v2/beers/random"
kinesis_client = boto3.client('kinesis')
http = urllib3.PoolManager()


def get_data():
    """
    Fetches random data from the API 
    and send it to Kinesis Data Streams.
    """
    resp = http.request("GET", DRINKS_ENDPOINT)
    resp_json = json.loads(resp.data.decode("utf-8"))[0]
    return json.dumps(resp_json)


def lambda_handler(event, context):

    kinesis_client.put_record(
        StreamName=STREAM_NAME,
        Data=get_data(),
        PartitionKey="partitionkey")

    return {
        "statusCode": 200,
        "body": json.loads(get_data())
    }
