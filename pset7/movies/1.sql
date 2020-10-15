-- CS50 Fall 2020
-- Problem Set 7
-- Author: kkphd

 -- Write a SQL query to list the titles of all movies released in 2008.

 SELECT title
 FROM movies
 WHERE year = 2008
 ORDER BY title ASC;