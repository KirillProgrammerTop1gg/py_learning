import pandas as pd

# task 1
data = {
    "TransactionID": [501, 502, 503, 504, 505],
    "TransactionDate": [
        "2023-12-01",
        "31/12/2023",
        "December 15, 2023",
        "2023/12/20",
        "2023-13-01",
    ],
}

transactions_df = pd.DataFrame(data)
transactions_df["TransactionDate"] = pd.to_datetime(
    transactions_df["TransactionDate"], format="mixed", errors="coerce"
)
transactions_df["Year"] = transactions_df["TransactionDate"].dt.year.astype("Int64")
transactions_df["Month"] = transactions_df["TransactionDate"].dt.month.astype("Int64")
print(f"Task 1:\n{transactions_df}\n")


# task 2
timestamps_df = pd.DataFrame(
    {
        "TimestampID": [601, 602, 603, 604],
        "UnixTimestamp": [1704067200, 1704153600, 1704240000, 1704326400],
    }
)
timestamps_df["UnixTimestamp"] = pd.to_datetime(
    timestamps_df["UnixTimestamp"], unit="s"
)
timestamps_df["Year"] = timestamps_df["UnixTimestamp"].dt.year.astype("Int64")
timestamps_df["Month"] = timestamps_df["UnixTimestamp"].dt.month.astype("Int64")
timestamps_df["Day"] = timestamps_df["UnixTimestamp"].dt.day.astype("Int64")
timestamps_df["Hour"] = timestamps_df["UnixTimestamp"].dt.hour.astype("Int64")
print(f"Task 2:\n{timestamps_df}\n")


# task 3
dates_df = pd.DataFrame(
    {
        "EntryID": [701, 702, 703, 704, 705],
        "DateString": [
            "2024-02-30",
            "02/28/2024",
            "2024/03/15",
            "March 32, 2024",
            "2024-04-10",
        ],
    }
)
dates_df["DateString"] = pd.to_datetime(
    dates_df["DateString"], format="mixed", errors="coerce"
)
print(f"Task 3:\n{dates_df}")
