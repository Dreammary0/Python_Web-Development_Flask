import sqlite3
import pandas as pd

con = sqlite3.connect("library.sqlite")
f_damp = open('library.db','r', encoding ='utf-8-sig')
damp = f_damp.read()
f_damp.close()
con.executescript(damp)
con.commit()
cursor = con.cursor()


# Для каждого жанра посчитать, сколько различных книг этого жанра представлено в
# библиотеке, каково общее количество доступных экземпляров книг (имеющихся в наличии)
# и какой самый ранний год издания книг, относящихся к этому жанру. Информацию
# отсортировать по названию жанра в алфавитном порядке.
print('Задание 1.1')
cursor.execute('''
    SELECT genre_name, count(book.book_id), sum(book.available_numbers), min(book.year_publication)
        FROM genre 
        JOIN book ON genre.genre_id=book.genre_id
        group by book.genre_id ORDER BY genre_name
    ''')
print(cursor.fetchall())
print(' ')


# Вывести информацию о всех книгах, который сдал заданный читатель. Для каждой
# книги указать дату выдачи, дату сдачи и сколько дней книга была на руках. Информацию
# отсортировать по убыванию количества дней
print('Задание 1.2')
cursor.execute('''
    SELECT book.title, book_reader.return_date, book_reader.borrow_date,
    CAST (julianday(book_reader.return_date) - julianday(book_reader.borrow_date) AS INTEGER)
        FROM book 
        JOIN book_reader ON
        (book_reader.book_id=book.book_id AND book_reader.reader_id=:reader AND book_reader.return_date IS NOT NULL )
        ORDER BY CAST (julianday(book_reader.return_date) - julianday(book_reader.borrow_date) AS INTEGER) DESC
    ''', {"reader": "2"})
print(cursor.fetchall())
print(" ")

# Вывести самый популярный жанр (жанры). Самым популярным считается жанр,
# книги которого чаще всего брали читатели в библиотеке. Вывести название жанра (жанров) и
# сколько раз читатели брали книги этого жанра. Информацию отсортировать по названию
# жанров в алфавитном порядке.
print('Задание 1.3')
cursor.execute('''
    create view if not exists populars as
    SELECT genre.genre_name, count(book_reader.book_reader_id) as number_of_readers
        FROM book_reader 
        inner JOIN book ON book.book_id=book_reader.book_id
        inner JOIN genre ON book.genre_id=genre.genre_id
        GROUP BY genre.genre_id        
                ''')
cursor.execute('''
 SELECT genre_name, max(number_of_readers)
        FROM populars
        ORDER BY genre_name ASC      
                ''')
print(cursor.fetchall())
print(' ')




# Вывести книги, которые были взяты в библиотеке в октябре месяце. Указать
# фамилии читателей, которые их взяли, а также дату, когда их взяли. Столбцы назвать
# Название, Читатель, Дата соответственно. Информацию отсортировать сначала по
# возрастанию даты, потом в алфавитном порядке по фамилиям читателей, и, наконец, по
# названиям книг тоже в алфавитном порядке.
print ('2.1 ')
df=pd.read_sql('''
    SELECT book.title AS Название, book_reader.borrow_date AS ДАТА, 
    SUBSTRING(reader.reader_name, 1, INSTR(reader.reader_name, ' ')-1) AS Фамилия
    FROM book, book_reader, reader 
    WHERE (book_reader.book_id=book.book_id AND reader.reader_id=book_reader.reader_id AND strftime('%m', book_reader.borrow_date)='10')
    ORDER BY book_reader.borrow_date ASC, SUBSTRING(reader.reader_name, 1, INSTR(reader.reader_name, ' ')-1)  ASC, 
    book.title ASC ''', con)
print(df)
print(' ')


# Для каждой книги, изданной в заданном издательстве, вывести информацию о ее принадлежности к группе:
# если книга издана раньше 2014 года, вывести "III";
# если книга издана в период с 2014 года по 2017 год, вывести "II";
# если книга издана позже 2017 года, вывести "I".
# Для каждой книги также указать ее жанр и год издания. Столбцы назвать Название, Жанр, Год, Группа. Информацию отсортировать по группе в
# порядке убывания, по возрастанию года издания по названию в алфавитном порядке.
print('Задание 2.2 / 2.3')
df=pd.read_sql('''
    SELECT book.title AS Название, genre.genre_name AS Жанр, book.year_publication AS Год,
        CASE WHEN book.year_publication<2014 THEN 'III'
        WHEN book.year_publication BETWEEN 2014 AND 2017 THEN 'II'
        WHEN book.year_publication>2017 THEN 'I' 
        END AS Группа FROM book
        JOIN genre ON genre.genre_id=book.genre_id
        JOIN publisher ON publisher.publisher_id=book.publisher_id
        WHERE publisher.publisher_name= :publisher_name
''', con, params={"publisher_name": "РОСМЭН"})
print(df)
print(' ')


# Для каждой книги вывести количество экземпляров, которые есть в наличии
# (available_numbers) в библиотеке, а также сколько раз экземпляры книги брали
# читатели. Если книгу читатели не брали - вывести 0. Столбцы назвать Название,
# Количество, Количество_выдачи. Информацию отсортировать сначала по убыванию
# количества выданных экземпляров, а потом по названию книги в алфавитном порядке и,
# наконец, по возрастанию доступного количества.
print('Задание 2.4')
df=pd.read_sql('''
    SELECT book.available_numbers AS Количество, book.title AS Название,
        CASE 
        WHEN count(book_reader.book_reader_id)>0 
        THEN count(book_reader.book_reader_id) ELSE 0 
        END AS Количество_выдачи FROM book 
        LEFT JOIN book_reader USING (book_id)
        GROUP BY book.book_id
        ORDER BY Количество_выдачи DESC, book.title ASC, book.available_numbers ASC
''', con)
print(df)
print(' ')

# Вывести информацию о всех читателях, которые держали книги больше 10 дней
print('Dop zapros: ')
df=pd.read_sql('''
SELECT reader.reader_name as Имя, book.title as Книга,
case 
    when CAST(julianday(book_reader.return_date) - julianday(book_reader.borrow_date) as integer) > 10
    then CAST(julianday(book_reader.return_date) - julianday(book_reader.borrow_date) as integer)
end as Дни_на_руках
from book_reader
join book on book_reader.book_id=book.book_id
join reader on book_reader.reader_id = reader.reader_id
where Дни_на_руках is not null
order by reader.reader_name, Дни_на_руках DESC
''', con)
print(df)
print(" ")

con.close()