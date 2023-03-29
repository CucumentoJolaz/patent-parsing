import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

# Загрузка стоп-слов и настройка токенизации
nltk.download('stopwords')
stop_words = stopwords.words('english')
tokenizer = RegexpTokenizer(r'\w+')

# Чтение данных из файла
df = pd.read_excel('united_patents.xlsx')

# Обработка текста
def process_text(text):
    tokens = tokenizer.tokenize(text.lower())
    meaningful_tokens = [token for token in tokens if token not in stop_words and len(token) > 2]
    return meaningful_tokens

# Создание словаря для каждого патента
word_counts = []
for i, row in df.iterrows():
    text = row['Title'] + ' ' + row['Abstract'] + ' ' + row['Claims']
    tokens = process_text(text)
    unique_tokens = list(set(tokens))
    word_count = {token: tokens.count(token) for token in unique_tokens}
    word_count = {k: v for k, v in word_count.items() if v > 0}
    sorted_word_count = {k: v for k, v in sorted(word_count.items(), key=lambda item: item[1], reverse=True)}
    word_counts.append(sorted_word_count)

# Добавление столбца с количеством вхождений каждого слова
df['Word Counts'] = word_counts

# Сохранение данных в файл
df.to_excel('united_patents.xlsx', index=False)