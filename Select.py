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

pprint(connection.execute(""" SELECT name FROM albums
WHERE id = (
SELECT artistalbum FROM artists
 GROUP BY artistalbum
HAVING COUNT(name) > 1
);""").fetchall())

