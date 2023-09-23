import os
from spark_template.main import spark_manager, load


def test_load():
    """_summary_"""
    with spark_manager(env="test") as spark:
        data = [(1, "User_1", 25, 55000), (2, "User_2", 30, 60000)]
        columns = ["id", "Name", "Age", "Salary"]
        df = spark.createDataFrame(data, columns)
        output_path = "./test_output/"
        load(df)
        assert os.path.exists(output_path)
        os.rmdir(output_path)
