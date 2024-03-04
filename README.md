# humanlog
Personal Logging Utility

## Design Notes
- [https://www.sqlite.org/fts5.html] sqlite backend for full text search
- Basic Design
    - basic usage: humanlog <CATEGORY> [tags...] - invoke $EDITOR (or vim), saves doc to db
    - option: --export (creates importable textfile)
    - option: --import (imports above file into sqlite)
    - option: --search (FTS search)
    - option: --category (gets all entries reverse order for given category)
    - option: --tag (gets all entries for a given tag, reverse order)
    - option: --limit (for search, category, tag - limits the results back)
- Stores config in xdg config dir
- Stores db in xdg data dir
- creates tempfile for $EDITOR portion
