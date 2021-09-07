import time
import boto3
import pandas as pd
from dotenv import load_dotenv
import io
import os

load_dotenv()

class QueryAthena:
    """
    This object takes care of creating and fetching the data
    table create by AWS Glue Crawler. It's returns a pd.DataFrame
    for proper data analysis and machine learning algorithms.
    """

    def __init__(self, query, s3_bucket, database):
        self.database = database
        self.folder = "drinks_table/"
        self.bucket = s3_bucket
        self.s3_input = 's3://' + self.bucket
        self.s3_output = 's3://' + self.bucket + '/' + self.folder
        self.region_name = os.environ.get("REGION_NAME")
        self.aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
        self.query = query

    def load_conf(self, q):
        """
        Creates a connection with AWS Athena for querying the data.

        Parameters
        ----------
        q : str
        The query SQL syntax for databasing.

        Returns
        -------

        """

        try:
            self.client = boto3.client('athena',
                                       region_name=self.region_name,
                                       aws_access_key_id=self.aws_access_key_id,
                                       aws_secret_access_key=self.aws_secret_access_key)
            response = self.client.start_query_execution(
                QueryString=q,
                QueryExecutionContext={
                    'Database': self.database
                },
                ResultConfiguration={
                    'OutputLocation': self.s3_output,
                }
            )
            self.filename = response['QueryExecutionId']
            print('Execution ID: ' + response['QueryExecutionId'])

        except Exception as e:
            print(e)

        return response

    def run_query(self):
        """
        Executes the query from load_conf, properly queueing it.

        Returns
        -------

        """

        queries = [self.query]
        for q in queries:
            res = self.load_conf(q)
        try:
            query_status = None
            while query_status == 'QUEUED' or query_status == 'RUNNING' or query_status is None:
                query_status = \
                self.client.get_query_execution(QueryExecutionId=res["QueryExecutionId"])['QueryExecution']['Status'][
                    'State']
                print(query_status)
                if query_status == 'FAILED' or query_status == 'CANCELLED':
                    raise Exception('Athena query with the string "{}" failed or was cancelled'.format(self.query))
                time.sleep(10)
            print('Query "{}" finished.'.format(self.query))

            df = self.obtain_data()
            return df

        except Exception as e:
            print(e)

    def obtain_data(self):
        """
        Fetches the table created and returns it as a pd.DataFrame.

        Returns
        -------

        """
        try:
            self.resource = boto3.resource('s3',
                                           region_name=self.region_name,
                                           aws_access_key_id=self.aws_access_key_id,
                                           aws_secret_access_key=self.aws_secret_access_key
                                           )

            response = self.resource \
                .Bucket(self.bucket) \
                .Object(key=self.folder + self.filename + '.csv') \
                .get()

            return pd.read_csv(io.BytesIO(response['Body'].read()), encoding='utf8')
        except Exception as e:
            print(e)