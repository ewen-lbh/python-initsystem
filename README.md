Manage services.
Supports SystemV init or systemd.

## Installation

Available [on PyPI](https://pypi.org/project/initsystem):

```
pip install initsystem
```

## Example

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
