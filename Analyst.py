def count_sets_per_line(filename, num_sets):
    count = 0
    with open(filename, 'r') as file:
        for line in file:
            if line.strip():
                sets = line.split(': ')[1].split(',')
                if len(sets) == num_sets:
                    count += 1
    return count

def count_occurrences(filename, triplet):
    occurrences = 0
    with open(filename, 'r') as file:
        for line in file:
            if line.strip():
                sets = line.split(': ')[1].split(',')
                occurrences += sets.count(triplet)
    return occurrences

def get_sets_by_unicode(filename, unicode_char):
    with open(filename, 'r') as file:
        for line in file:
            if line.strip():
                unicode, sets_str = line.split(': ')
                if unicode == unicode_char:
                    return sets_str.strip().split(',')
    return []

# Пример использования:
filename = 'Data.txt'
print(count_sets_per_line(filename, 3))  # Замените 3 на нужное число наборов
print(count_occurrences(filename, '001'))  # Замените '001' на нужный трёхсимвольный набор
print(get_sets_by_unicode(filename, 'U+4E00'))  # Замените 'U+4E00' на нужный Юникод иероглифа
