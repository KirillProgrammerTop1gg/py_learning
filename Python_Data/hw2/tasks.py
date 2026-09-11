# Task 1
a = input('Input length of rectangle side a: ')
b = input('Input length of rectangle side b: ')

try:
    a, b = float(a), float(b)
    if a <= 0 or b <= 0:
        print('Values can not be less or equal than zero')
        exit()
    print(f'The area of a rectangle with sides {a} and {b} is {a*b}')
except ValueError:
    print('Values are not numbers')
    
# Task 3
year = int(input('Input the year: '))

if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
    print('This is a leap year')
else:
    print("This isn't a leap year")

# Task 4
number = int(input('Input a number for the multiplication table: '))
for i in range(1,11):
    print(f'{i} * {number} = {i*number}')
    
# Task 5
number = 1
total = 0

while number <= 50:
    # total += number if number % 2 else 0
    if number % 2 == 0:
        number += 1
        continue
    
    total += number
    number += 1

print(f"Сума непарних чисел від 1 до 50: {total}")

# Task 6
def create_full_name(first_name, last_name="Іванов"):
    return f'{last_name} {first_name}'


full_name1 = create_full_name(first_name="Петро", last_name="Петренко")
print(f"Повне ім'я: {full_name1}")
full_name2 = create_full_name(first_name="Олена")
print(f"Повне ім'я: {full_name2}")

assert full_name1 == "Петренко Петро", "Функція повинна повертати 'Петренко Петро'"
assert full_name2 == "Іванов Олена", "Функція повинна використовувати 'Іванов' як прізвище за замовчуванням"