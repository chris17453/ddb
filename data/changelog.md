### ddb Recent additions

- load/reload of database configuration unified, temp table safe
- failed table configurations pass warnings, and do not trigger a fail
- sql function: "version()" returns ddb version
- created output options json / yaml / raw / xml / term
- removed bumpversion
- updated pyyaml
- pyinstaller creates single file executable for packaging. in dist/
- makefile
- unittesting for basic operations
- base support for non aggregate functions in select column, with renaming, up to 3 parameters
- sql function: "database()" returns the curently selected database context
- added sql parsing support for join, left join, right join, full join *not implimented*
- added sql parsing support renaming tables "AS" with joins and from *not implimented*
