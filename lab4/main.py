from sequential_runner import run_sequential
from threading_runner import run_threading
from multiprocessing_runner import run_multiprocessing


def main():
    print("\n Выберите режим выполнения:")
    print("1 — Последовательное")
    print("2 — Многопоточное")
    print("3 — Многопроцессорное")

    for i in range(3):
        choice = input("\n Введите номер (1/2/3) или напишите None чтобы закончить: ").strip()

        if choice == "1":
            run_sequential()
        elif choice == "2":
            run_threading()
        elif choice == "3":
            run_multiprocessing()
        elif choice == "None":
            return
        else:
            print("\nНекорректный выбор.")
            return


if __name__ == "__main__":
    main()