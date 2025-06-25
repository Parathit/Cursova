# io_utils.py

import json
import os
import random
from task import Task

current_task = None

def input_manual():
    n = int(input("Кількість замовлень: "))
    m = int(input("Кількість кур'єрів: "))
    W = int(input("Максимальна вага для кур'єра: "))
    orders = []
    for i in range(n):
        print(f"Замовлення {i + 1}:")
        weight = int(input("  Вага: "))
        cost = int(input("  Вартість: "))
        orders.append({'id': i, 'weight': weight, 'cost': cost})
    return Task(orders, m, W)

def input_random_custom():
    n = int(input("Кількість замовлень: "))
    m = int(input("Кількість кур'єрів: "))
    W = int(input("Максимальна вага для кур'єра: "))
    orders = []
    for i in range(n):
        orders.append({
            'id': i,
            'weight': random.randint(1, W // 2),
            'cost': random.randint(100, 500)
        })
    return Task(orders, m, W)

def input_random(n, m, W):
    orders = []
    for i in range(n):
        orders.append({
            'id': i,
            'weight': random.randint(1, 10),
            'cost': random.randint(100, 500)
        })
    return Task(orders, m, W)

def edit_task(current_task):
    if current_task:
        print("\nПоточна задача:")
        print(json.dumps(current_task.to_dict(), indent=2, ensure_ascii=False))
        try:
            new_couriers = input("Нова кількість кур’єрів (залишити порожнім, щоб не змінювати): ")
            new_weight = input("Нове обмеження по вазі (залишити порожнім, щоб не змінювати): ")
            if new_couriers.strip():
                current_task.num_couriers = int(new_couriers)
            if new_weight.strip():
                current_task.max_weight = int(new_weight)
            print("✅ Параметри задачі оновлено.")
        except ValueError:
            print("❗ Неправильне значення. Зміни не збережено.")
    else:
        print("❗ Поточна задача відсутня.")

def save_task(current_task):
    if current_task:
        filename = input("Введіть назву файлу: ")
        with open(filename + ".json", 'w', encoding='utf-8') as f:
            json.dump(current_task.to_dict(), f, indent=2, ensure_ascii=False)
        print("✅ Збережено.")
    else:
        print("❗ Поточна задача відсутня.")

def load_task():
    filename = input("Введіть назву файлу: ")
    if not os.path.exists(filename + ".json"):
        print("❗ Файл не знайдено.")
        return None
    with open(filename + ".json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    print("✅ Завантажено.")
    return Task.from_dict(data)

def show_task(current_task):
    if current_task:
        print(json.dumps(current_task.to_dict(), indent=2, ensure_ascii=False))
    else:
        print("❗ Поточна задача відсутня.")
