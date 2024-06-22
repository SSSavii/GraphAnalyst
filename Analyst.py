import pandas as pd
import re
import os

from openpyxl.workbook import Workbook


# Считываем данные из файла и сохраняем в словарь
def read_data_from_file(filename):
    """
       Считывает данные из текстового файла и сохраняет их в словарь.

       :param filename: Имя файла для чтения данных
       :return: Словарь, где ключ - Unicode символ, а значение - список графем
       """
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
    """
        Подсчитывает количество каждой графемы в данных.

        :param glyph_data: Словарь с данными о графемах
        :return: Отсортированный список словарей с информацией о графемах и их количестве
        """
    glyph_count = {}
    for glyphs in glyph_data.values():
        for glyph in glyphs:
            glyph_count[glyph] = glyph_count.get(glyph, 0) + 1
    result_list = [{"Графемы": k, "Кол-во": v} for k, v in glyph_count.items()]
    return sorted(result_list, key=lambda x: x["Графемы"])


# Функция для поиска символов с повторяющимися графемами
def find_repeated_glyphs(glyph_data):
    """
        Находит символы с повторяющимися графемами.

        :param glyph_data: Словарь с данными о графемах
        :return: Отсортированный список словарей с информацией о повторяющихся графемах и их количестве
        """
    repeated_glyphs = []
    for unicode, glyphs in glyph_data.items():
        for glyph in set(glyphs):
            count = glyphs.count(glyph)
            if count > 1:
                repeated_glyphs.append({"Графема": glyph, "Unicode": unicode, "Кол-во": count})
    return sorted(repeated_glyphs, key=lambda x: x["Графема"])


# Функция для поиска всех повторяющихся паттернов графем
def find_all_repeated_patterns(glyph_data):
    """
        Находит все повторяющиеся пары графем в символах.

        :param glyph_data: Словарь с данными о графемах
        :return: Список словарей с информацией о парах графем и символах, где они встречаются
        """
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
    repeated_patterns = [{"Пара": pair, "Unicodes": list(unicodes)} for pair, unicodes in glyph_pairs.items() if
                         len(unicodes) > 1]
    return sorted(repeated_patterns, key=lambda x: x["Пара"])


# Подсчёт количества графем в каждом символе
def count_glyphs_in_uni(glyph_data):
    """
        Подсчитывает количество графем в каждом символе.

        :param glyph_data: Словарь с данными о графемах
        :return: Отсортированный список словарей с информацией о количестве графем в символах и количестве символов
        """
    count_dict = {}
    for glyphs in glyph_data.values():
        glyph_count = len(glyphs)
        count_dict[glyph_count] = count_dict.get(glyph_count, 0) + 1
    result_list = [{"Кол-во графем": k, "Кол-во иероглифов": v} for k, v in count_dict.items()]
    return sorted(result_list, key=lambda x: x["Кол-во графем"])


# Функция для поиска одинаковых наборов графем
def find_same_glyph_sets(glyph_data):
    """
        Находит символы с одинаковыми наборами графем.

        :param glyph_data: Словарь с данными о графемах
        :return: Отсортированный список словарей с информацией о наборах
        графем и символах, где они встречаются
        """
    same_glyph_sets = {}
    for unicode, glyphs in glyph_data.items():
        sorted_glyphs = tuple(sorted(glyphs))
        if sorted_glyphs in same_glyph_sets:
            same_glyph_sets[sorted_glyphs].append(unicode)
        else:
            same_glyph_sets[sorted_glyphs] = [unicode]
    result_list = [{"Набор графем": glyphs, "Unicodes": unicodes} for glyphs, unicodes in same_glyph_sets.items() if
                   len(unicodes) >= 2]
    return sorted(result_list, key=lambda x: x["Набор графем"])


# Новые названия листов
analysisFunctionNames = {
    'count_glyphs': 'Кол-во графем',
    'find_repeated_glyphs': 'Повторяющиеся графемы',
    'find_all_repeated_patterns': 'Часто используемые пары графем',
    'count_glyphs_in_uni': 'Длины иероглифов',
    'find_same_glyph_sets': 'Одинаковые наборы графем',
    'glyph_combinations_analysis': 'Анализ комбинаций графем'
}


