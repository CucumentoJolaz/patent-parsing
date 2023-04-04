import os
from multiprocessing import freeze_support

import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer


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
    all_files = os.listdir(directory)

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
        text = row['Title'] + ' ' + row['Abstract']
        tokens = process_text(text)
        unique_tokens = list(set(tokens))
        words = {token: tokens.count(token) for token in unique_tokens}
        word_count = {k: v for k, v in words.items() if v > 0}
        sorted_word_count = {k: v for k, v in sorted(word_count.items(), key=lambda item: item[1], reverse=True)}
        word_counts.append(sorted_word_count)
    return word_counts

def write_df_to_xlsx(df, filename='united_patents.xlsx'):
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')

    df.to_excel(writer, sheet_name='Sheet1', index=False)
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'left',
        'fg_color': '#C7E4F3',
        'border': 1})
    for i, col in enumerate(df.columns):
        worksheet.write(0, i, col, header_format)
    worksheet.set_column(0, len(df.columns), 60)
    worksheet.set_default_row(100)
    writer.close()


def main():
    df = get_dataframe_with_patents()
    df['Word Counts'] = count_words(df)
    write_df_to_xlsx(df)


if __name__ == '__main__':
    freeze_support()
    main()