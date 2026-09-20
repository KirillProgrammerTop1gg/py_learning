import numpy as np


def array_stats(arr):
    return f"""Сума масиву: {arr.sum()}
Середнє арифметичне значення масиву: {arr.mean()}
Мінімальне значення масиву: {arr.min()}
Максимальне значення масиву: {arr.max()}
"""


# task 1
arr = np.arange(10, 20)
print(f"Task 1:\n{array_stats(arr)}")

# task 2
arr = np.random.rand(1000)
print(f"Task 2:\n{array_stats(arr)}")

# task 3
matrix = np.random.randint(1, 10, (5, 5))
print(f"""Task3
Матриця:
{matrix}
Всі елементи другого стовпця: {matrix[:, 1]}
Всі елементи з другого рядка: {matrix[1, :]}
Одновимірний вигляд: {matrix.flatten()}
""")

# task 4
arr = np.random.rand(500_000)
print(f"Task 4:\n{array_stats(arr)}")
