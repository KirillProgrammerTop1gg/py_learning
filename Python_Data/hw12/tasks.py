import pandas as pd


# task 1
print('task 1:')
data = {
    'Product': ['Laptop', 'Smartphone', 'Tablet'],
    'Price': [1200, 800, 400],
    'Stock': [50, 150, 200]
}
df = pd.DataFrame(data)
new_row = pd.DataFrame({'Product': ['USB Hub'], 'Price': [40], 'Stock': [150], 'Warranty': ['2 years']})
df = pd.concat([df, new_row], ignore_index=True)
print(df)

# task 2
print('\ntask 2:')
data = {
    'Product': ['Laptop', 'Smartphone', 'Tablet'],
    'Price': [1200, 800, 400],
    'Stock': [50, 150, 200]
}
df = pd.DataFrame(data)
new_row = pd.DataFrame({'Product': ['USB Hub'], 'Price': ['Forty'], 'Stock': [150]})
# Pandas допускає різні типи даних в одному стопвці і значення "Forty" буде добавлено як строка тип Price як Object
df = pd.concat([df, new_row], ignore_index=True)
print(df)

# task 3
print('\ntask 3:')
df = pd.read_csv('customer_feedback.csv')
print(df)
overall_mean = df['Rating'].mean()
grouped = df.groupby(['Region', 'Month'])
average_rating = grouped['Rating'].mean()
df = average_rating.unstack()
df = df.fillna(overall_mean)
print(df)