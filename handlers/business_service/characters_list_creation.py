def create_characters_list_text(characters_list):
    lines = (f'{character["name"]} - {character["height"]} см: {character["url"]}' for character in characters_list)
    return '\n'.join(lines)
