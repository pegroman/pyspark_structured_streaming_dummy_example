from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split

spark = SparkSession.builder.appName("Ejemplo1").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

lines = spark.readStream.format("socket").option("host", "localhost") \
    .option("port", 9999).load()

# Split the lines into words
words = lines.select(
   explode(
       split(lines.value, " ")
   ).alias("word")
)

# Generate running word count
wordCounts = words.groupBy("word").count()

query = wordCounts.writeStream.outputMode("complete") \
    .format("console").option("numRows","1000").start()

query.awaitTermination()