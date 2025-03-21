import random

def flip_coin():
    return random.choice(['Орел', 'Решка'])

def play_round():
    results = []
    attempts = 0
    
    while True:
        result = flip_coin()
        results.append(result)
        attempts += 1
        
        
        if len(results) >= 3:
            if results[-1] == results[-2] == results[-3]:
                break
    
    return results, attempts

def main():
    total_attempts = 0
    all_results = []
    
    # Проводим 10 раундов
    for round_num in range(1, 11):
        results, attempts = play_round()
        total_attempts += attempts
        all_results.append((results, attempts))
        
        print(f"Раунд {round_num}:")
        print(f"  Результаты: {', '.join(results)}")
        print(f"  Количество попыток: {attempts}")
        print()
    

    average_attempts = total_attempts / 10
    print(f"Среднее количество попыток за раунд: {average_attempts:.2f}")

if __name__ == "__main__":
    main()