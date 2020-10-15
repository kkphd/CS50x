-- CS50 Fall 2020
-- Problem Set 7
-- Author: kkphd

-- Write a SQL query to list the names of all people who starred in a movie
-- in which Kevin Bacon also starred.

SELECT DISTINCT people.name
FROM people
INNER JOIN stars ON people.id = stars.person_id
WHERE stars.movie_id IN
(SELECT movie_id
FROM stars
INNER JOIN people ON stars.person_id = people.id
WHERE people.name = 'Kevin Bacon' AND people.birth = 1958)
AND people.name <> 'Kevin Bacon';