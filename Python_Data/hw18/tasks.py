import pandas as pd

# task 1
df_a = pd.DataFrame(
    {
        "EmployeeID": [1, 2, 3],
        "Name": ["Alice", "Bob", "Charlie"],
        "Department": ["HR", "Engineering", "Marketing"],
    }
)

df_b = pd.DataFrame(
    {"EmployeeID": [4, 5], "Name": ["David", "Eva"], "Department": ["Finance", "IT"]}
)

df_sum = pd.concat([df_a, df_b], ignore_index=True)
df_groups = pd.concat([df_a, df_b], keys=["Group_A", "Group_B"])

print(f"""Task 1:
DataFrame A:\n{df_a}
DataFrame B:\n{df_b}
Result DataFrame with resetting index:\n{df_sum}
Result DataFrame with keys:\n{df_groups}
""")

# task 2
orders_df = pd.DataFrame(
    {
        "OrderID": [1001, 1002, 1003, 1004],
        "CustomerID": [1, 2, 1, 3],
        "ProductID": [501, 502, 503, 504],
        "Quantity": [2, 1, 5, 3],
    }
)

customers_df = pd.DataFrame(
    {"CustomerID": [1, 2, 3, 4], "CustomerName": ["Alice", "Bob", "Charlie", "David"]}
)

accounts_df = pd.merge(
    orders_df, customers_df, how="inner", on="CustomerID", indicator=True
)
accounts_df = accounts_df.set_index(["CustomerID", "ProductID"])
print(f"""Task 2:
Orders DataFrame:\n{orders_df}
Customers DataFrame:\n{customers_df}
Result DataFrame:\n{accounts_df}

""")

# task 3
import numpy as np
import time

np.random.seed(0)
transactions_df = pd.DataFrame(
    {
        "TransactionID": range(1, 100001),
        "UserID": np.random.randint(1, 1001, size=100000),
        "ProductID": np.random.randint(1, 500, size=100000),
        "Date": pd.date_range(start="2023-01-01", periods=100000, freq="min"),
        "Amount": np.random.uniform(10.0, 1000.0, size=100000),
    }
)
products_df = pd.DataFrame(
    {
        "ProductID": range(1, 500),
        "Price": np.random.uniform(1.0, 100.0, size=499),
        "StorageAmount": np.random.randint(0, 1000, size=499),
        "Likes": np.random.randint(0, 100000, size=499),
    }
)
transactions_df = transactions_df.set_index(["UserID", "ProductID"])
products_df = products_df.set_index("ProductID")
transactions_df["Amount"] = transactions_df["Amount"].astype("float32")

start = time.perf_counter()
optimized_df = transactions_df.join(products_df, on="ProductID", how="inner")
optimized_time = time.perf_counter() - start

normal_transactions = transactions_df.reset_index()
normal_products = products_df.reset_index()

start = time.perf_counter()
normal_df = pd.merge(normal_transactions, normal_products, on="ProductID", how="inner")
normal_time = time.perf_counter() - start

print(f"""Task 3:
Optimized merge: {optimized_time:.6f} seconds
Normal merge: {normal_time:.6f} seconds

""")

# task 4
df_sales = pd.DataFrame(
    {
        "SaleID": [2001, 2002, 2003, 2004, 2005],
        "StoreID": [10, 20, 10, 30, 20],
        "ProductID": [301, 302, 303, 301, 304],
        "UnitsSold": [50, 60, 70, 80, 90],
    }
)

df_suppliers = pd.DataFrame(
    {
        "SupplierID": [401, 402, 403, 404],
        "ProductID": [301, 302, 303, 305],
        "SupplierName": ["Supplier A", "Supplier B", "Supplier C", "Supplier D"],
    }
)
df_sales = df_sales.set_index(["StoreID", "ProductID"])

# many-to-one є доцільним в цьому випадку, бо ProductID може повторюватися у декілька продажів у df_sales, але у df_suppliers ProductID є унікальним, отже кожному продажу відповідає не більше одного посточальника

df_total = pd.merge(
    df_sales,
    df_suppliers,
    on="ProductID",
    how="inner",
    validate="many_to_one",
    suffixes=("_sale", "_supplier"),
)

print(f"""Task 4:
Total df:\n{df_total}
""")
