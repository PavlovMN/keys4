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


def solve_dragon_problem():
    """
    Основная функция для решения задачи о драконьей стае.
    """
    print("Программа для вычисления максимальной силы драконьей стаи")
    print("=" * 55)
    
    while True:
        try:
            N = int(input("Введите количество голов в стае (0 < N < 100) или 0 для выхода: "))
            
            if N == 0:
                print("Программа завершена.")
                break
            
            if N <= 0 or N >= 100:
                print("Ошибка: N должно быть натуральным числом в диапазоне (0, 100)")
                continue
            
            max_power = max_dragon_power(N)
            print(f"Максимальная сила стаи из {N} голов: {max_power}")
            
            # Показываем разбиение для понимания
            print(f"Оптимальное разбиение: ", end="")
            show_optimal_breakdown(N)
            print()
            
        except ValueError:
            print("Ошибка: введите корректное число")
        except KeyboardInterrupt:
            print("\nПрограмма завершена.")
            break


def show_optimal_breakdown(N):
    """
    Показывает оптимальное разбиение N голов на драконов.
    """
    if N <= 7:
        print(f"{N}")
        return
    
    # Находим оптимальное разбиение с помощью динамического программирования
    breakdown = find_optimal_breakdown(N, 7)
    print(" × ".join(map(str, breakdown)))


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


def find_best_breakdown(n, max_size):
    """
    Находит лучшее разбиение числа n на слагаемые от 1 до max_size.
    """
    if n <= max_size:
        return [n]
    
    # Простой подход: пробуем разные комбинации
    best_product = 0
    best_breakdown = []
    
    # Используем жадный алгоритм с учетом математических принципов
    breakdown = []
    remaining = n
    
    # Предпочитаем числа 3, но корректируем при необходимости
    while remaining > 0:
        if remaining <= max_size:
            breakdown.append(remaining)
            break
        
        if remaining >= 6:
            # Для чисел >= 6 предпочитаем 3
            breakdown.append(3)
            remaining -= 3
        elif remaining >= 4:
            # Для чисел 4-5 используем их целиком
            breakdown.append(remaining)
            break
        else:
            # Для малых чисел используем как есть
            breakdown.append(remaining)
            break
    
    # Проверяем, можно ли улучшить результат
    # Особенно важно проверить случаи, когда лучше использовать 4 вместо 2+2
    improved_breakdown = improve_breakdown(breakdown)
    
    return improved_breakdown


def improve_breakdown(breakdown):
    """
    Улучшает разбиение, заменяя пары 2+2 на 4, пары 3+1 на 2+2 и т.д.
    """
    improved = breakdown.copy()
    
    # Заменяем 2+2 на 4 (2*2 = 4, но 4 лучше для дальнейших операций)
    while improved.count(2) >= 2:
        improved.remove(2)
        improved.remove(2)
        improved.append(4)
    
    # Заменяем 3+1 на 2+2 (3*1=3 < 2*2=4)
    while 3 in improved and 1 in improved:
        improved.remove(3)
        improved.remove(1)
        improved.append(2)
        improved.append(2)
    
    # Сортируем для лучшего представления
    improved.sort(reverse=True)
    
    return improved


# Функция для тестирования
def test_solution():
    """
    Тестирует решение на различных примерах.
    """
    test_cases = [
        (1, 1),      # Один дракон с 1 головой
        (3, 3),      # Один дракон с 3 головами  
        (4, 4),      # Два дракона по 2 головы (2*2=4)
        (6, 9),      # Два дракона по 3 головы (3*3=9)
        (7, 12),     # Три дракона: 2, 2, 3 головы (2*2*3=12)
        (8, 18),     # Три дракона: 2, 3, 3 головы (2*3*3=18)
        (9, 27),     # Три дракона по 3 головы (3*3*3=27)
        (10, 36),    # Четыре дракона: 2, 2, 3, 3 головы (2*2*3*3=36)
        (12, 81),    # Четыре дракона по 3 головы (3^4=81)
        (13, 108),   # Пять драконов: 2, 2, 3, 3, 3 головы (2*2*3*3*3=108)
    ]
    
    print("Тестирование решения:")
    print("-" * 40)
    
    for N, expected in test_cases:
        result = max_dragon_power(N)
        status = "✓" if result == expected else "✗"
        print(f"N={N:2d}: получено={result:3d}, ожидалось={expected:3d} {status}")


if __name__ == "__main__":
    # Запускаем тесты
    test_solution()
    print()
    
    # Запускаем интерактивную программу
    solve_dragon_problem()
