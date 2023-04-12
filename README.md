# pleiades_python

Python wrapper for Pleiades gazetteer APIs

## Initialize gazetteer interface

```python
from pleiades_python.gazetteer import Gazetteer
g = Gazetteer()
Using default user-agent (PleiadesPythonBot/0.0.1) for all requests to the Pleiades gazetteer website. We strongly prefer you define your own unique user-agent string and pass it to the Gazetteer class at instantiation.
```

## Set your own user agent string (please!)

```python
g = Gazetteer(user_agent="MyPleiadesBot/1.0")
```

## Caching

pleiades_python caches web responses (using requests-cache, via webiquette). 

By default, platformdirs is used to determine where requests-cache puts the cache file (in the "user cache dir" appropriate for your OS). You can override this too. Here's a mac example:

```python
from pleiades_python.gazetteer import DEFAULT_CACHE_DIR
print(DEFAULT_CACHE_DIR)
/Users/paregorios/Library/Caches/pleiades-python/webi_cache/
g = Gazetteer(cache_dir="/Users/paregorios/my/custom/cache/directory/")
```

The defaults for this package are designed to cache Pleiades content for a day. This insulates the Pleiades servers from multiple rapid-fire requests if you're testing, developing, or running things frequently in your application, but also ensures you'll get up-to-date information if something has changed in the last day. At initialization of a `Gazetteer` object, you can override these defaults for some of the parameters that [requests-cache uses to control expiration](https://requests-cache.readthedocs.io/en/stable/user_guide/expiration.html): 

- cache_control
- expire_after

```python
from pleiades_python.gazetteer import DEFAULT_CACHE_CONTROL, DEFAULT_EXPIRE_AFTER
print(DEFAULT_CACHE_CONTROL)
False
print(DEFAULT_EXPIRE_AFTER)
7 days, 0:00:00
type(DEFAULT_EXPIRE_AFTER)
<class 'datetime.timedelta'>
from datetime import timedelta
g = Gazetteer(expire_after=timedelta(days=1), user_agent="MyPleiadesBot/1.0")
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