# Функция для вывода в Excel с новыми названиями
def output_to_excel(data_dict, filename='output.xlsx', sort=True):
    """
    Сохраняет результаты анализа в Excel файл.

    :param data_dict: Словарь, где ключ - имя функции анализа, значение - результат анализа.
    :param filename: Имя Excel файла для сохранения результатов.
    :param sort: Флаг сортировки данных по первому столбцу.
    """
    try:
        # Проверяем, существует ли файл
        if os.path.exists(filename):
            # Открываем существующий файл
            mode = 'a'
            book = pd.ExcelWriter(filename, engine='openpyxl', mode=mode)
        else:
            # Создаём новый файл без автоматического листа "Sheet"
            mode = 'w'
            book = pd.ExcelWriter(filename, engine='openpyxl', mode=mode)
            book.book = Workbook()
            book.book.remove(book.book.active)

        with book as writer:
            for func_name, data in data_dict.items():
                # Получаем или задаём имя листа
                sheet_name = analysisFunctionNames.get(func_name, func_name)

                if not isinstance(data, pd.DataFrame):
                    data = pd.DataFrame(data)

                if sort and not data.empty:
                    # Сортировка по первому столбцу
                    data = data.sort_values(by=data.columns[0])

                # Записываем данные в лист
                data.to_excel(writer, sheet_name=sheet_name, index=False)
                if 'Sheet' in writer.book.sheetnames:
                    writer.book.remove(writer.book['Sheet'])

        # Очищаем data_dict после успешного сохранения данных
        data_dict.clear()

        print(f"Data successfully saved to '{filename}'.")
    except Exception as e:
        print(f"An error occurred while writing to the file '{filename}': {e}")


# Функция для конвертации данных в файле
def convert_data_in_file(filename, download_folder='downloads'):
    """
        Конвертирует данные в файле между текстовым представлением графем и их Unicode кодами.

        :param filename: Имя файла для конвертации
        :param download_folder: Директория, в которой будет сохранён результат
        """
    converted_data = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip().lower()
            # Проверяем, содержит ли строка графемы (китайские, японские, корейские и т.д.)
            if re.match(r'^[\u4e00-\u9fff]+$', line):
                # Преобразуем графемы в Unicode без префикса 'U+' и в нижнем регистре
                unicode_line = ' '.join([f'{ord(glyph):04x}' for glyph in line])
                converted_data.append(unicode_line)
            # Проверяем, содержит ли строка представления Unicode без префикса 'U+'
            elif re.match(r'^([a-f0-9]{4,5}\s?)+$', line):
                # Преобразуем Unicode обратно в графемы
                unicodes = line.split()
                glyphs_line = ''.join([chr(int(unicode_code, 16)) for unicode_code in unicodes])
                converted_data.append(glyphs_line)
            else:
                # Если формат не распознан, оставляем оригинальную строку
                converted_data.append(line)

    # Сохраняем файл в папке downloads с тем же именем, что и исходный файл
    output_path = os.path.join(download_folder, os.path.basename(filename))
    with open(output_path, 'w', encoding='utf-8') as output_file:
        for line in converted_data:
            output_file.write(line + '\n')

    print(f"Data successfully converted and saved to '{output_path}'.")


# Функция для анализа комбинаций графем
def glyph_combinations_analysis(glyph_data):
    """
       Анализирует комбинации графем внутри каждого символа.

       :param glyph_data: Словарь с данными о графемах
       :return: Отсортированный список словарей с информацией о графемах и их комбинациях
       """
    glyph_combinations = {}

    # Собираем информацию о комбинациях графем
    for unicode, glyphs in glyph_data.items():
        for i, glyph in enumerate(glyphs):
            if glyph not in glyph_combinations:
                glyph_combinations[glyph] = {}
            for other_glyph in glyphs[:i] + glyphs[i + 1:]:
                glyph_combinations[glyph][other_glyph] = glyph_combinations[glyph].get(other_glyph, 0) + 1

    # Подготавливаем данные для вывода в Excel
    data_for_excel = []
    for glyph, combinations in glyph_combinations.items():
        sorted_combinations = sorted(combinations.items(), key=lambda x: x[0])
        combinations_str = ', '.join([f'{g}: {count}' for g, count in sorted_combinations])
        data_for_excel.append({"Графема": glyph, "Комбинации": combinations_str})
    return sorted(data_for_excel, key=lambda x: x["Графема"])


# Функция для запуска анализа с использованием конкретной функции анализа
def run_analysis(analysis_function):
    """
        Запускает анализ данных с использованием конкретной функции анализа.

        :param analysis_function: Функция анализа, которая будет применена к данным
        """
    data_filename = "Data(моя).txt"
    excel_filename = 'output.xlsx'
    glyph_data = read_data_from_file(data_filename)
    result = analysis_function(glyph_data)
    output_to_excel({analysis_function.__name__: result}, excel_filename)
