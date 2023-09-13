# st-combobox

- [Installation](#installation)
- [Overview](#overview)
- [Usage](#usage)
- [Example](#example)

---

A streamlit custom component providing a searchbox with autocomplete.

![Example](./assets/example.gif)


## Installation

```python
pip install st-combobox
```

## Overview

Create a searchbox component and pass a `search_function` that accepts a `str` searchterm. The searchbox is triggered on user input, calls the search function for new options and redraws the page via `st.experimental_rerun()`.

You can either pass a list of arguments, e.g.

```python
import wikipedia
from streamlit_searchbox import st_searchbox

# function with list of labels
def search_wikipedia(searchterm: str) -> List[any]:
    return wikipedia.search(searchterm) if searchterm else []


# pass search function to searchbox
selected_value = st_searchbox(
    search_wikipedia,
    key="wiki_searchbox",
)
```

This example will call the Wikipedia Api to reload suggestions. The `selected_value` will be one of the items the `search_wikipedia` function returns, the suggestions shown in the UI components are a `str` representation. In case you want to provide custom text for suggestions, pass a `Tuple`.

```python
def search(searchterm: str) -> List[Tuple[str, any]]:
    ...
```

## Usage

To customize the searchbox you can pass the following arguments:

```python
search_function: Callable[[str], List[any]]
```

Function that will be called on user input

```python
placeholder: str = "Search ..."
```

Placeholder for empty searches shown within the component.

```python
label: str = None
```

Label shown above the component.

```python
default: any = None
```

Default return value in case nothing was submitted or the searchbox cleared.

```python
clear_on_submit: bool = False
```

Automatically clear the input after selection.


```python
key: str = "searchbox"
```

Streamlit key for unique component identification.

### Example

An example Streamlit app can be found [here](./example.py)

## Build

If any changes were made to the frontend, go to `st_combobox/frontend` and run `npm run build` (`npm install` if you don't have the packages on your machine). Then push the changes made to the `frontend/build` folder to the repo. 

You may need to follow [this](https://stackoverflow.com/questions/69692842/error-message-error0308010cdigital-envelope-routinesunsupported) help if you run into issues while building.

Now all you have to do is make a release and the github action will push to PyPi (make sure `setup.py` has a new verison)