import sqlite3
import pandas as pd

# создаем базу данных и устанавливаем соединение с ней
con = sqlite3.connect("lib.sqlite")
# создаем таблицу, если ее еще не было, заносим в нее записи
con.executescript(
    '''

DROP TABLE IF EXISTS genre;

CREATE TABLE genre (
       genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
	   genre_name VARCHAR(30)
);

INSERT INTO genre (genre_name)  VALUES 
('Роман'),
('Приключения'),
('Детектив'),
('Поэзия'),
('Фантастика'),
('Фэнтези');

DROP TABLE IF EXISTS publisher;

CREATE TABLE publisher (
       publisher_id INTEGER PRIMARY KEY AUTOINCREMENT,
	   publisher_name VARCHAR(40)
);

INSERT INTO publisher (publisher_name)  VALUES 
('ЭКСМО'),
('ДРОФА'),
('АСТ');

DROP TABLE IF EXISTS book;

CREATE TABLE book (
      book_id INTEGER PRIMARY KEY AUTOINCREMENT, 
	  title VARCHAR(80),
      genre_id int, 
      publisher_id INT,
      year_publication INT,
      available_numbers INT, 
      FOREIGN KEY (genre_id)  REFERENCES genre (genre_id) ON DELETE CASCADE,
      FOREIGN KEY (publisher_id)  REFERENCES publisher (publisher_id) ON DELETE CASCADE
);

INSERT INTO book(title, genre_id, publisher_id, year_publication, available_numbers)  VALUES
('Мастер и Маргарита', 1, 2, 2014, 5),
('Таинственный остров', 2, 2, 2015, 10),
('Бородино', 4, 3, 2015, 12),
('Дубровский', 1, 2, 2020, 7),
('Вокруг света за 80 дней', 2, 2, 2019, 5),
('Убийства по алфавиту', 1, 1, 2017, 9),
('Затерянный мир', 2, 1, 2020, 3),
('Герой нашего времени', 1, 3, 2017, 2),
('Смерть поэта', 4, 1, 2020, 2),
('Поэмы', 4, 3, 2019, 5);

DROP TABLE IF EXISTS book_author;

CREATE TABLE book_author (
      book_author_id INTEGER PRIMARY KEY AUTOINCREMENT, 
      book_id INT, 
      author_id INT,
      FOREIGN KEY (book_id)  REFERENCES book (book_id) ON DELETE CASCADE,
      FOREIGN KEY (author_id)  REFERENCES author (author_id) ON DELETE CASCADE
);



''');

# сохраняем информацию в базе данных
con.commit()

cursor = con.cursor()

print('\033[1m' + 'Первый запрос: ' + '\033[0m')
cursor.execute('''
SELECT book.title, genre.genre_name
from book
JOIN genre on book.genre_id = genre.genre_id
WHERE book.available_numbers between :a and :b
''', {"a": 1, "b": 5})
print(cursor.fetchall())
print(" ")

print('\033[1m' + 'Второй запрос: ' + '\033[0m')
cursor.execute('''
SELECT book.title as "название", publisher.publisher_name as "издательство", book.year_publication as год
from book
JOIN publisher on book.publisher_id = publisher.publisher_id
WHERE book.title NOT LIKE  '% %'
and book.year_publication >= :y
''', {"y": 2015})
print(cursor.fetchall())
print(" ")

print('\033[1m' + 'Третий запрос: ' + '\033[0m')
cursor.execute('''
SELECT  sum(book.available_numbers) as "количество", genre.genre_name as жанр
from book
JOIN genre on genre.genre_id = book.genre_id 
and book.year_publication >= :y
group by genre.genre_name
''', {"y": 2015})
print(cursor.fetchall())
print(" ")

print('\033[1m' + 'Pandas запрос: ' + '\033[0m')

df = pd.read_sql('''
 SELECT
 book.title AS Название,
 publisher.publisher_name AS Издательство,
 genre.genre_name AS Жанр,
 book.available_numbers AS количество
 FROM book
 JOIN genre on book.genre_id = genre.genre_id
 JOIN publisher on book.publisher_id = publisher.publisher_id
  WHERE available_numbers >= :p_genre
''', con, params={"p_genre": 3})
print(df)
print(" ")

print(df["Название"])
print(" ")

print(df.loc[2])
print(" ")

print("Количество строк:", df.shape[0])
print("Количество столбцов:", df.shape[1])
print(" ")
print(df.dtypes.index)
print(" ")

print('\033[1m' + 'Четвертый запроКс: ' + '\033[0m')
pub_list = ("ДРОФА", "АСТ")
df = pd.read_sql(f'''
 SELECT
 book.title AS Название,
 publisher.publisher_name AS Издательство,
 book.year_publication AS Год
 FROM book
  JOIN publisher on book.publisher_id = publisher.publisher_id and book.year_publication between 2016 and 2019 
  where  publisher.publisher_name in {pub_list} 



''', con)

print(df)
con.close()
