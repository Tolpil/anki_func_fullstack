import random
import sys
import time
from typing import Dict, Tuple


STOP_WORD = 'СТОП'


def load_words(filename: str = 'words.txt') -> Dict[str, str]:
    """Загружает словарь пар «слово, перевод» из текстового файла."""
    words: Dict[str, str] = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                parts = line.strip().split(',')
                if len(parts) == 2:
                    words[parts[0].strip()] = parts[1].strip()
    except FileNotFoundError:
        print(f'Файл {filename} не найден.')
        sys.exit(1)
    return words


def print_statistics(score: int, total_time: float) -> None:
    """Выводит итоговую статистику игры."""
    print(f'Ваш итоговый счет: {score}')
    if score > 0:
        average = total_time / score
        print(f'Время игры: {total_time:.2f} секунд '
              f'(среднее время: {average:.2f} сек.)')
    else:
        print(f'Время игры: {total_time:.2f} секунд '
              f'(среднее время: —)')


def ask_and_check(word: str, correct: str) -> Tuple[bool, bool, float]:
    """Спрашивает перевод слова и проверяет ответ."""
    print(f'Ваше слово: {word}')
    start_time = time.time()
    answer = input('Ваш перевод: ')
    answer_time = time.time() - start_time
    if answer.strip().upper() == STOP_WORD:
        return True, False, 0.0
    is_correct = answer.strip().lower() == correct.strip().lower()
    return False, is_correct, answer_time


def start_game(words: Dict[str, str]) -> None:
    """Запускает игровой режим перевода случайных слов."""
    if not words:
        print('Словарь пуст. Добавьте слова для игры.')
        return
    print('Чтобы закончить, введите СТОП')
    score = 0
    total_time = 0.0
    while True:
        word = random.choice(list(words.keys()))
        correct = words[word]
        is_stop, is_correct, answer_time = ask_and_check(word, correct)
        if is_stop:
            break
        total_time += answer_time
        if is_correct:
            score += 1
            print(f'Верно! Время на ответ: {answer_time:.2f} секунд')
        else:
            print(f'Неправильно, правильный ответ: {correct} '
                  f'(Время на ответ: {answer_time:.2f} секунд)')
    print('Спасибо за игру!')
    print_statistics(score, total_time)


def train_until_mistake(words: Dict[str, str]) -> None:
    """Запускает режим «до первой ошибки»."""
    if not words:
        print('Словарь пуст. Добавьте слова для игры.')
        return
    print('Режим: Игра до первой ошибки! '
          'Чтобы выйти вручную, введите СТОП')
    score = 0
    total_time = 0.0
    word_list = list(words.keys())
    while True:
        word = random.choice(word_list)
        correct = words[word]
        is_stop, is_correct, answer_time = ask_and_check(word, correct)
        if is_stop:
            print('Выход из режима по запросу пользователя.')
            break
        total_time += answer_time
        if is_correct:
            score += 1
            print(f'Верно! Всего очков: {score} '
                  f'(ответ за {answer_time:.2f} секунд)')
        else:
            print(f'Ошибка! Неверно. Правильный ответ: {correct}')
            break
    print_statistics(score, total_time)


def add_words(words: Dict[str, str]) -> None:
    """Добавляет новые пары «слово - перевод» в словарь."""
    print('Чтобы закончить, введите СТОП')
    while True:
        word = input('Введите слово: ')
        if word.strip().upper() == STOP_WORD:
            break
        translation = input('Введите перевод: ')
        if translation.strip().upper() == STOP_WORD:
            break
        words[word.strip()] = translation.strip()


def show_all_words(words: Dict[str, str]) -> None:
    """Выводит все пары «слово - перевод» одной строкой."""
    print('; '.join(f'{word} - {translation}'
                    for word, translation in words.items()))


def save_words(words: Dict[str, str],
               filename: str = 'words.txt') -> None:
    """Сохраняет словарь пар «слово, перевод» в текстовый файл."""
    with open(filename, 'w', encoding='utf-8') as file:
        for word, translation in words.items():
            file.write(f'{word},{translation}\n')
    print(f'Было сохранено {len(words)} слов в файл {filename}')


def main() -> None:
    """Запускает основной цикл приложения-тренажёра."""
    words = load_words()
    print(f'Было загружено {len(words)} слов из файла words.txt')
    while True:
        menu = '''Меню:
        1. Начать игру
        2. Добавить слова
        3. Тренировка до первой ошибки
        4. Вывод всех слов
        5. Выход
        '''
        print(menu)
        menu_choice = input('Пункт меню: ').strip()
        if menu_choice == '1':
            start_game(words)
        elif menu_choice == '2':
            add_words(words)
        elif menu_choice == '3':
            train_until_mistake(words)
        elif menu_choice == '4':
            show_all_words(words)
        elif menu_choice == '5':
            save_words(words)
            sys.exit()
        else:
            print('Неизвестный пункт меню')


if __name__ == '__main__':
    main()
