# pleiades_python

Python wrapper for Pleiades gazetteer APIs

## Initialize gazetteer interface

```python
from pleiades_python.gazetteer import Gazetteer
g = Gazetteer()
Using default user-agent (PleiadesPythonBot/0.0.1) for all requests to the Pleiades gazetteer website. We strongly prefer you define your own unique user-agent string and pass it to the Gazetteer class at instantiation.

```

## Validate a Pleiades Place Identifier (PID)

```python
pid = "https://pleiades.stoa.org/places/295374"
uri = g.valid_pid(pid)
print(uri)
https://pleiades.stoa.org/places/295374
```

Alternate short form:

```python
pid = "295374"
uri = g.valid_pid(pid)
print(uri)
https://pleiades.stoa.org/places/295374
```

If the place resource corresponding to the PID you're using has been withdrawn because it was a duplicate for another one, `valid_pid` will return the URI for the consolidated place resource:

```python
pid = "https://pleiades.stoa.org/places/1001902"
uri = self.g.valid_pid(pid)
print(uri)
https://pleiades.stoa.org/places/991367
```

Malformed PIDs will raise errors:

```python
g.valid_pid("Zucchabar")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/paregorios/Documents/files/P/pleiades_python/src/pleiades_python/gazetteer.py", line 70, in valid_pid
    int(pid)
ValueError: invalid literal for int() with base 10: 'Zucchabar'
g.valid_pid("https://nowhere.com/is/purple")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/paregorios/Documents/files/P/pleiades_python/src/pleiades_python/gazetteer.py", line 91, in valid_pid
    raise ValueError(pid)
ValueError: https://nowhere.com/is/purple
```

If the PID is well-formed, but there is no corresponding Pleiades place resource, an HTTPError will be raised:

```python
g.valid_pid("https://pleiades.stoa.org/places/0")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/paregorios/Documents/files/P/pleiades_python/src/pleiades_python/gazetteer.py", line 92, in valid_pid
    r = self.webi.head(place_uri, allow_redirects=True)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/paregorios/Documents/files/P/pleiades_python/.direnv/python-3.11.3/lib/python3.11/site-packages/webiquette/webi.py", line 213, in head
    r.raise_for_status()
  File "/Users/paregorios/Documents/files/P/pleiades_python/.direnv/python-3.11.3/lib/python3.11/site-packages/requests/models.py", line 1021, in raise_for_status
    raise HTTPError(http_error_msg, response=self)
requests.exceptions.HTTPError: 404 Client Error: Not Found for url: https://pleiades.stoa.org/places/0
```
