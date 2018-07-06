import sys

from pyspark.sql.context import SQLContext, SparkSession
from pyspark import SparkContext
from pyspark.conf import SparkConf


LINE_LENGTH = 200


def print_horizontal():
    """
    Simple method to print horizontal line
    :return: None
    """
    for i in range(LINE_LENGTH):
        sys.stdout.write('-')
    print("")


print ("Successfully imported Spark Modules -- `SparkContext, SQLContext, SparkConf`")
print_horizontal()


def get_configured_context():
    conf = SparkConf().setAppName("parquet_testing")
    sc = SparkContext(conf=conf)
    # Update to use the minio instance
    sc._jsc.hadoopConfiguration().set('fs.s3a.endpoint', 'http://127.0.0.1:9000')
    sc._jsc.hadoopConfiguration().set('fs.s3a.access.key', 'QDLKDBDPFW9W2I1A70JA')
    sc._jsc.hadoopConfiguration().set('fs.s3a.secret.key', 'x/doxcI1HByF/S4M1gF5y4e2NFt3XFkZ9SISqen7')
    sc._jsc.hadoopConfiguration().set('fs.s3a.path.style.access', 'true')
    sc._jsc.hadoopConfiguration().set('fs.s3a.impl', 'org.apache.hadoop.fs.s3a.S3AFileSystem')
    return sc


def read_existing_parquet():
    sc = get_configured_context()
    sql_context = SQLContext(sparkContext=sc)

    # Loads parquet file located in AWS S3 / minio into RDD Data Frame
    parquet_file = sql_context.read.parquet("s3a://testparquet/nation.parquet")
    parquet_file.registerTempTable("parquet_file")

    # Run standard SQL queries against temporary table
    nations_all_sql = sql_context.sql("SELECT * FROM parquet_file")
    nations_all = nations_all_sql.rdd.map(lambda p: "Country: {0:15} Ipsum Comment: {1}".format(p.N_NAME, p.N_COMMENT))

    for idx, nation in enumerate(nations_all.collect()):
        if idx == 0:
            print("All Nations and Comments -- `SELECT * FROM parquet_file`")
            print_horizontal()
        print(nation)
    else:
        print_horizontal()

    # Use standard SQL to filter
    nations_filtered_sql = sql_context.sql("SELECT N_NAME FROM parquet_file WHERE N_NAME LIKE '%IND%'")
    nations_filtered = nations_filtered_sql.rdd.map(lambda p: "Country: {0:20}".format(p.N_NAME))

    for idx, nation in enumerate(nations_filtered.collect()):
        if idx == 0:
            print("Nations Filtered -- `SELECT name FROM parquet_file WHERE name LIKE '%IND%'`")
            print_horizontal()
        print(nation)
    else:
        print_horizontal()


def csv_to_parquet():
    sc = get_configured_context()
    session = SparkSession(sparkContext=sc)
    # This will need to be in location where worker has access to it
    df = session.read.csv("/Users/bogdanneacsa/Work/sparkenv/cookbooks/GPR-sample2.csv")
    df.show()
    df.write.parquet("s3a://testparquet/gprsample.parquet")


def query_own_parquet():
    sc = get_configured_context()
    session = SparkSession(sparkContext=sc)

    df = session.read.parquet("s3a://testparquet/gprsample.parquet")
    df.select('browserFamily').distinct().show()


# read_existing_parquet()
# csv_to_parquet()
query_own_parquet()
