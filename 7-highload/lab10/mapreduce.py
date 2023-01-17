from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType, TimestampType, MapType
import pyspark.sql.functions as F

# class WikipediaArticle:
#     title: str
#     text: str
#     def __init__(self, title, text):
#         self.title = title
#         self.text = text

schema = StructType([
    StructField("title", StringType(), nullable=False), 
    StructField("text", StringType(), nullable=False)
])

LANGS = ["JavaScript", "Java", "PHP", "Python", "C#", "C++", "Ruby", "CSS", "Objective-C", "Perl", "Scala", "Haskell", "MATLAB", "Clojure", "Groovy"]

def parse_line(line: str) -> tuple:
    subs = "</title><text>"
    i = line.find(subs)
    title = line[14:i]
    text = line[i+len(subs):-16]
    return (title, text)

def occurences(line:str):
    counts = dict()
    for l in LANGS:
        ll = l.lower()
        counts[ll] = line.count(ll)
    return counts

def mapgt0(map):
    return zip()

def main():
    spark = SparkSession.builder.appName("SimpleApp").getOrCreate()
    textFile = spark.read.text("/app/wikipedia.dat")
    # user defined function to transform data to my model
    udf_read = udf(parse_line, schema)
    # transform data to my model:
    # - add column 'article' with a structured data
    df = textFile.withColumn('article', udf_read(textFile['value']))
    # split and to lower
    df = df.select(F.lower(df.article.title).alias('title'), F.lower(df.article.text).alias('text'))
    
    # count total number of occurences of lanuage names
    udf_occ = udf(occurences, MapType(StringType(), LongType()))
    df = df.withColumn('occurences', udf_occ(df.text))
    
    # compute max(occurences, 1) as bOccured.
    # sum of this column will be the number of articles.
    df = df.withColumn('bOccured', 
            F.transform_values(
                df.occurences, 
                lambda k,v: F.when(v > 0, 1).when(v == 0, 0)
            )
        )

    # reduce for total lang occurences
    A = df.select(F.explode(df.occurences).alias('lang','occurences'))
    A = A.groupBy('lang').sum('occurences').show()

    # reduce for number of articles
    B = df.select(F.explode(df.bOccured).alias('lang','bOccured'))
    B = B.groupBy('lang').sum('bOccured').show()






if __name__ == "__main__":
    main()