from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split

spark = SparkSession.builder.appName("Ejemplo1").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

lines = spark.readStream.format("socket").option("host", "localhost") \
    .option("port", 9999).load()

# Split the lines into words
temp = lines.select(
   explode(
       split(lines.value, " ")
   ).alias("temp")
)

# Generate running word count
temperaturas = temp.filter("temp > 25").groupBy("temp").count()

query = temperaturas.writeStream.outputMode("complete") \
    .format("console").start()

query.awaitTermination()