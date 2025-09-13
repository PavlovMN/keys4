def max_dragon_power(N):
    """
    Вычисляет максимальную силу драконьей стаи из N голов.
    
    Сила стаи = произведение количества голов каждого дракона.
    Максимум голов у одного дракона = 7.
    
    Args:
        N (int): Количество голов в стае (0 < N < 100)
    
    Returns:
        int: Максимальная сила стаи
    """
    
    # Используем математически оптимальную стратегию
    # Предпочитаем числа 3, но учитываем ограничение максимум 7 голов на дракона
    
    # Начинаем с базового распределения тройками
    threes = N // 3
    remainder = N % 3
    
    # Корректируем распределение в зависимости от остатка
    if remainder == 0:
        # N делится на 3 нацело - используем только тройки
        result = 3 ** threes
    elif remainder == 1:
        # N = 3k + 1, заменяем одну тройку на две двойки (3+1=2+2)
        # потому что 2*2=4 > 3*1=3
        if threes > 0:
            result = (3 ** (threes - 1)) * 2 * 2
        else:
            result = 1
    else:  # remainder == 2
        # N = 3k + 2, добавляем одну двойку
        result = (3 ** threes) * 2
    
    # Теперь проверяем, можно ли улучшить результат, используя числа больше 3
    # но не больше 7, учитывая ограничение
    
    # Для небольших чисел (до 21) можем использовать полный перебор
    if N <= 21:
        # Пробуем все возможные комбинации
        def generate_combinations(n, max_size, current_combination, start):
            if n == 0:
                # Вычисляем произведение текущей комбинации
                product = 1
                for num in current_combination:
                    product *= num
                return product
            
            best_product = 0
            for i in range(start, min(n + 1, max_size + 1)):
                new_combination = current_combination + [i]
                product = generate_combinations(n - i, max_size, new_combination, i)
                best_product = max(best_product, product)
            
            return best_product
        
        max_power = generate_combinations(N, 7, [], 1)
        return max_power
    
    # Для больших чисел используем оптимизированный подход
    # Проверяем, можно ли заменить некоторые тройки на более эффективные числа
    
    # Пробуем заменить одну тройку на 2+1 (если это дает лучший результат)
    # Но 3 > 2*1, поэтому это не улучшит результат
    
    # Пробуем заменить одну тройку на 4 (если это возможно)
    # Но 4 < 3*1.33..., поэтому это тоже не улучшит результат
    
    # Основная стратегия: использовать как можно больше троек
    # с минимальными корректировками для остатка
    
    return result


def find_optimal_breakdown(n, max_size):
    """
    Находит оптимальное разбиение числа n на слагаемые от 1 до max_size.
    """
    
    # Используем полный перебор для небольших чисел
    if n <= 21:
        def generate_combinations(n, max_size, current_combination, start):
            if n == 0:
                return current_combination
            
            best_combination = None
            best_product = 0
            
            for i in range(start, min(n + 1, max_size + 1)):
                new_combination = current_combination + [i]
                combination = generate_combinations(n - i, max_size, new_combination, i)
                if combination:
                    product = 1
                    for num in combination:
                        product *= num
                    if product > best_product:
                        best_product = product
                        best_combination = combination
            
            return best_combination
        
        result = generate_combinations(n, max_size, [], 1)
        return result if result else [n]
    
    # Для больших чисел используем математически оптимальную стратегию
    threes = n // 3
    remainder = n % 3
    
    breakdown = []
    
    if remainder == 0:
        breakdown = [3] * threes
    elif remainder == 1:
        if threes > 0:
            breakdown = [3] * (threes - 1) + [2, 2]
        else:
            breakdown = [1]
    else:  # remainder == 2
        breakdown = [3] * threes + [2]
    
    return breakdown


def main():
    """
    Основная функция программы.
    """
    print("Программа для вычисления максимальной силы драконьей стаи")
    print("=" * 55)
    print("Введите количество голов в стае (0 < N < 100)")
    
    try:
        N = int(input("N = "))
        
        if N <= 0 or N >= 100:
            print("Ошибка: N должно быть натуральным числом в диапазоне (0, 100)")
            return
        
        max_power = max_dragon_power(N)
        breakdown = find_optimal_breakdown(N, 7)
        
        print(f"\nМаксимальная сила стаи из {N} голов: {max_power}")
        print(f"Оптимальное разбиение: {' × '.join(map(str, breakdown))}")
        
        # Проверяем правильность
        product = 1
        for num in breakdown:
            product *= num
        
        print(f"Проверка: {' × '.join(map(str, breakdown))} = {product}")
        
    except ValueError:
        print("Ошибка: введите корректное число")
    except KeyboardInterrupt:
        print("\nПрограмма завершена.")


if __name__ == "__main__":
    main()
