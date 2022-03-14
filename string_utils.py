def explode_string(a_string):
    """
    Transforma una cadena en una lista de caracters
    'Han' => ['H', 'a', 'n']
    """
    return list(a_string)


def explode_list_of_strings(list_of_strings):
    """
    Aplica explode_string a cada cadena de la lista
    """
    result = []
    for each_string in list_of_strings:
        result.append(explode_string(each_string))
    return result
