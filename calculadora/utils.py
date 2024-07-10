import re

NUM_OR_DOT_REGEX= re.compile(r'^[0-9.]$')

def isnumordot(string:str):
    return bool (NUM_OR_DOT_REGEX.search(string))


def isempty(string:str):
    return string==''

def isInteger(string:str):
    number=float(string)
    if number.is_integer():
        number=int(number)
    return number

def isValidNumber(string:str):

    try:
        float(string)
        return True
    except ValueError:
      return False

def isNumber(value,value2) -> bool:
    if isinstance(value,value2, int):  # Verifica se o valor recebido é do tipo int
        return True  # Se for, considera como um número inteiro válido
    else:
        return False  # Caso contrário, considera como inválido





