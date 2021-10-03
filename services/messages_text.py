from typing import ValuesView


def create_start_poll_text():
    """Returns message for 'start' command."""

    return ('Теперь можете приступить к прохождению опроса. Вам предстоит выполнить ряд '
            'попарных сравнений между персонажами на предмет оценки их относительной силы. '
            'Подразумевается, что сравнивается не только физическая сила в самом непосредственном '
            'смысле, а берется во внимание и ряд других качеств, например, степень влияния '
            'персонажа на сюжет.')


def create_characters_list_text(characters_list: ValuesView) -> str:
    """Returns string representation of sequence of characters dictionaries."""

    lines = (f'{character["name"]} - {character["height"]} см: {character["url"]}' for character in characters_list)
    return '\n'.join(lines)


def create_stop_poll_text() -> str:
    """Returns message for stopping a poll."""

    return 'Вы прервали прохождение опроса.'
