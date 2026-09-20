import numpy as np

# task 1
print("Task 1")
# Створіть три двовимірні масиви
array1 = np.random.randint(-10, 11, (4, 4))
array2 = np.random.randint(-10, 11, (4, 4))
array3 = np.random.randint(-10, 11, (4, 4))

# Об'єднайте масиви уздовж нової осі
combined_array = np.stack([array1, array2, array3])

# Виведіть об'єднаний масив
print(f"Об'єднаний масив з новою віссю:\n{combined_array}\n")

assert combined_array.shape == (
    3,
    4,
    4,
), "Розмір об'єднаного масиву повинен бути (3, 4, 4)"


# task 2
print("Task 2")
B = np.random.randint(1, 10, (2, 3, 4))
print("Оригінальний тривимірний масив B:\n", B)

# Перетворення у двовимірний масив
B_reshaped = B.reshape((6, 4))
print("Масив після зміни форми:\n", B_reshaped)

# Перетворення у одновимірний
B_flattened = B_reshaped.flatten()
print("Одновимірний масив:\n", B_flattened, "\n")


# task 3
print("Task 3")
C = np.random.randint(1, 10, (3, 3, 3))
print("Оригінальний масив C:\\n", C)

# Сума по першій осі
sum_axis0 = C.sum(0)
print("Сума по осі 0:\n", sum_axis0)

# Сума по другій осі
sum_axis1 = C.sum(1)
print("Сума по осі 1:\n", sum_axis1)

# Загальна сума
total_sum = C.sum()
print("Загальна сума елементів масиву:", total_sum)
