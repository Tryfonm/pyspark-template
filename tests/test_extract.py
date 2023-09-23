from spark_template.main import spark_manager, extract


def test_extract():
    """_summary_"""
    with spark_manager(env="test") as spark:
        num_rows = 100
        synthetic_data = extract(spark, num_rows)
        assert synthetic_data.count() == num_rows
        assert "Name" in synthetic_data.columns
        assert "Age" in synthetic_data.columns
        assert "Salary" in synthetic_data.columns
