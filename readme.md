<h1>Nextcloud Apps API</h1>

This package is meant to add a python interface for popular nextcloud apps. Current supported are:

- Notes
- Bookmarks

<h3>Notes:</h3>

```python
from nextcloud_apps_api import NotesClient

nc = NotesClient(host="host-address", username="my-username", password="my-username")
notes = nc.get_notes(category="Journal", exclude=["content", "favorite"])
new_note = nc.post_note(title="Hello", content="World", category="Journal")
updated = nc.put_note(new_note['notes']['id'], title="Oops", content="Better content")
deleted = nc.delete_note(new_note['notes']['id'])
```

<h3>Bookmarks:</h3>

```python
from nextcloud_apps_api import BookmarkClient

bc = BookmarkClient(host="host-address", username="my-username", password="my-password")
bookmarks = bc.get_bookmarks(tags=['python'])
new_mark = bc.post_bookmark("https://www.example.com", title="Example", description="Only a test.", tags=['python'])
updated = bc.put_bookmark(new_mark['bookmark']['id'], title="A much better title")
deleted = bc.delete_bookmark(new_mark['bookmark']['id'])
```