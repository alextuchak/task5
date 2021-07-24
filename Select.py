from pprint import pprint
import sqlalchemy

dsn = 'postgresql://task4:task4@localhost:5432/task4'
engine = sqlalchemy.create_engine(dsn)
connection = engine.connect()

# 1.количество исполнителей в каждом жанре;

pprint(connection.execute(""" SELECT g.name, COUNT(a.name) FROM genre g
 LEFT JOIN artists a ON a.artistgenre = g.id 
 GROUP BY g.id""").fetchall())

# 2.количество треков, вошедших в альбомы 2019-2020 годов;

pprint(connection.execute(""" SELECT COUNT(t.name) FROM albums al
 LEFT JOIN tracks t ON t.trackalbum = al.id
 WHERE al.released BETWEEN 2019 AND 2020 """).fetchall())

# 3.средняя продолжительность треков по каждому альбому;

pprint(connection.execute(""" SELECT al.name, AVG(t.length) FROM albums al
 LEFT JOIN tracks t ON t.trackalbum = al.id
 GROUP BY al.id """).fetchall())

# 4.все исполнители, которые не выпустили альбомы в 2020 году;

pprint(connection.execute(""" SELECT a.name FROM albums al
 LEFT JOIN artists a ON a.artistalbum = al.id
 WHERE NOT al.released = 2019
 GROUP BY a.name """).fetchall())

# 5.названия сборников, в которых присутствует конкретный исполнитель (выберите сами);

pprint(connection.execute(""" SELECT DISTINCT m.name FROM artists a
 LEFT JOIN tracks t ON a.id = t.trackartist
 LEFT JOIN mixtapes m ON t.trackmixtapes = m.id
 WHERE a.name LIKE '%%Machine Gun Kelly%%'
  """).fetchall())

# 6.название альбомов, в которых присутствуют исполнители более 1 жанра;

pprint(connection.execute(""" SELECT al.name FROM albums al
LEFT JOIN artists ar ON al.id = ar.artistalbum
WHERE ar.name = (
SELECT name FROM artists
GROUP by name
HAVING MAX(artistgenre) != AVG(artistgenre)) """).fetchall())
# В моей БД связь артиста с жанрами происходит через столбец INTEGER artistgenre. Если артист поет в одном жанре, то
# при любом кол-ве записей с разными альбомами AVG значение столбца artistgenre будет равно самому себе. Если поет в
# разных условие запроса выполнится

# 7. наименование треков, которые не входят в сборники;
pprint(connection.execute(""" SELECT DISTINCT t.name FROM tracks t
LEFT JOIN mixtapes m ON t.trackmixtapes = m.id
WHERE t.trackmixtapes IS NULL;
""").fetchall())

# 8.исполнителя(-ей), написавшего самый короткий по продолжительности трек (теоретически таких треков может быть
# несколько);

pprint(connection.execute(""" SELECT name, length from tracks
WHERE length = (
SELECT MIN(length) from tracks);
""").fetchall())

# 9. название альбомов, содержащих наименьшее количество треков.
pprint(connection.execute("""
CREATE TABLE IF NOT EXISTS temptable
(Name VARCHAR(64), albumid INTEGER);
INSERT INTO temptable SELECT DISTINCT name, trackalbum from tracks;

SELECT al.name FROM albums al
LEFT JOIN temptable te ON te.albumid = al.id
GROUP BY al.name
HAVING COUNT(al.name) <= 1;

 """).fetchall())
(connection.execute("""DROP TABLE temptable """).fetchall())
 # В моей БД есть песня которую исполняют два исполнителя и это единственная песня в альбоме. Для корректного вывода
 # названия альбомов с наименьшим колличеством песен использовал промежуточную фильтрацию через временную таблицу