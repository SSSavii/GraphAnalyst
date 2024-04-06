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
    # Сортировка и вывод с сохранением ведущих нулей
    sorted_glyph_count = {k: glyph_count[k] for k in sorted(glyph_count, key=lambda x: int(x))}
    return sorted_glyph_count

# Функция для поиска символов с повторяющимися графемами
def find_repeated_glyphs(glyph_data):
    repeated_glyphs = {}
    for unicode, glyphs in glyph_data.items():
        for glyph in set(glyphs):
            count = glyphs.count(glyph)
            if count > 1:
                if glyph not in repeated_glyphs:
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

# Использование функции чтения данных из файла
glyph_data = read_data_from_file('data.txt')

# Использование функций анализа данных
glyph_count = count_glyphs(glyph_data)
repeated_glyphs = find_repeated_glyphs(glyph_data)
all_repeated_patterns = find_all_repeated_patterns(glyph_data)

# Вывод результатов
print("Счётчик графем:", glyph_count)
print("Повторяющиеся графемы:", repeated_glyphs)
print("Все повторяющиеся паттерны:", all_repeated_patterns)
