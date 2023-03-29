import os
from multiprocessing import freeze_support

import pandas as pd
import gensim
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

def main():
    directory = 'patent_unloadings'
    all_files = os.listdir(directory)

    # Функция для чтения файла и преобразования его в словарь
    def read_file(filename):
        df = pd.read_excel(filename)
        return df.to_dict('records')

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

    # Предварительная обработка данных
    texts = []
    for text in data:
        text = text['Title'] + ' ' + text['Abstract'] + ' ' + text['Claims']
        tokens = tokenizer.tokenize(text.lower())
        stopped_tokens = [token for token in tokens if token not in stop_words]
        texts.append(stopped_tokens)

    # Создание словаря и корпуса для модели LDA
    dictionary = gensim.corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    # Обучение модели LDA на корпусе
    lda_model = gensim.models.LdaMulticore(corpus, num_topics=16, id2word=dictionary, passes=2, workers=2)

    # Получение списка тем для каждого документа
    topics = []
    for text in texts:
        bow = dictionary.doc2bow(text)
        topic_weights = lda_model.get_document_topics(bow, minimum_probability=0.0)
        topic = max(topic_weights, key=lambda x: x[1])[0]
        topics.append(topic)


    # Запись данных в файл "united_patents.xlsx" с форматированием
    df = pd.DataFrame(data)
    df['Topic'] = topics
    writer = pd.ExcelWriter('united_patents.xlsx', engine='xlsxwriter')
    df.to_excel(writer, index=False)

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
    for i, topic in lda_model.print_topics(num_topics=16, num_words=10):
        print(f"Topic {i}: {topic}")
    writer.save()


if __name__ == '__main__':
    freeze_support()
    main()