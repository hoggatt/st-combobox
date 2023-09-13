# st-combobox

- [Installation](#installation)
- [Overview](#overview)
- [Usage](#usage)
- [Example](#example)

---

A streamlit custom component providing a combobox with autocomplete.

![Example](https://raw.githubusercontent.com/hoggatt/st-combobox/main/assets/example.gif)


## Installation

```python
pip install st-combobox
```

## Overview

Create a searchbox component and pass a `search_function` that accepts a `str` searchterm. The searchbox is triggered on user input and calls the search function for new options.`.

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


Function that will be called on user input
```python
search_function: Callable[[str], List[any]]
```


Placeholder text when the combobox is blank.
```python
placeholder: str = "Search ..."
```


Label shown above the component. If `None`, no label is shown.
```python
label: str = None
```


Default return value in case nothing was submitted or the searchbox cleared.
```python
default: any = None
```


Automatically clear the input after selection.
```python
clear_on_submit: bool = False
```


Streamlit key for unique component identification.
```python
key: str = "combobox"
```


If true, will call `st.experimental_rerun()` on each search keystroke.
```python
rerun_on_update: bool = False
```


If true (and `rerun_on_update` is false), will call `st.stop()` on each search keystroke.
```python
stop_on_update: bool = False
```


If not None, will set the default search value when the box is initialized or reset. 
```python
blank_search_value: str = None
```


If true, will only return a non None value when the user selects an option. Otherwise, will keep returning the last value.
```python
return_only_on_submit: bool = False
```


### Example

An example Streamlit app can be found [here](./example.py)

## Build

If any changes were made to the frontend, go to `st_combobox/frontend` and run `npm run build` (`npm install --legacy-peer-deps` if you don't have the packages on your machine). Then push the changes made to the `frontend/build` folder to the repo. 

You may need to follow [this](https://stackoverflow.com/questions/69692842/error-message-error0308010cdigital-envelope-routinesunsupported) help if you run into issues while building.

Now all you have to do is make a release and the github action will push to PyPi (make sure `setup.py` has a new verison).