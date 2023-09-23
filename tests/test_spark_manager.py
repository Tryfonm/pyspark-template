from spark_template.main import spark_manager
from pyspark.sql import SparkSession

APPNAME = "mySimpleApp"


def test_spark_manager():
    """_summary_"""
    env = "test"

    with spark_manager(env) as spark:
        assert isinstance(spark, SparkSession)

        assert spark.sparkContext.appName == APPNAME
        assert spark.sparkContext._jsc.sc().isStarted()
