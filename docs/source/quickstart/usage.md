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

This extension doesn't have options for now

## Compatibility

- [x] autodoc_pydantic (Tested with basic BaseModel and Field (description and ge))
- [ ] The next one to test