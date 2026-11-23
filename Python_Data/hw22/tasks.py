import pandas as pd
import time

# Task 1
aggregated_sum = 0
aggregated_count = 0

for chunk in pd.read_csv("homework.csv", chunksize=10000):
    aggregated_sum += chunk["score"].sum()
    aggregated_count += chunk["score"].count()

print(f"Task 1\nMean score: {aggregated_sum / aggregated_count:.2f}\n")


# Task 2
# Non-optimized
start = time.time()
df = pd.read_csv("homework.csv")
normal_time = time.time() - start
normal_memory = df.memory_usage(deep=True).sum()
normal_types = df.dtypes
del df

# Optimized
start = time.time()
df_optimized = pd.read_csv(
    "homework.csv",
    dtype={"id": "int32", "name": "category", "age": "int8", "score": "float32"},
)
optimized_time = time.time() - start
optimized_memory = df_optimized.memory_usage(deep=True).sum()

print(f"""
Task 2:
Normal types:
{normal_types}

Optimized types:
{df_optimized.dtypes}

Normal time: {normal_time:.4f}s
Optimized time: {optimized_time:.4f}s

Normal memory: {normal_memory / 1024**2:.2f} MB
Optimized memory: {optimized_memory / 1024**2:.2f} MB
""")


# Task 3
df_optimized.to_parquet("homework.parquet", index=False)
del df_optimized

start = time.time()
parquet_df = pd.read_parquet("homework.parquet")
parquet_time = time.time() - start
parquet_memory = parquet_df.memory_usage(deep=True).sum()

print(f"""Task 3:
Optimized CSV read time: {optimized_time:.4f}s
Parquet read time: {parquet_time:.4f}s

Optimized CSV memory: {optimized_memory / 1024**2:.2f} MB
Parquet memory: {parquet_memory / 1024**2:.2f} MB""")
