# How to use this extension

## Start
For now usage is really simple you have just to:
1. Add it to your extension list:
    ```python
    extensions = ['sphinx_autoindex']
    ```
2. Add your package root path:
    ```python
    package_toindex = str(Path(__file__).parent.parent.parent / "src" / "sphinx_autoindex")
    ```
   
## Options
You can customize autodoc options for global documentation and customize by module or package name applied extra options

Default global options:
```python
sai_autodoc_global_config = {
    "members":{},
    "undoc-members":True,
    "show-inheritance":True,
    "inherited-members":True,
    "exclude-members":{},
    "special-members":{},
    "private-members":{},
}
```
Specific option example
```python
sai_autodoc_specific_config = {
    "sphinx_autoindex.test_abc": {
        "no-index": True
    }
}
```


## Compatibility

- [x] autodoc_pydantic (Tested with basic BaseModel and Field (description and ge))
- [ ] The next one to test