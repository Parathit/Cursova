# main.py

from io_utils import current_task, input_manual, input_random, edit_task, save_task, load_task, show_task, \
    input_random_custom
from algorithms import solve_task
from experiments import experiment_t_max, experiment_size
2
def individual_task_menu():
    global current_task
    while True:
        print("\n-- ІЗ --")
        print("1. Введення вручну")
        print("2. Випадкова генерація")
        print("3. Редагування")
        print("4. Зберегти ІЗ")
        print("5. Завантажити ІЗ")
        print("6. Показати")
        print("7. Розв'язати")
        print("8. Назад")
        choice = input("Вибір: ")
        if choice == '1':
            current_task = input_manual()
        elif choice == '2':
            current_task = input_random_custom()
        elif choice == '3':
            edit_task(current_task)
        elif choice == '4':
            save_task(current_task)
        elif choice == '5':
            loaded = load_task()
            if loaded:
                current_task = loaded
        elif choice == '6':
            show_task(current_task)
        elif choice == '7':
            if current_task:
                solve_task(current_task)
            else:
                print("❗ Поточна задача відсутня.")
        elif choice == '8':
            break
        else:
            print("❗ Невірний вибір. Спробуйте ще раз.")

def experiment_menu():
    while True:
        print("\n-- Виберіть експеримент --")
        print("1. Параметр завершення роботи локально-жадібного алгоритму")
        print("2. Вплив розмірності")
        print("3. Назад")
        choice = input("Вибір: ")
        if choice == '1':
            experiment_t_max()
        elif choice == '2':
            experiment_size()
        elif choice == '3':
            break
        else:
            print("❗ Невірний вибір. Спробуйте ще раз.")

def main_menu():
    while True:
        print("\n=== Розподіл між кур'єрами ===")
        print("1. Індивідуальна задача")
        print("2. Експериментальне дослідження розроблених алгоритмів")
        print("3. Вихід")
        choice = input("Вибір: ")
        if choice == '1':
            individual_task_menu()
        elif choice == '2':
            experiment_menu()
        elif choice == '3':
            print("✅ Завершення програми.")
            break
        else:
            print("❗ Невірний вибір. Спробуйте ще раз.")

if __name__ == '__main__':
    main_menu()
