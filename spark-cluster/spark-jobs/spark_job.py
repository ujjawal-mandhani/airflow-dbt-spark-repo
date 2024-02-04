from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("SampleSparkJob").getOrCreate()
df = spark.sql("""
select 1 as t
""")
df.show()