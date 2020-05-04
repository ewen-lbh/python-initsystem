Manage services.
Supports SystemV init or systemd.
Example:

```python
>>> from initsystem import Service
>>> couchdb = Service('couchdb')
>>> couchdb.is_running()
False
>>> couchdb.start()
>>> couchdb.is_running()
True
>>> couchdb.stop()
>>> couchdb.is_running()
False
```