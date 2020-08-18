from random import randint

global_field = [None for x in range(9)]


def display_field(field, valid_symbols=None):
    print('\n' * 100)
    print('+-+-+-+')
    for i in range(0, 3):
        print('|', end='')
        for j in range(i * 3, i * 3 + 3):
            if field[j] not in valid_symbols:
                print(str(j + 1) + '|', end='')
            else:
                print(field[j] + '|', end='')
        print()
    print('+-+-+-+')


def valid_input(invitation='', valid_answer=None, attempts=3, error_answer_message=None):
    for i in range(attempts):
        answer = input(invitation)
        if valid_answer is None or answer in valid_answer:
            return answer
        elif error_answer_message:
            print(error_answer_message)
    else:
        return None


if __name__ == '__main__':
    symbols = ['X', 'O']
    players = []
    for i in range(1, 3):
        players.append(input(f'Имя игрока №{i}: '))

    choice = valid_input(
        invitation=f'Кто начнёт игру? ("1" - {players[0]}, "2" - {players[1]}, "?" - случайный выбор): ',
        valid_answer=['1', '2', '?'],
        error_answer_message='Ваш ответ далёк от идеала!'
        )
    r = randint(1, 2)
    if choice == '2' or choice in ('?', None) and r == 2:
        players[0], players[1] = players[1], players[0]

    display_field(global_field, symbols)
    print('Перед Вами доска для игры в крестики-нолики. Цифры означают позиции, в которые можно поставить свой символ.')

    move = 0
    while True:
        side = move % 2

        position = valid_input(invitation=f'Ход игрока {players[side]}. Куда поставить "{symbols[side]}"? ',
                               valid_answer=[str(x) for x in range(10)],
                               error_answer_message='Непонимаю Ваш выбор! Необходимо указать номер клетки от 1 до 9.'
                               )
        if position is None:
            'Я понял, Вы не хотите играть. Прощайте!'
            exit(0)
        else:
            position = int(position) - 1

        # Is this position available?
        if global_field[position] in symbols:
            print('К сожалению, данное место под солнцем уже занято! Попробуйте найти себе другое.')
            continue

        # Place symbol in desired position.
        global_field[position] = symbols[side]

        # Does current player win?
        if (global_field[0] == global_field[1] == global_field[2] == symbols[side] or
                global_field[3] == global_field[4] == global_field[5] == symbols[side] or
                global_field[6] == global_field[7] == global_field[8] == symbols[side] or
                global_field[0] == global_field[3] == global_field[6] == symbols[side] or
                global_field[1] == global_field[4] == global_field[7] == symbols[side] or
                global_field[2] == global_field[5] == global_field[8] == symbols[side] or
                global_field[0] == global_field[4] == global_field[8] == symbols[side] or
                global_field[3] == global_field[5] == global_field[7] == symbols[side]):
            display_field(global_field, symbols)
            print(f'Поздравляю! Игрок {players[side]}, управлявший "{symbols[side]}" победил!')
            break

        # Is it a draw?
        for i in range(len(global_field)):
            if global_field[i] not in symbols:
                break
        else:
            display_field(global_field, symbols)
            print('Похоже, у нас тут ничья!')
            break

        display_field(global_field, symbols)
        move += 1
