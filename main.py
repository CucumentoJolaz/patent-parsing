import os
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


from revChatGPT.V1 import Chatbot

def define_sector_by_chatGPT(patent_text):
    chatbot = Chatbot(config={
        "email": "cucumento2@gmail.com",
        "password": "Nebraska77778888__"
    })
    for data in chatbot.ask(
            f"""{rik} - рецептуростроение и компунды
                {tiv} - трубы и волокна
                {gy} - гибкая упаковка
                {jy} - жёсткая упаковка
                {nd} - не определено, другая тема
                
                Есть 4 темы + отдельная 'неопределено'. 
                Ниже представлен текст патента. Определи к какой теме относится тема данного патента. Ответь только буквами (rik, tiv, gy, jy, no). и только. Больше ничего отвечать не нужно.
                Ещё раз: только несколько букв, которые маркируют тему, не более.
                
                Текст:
                
                {patent_text}""",
        conversation_id="80c17a80-cc42-4d18-8ba9-81a4cb082d1d"
    ):
        message = data["message"][len(prev_text) :]
        prev_text = data["message"]
    return message


# Обработка текста
def process_text(text):
    # Загрузка стоп-слов и настройка токенизации

    stop_words = stopwords.words('english')
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text.lower())
    meaningful_tokens = [token for token in tokens if token not in stop_words and len(token) > 2]
    return meaningful_tokens

# Функция для чтения файла и преобразования его в словарь
def read_file(filename):
    df = pd.read_excel(filename)
    return df.to_dict('records')

def get_dataframe_with_patents():
    directory = 'patent_unloadings'
    all_files = ['Sinopec.xlsx']#os.listdir(directory)

    # Чтение всех файлов с расширением xlsx и преобразование их в словари
    data = []
    for filename in all_files:
        if filename.endswith('.xlsx'):
            filepath = os.path.join(directory, filename)
            data.extend(read_file(filepath))

    # Создание словаря для каждого патента
    return pd.DataFrame(data)


def count_words(df):
    word_counts = []
    nltk.download('stopwords')
    for i, row in df.iterrows():
        text = row['Title'] + ' ' + row['Abstract'] + '' + row['Claims']
        tokens = process_text(text)
        unique_tokens = list(set(tokens))
        words = {token: tokens.count(token) for token in unique_tokens}
        word_count = {k: v for k, v in words.items() if v > 0}
        sorted_word_count = {k: v for k, v in sorted(word_count.items(), key=lambda item: item[1], reverse=True)}
        word_counts.append(sorted_word_count)
    return word_counts


def write_to_excel(df, filename="patents.xlsx"):
    # Создаем writer и engine
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')

    # Записываем df в excel
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']

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

    last_row = len(df.index)
    last_col = len(df.columns) - 1
    worksheet.autofilter(0, 0, last_row, last_col)

    # Закрываем writer
    writer.close()


def calculate_sector_tokens(patent_tokens: dict) -> dict:
    """
    Calculate how many sector-specific tokens are present in a patent.
    :param patent_tokens: a dictionary of tokens in the patent
    :return: a dictionary with the count of sector-specific tokens in the patent
    """

    rik_tokens = ['compounds', 'formulation', 'formulations', 'compound', 'preparation',
                  'preparations', 'peroxide']
    tiv_tokens = ['pipe', 'tube', 'tubes', 'fiber', 'fibers', 'filament', 'filaments']
    gy_tokens = ['packaging', 'film', 'films', 'bag', 'bags', 'pouch', 'pouches', 'blow']
    jy_tokens = ['box', 'boxes', 'carton', 'cartons', 'container', 'containers']

    tokens_sector_counter = {rik: 0, tiv: 0, gy: 0, jy: 0, nd: 0}

    patent_tokens_copy = patent_tokens.copy()
    for token in patent_tokens_copy.keys():
        if token in rik_tokens:
            tokens_sector_counter[rik] += patent_tokens.pop(token)
        elif token in tiv_tokens:
            tokens_sector_counter[tiv] += patent_tokens.pop(token)
        elif token in gy_tokens:
            tokens_sector_counter[gy] += patent_tokens.pop(token)
        elif token in jy_tokens:
            tokens_sector_counter[jy] += patent_tokens.pop(token)
        else:
            tokens_sector_counter[nd] += patent_tokens.pop(token)

    return tokens_sector_counter

def identify_sector(patent_tokens: dict) -> str:
    """
    Identify the most likely sector for a given patent.
    :param patent_tokens: a dictionary of tokens in the patent
    :return: the sector of the patent: 'rik', 'tiv', 'gy', 'jy', 'nd'
    """
    section_tokens = calculate_sector_tokens(patent_tokens)
    section_tokens_no_nd = section_tokens.copy()
    section_tokens_no_nd.pop(nd)
    max_sector = max(section_tokens_no_nd, key=section_tokens.get)

    if not any(section_tokens_no_nd.values()):
        return nd
    return max_sector


def main():
    wc = 'Word Counts'
    sector = 'Sector'
    df = get_dataframe_with_patents()
    df[wc] = count_words(df)
    for i in df[wc]:
        print("-------------SEPARATION---------------")
        print(i)
    df.insert(loc=0, column=sector, value=[identify_sector(dict(row[wc])) for i, row in df.iterrows()])
    write_to_excel(df)


if __name__ == '__main__':
    freeze_support()
    main()