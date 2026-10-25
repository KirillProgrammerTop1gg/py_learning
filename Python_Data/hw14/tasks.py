import matplotlib.pyplot as plt
import numpy as np

# task 1
weeks = ["Тиждень 1", "Тиждень 2", "Тиждень 3", "Тиждень 4"]

traffic = [1500, 1600, 1700, 1800]

sales_product_a = [300, 350, 400, 450]
sales_product_b = [200, 250, 300, 350]
sales_product_c = [100, 150, 200, 250]

plt.plot(
    weeks,
    traffic,
    color="green",
    linestyle="--",
    linewidth=2,
    marker="H",
    markersize=9,
    label="Графік активності трафіку",
)
plt.plot(
    weeks,
    sales_product_a,
    color="blue",
    linestyle="-",
    linewidth=2,
    marker="o",
    markersize=7,
    label="Графік продажів продукту A",
)
plt.plot(
    weeks,
    sales_product_b,
    color="purple",
    linestyle="-.",
    linewidth=2,
    marker="o",
    markersize=7,
    label="Графік продажів продукту B",
)
plt.plot(
    weeks,
    sales_product_c,
    color="orange",
    linestyle=":",
    linewidth=2,
    marker="o",
    markersize=7,
    label="Графік продажів продукту C",
)
plt.title("Завдання 1")
plt.ylabel("Значення")
plt.xlabel("Тижні")
plt.legend()
plt.twinx()
plt.show()

# task 2
x = np.linspace(0, 10, 1000)
y = np.sin(x) * np.cos(x)

plt.figure(figsize=(12, 6))

plt.plot(x, y)

plt.title("Завдання 2")
plt.xlabel("Ось x")
plt.ylabel("Ось y")
plt.tight_layout()
plt.show()

# task 3
sizes = [50, 25, 15, 10]
labels = ["Продажі", "Інвестиції", "Ліцензії", "Інше"]
plt.pie(sizes, labels=labels, colors=["#FF9999", "#66B3FF", "#f25589", "#77edbc"])
plt.title("Кольори сегментів")
plt.show()
