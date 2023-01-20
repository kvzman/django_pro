from django import template


register = template.Library()

no_good_words = [
    'ведро',
    'добряк',
    'отважный',
    'попугай',
]


@register.filter()
def censor(value):
    if not isinstance(value, str):
        raise TypeError("должно быть строковое значение")

    for n_word in no_good_words:
        for word in value.split():
            if word.lower().count(n_word) and len(word) > len(n_word):
                value = value.replace(word, f"{word[0]}{'*'*(len(n_word)-1)}{word[-1]}")
            elif word.lower().count(n_word):
                value = value.replace(word, f"{word[0]}{'*' * (len(n_word) - 1)}")
    return value
