"""
module for streamlit combobox component
"""
import functools
import logging
import os
from typing import Callable, List

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


def _process_search(
    search_function: Callable[[str], List[any]],
    key: str,
    searchterm: str,
    rerun_on_update: str
) -> bool:
    # nothing changed, avoid new search
    if searchterm == st.session_state[key]["search"]:
        return st.session_state[key]["result"]

    st.session_state[key]["search"] = searchterm
    search_results = search_function(searchterm)

    if search_results is None:
        search_results = []

    def _get_label(label: any) -> str:
        return str(label[0]) if isinstance(label, tuple) else str(label)

    def _get_value(value: any) -> any:
        return value[1] if isinstance(value, tuple) else value

    # used for react component
    st.session_state[key]["options"] = [
        {
            "label": _get_label(v),
            "value": i,
        }
        for i, v in enumerate(search_results)
    ]

    # used for proper return types
    st.session_state[key]["options_real_type"] = [_get_value(v) for v in search_results]

    if rerun_on_update:
        st.experimental_rerun()


@wrap_inactive_session
def st_combobox(
    search_function: Callable[[str], List[any]],
    placeholder: str = "Search ...",
    label: str = None,
    default: any = None,
    clear_on_submit: bool = False,
    key: str = "combobox",
    rerun_on_update: bool = True,
    blank_search_value: str = None,
    return_only_on_submit: bool = False,
    **kwargs,
) -> any:
    """
    Create a new combobox instance, that provides suggestions based on the user input
    and returns a selected option or empty string if nothing was selected

    Args:
        search_function (Callable[[str], List[any]]):
            Function that is called to fetch new suggestions after user input.
        placeholder (str, optional):
            Label shown in the combobox. Defaults to "Search ...".
        label (str, optional):
            Label shown above the combobox. Defaults to None.
        default (any, optional):
            Return value if nothing is selected so far. Defaults to None.
        clear_on_submit (bool, optional):
            Remove suggestions on select. Defaults to False.
        key (str, optional):
            Streamlit session key. Defaults to "combobox".
        rerun_on_update (bool, optional):
            Rerun the search function on each keystroke. Defaults to True.
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
            "options": [],
        }

        # load stuff the first run if called for
        if blank_search_value is not None:
            print("-initial population of box")
            _process_search(search_function, key, blank_search_value, rerun_on_update)

    # everything here is passed to react as this.props.args
    react_state = _get_react_component(
        options=st.session_state[key]["options"],
        clear_on_submit=clear_on_submit,
        placeholder=placeholder,
        label=label,
        # react return state within streamlit session_state
        key=key_react,
        **kwargs,
    )

    if react_state is None:
        print("-react_state is None! Returning",st.session_state[key]["result"])
        return st.session_state[key]["result"]

    interaction, value = react_state["interaction"], react_state["value"]

    print("\n-interaction", interaction, "value", value)

    if interaction == "search":
        print("-Search happening")
        # triggers rerun, no ops afterwards executed
        _process_search(search_function, key, value, rerun_on_update)

    if interaction == "submit":
        st.session_state[key]["result"] = (
            st.session_state[key]["options_real_type"][value]
            if "options_real_type" in st.session_state[key]
            else value
        )
        print("-submit happening!!!!", st.session_state[key]["result"])
        return st.session_state[key]["result"]

    if interaction == "reset":
        print("-reset triggered:",default)
        st.session_state[key] = {
            # updated after each selection / reset
            "result": default,
            # updated after each search keystroke
            "search": "",
            # updated after each search_function run
            "options": [],
        }

        if blank_search_value is not None:
            print("-reset population")
            _process_search(search_function, key, blank_search_value, rerun_on_update)
            # reload box on reset
            st.experimental_rerun()

        return default

    # only return something real if there was a submit. If anything else happens, return nothing
    if return_only_on_submit:
        print("-no interaction",None)
        return None
    else:
        print("-no interaction",st.session_state[key]["result"])
        return st.session_state[key]["result"]

