"""
module for streamlit combobox component
"""
import functools
import logging
import os
from typing import Any, Callable, List

import streamlit as st
import streamlit.components.v1 as components

# point to build directory
parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "frontend/build")
_get_react_component = components.declare_component(
    "combobox",
    path=build_dir,
)

logger = logging.getLogger(__name__)


def wrap_inactive_session(func):
    """
    session state isn't available anymore due to rerun (as state key can't be empty)
    if the proxy is missing, this thread isn't really active and an early return is noop
    """

    @functools.wraps(func)
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as error:
            if kwargs.get("key", None) == error.args[0]:
                logger.debug(f"Session Proxy unavailable for key: {error.args[0]}")
                return

            raise error

    return inner_function

def _list_to_options_py(options: list[Any] | list[tuple[str, Any]]) -> list[Any]:
    """
    unpack search options for proper python return types
    """
    return [v[1] if isinstance(v, tuple) else v for v in options]


def _list_to_options_js(
    options: list[Any] | list[tuple[str, Any]]
) -> list[dict[str, Any]]:
    """
    unpack search options for use in react component
    """
    return [
        {
            "label": str(v[0]) if isinstance(v, tuple) else str(v),
            "value": i,
        }
        for i, v in enumerate(options)
    ]

def _process_search(
    search_function: Callable[[str], List[any]],
    key: str,
    searchterm: str,
    rerun_on_update: str,
    stop_on_update: bool,
    blank_search_value: str = None,
) -> bool:
    # nothing changed, avoid new search
    if searchterm == st.session_state[key]["search"]:
        return st.session_state[key]["result"]

    st.session_state[key]["search"] = searchterm
    search_results = search_function(searchterm)

    if search_results is None:
        search_results = []

    prev_size = len(st.session_state[key]["options_js"])
    st.session_state[key]["options_js"] = _list_to_options_js(search_results)
    st.session_state[key]["options_py"] = _list_to_options_py(search_results)

    # rerun if specified unless we are making the default search and our results are the same size as the previous search (prevent infinite loop)
    if rerun_on_update and not (
        blank_search_value is not None
        and searchterm == blank_search_value
        and prev_size == 0
    ):
        st.experimental_rerun()

    # if not reruning, can also call for stopping on update
    if stop_on_update:
        st.stop()


@wrap_inactive_session
def st_combobox(
    search_function: Callable[[str], List[Any]],
    reset_function: Callable[[], None] = None,
    placeholder: str = "Search ...",
    label: str = None,
    default: Any = None,
    default_options: List[Any] | None = None,
    clear_on_submit: bool = False,
    key: str = "combobox",
    rerun_on_update: bool = False,
    stop_on_update: bool = False,
    blank_search_value: str = None,
    return_only_on_submit: bool = False,
    **kwargs,
) -> Any:
    """
    Create a new combobox instance, that provides suggestions based on the user input
    and returns a selected option or empty string if nothing was selected

    Args:
        search_function (Callable[[str], List[any]]):
            Function that is called to fetch new suggestions after user input.
        reset_function (Callable[[], None], optional):
            Function that is called after the user has reset the combobox. Defaults to None.
        placeholder (str, optional):
            Label shown in the combobox. Defaults to "Search ...".
        label (str, optional):
            Label shown above the combobox. Defaults to None.
        default (any, optional):
            Return value if nothing is selected so far. Defaults to None.
        default_options (List[any], optional):
            Default options to show in the combobox. Defaults to None.
        clear_on_submit (bool, optional):
            Remove suggestions on select. Defaults to False.
        key (str, optional):
            Streamlit session key. Defaults to "combobox".
        rerun_on_update (bool, optional):
            Rerun the search function after each search keystroke. Defaults to False.
        stop_on_update (bool, optional):
            Stop the streamlit script after each search keystroke. Defaults to False.
        blank_search_value (str, optional):
            Blank search value. If none, will not do an search if the box is blank/reset. Defaults to None.
        return_only_on_submit (bool, optional):
            Only return a value if the user has submitted a value. Defaults to False.

    Returns:
        any: based on user selection
    """

    # key without prefix used by react component
    key_react = f"{key}_react"

    if key not in st.session_state:
        st.session_state[key] = {
            # updated after each selection / reset
            "result": default,
            # updated after each search keystroke
            "search": "",
            # updated after each search_function run
            "options_js": [],
        }

        # if default options are given, set them
        if default_options:
            st.session_state[key]["options_js"] = _list_to_options_js(default_options)
            st.session_state[key]["options_py"] = _list_to_options_py(default_options)

        # if there is a blank search value specified, run that search
        if blank_search_value is not None:
            _process_search(
                search_function,
                key,
                blank_search_value,
                rerun_on_update,
                stop_on_update,
                blank_search_value,
            )

    # everything here is passed to react as this.props.args
    react_state = _get_react_component(
        options=st.session_state[key]["options_js"],
        clear_on_submit=clear_on_submit,
        placeholder=placeholder,
        label=label,
        # react return state within streamlit session_state
        key=key_react,
        **kwargs,
    )

    if react_state is None:
        return st.session_state[key]["result"]

    interaction, value = react_state["interaction"], react_state["value"]

    if interaction == "search":
        # triggers rerun, no ops afterwards executed
        _process_search(search_function, key, value, rerun_on_update, stop_on_update)

    if interaction == "submit":
        st.session_state[key]["result"] = (
            st.session_state[key]["options_py"][value]
            if "options_py" in st.session_state[key]
            else value
        )
        return st.session_state[key]["result"]

    if interaction == "reset":
        st.session_state[key] = {
            # updated after each selection / reset
            "result": default,
            # updated after each search keystroke
            "search": "",
            # updated after each search_function run
            "options_js": [],
        }

        # if default options are given, set them
        if default_options:
            st.session_state[key]["options_js"] = _list_to_options_js(default_options)
            st.session_state[key]["options_py"] = _list_to_options_py(default_options)

        if blank_search_value is not None:
            # reset default search if specified (must reload for this to actually show, hitting backspace again works)
            _process_search(
                search_function,
                key,
                blank_search_value,
                rerun_on_update,
                stop_on_update,
                blank_search_value,
            )
        if reset_function is not None:
            reset_function()

        return default

    # only return something real if there was a submit. If anything else happens, return nothing
    if return_only_on_submit:
        return None
    else:
        return st.session_state[key]["result"]
