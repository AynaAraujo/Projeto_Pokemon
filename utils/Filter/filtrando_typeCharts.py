from pyspark.sql.functions import col, when, regexp_replace, trim
from pyspark.sql.types import DoubleType

def ajuste_TypeChart(df):
    colunas_numericas = [c for c in df.columns if c != "Types"]

    for coluna in colunas_numericas:
        df = df.withColumn(coluna, trim(col(coluna)))
        df = df.withColumn(coluna, regexp_replace(col(coluna), ",", "."))
        df = df.withColumn(
            coluna,
            when(
                col(coluna).rlike(r'^(\d+(\.\d+)?|\.\d+)$'),
                col(coluna).cast(DoubleType())
            ).otherwise(None)
        )

    for coluna in colunas_numericas:
        df = df.withColumn(coluna, when(col(coluna).isNull(), 1.0).otherwise(col(coluna)))

    print("\n--- DEBUG: Após ajuste_TypeChart ---")
    df.printSchema()
    df.show(5, truncate=False)

    return df
