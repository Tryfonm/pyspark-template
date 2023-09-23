import os
from pathlib import Path
from contextlib import contextmanager
from typing import Generator

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, desc, avg, concat, lit, rand

from .logger import get_logger

ENV = os.getenv("ENV", "dev")
LOGGER = get_logger(Path(__file__).stem)
APPNAME = "mySimleApp"


@contextmanager
def spark_manager(env: str) -> Generator[SparkSession, None, None]:
    spark = SparkSession.builder.appName(APPNAME).getOrCreate()

    try:
        yield spark
    except Exception as e:
        LOGGER.debug(e)
    finally:
        spark.stop()


def extract(spark, num_rows=1000000):
    synthetic_data = (
        spark.range(1, num_rows + 1)
        .withColumn("Name", concat(lit("User_"), col("id")))
        .withColumn("Age", (rand() * 50 + 18).cast("int"))
        .withColumn("Salary", (rand() * 50000 + 30000).cast("bigint"))
    )
    synthetic_data.show()
    return synthetic_data


def transform(df):
    ordered_data = df.orderBy(desc("Salary")).withColumn(
        "HighSalary", col("Salary") >= 50000
    )

    grouped_by_age_ordered = (
        ordered_data.groupBy("Age")
        .agg(avg("Salary").cast("bigint").alias("AverageSalary"))
        .orderBy(desc("AverageSalary"))
    )

    grouped_by_age_ordered.show()
    return grouped_by_age_ordered


def load(df):
    df.write.format("parquet").mode("overwrite").save("./output/")


def run_job():
    with spark_manager(env=ENV) as spark:
        df = extract(spark, num_rows=1000000)
        df = transform(df)
        load(df)


if __name__ == "__main__":
    run_job()
