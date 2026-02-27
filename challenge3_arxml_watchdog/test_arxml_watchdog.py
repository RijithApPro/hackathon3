"""Tests for Challenge 3: ARXML Watchdog Boilerplate."""
import xml.etree.ElementTree as ET
from pathlib import Path
import pytest
from arxml_utils import load_arxml, get_component_names, get_runnables

ARXML_PATH = Path(__file__).parent / "watchdog.arxml"


@pytest.fixture(scope="module")
def root():
    return load_arxml(ARXML_PATH)


def test_arxml_is_valid_xml():
    """The boilerplate ARXML must be well-formed XML."""
    ET.parse(str(ARXML_PATH))  # raises if malformed


def test_autosar_root_tag(root):
    assert "AUTOSAR" in root.tag


def test_wdgm_component_present(root):
    names = get_component_names(root)
    assert "WdgM_Component" in names


def test_app_component_present(root):
    names = get_component_names(root)
    assert "App_Component" in names


def test_composition_present(root):
    names = get_component_names(root)
    assert "WdgM_App_Composition" in names


def test_wdgm_main_function_runnable(root):
    runnables = get_runnables(root)
    assert "WdgM_MainFunction" in runnables


def test_wdgm_init_runnable(root):
    runnables = get_runnables(root)
    assert "WdgM_Init" in runnables


def test_app_main_function_runnable(root):
    runnables = get_runnables(root)
    assert "App_MainFunction" in runnables
