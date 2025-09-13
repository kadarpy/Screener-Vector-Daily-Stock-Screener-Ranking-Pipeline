from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lag, avg, when, to_date, max, min, round
from pyspark.sql.window import Window
import yfinance as yf
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

spark = SparkSession.builder.appName("PysparkStock").getOrCreate()

ticker_dic = {
 "indrenew.bo": "IND Renewable",
 "veerenrgy.bo": "Veer Energy",
 "amtl.bo": "Advance Meter",
 "gitarenew.bo": "Gita Renewable",
 "karmaeng.bo": "Karma Energy Ltd",
 "waa.bo": "Waa Solar",
 "globuscon.bo": "Globus Power",
 "indowind.bo": "Indowind Energy",
 "suranat&p.bo": "Surana Telecom",
 "waaree.bo": "Waaree Tech",
 "greenpower.bo": "Orient Green",
 "gipcl.bo": "Guj Inds. Power",
 "uel.bo": "Ujaas Energy",
 "kpel.bo": "K.P. Energy",
 "ina.bo": "Insolation Ener",
 "ptc.bo": "PTC India",
 "inoxgreen.bo": "Inox Green",
 "rtnpower.bo": "RattanIndia Pow.",
 "gmrp&ui.bo": "GMR Urban",
 "pginvit.bo": "Powergrid Infra.",
 "kpigreen.bo": "KPI Green Energy",
 "relinfra.bo": "Reliance Infra.",
 "indigrid.bo": "IndiGrid Trust",
 "jppower.bo": "JP Power Ven.",
 "acmesolar.bo": "ACME Solar Hold.",
 "nava.ns": "Nava",
 "rpower.bo": "Reliance Power",
 "cesc.bo": "CESC",
 "nlcindia.bo": "NLC India",
 "sjvn.bo": "SJVN",
 "torntpower.bo": "Torrent Power",
 "nhpc.bo": "NHPC Ltd",
 "ntpc.bo": "NTPC",
 "jswenergy.bo": "JSW Energy",
 "adaniensol.bo": "Adani Energy Sol",
 "tatapower.bo": "Tata Power Co.",
 "adanigreen.bo": "Adani Green",
 "adanipower.bo": "Adani Power",
 "powergrid.bo": "Power Grid Corpn",
 "ntpcgreen.bo": "NTPC Green Ene."
}
tickers = list(ticker_dic.keys())

data = []
for tick in tickers:
    try:
        historical = yf.Ticker(tick).history(period="2y")
        if historical.empty:
            continue
        historical.reset_index(inplace=True)
        for i in historical.itertuples():
            data.append({"company": ticker_dic[tick],"date": i.Date.strftime("%Y-%m-%d"),"open": i.Open,"high": i.High,"low": i.Low,"close": i.Close,"volume": i.Volume})
        print(f"fetch success for company - {ticker_dic[tick]}")
    except:
        print(f"fail {ticker_dic[tick]}")

df = spark.createDataFrame(data)

df = df.withColumn("date", to_date("date")).dropna()

w = Window.partitionBy("Company").orderBy("date")

df = df.withColumn("return_3months", round((col("close") - lag("close", 63).over(w)) / lag("close", 63).over(w) * 100, 2))

df = df.withColumn("return_6months", round((col("Close") - lag("close", 126).over(w)) / lag("close", 126).over(w) * 100, 2))

df = df.withColumn("return_1year", round((col("Close") - lag("close", 252).over(w)) / lag("close", 252).over(w) * 100, 2))

df = df.withColumn("gap_bias", round((col("open") - lag("close", 1).over(w)) / lag("close", 1).over(w) * 100, 2))

df = df.withColumn("intraday_sentiment",round(when (col("high") != col("low"),(col("close") - col("open")) / (col("high") - col("low")) * 100 ).otherwise(0),2))

df = df.withColumn("avg_vol_20d", round(avg("volume").over(w.rowsBetween(-20, -1)), 0))

df = df.withColumn("vol_spike_ratio", round(when(col("avg_vol_20d") > 0, col("volume") / col("avg_vol_20d")), 2))

"""To fetch the latest date data"""
latest = df.groupBy("company").agg(max("date").alias("latest_date"))

snap = df.join(latest, (df.company == latest.company) & (df.date == latest.latest_date), "inner").drop(latest.company).drop("latest_date")
pdf = snap.toPandas()
pdf.to_csv("snap.csv")

try:
    pdf = df.toPandas()
    engine = create_engine(f"postgresql+psycopg2://myuser:mypassword@postgres:5432/mydatabase", echo=True)
    with engine.connect() as conn:
        print("Connected to PostgreSQL",conn)
    try:
        pdf.to_sql("ohlc_power", con=engine, if_exists="append", index=False)
        print("Data inserted into PostgreSQL")
        conn.commit()
        conn.close()
    except:
        print("Can not insert data!")
except Exception as error:
    print("Error loading to database",error)