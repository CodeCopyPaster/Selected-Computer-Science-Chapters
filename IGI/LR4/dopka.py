import pandas as pd

def doptask():

    df = pd.read_csv('imdb_top_250.csv')

    print("Информация о столбцах и типах данных")
    print(df.info())
    print("Размерность датафрейма")
    print(df.shape)
    print("Первые 5 строк")
    print(df.head())
    print("Статистика по числовым столбцам")
    print(df.describe())
    print("Список столбцов")
    print(df.columns)
    print("Количество пропущенных значений")
    print(df.isnull().sum())
    print('==============================')

    # the most new film
    mostNewDF = df['Year'].max()
    print("Самый новый фильм")
    print(mostNewDF)
    print('==============================')

    # the most old film
    mostOldDF = df['Year'].min()
    print("Самый старый фильм")
    print(mostOldDF)
    print('==============================')

    # find avg score from csv
    avg_score = df['Rating'].mean()
    print(f"Средний рейтинг фильмов из топа:{avg_score:.2f}")
    print('==============================')

    # print list of films which rating is less than average
    upper_avg_wage = df[df['Rating'] < avg_score]
    print("Фильмы из топа с рейтингом ниже среднего")
    print(upper_avg_wage)
    print('==============================')
