**GraphAnalyst**
Описание проекта
GraphAnalyst - это веб-приложение, разработанное на языке Python с использованием фреймворка Flask. Приложение предназначено для анализа и оптимизации базы данных китайских иероглифов и их графем. Основная цель программы - сократить количество графем для упрощения их использования в различных приложениях, сохраняя при этом информативность данных.
Функциональные возможности
Аналитика
Счётчик графем: Подсчитывает количество каждой графемы во всех иероглифах.
Поиск повторяющихся графем: Находит графемы, которые повторяются внутри одного иероглифа.
Поиск всех повторяющихся паттернов графем: Ищет пары графем, которые часто используются вместе.
Подсчёт графем в иероглифах: Подсчитывает, сколько иероглифов содержит конкретное количество графем.
Поиск одинаковых наборов графем: Находит иероглифы, которые состоят из одинаковых наборов графем.
Анализ комбинаций графем: Анализирует, какие графемы часто используются вместе с другими.
Конвертация
Конвертация данных: Преобразует юникоды иероглифов в иероглифы и наоборот.
Технологический стек
Python
Flask
HTML
JavaScript
pandas
openpyxl
PyInstaller
Для запуска приложения можете скачать репозиторий полностью и запустить файл app.py или воспользоваться уже собранным файлом который находится в \dist\GraphAnalyst
Использование
Аналитика
Перейдите в раздел "Аналитика".
Загрузите файл с данными (формат .txt).
Выберите тип анализа.
Нажмите кнопку "Анализировать".
Скачайте результаты анализа.
Конвертация
Перейдите в раздел "Конвертация".
Загрузите файл с данными (формат .txt).
Нажмите кнопку "Конвертировать".
Скачайте сконвертированный файл.
Примеры файлов
Пример файла для анализа
4E01: 124,002
4E02: 231,003,125
4E03: 004,126,358,232
4E04: 005,237,361,129,467
4E05: 006,238,362,130,472,578
4E06: 007,239,363,131,473,579,689
Пример файла для конвертации
4e02
4e10
4e17
или
丂
丐
丗
Контакты
Если у вас есть вопросы или предложения, пожалуйста, свяжитесь со мной через GitHub или телеграм .
Если вас интересует использование этой технологии где-то ещё свяжитесь с https://vk.com/moiseenko_v_n
