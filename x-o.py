from random import randint


def get_player_names():
    """
    Получает имена игроков.

    :return: Список с двумя строковыми элементами
    """
    return [input(f'Игрок №{i}, представьтесь, пожалуйста: ') for i in range(1, 3)]


def choose_1st_player(players: list):
    """
    Получает от пользователя выбор игрока, который будет ходить первым.
    Пользователь может использовать функцию "случайный выбор" для случайного распределения игроков.

    :param players:
    :return:
    """
    choice = valid_input(
        invitation=f'Кто начнёт игру? ("1" - {players[0]}, "2" - {players[1]}, "?" - случайный выбор): ',
        valid_answer=['1', '2', '?'],
        error_answer_message='Ваш ответ далёк от идеала!'
        )

    if choice == '2' or choice in ('?', None) and randint(1, 2) == 2:
        players[0], players[1] = players[1], players[0]


def get_move_position(field, player, symbol):
    """
    Получает от игрока клетку, в которую он желает поставить свой символ.

    :param field: Игровой стол в виде списка.
    :param player: Имя игрока
    :param symbol: Символ игрока
    :return str: Возвращает введённый номер поля.
    """
    return valid_input(invitation=f'Ход игрока {player}. Куда поставить "{symbol}"? ',
                       valid_answer=[str(x) for x in field if x in '123456789'],
                       error_answer_message='Необходимо указать номер СВОБОДНОЙ клетки от 1 до 9. Попробуйте ещё раз!')


def check_for_winner(field, symbols):
    """
    Проверяет статус игры, выявляя победителя.

    :param field: Игровое поле.
    :return: int
        0 - победил игрок, ходивший первым
        1 - победил игрок, ходивший вторым
        -1 - ничья
        None - игра не завершена
    """
    # Ничья. Не осталось свободных клеток на поле.
    if not set(field) & set('123456789'):
        return -1

    for side in range(len(symbols)):
        if (
                game_table[0] == game_table[1] == game_table[2] == symbols[side] or
                game_table[3] == game_table[4] == game_table[5] == symbols[side] or
                game_table[6] == game_table[7] == game_table[8] == symbols[side] or
                game_table[0] == game_table[3] == game_table[6] == symbols[side] or
                game_table[1] == game_table[4] == game_table[7] == symbols[side] or
                game_table[2] == game_table[5] == game_table[8] == symbols[side] or
                game_table[0] == game_table[4] == game_table[8] == symbols[side] or
                game_table[2] == game_table[4] == game_table[6] == symbols[side]
        ):
            # Определён победитель. Найдено совпадение трёх симолов по горизонтали, вертикали или диагонали.
            return side

    # Игра продолжается. Победитель неопределён.
    return None


def valid_input(invitation, valid_answer, error_answer_message=None, attempts=3):
    """
    Получает выбор пользователя в рамках вариантов, представленных в valid_answer.
    Если пользователь не ввёл корректные данные несколько раз (attempts), то выбрасывает исключение ValueError.
    Если список корректных вариантов отсутствует (None), то возвращает первый введённый пользователем вариант.

    :param invitation: Приглашение ввода для пользователя.
    :param valid_answer: Список возможных вариантов ввода.
    :param error_answer_message: Сообщение о некорректном вводе.
    :param attempts: Количество попыток ввода.
    :return: Возвращает введённое пользователем значение в виде строки.
    """
    for i in range(attempts):
        answer = input(invitation)
        if valid_answer is None or answer in valid_answer:
            return answer
        elif error_answer_message:
            print(error_answer_message)
    else:
        raise ValueError('Пользователь исчерпал попытки ввести корректный вариант ответа.')


def display_field(field, valid_symbols):
    """
    Выводит поле игры на экран в текстовом виде.

    :param field: Игровой стол в виде списка симовлов на игровых позициях.
    :param valid_symbols: Список игровых символов: ["X", "O"]
    :return:
    """
    print('\n'*24)
    print('+---+---+---+')
    for x in range(3):
        string = '| '
        for y in range(x * 3, x * 3 + 3):
            if field[y] == valid_symbols[0]:
                # Выделить символ жирным и красным цветом
                string += '\033[1m\033[31m' + field[y] + '\033[0m'
            elif field[y] == valid_symbols[1]:
                # Выделить символ жирным и зелёным цветом
                string += '\033[1m\033[32m' + field[y] + '\033[0m'
            else:
                string += field[y]
            string += ' | '
        print(string)
    print('+---+---+---+')


if __name__ == '__main__':
    # В игре будут использоваться символы 'X' и 'O'
    symbols = ['X', 'O']

    # Переменная для ответа на вопрос "Хотите сыграть ещё раз?"
    play_again = 'д'

    print('\n{:-^80}\n'.format(' Крестики-Нолики '))

    # Получить имена игроков.
    players = get_player_names()

    while play_again in ['д', 'Д', 'н', 'Н']:
        # Создать игровое поле ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        game_table = [str(x) for x in range(1, 10)]

        # Выбрать игрока, который будет ходить первым.
        try:
            choose_1st_player(players)
        except ValueError:
            print('Возвращайтесь, когда сможете определиться с тем, кто ходит первый!')
            exit(0)

        # Вывести на экран игровой стол
        display_field(game_table, symbols)

        print('Перед Вами доска для игры в крестики-нолики. '
              'Цифры означают позиции, в которые можно поставить свой символ.')

        # Начать с нулевого хода. Для этого перед началом установить значение хода равным -1.
        move = -1

        while True:
            # Вычислить игрока, которому принадлежит текущий ход
            move += 1
            side = move % 2

            # Получить позицию для установки символа текущего игрока.
            try:
                position = int(get_move_position(game_table, players[side], symbols[side])) - 1
            except ValueError:
                print('Я понял, Вы не хотите играть. Прощайте!')
                exit(0)

            # Разместить символ на игровом поле.
            game_table[position] = symbols[side]

            # Вывести на экран игровое поле.
            display_field(game_table, symbols)

            # Проверить статус игры на победителя или ничью.
            result = check_for_winner(game_table, symbols)

            if result in [0, 1]:    # Определён победитель
                print(f'Поздравляю! Игрок {players[result]}, управлявший "{symbols[result]}" победил!')
                break
            elif result == -1:      # Ничья
                print('Похоже, здесь ничья!')
                break

        # Узнать, хотят ли игроки сыграть снова.
        try:
            play_again = valid_input(
                invitation=f'Хотите сыграть ещё раз? ("Д" - Да, "Н" - Нет): ',
                valid_answer=['д', 'Д', 'н', 'Н'],
                error_answer_message='Я не могу решить за Вас!'
            )
        except ValueError:
            print('Не хотите, как хотите. Прощайте!')
            exit(0)


