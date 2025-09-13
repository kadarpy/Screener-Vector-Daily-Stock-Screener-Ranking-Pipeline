import json
import pandas as pd
import numpy as np
from kafka import KafkaConsumer
from pyspark.sql import SparkSession, Window 
from pyspark.sql.functions import col,to_date,row_number,percent_rank,min,max,when
from pyspark.sql.types import DoubleType,StringType,DateType
from sqlalchemy import create_engine

spark = SparkSession.builder.appName("kafkatopyspark").getOrCreate()

consumer = KafkaConsumer(
    'New_screener', # change the topic name 
    bootstrap_servers=['kafka:9092'],
    auto_offset_reset = 'earliest',                      
    consumer_timeout_ms = 5000,
    value_deserializer = lambda m: json.loads(m.decode('utf-8'))
)

lst = []                                                       
try:
    for i in consumer:
        data = i.value
        lst.append(data)
except Exception as error:
    print(f"error - {error}")
finally:
    consumer.close()

pandas_df = pd.DataFrame(lst)

columns = list(pandas_df.columns)
for i in columns:
    pandas_df[i] = pandas_df[i].replace('', np.nan)

df = spark.createDataFrame(pandas_df)

df =  df.drop("id")

new_colnames = {'name':'Company name',
 'cmprs.':"Current price",
 '3mth return%':"Return over 3months",
 '6mth return%':"Return over 6months",
 'p/e':"Price to Earning",
 'mar caprs.cr.':"Market Capitalization",
 'earnings yield%':"Earnings yield",
 'sales qtrrs.cr.':"Sales latest quarter",
 'pat qtrrs.cr.':"Profit after tax latest quarter",
 'qtr sales var%':"YOY Quarterly sales growth",
 'qtr profit var%':"YOY Quarterly profit growth",
 'roce%':"Return on capital employed",
 'debt / eq':"Debt to equity",
 'roe%':"Return on equity",
 'date':"Date"}

df_renamed = df
for old_name, new_name in new_colnames.items():
    df_renamed = df_renamed.withColumnRenamed(old_name, new_name)

df = df_renamed

df =  df.withColumn("Date", to_date(df["Date"], "yyyy-MM-dd")) \
        .withColumn("Current price", col("Current price").cast(DoubleType())) \
        .withColumn("Return over 3months", col("Return over 3months").cast(DoubleType())) \
        .withColumn("Return over 6months", col("Return over 6months").cast(DoubleType())) \
        .withColumn("Price to Earning", col("Price to Earning").cast(DoubleType())) \
        .withColumn("Market Capitalization", col("Market Capitalization").cast(DoubleType())) \
        .withColumn("Earnings yield", col("Earnings yield").cast(DoubleType())) \
        .withColumn("Sales latest quarter", col("Sales latest quarter").cast(DoubleType())) \
        .withColumn("Profit after tax latest quarter", col("Profit after tax latest quarter").cast(DoubleType())) \
        .withColumn("YOY Quarterly sales growth", col("YOY Quarterly sales growth").cast(DoubleType())) \
        .withColumn("YOY Quarterly profit growth", col("YOY Quarterly profit growth").cast(DoubleType())) \
        .withColumn("Return on capital employed", col("Return on capital employed").cast(DoubleType())) \
        .withColumn("Debt to equity", col("Debt to equity").cast(DoubleType())) \
        .withColumn("Return on equity", col("Return on equity").cast(DoubleType()))

df = df.fillna({
    "Price to Earning": 0,
     "Return on equity": 0,
     "Debt to equity": 0,
     "Earnings yield": 0,
     "Return over 3months": 0,
     "Return over 6months": 0,
     "YOY Quarterly profit growth": 0,
     "YOY Quarterly sales growth": 0
})

df = df.withColumn("MarketCapCategory",when(col("Market Capitalization") < 5000, "Small Cap").when((col("Market Capitalization") >= 5000) & (col("Market Capitalization") < 20000), "Mid Cap").otherwise("Large Cap"))


def normalize(colname):
    return (
        (col(colname) - min(col(colname)).over(Window.partitionBy("Date", "MarketCapCategory"))) /  (max(col(colname)).over(Window.partitionBy("Date", "MarketCapCategory")) - min(col(colname)).over(Window.partitionBy("Date", "MarketCapCategory"))))


df = df.withColumn("Return_3m_norm", normalize("Return over 3months"))
df = df.withColumn("Return_6m_norm", normalize("Return over 6months"))
df = df.withColumn("Earnings_yield_norm", normalize("Earnings yield"))
df = df.withColumn("PE_norm", normalize("Price to Earning"))
df = df.withColumn("Debt_eq_norm", normalize("Debt to equity"))
df = df.withColumn("ROCE_norm", normalize("Return on capital employed"))
df = df.withColumn("Profit_var_norm", normalize("YOY Quarterly profit growth"))
df = df.withColumn("Sales_var_norm", normalize("YOY Quarterly sales growth"))


df = df.withColumn(
    "Score", 
    (col("Return_3m_norm") * 0.15) +
    (col("Return_6m_norm") * 0.15) +
    (col("Earnings_yield_norm") * 0.20) +
    ((1 - col("PE_norm")) * 0.10) +
    ((1 - col("Debt_eq_norm")) * 0.10) +
    (col("ROCE_norm") * 0.20) +
    (col("Profit_var_norm") * 0.10) +
    (col("Sales_var_norm") * 0.10)
)


rank_window = Window.partitionBy("Date", "MarketCapCategory").orderBy(col("Score").desc())
df = df.withColumn("Rank", row_number().over(rank_window))


final_col = [
    "Company name", "Current price", "Price to Earning", "Market Capitalization",
    "YOY Quarterly profit growth", "Sales latest quarter", "YOY Quarterly sales growth",
    "Return on capital employed", "Profit after tax latest quarter", "Debt to equity",
    "Return on equity", "Earnings yield", "Return over 3months", "Return over 6months",
    "Date", "MarketCapCategory","Return_3m_norm","Return_6m_norm","Earnings_yield_norm",
    "PE_norm","Debt_eq_norm","ROCE_norm","Profit_var_norm","Sales_var_norm","Score","Rank"]

final = df.select(final_col)
final.show(10)
pdf = final.toPandas()
pdf.to_csv("screenerranked.csv")
try:
    engine = create_engine(f"postgresql+psycopg2://myuser:mypassword@postgres:5432/mydatabase", echo=True)
    with engine.connect() as conn:
        print("Connected to PostgreSQL",conn)
                
    try:
        pdf.to_sql("screenerrank", con=engine, if_exists="replace", index=False)
        print("Data inserted into PostgreSQL")
        conn.commit()
        conn.close()
    except:
        print("Can not insert data!")
        
except Exception as error:
    print("Error loading to database",error)