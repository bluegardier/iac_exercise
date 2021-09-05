import base64
import json
import boto3
import csv
import io
from datetime import datetime

s3 = boto3.client('s3')
now = datetime.now()

headers = [
    "id",
    "name",
    "abv",
    "ibu",
    "target_fg",
    "target_og",
    "ebc",
    "srm",
    "ph"
]


def lambda_handler(event, context):
    output = []

    for record in event['records']:
        payload = base64.b64decode(record['data']).decode('utf-8')
        payload = json.loads(payload)

        # Creates the data and columns to generate the .csv.
        data_drinks = [
            payload["id"],
            payload["name"],
            payload["abv"],
            payload["ibu"],
            payload["target_fg"],
            payload["target_og"],
            payload["ebc"],
            payload["srm"],
            payload["ph"]
        ]

        for i in range(len(data_drinks)):
            data_drinks[i] = str(data_drinks[i])

        csvio = io.StringIO()
        writer = csv.writer(csvio)
        writer.writerow(headers)
        writer.writerows([data_drinks])

        # Generate the selected columns for Firehose Delivery Stream.
        new_data = {
            "id": data_drinks[0],
            "name": data_drinks[1],
            "abv": data_drinks[2],
            "ibu": data_drinks[3],
            "target_fg": data_drinks[4],
            "target_og": data_drinks[5],
            "ebc": data_drinks[6],
            "srm": data_drinks[7],
            "ph": data_drinks[8]
        }

        new_data = json.dumps(new_data)

        output_record = {
            'recordId': record['recordId'],
            'result': 'Ok',
            'data': base64.b64encode(new_data.encode('utf-8'))
        }

        output.append(output_record)

        # Exporting the .csv to the bucket.
        s3.put_object(
            Body=csvio.getvalue(),
            ContentType='text/csv',
            Bucket='bgardier-clean-bucket',
            Key='clean_drinks_{}.csv'.format(now)
        )

    return {'records': output}

