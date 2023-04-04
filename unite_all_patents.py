import os
from multiprocessing import freeze_support

import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer


# Функция для чтения файла и преобразования его в словарь
def read_file(filename):
    df = pd.read_excel(filename)
    return df.to_dict('records')

def main():
    directory = 'patent_unloadings'
    all_files = os.listdir(directory)

    # Чтение всех файлов с расширением xlsx и преобразование их в словари
    data = []
    for filename in all_files:
        if filename.endswith('.xlsx'):
            filepath = os.path.join(directory, filename)
            data.extend(read_file(filepath))


    # Загрузка стоп-слов и настройка токенизации
    nltk.download('stopwords')
    stop_words = stopwords.words('english')
    tokenizer = RegexpTokenizer(r'\w+')

    # Обработка текста
    def process_text(text):
        tokens = tokenizer.tokenize(text.lower())
        meaningful_tokens = [token for token in tokens if token not in stop_words and len(token) > 2]
        return meaningful_tokens


    # Создание словаря для каждого патента
    word_counts = []
    for i, row in df.iterrows():
        text = row['Title'] + ' ' + row['Abstract']
        tokens = process_text(text)
        unique_tokens = list(set(tokens))
        word_count = {token: tokens.count(token) for token in unique_tokens}
        word_count = {k: v for k, v in word_count.items() if v > 0}
        sorted_word_count = {k: v for k, v in sorted(word_count.items(), key=lambda item: item[1], reverse=True)}
        word_counts.append(sorted_word_count)

    # Добавление столбца с количеством вхождений каждого слова
    df = pd.DataFrame(data)
    df['Word Counts'] = word_counts

    # Запись данных в файл "united_patents.xlsx" с форматированием

    writer = pd.ExcelWriter('united_patents.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)


    # Получение объекта xlsxwriter и добавление форматирования
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']

    # Add a header format.
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'left',
        'fg_color': '#C7E4F3',
        'border': 1})

    # Write the column headers with the defined format.
    for i, col in enumerate(df.columns):
        worksheet.write(0, i, col, header_format)

    worksheet.set_column(0, len(data[0]), 60)
    worksheet.set_default_row(100)
    writer.close()


if __name__ == '__main__':
    freeze_support()
    main()