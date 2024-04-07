import pandas as pd

# Считываем данные из файла и сохраняем в словарь
def read_data_from_file(filename):
    glyph_data = {}
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split(': ')
            unicode = parts[0]
            glyphs = parts[1].split(',')
            glyph_data[unicode] = glyphs
    return glyph_data

# Функция для подсчёта графем
def count_glyphs(glyph_data):
    glyph_count = {}
    for glyphs in glyph_data.values():
        for glyph in glyphs:
            glyph_count[glyph] = glyph_count.get(glyph, 0) + 1
    sorted_glyph_count = {k: glyph_count[k] for k in sorted(glyph_count, key=lambda x: int(x))}
    return sorted_glyph_count

# Функция для поиска символов с повторяющимися графемами
def find_repeated_glyphs(glyph_data):
    repeated_glyphs = {}
    for unicode, glyphs in glyph_data.items():
        for glyph in set(glyphs):
            count = glyphs.count(glyph)
            if count > 1:
                repeated_glyphs[glyph] = (unicode, count)
    return repeated_glyphs

# Функция для поиска всех повторяющихся паттернов графем
def find_all_repeated_patterns(glyph_data):
    glyph_pairs = {}
    for unicode, glyphs in glyph_data.items():
        seen_pairs = set()
        for i in range(len(glyphs)):
            for j in range(i + 1, len(glyphs)):
                glyph_pair = tuple(sorted((glyphs[i], glyphs[j])))
                if glyph_pair not in seen_pairs:
                    seen_pairs.add(glyph_pair)
                    if glyph_pair in glyph_pairs:
                        glyph_pairs[glyph_pair].add(unicode)
                    else:
                        glyph_pairs[glyph_pair] = {unicode}
    repeated_patterns = {pair: unicodes for pair, unicodes in glyph_pairs.items() if len(unicodes) > 1}
    return repeated_patterns

def count_glyphs_in_uni(glyph_data):
    count_dict = {}
    for glyphs in glyph_data.values():
        glyph_count = len(glyphs)
        count_dict[glyph_count] = count_dict.get(glyph_count, 0) + 1
    return count_dict

# Функция для вывода данных в Excel
def output_to_excel(data_dict, filename='output.xlsx'):
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        for sheet_name, data in data_dict.items():
            df = pd.DataFrame(list(data.items()), columns=['Key', 'Value'])
            df.to_excel(writer, sheet_name=sheet_name, index=False)

# Использование функции чтения данных из файла
glyph_data = read_data_from_file('data.txt')

# Использование функций анализа данных
glyph_count = count_glyphs(glyph_data)
repeated_glyphs = find_repeated_glyphs(glyph_data)
all_repeated_patterns = find_all_repeated_patterns(glyph_data)
glyphs_in_uni_count = count_glyphs_in_uni(glyph_data)

# Создание словаря с данными для вывода в Excel
data_to_output = {
    'Счётчик графем': glyph_count,
    'Повторяющиеся графемы': repeated_glyphs,
    'Все повторяющиеся паттерны': all_repeated_patterns,
    'Количество иероглифов по количеству графем': glyphs_in_uni_count
}

# Использование функции вывода данных в Excel
output_to_excel(data_to_output)