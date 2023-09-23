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
    """_summary_

    Args:
        env (str): _description_

    Yields:
        Generator[SparkSession, None, None]: _description_
    """
    spark = SparkSession.builder.appName(APPNAME).getOrCreate()
    try:
        yield spark
    except Exception as e:
        LOGGER.debug(e)
    finally:
        spark.stop()


def extract(spark, num_rows=1000000):
    """_summary_

    Args:
        spark (_type_): _description_
        num_rows (int, optional): _description_. Defaults to 1000000.

    Returns:
        _type_: _description_
    """
    synthetic_data = (
        spark.range(1, num_rows + 1)
        .withColumn("Name", concat(lit("User_"), col("id")))
        .withColumn("Age", (rand() * 50 + 18).cast("int"))
        .withColumn("Salary", (rand() * 50000 + 30000).cast("bigint"))
    )
    synthetic_data.show()
    return synthetic_data


def transform(df):
    """_summary_

    Args:
        df (_type_): _description_

    Returns:
        _type_: _description_
    """
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
    """_summary_

    Args:
        df (_type_): _description_
    """
    df.write.format("parquet").mode("overwrite").save("./output/")


def run_job():
    """_summary_"""
    with spark_manager(env=ENV) as spark:
        df = extract(spark, num_rows=1000000)
        df = transform(df)
        load(df)


if __name__ == "__main__":
    # 123
    run_job()
