import json

# Чтение текста из файла и поиск всех JSON объектов в нём
import pandas as pd

from main import read_file, write_to_excel


def get_dict_from_text(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
        json_objs = []
        while True:
            try:
                # Ищем индекс первого JSON объекта
                start_idx = text.index('{')
                # Обрезаем текст до первого JSON объекта
                text = text[start_idx:]
                # Ищем индекс последней закрывающей скобки JSON объекта
                end_idx = text.index('}') + 1
                # Вырезаем JSON объект из текста и преобразуем в словарь
                json_obj = json.loads(text[:end_idx])
                json_objs.append(json_obj)
                # Обрезаем текст после обработанного JSON объекта
                text = text[end_idx:]
            except ValueError:
                # Если не найдено больше JSON объектов, выходим из цикла
                break
    return json_objs

data = read_file('Basell_1.xlsx')
df = pd.DataFrame(data)
descriptions = [obj['description'] for obj in get_dict_from_text('basell_text.txt')]
df.insert(loc=1, column='Description', value=descriptions)
write_to_excel(df, filename='ready_patents/Basell_1_1.xlsx')