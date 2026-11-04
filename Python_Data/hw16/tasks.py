import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# task 1
df = sns.load_dataset("tips")
sns.histplot(
    data=df,
    x="total_bill",
    bins=20,
    kde=True,
    hue="smoker",
    palette={"Yes": "teal", "No": "orange"},
)
plt.title("Розподіл Суми Рахунку за Категорією Курців")
plt.xlabel("Сума Рахунку (USD)")
plt.ylabel("Щільність Ймовірності")
plt.show()


# task 2
sns.histplot(
    data=df,
    x="total_bill",
    bins=20,
    kde=True,
    color="brown",
    alpha=0.7,
    line_kws={"linewidth": 3},
)
plt.title("Розподіл Суми Рахунку з Налаштуваннями Графіка")
plt.xlabel("Сума Рахунку (USD)")
plt.ylabel("Щільність Ймовірності")
plt.show()

# task 3
df = sns.load_dataset("penguins").dropna()
df_encoded = df.copy()
for col in ["species", "island", "sex"]:
    df_encoded[col] = df_encoded[col].astype("category").cat.codes

corr = df_encoded.corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Кореляційна матриця (з категоріальними змінними)")
plt.show()
