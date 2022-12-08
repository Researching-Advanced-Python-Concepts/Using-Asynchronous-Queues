# Using-Asynchronous-Queues

- A rudimentary web crawler, which recursively follows links on a specified website up to a given depth level and counts the number of visits per link.
- So I vist an online store, go to shoes section, go to a particular shoe brand, particular shoe size and this program deals with how far deep should I go and counts the number of visits per link.

- `python -m http.server` start a server in a local folder with python virtual environment

## FIFO

- visits the first level
- after visiting all links on the 2nd level, the crawler proceeds to the 3rd level and so on until reaching the maximum depth level requested.
- once all links on a given level are explored, the crawler never goes back to an earlier level. (BREADTH FIRST SEARCH)