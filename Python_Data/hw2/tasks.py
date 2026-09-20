# Task 1
a = input("Введіть сторону a: ")
b = input("Введість сторону b: ")

try:
    a, b = float(a), float(b)
    if a <= 0 or b <= 0:
        print("Дані повинні бути більше 0")
        exit()
    print(f"Площа прямокутника зі сторонами {a} та {b} дорівнює {a*b}.")
except ValueError:
    print("Дані не є числом")

# Task 3
year = int(input("Введіть рік: "))

if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
    print(f"{year} є високосним.")
else:
    print(f"{year} не є високосним.")

# Task 4
number = int(input("Введіть число для таблиці множення: "))
for i in range(1, 11):
    print(f"{i} * {number} = {i*number}")

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
    return f"{last_name} {first_name}"


full_name1 = create_full_name(first_name="Петро", last_name="Петренко")
print(f"Повне ім'я: {full_name1}")
full_name2 = create_full_name(first_name="Олена")
print(f"Повне ім'я: {full_name2}")

assert full_name1 == "Петренко Петро", "Функція повинна повертати 'Петренко Петро'"
assert (
    full_name2 == "Іванов Олена"
), "Функція повинна використовувати 'Іванов' як прізвище за замовчуванням"
