import os
import shutil
from spark_template.main import spark_manager, load


def test_load():
    """_summary_"""
    with spark_manager(env="test") as spark:
        output_path = "./test_output/"
        data = [(1, "User_1", 25, 55000), (2, "User_2", 30, 60000)]
        columns = ["id", "Name", "Age", "Salary"]
        df = spark.createDataFrame(data, columns)

        load(df, output_path=output_path)
        assert os.path.exists(output_path)
        shutil.rmtree(output_path)
