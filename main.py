import datetime
import json
import os
import time
from multiprocessing import freeze_support

import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

rik_tokens = []
tiv_tokens = []
gy_tokens = []
jy_tokens = []
rik = 'рик'
tiv = 'тив'
gy = 'гу'
jy = 'жу'
nd = 'н/о'

company = 'LyondellBasell'

from revChatGPT.V1 import Chatbot


def define_sector_by_chat(patent_text):
    chatbot = Chatbot(config={
        "access_token": os.environ.get('access_token'),
    })
    for data in chatbot.ask(
            f"""
            Ниже представлен текст патента. Определи к какой теме относится тема данного патента.
            Тему, пожалуйста, определи подробно.
            Так же дай подборное описание патента. 
            Ответ на русском. По возможности.
            Ответ следует вернуть в формате json со следующими полями:
            
            "sector": "Слово обозначающее тему",
            "description": "подробное описание патента"
            
            Желательные темы: гели, пленки, жесткая упаковка, полимерные трубы, полимерные волокна, рецептуры полимерных смесей, полимерные компаунды.
            Однако, если считаешь что ни одна из тем не подходит - давай определение темы на собственное усмотрение. 
            Можно выбрать несколько тем, если это уместно.
            Перечисление тем через запятую.
            Больше никаких дополнительных пояснений не нужно. Только json в заданном выше формате.

            Текст:
            
            {patent_text}
            
             Напоминаю - только json. Никакого пояснения быть не должно. Это очень важно.
            """,
            conversation_id="257d145b-9444-4eca-96ad-e9f0d2be9b6a"

    ):
        message = data["message"]
    return message

# Функция для чтения файла и преобразования его в словарь
def read_file(filename):
    df = pd.read_excel(filename, engine='openpyxl')
    return df.to_dict('records')


def get_dataframe_with_patents():
    directory = 'ready_patents'
    all_files = [f"{company}.xlsx"]  # os.listdir(directory)

    # Чтение всех файлов с расширением xlsx и преобразование их в словари
    data = []
    for filename in all_files:
        if filename.endswith('.xlsx'):
            filepath = os.path.join(directory, filename)
            data.extend(read_file(filepath))

    # Создание словаря для каждого патента
    return pd.DataFrame(data)


def write_to_excel(df, filename="patents.xlsx"):
    # Создаем writer и engine
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')

    df = df[['Section', 'Description', 'Publication numbers',
             'Current assignees', 'Priority dates', 'Title',
             'Abstract', 'Claims',
             'Legal status (Pending, Granted, Revoked, Expired, Lapsed)', 'Advantages / Previous drawbacks',
             'Independent claims', 'Object of invention', 'Keywords in context']]
    workbook = writer.book
    worksheet = workbook.add_worksheet('Sheet1')

    # Форматирование заголовка
    header_format = workbook.add_format({
        'bold': True,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color': '#C6E0B4',
        'font_color': '#006100',
        'border': 1
    })

    # Применяем форматирование заголовка
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format)
        worksheet.set_column(col_num, col_num, 70)

    # Форматирование клеток с данными
    cell_format = workbook.add_format({
        'valign': 'top',
        'align': 'left',
        'text_wrap': True,
        'border': 1
    })

    # Применяем форматирование клеток с данными
    for row_num in range(1, len(df) + 1):
        for col_num, value in enumerate(df.iloc[row_num - 1]):
            worksheet.write(row_num, col_num, str(value), cell_format)
            worksheet.set_column(col_num, col_num, 80)
            worksheet.set_row(row_num, 150)

    print("Saving")
    last_row = len(df.index)
    last_col = len(df.columns) - 1
    worksheet.autofilter(0, 0, last_row, last_col)

    # Закрываем writer
    writer.close()


def main():
    start_time = time.time()
    description = 'Description'
    sector = 'Sector'
    df = get_dataframe_with_patents()
    # Проверяем, есть ли колонки 'Section' и 'Description' в DataFrame
    has_section = 'Section' in df.columns
    has_description = 'Description' in df.columns

    # Если колонок нет, то создаем их
    if not has_section:
        df['Section'] = ''

    if not has_description:
        df['Description'] = ''

    # Обрабатываем только пустые ячейки в колонках 'Section' и 'Description'
    for i, row in df.iterrows():
        if has_section and pd.notna(row['Section']):
            continue
        if has_description and pd.notna(row['Description']):
            continue

        text = row['Title'] + ' ' + row['Abstract'] + '' + row['Claims']
        while True:
            try:
                chat_dict_answer = json.loads(define_sector_by_chat(text[:7000]))
            except json.decoder.JSONDecodeError:
                continue
            break
        df.at[i, 'Section'] = chat_dict_answer['sector']
        df.at[i, 'Description'] = chat_dict_answer['description']
        print(row['Title'])
        print(chat_dict_answer)

        # Сохраняем результаты в файл каждые 5 строк
        if (i + 1) % 1 == 0:
            write_to_excel(df, filename=f'ready_patents/{company}.xlsx')

    write_to_excel(df, filename=f'ready_patents/{company}.xlsx')
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    freeze_support()
    main()
