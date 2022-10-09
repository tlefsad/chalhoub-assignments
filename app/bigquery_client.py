import logging
import os
from io import BytesIO
from typing import Optional
from google.cloud import bigquery


BQ_SCHEMA = os.path.join(os.path.dirname(__file__), "resources/bq_schema.json")


class BigQueryClient:
    """
    BigQuery Client Class.
    Attributes
        client: google.cloud.bigquery client instance.
        schema: bigquery schema as JSON format
    """
    def __init__(self, project: Optional[str] = None):
        self.client = bigquery.Client(project=project)
        self.schema = self.client.schema_from_json(BQ_SCHEMA)

    def load(self, table_id: str, payload: BytesIO) -> None:
        """
        Load data to the destination table.
        """
        job_config = bigquery.LoadJobConfig(
            schema=self.schema,
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
            source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
            ignore_unknown_values=True,
        )

        load_job = self.client.load_table_from_file(
            payload,
            table_id, 
            job_config=job_config,
            rewind=True
        )

        load_job.result()
        destination_table = self.client.get_table(table_id)
        logging.info(f"{destination_table.num_rows} rows.")
