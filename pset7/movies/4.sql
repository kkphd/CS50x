-- CS50 Fall 2020
-- Problem Set 7
-- Author: kkphd

-- Write a SQL query to determine the number of movies with an IMDb rating of 10.0.

SELECT COUNT(movie_id)
FROM ratings
WHERE rating = 10.0;