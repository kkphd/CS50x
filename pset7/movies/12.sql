-- CS50 Fall 2020
-- Problem Set 7
-- Author: kkphd

-- Write a SQL query to list the titles of all movies in which both Johnny Depp and
-- Helena Bonham Carter starred.

SELECT title
FROM movies
JOIN stars ON stars.movie_id = movies.id
JOIN people on stars.person_id = people.id
WHERE people.name = "Johnny Depp"
INTERSECT
SELECT title
FROM movies
JOIN stars ON stars.movie_id = movies.id
JOIN people on stars.person_id = people.id
WHERE people.name = "Helena Bonham Carter";
