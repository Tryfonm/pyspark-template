from spark_template.main import spark_manager, transform


def test_transform():
    """_summary_"""
    with spark_manager(env="test") as spark:
        data = [(1, "User_1", 25, 55000), (2, "User_2", 30, 60000)]
        columns = ["id", "Name", "Age", "Salary"]
        df = spark.createDataFrame(data, columns)

        result_df = transform(df)
        assert (
            result_df.count() == 2
        )  # Check the number of rows in the transformed DataFrame
        assert "Age" in result_df.columns
        assert "AverageSalary" in result_df.columns
