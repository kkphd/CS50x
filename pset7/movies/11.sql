-- CS50 Fall 2020
-- Problem Set 7
-- Author: kkphd

-- Write a SQL query to list the titles of the five highest rated movies (in order) that
-- Chadwick Boseman starred in, starting with the highest rated.

SELECT title
FROM people -- Since our search criteria concerns a person's name
JOIN ratings ON movies.id = ratings.movie_id
JOIN stars ON people.id = stars.person_id
JOIN movies ON stars.movie_id = movies.id
WHERE people.name = "Chadwick Boseman"
ORDER BY ratings.rating DESC
LIMIT 5;