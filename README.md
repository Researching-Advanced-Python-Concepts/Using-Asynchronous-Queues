# Using-Asynchronous-Queues

- A rudimentary web crawler, which recursively follows links on a specified website up to a given depth level and counts the number of visits per link.
- So I vist an online store, go to shoes section, go to a particular shoe brand, particular shoe size and this program deals with how far deep should I go and counts the number of visits per link.

- `python -m http.server` start a server in a local folder with python virtual environment

- asyncronous queues deliberately mimic an interface of the corresponding thread-safe queues.
- we can use asynchronous queues to exchange data between coroutines.

## FIFO

- visits the first level
- after visiting all links on the 2nd level, the crawler proceeds to the 3rd level and so on until reaching the maximum depth level requested.
- once all links on a given level are explored, the crawler never goes back to an earlier level. (BREADTH FIRST SEARCH)

## LIFO

- Crawler visits identical links but in a different order
- the last coming link is evaluated first while the previous caught links wait for the new ones to finish
- we visit deeper links too
- visit depth 2 and visit its subsequent depth down the line
  - like `videos` depth 2 -> `videos/bin` depth 3

## Priority Queue

- crawler visists identical links but in a different order
- in case of same depth url, the one with the smallest url are crawled first
- whereas in lifo if a depth 2 url appears the first appearing one's depth is first evaluated
- but here the least length one is evaluated

