from pyspark.sql import SparkSession

# Initialize Spark
spark = SparkSession.builder \
    .appName("POC-App") \
    .getOrCreate()

# Create a small dataset
data = [("Spark", 10), ("Docker", 20), ("POC", 30)]
df = spark.createDataFrame(data, ["Tool", "Speed_Score"])

# Run a SQL query
df.createOrReplaceTempView("tools")
result = spark.sql("SELECT * FROM tools WHERE Speed_Score > 15")

result.show()
spark.stop()