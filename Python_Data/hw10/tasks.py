import numpy as np
import pandas as pd

# task 1
print("----task 1----")
data = {
    "Name": ["Alex", "Bella", "Chris"],
    "Age": [30, 25, 35],
    "City": ["Kyiv", "Lviv", "Odesa"],
}
df = pd.DataFrame(data)

df["Salary"] = [50000, 60000, 55000]
df = df.drop("Age", axis=1)
new_row = pd.DataFrame({"Name": ["Diana"], "City": ["Dnipro"], "Salary": [58000]})
df = pd.concat([df, new_row], ignore_index=True)
df = df.drop(0, axis=0)
df["Department"] = "Sales"
df = df.drop("Salary", axis=1)

print(df)

# task 2
print("\n----task 2----")
data = {
    "Product": ["Book", "Pen", "Notebook"],
    "Price": [15, 2, 5],
    "Stock": [100, 500, 200],
}
df = pd.DataFrame(data)

df["Discount"] = "10%"
df = df.drop("Stock", axis=1)
new_row = pd.DataFrame({"Product": ["Pencil"], "Price": [1], "Discount": ["5%"]})
df = pd.concat([df, new_row], ignore_index=True)
df = df.drop(1, axis=0)
df["Supplier"] = "Stationery Co."
df = df.drop(2, axis=0)

print(df)
