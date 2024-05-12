import pandas as pd
import re
import os
from openpyxl import load_workbook
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

def find_same_glyph_sets(glyph_data):
    same_glyph_sets = {}
    for unicode, glyphs in glyph_data.items():
        sorted_glyphs = tuple(sorted(glyphs))  # Сортируем графемы для их сравнения
        if sorted_glyphs in same_glyph_sets:
            # Если набор графем уже есть в словаре и уникод отсутствует в списке, добавляем его
            if unicode not in same_glyph_sets[sorted_glyphs]:
                same_glyph_sets[sorted_glyphs].append(unicode)
        else:
            # Если набор графем еще не встречался, добавляем его в словарь с единственным уникодом
            same_glyph_sets[sorted_glyphs] = [unicode]
    # Фильтруем словарь, оставляя только те наборы графем, которые имеют 2 или более уникода
    same_glyph_sets = {k: v for k, v in same_glyph_sets.items() if len(v) >= 2}
    return same_glyph_sets
# Функция для вывода данных в Excel
import pandas as pd
import os
from openpyxl import load_workbook

def output_to_excel(data_dict, filename='output.xlsx'):
    try:
        book_exists = os.path.exists(filename)
        if book_exists:
            book = load_workbook(filename)
            print(f"Файл '{filename}' найден. Добавляем/обновляем листы.")
            writer = pd.ExcelWriter(filename, engine='openpyxl', mode='a')
            writer.book = book
        else:
            print(f"Файл '{filename}' не найден. Создаем новый файл.")
            writer = pd.ExcelWriter(filename, engine='openpyxl')
            book = writer.book

        for sheet_name, data in data_dict.items():
            df = pd.DataFrame(data)
            if sheet_name in book.sheetnames:
                book.remove(book[sheet_name])
                print(f"Лист '{sheet_name}' найден. Обновляем данные.")
            else:
                print(f"Создаем лист '{sheet_name}'.")
            df.to_excel(writer, sheet_name=sheet_name, index=False)

        writer.save()
        writer.close()
        print(f"Данные успешно сохранены в файл '{filename}'.")
    except Exception as e:
        print(f"Произошла ошибка при записи в файл '{filename}': {e}")
def convert_data_in_file(filename):
    converted_data = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip().lower()
            # Check if the line contains glyphs (Chinese, Japanese, Korean, etc.)
            if re.match(r'^[\u4e00-\u9fff]+$', line):
                # Convert glyphs to Unicode without 'U+' prefix and in lowercase
                unicode_line = ' '.join([f'{ord(glyph):04x}' for glyph in line])
                converted_data.append(unicode_line)
            # Check if the line contains Unicode representations without 'U+' prefix
            elif re.match(r'^([a-f0-9]{4,5}\s?)+$', line):
                # Convert Unicode to glyphs
                unicodes = line.split()
                glyphs_line = ''.join([chr(int(unicode_code, 16)) for unicode_code in unicodes])
                converted_data.append(glyphs_line)
            else:
                # If the format is not recognized, keep the original line
                converted_data.append(line)

def glyph_combinations_analysis(glyph_data):
    glyph_combinations = {}

    # Собираем информацию о комбинациях графем
    for unicode, glyphs in glyph_data.items():
        for i, glyph in enumerate(glyphs):
            if glyph not in glyph_combinations:
                glyph_combinations[glyph] = {}
            for other_glyph in glyphs[:i] + glyphs[i+1:]:
                glyph_combinations[glyph][other_glyph] = glyph_combinations[glyph].get(other_glyph, 0) + 1

    # Подготавливаем данные для вывода в Excel
    data_for_excel = []
    for glyph, combinations in glyph_combinations.items():
        row = [glyph]
        combinations_str = ', '.join([f'{g}: {count}' for g, count in combinations.items()])
        row.append(combinations_str)
        data_for_excel.append(row)
    return data_for_excel