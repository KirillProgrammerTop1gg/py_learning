import numpy as np

# task 1
print('----task 1----')
array = np.array([12, -5, 7, 9, -3, 15])
array = np.append(array, 10)
print(array)

# task 2
print('\n----task 2----')
array = np.array([[5, 2, 8], [1, 7, 4], [3, 6, 9]])
array = np.delete(array, 1, 0)
print(array)

# task 3
print('\n----task 3----')
conversions = np.array([50, 65, 80, 45, 70, 90, 55, 85, 60, 75], dtype='float64')
print(conversions)
print(f'''Медіана: {np.median(conversions)}
Дисперсія: {conversions.var()}
Стандартне відхилення: {conversions.std()}''')

rng = np.random.default_rng()
arr1 = rng.random(10)
arr2 = rng.uniform(1, 101, 10)
arr3 = rng.normal(0, 1, 10)
arr4 = rng.exponential(1, 10)

combined = np.concatenate([conversions, arr1, arr2, arr3, arr4])
mean_value = combined.mean()
print(f'''-------
Сума: {mean_value}
Чи більше 2000? {'так' if mean_value > 2000 else 'ні'}
''')