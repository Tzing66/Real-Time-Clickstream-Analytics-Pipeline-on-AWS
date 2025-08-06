import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql.functions import col, from_json, to_timestamp, to_date
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.types import StructType, StringType

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

#read raw JSON data recursively - these are the records placed here by the lambda function through the kinesis data stream
input_path = "s3://yourbucketname/" #change bucket name
raw_df = spark.read.option("recursiveFileLookup", "true").json(input_path)

#data cleaning
flattened_df = raw_df \
    .withColumn("ip", col("geo.ip")) \
    .withColumn("country", col("geo.country")) \
    .withColumn("city", col("geo.city")) \
    .drop("geo")

clean_df = flattened_df \
    .withColumn("event_time", to_timestamp("event_time")) \
    .filter(col("event_time").isNotNull())
    
clean_df = clean_df.withColumn("event_date", to_date("event_time"))

#check data - this is just for debugging
print("Schema:")
clean_df.printSchema()

print("Sample data:")
clean_df.show(5)

#output details - again for verification and debugging
output_path = "s3://outputbucketname/folder" #change this path. bucket must exist
print("Output path:", output_path)

print("Record count before filter:", clean_df.count())
clean_df = clean_df.filter(col("event_date").isNotNull())
print("Record count before write:", clean_df.count())

# Write data partitioned by event_date
clean_df  \
    .write \
    .mode("overwrite") \
    .partitionBy("event_date") \
    .parquet(output_path)

job.commit()

# import sys
# from awsglue.utils import getResolvedOptions
# from pyspark.context import SparkContext
# from awsglue.context import GlueContext
# from awsglue.job import Job
# from pyspark.sql.functions import col, to_timestamp

# args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# sc = SparkContext()
# glueContext = GlueContext(sc)
# spark = glueContext.spark_session
# job = Job(glueContext)
# job.init(args['JOB_NAME'], args)

# input_path = "s3://clickstream-raw-data-tanzini/"
# output_path = "s3://clickstream-processed-data-tanzini/debug-output/"

# df = spark.read.option("recursiveFileLookup", "true").json(input_path)
# df = df.withColumn("event_time", to_timestamp("event_time"))
# df = df.filter(col("event_time").isNotNull())

# # Try writing without partitioning or schema mods
# df.write.mode("overwrite").parquet(output_path)

# job.commit()
