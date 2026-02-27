"""Tests for Challenge 2: ISO 26262 ASIL Decomposition Analyst."""
import pytest
from asil_analyst import get_decompositions, is_valid_decomposition, describe_decomposition


class TestGetDecompositions:
    def test_asil_d_has_three_options(self):
        result = get_decompositions("D")
        assert len(result) == 3

    def test_asil_d_contains_b_b(self):
        assert ("B", "B") in get_decompositions("D")

    def test_asil_d_contains_c_a(self):
        assert ("C", "A") in get_decompositions("D")

    def test_asil_d_contains_d_qm(self):
        assert ("D", "QM") in get_decompositions("D")

    def test_asil_c_has_two_options(self):
        assert len(get_decompositions("C")) == 2

    def test_asil_b_has_two_options(self):
        assert len(get_decompositions("B")) == 2

    def test_asil_a_has_one_option(self):
        assert len(get_decompositions("A")) == 1
        assert ("A", "QM") in get_decompositions("A")

    def test_asil_qm_has_no_decompositions(self):
        assert get_decompositions("QM") == []

    def test_case_insensitive(self):
        assert get_decompositions("d") == get_decompositions("D")

    def test_unknown_level_raises(self):
        with pytest.raises(ValueError):
            get_decompositions("X")


class TestIsValidDecomposition:
    def test_d_to_b_b_is_valid(self):
        assert is_valid_decomposition("D", "B", "B") is True

    def test_d_to_c_a_is_valid(self):
        assert is_valid_decomposition("D", "C", "A") is True

    def test_d_to_d_qm_is_valid(self):
        assert is_valid_decomposition("D", "D", "QM") is True

    def test_d_to_a_c_is_valid_symmetric(self):
        # Order should not matter
        assert is_valid_decomposition("D", "A", "C") is True

    def test_d_to_a_a_is_invalid(self):
        assert is_valid_decomposition("D", "A", "A") is False

    def test_c_to_b_a_is_valid(self):
        assert is_valid_decomposition("C", "B", "A") is True

    def test_c_to_a_a_is_invalid(self):
        assert is_valid_decomposition("C", "A", "A") is False

    def test_b_to_a_a_is_valid(self):
        assert is_valid_decomposition("B", "A", "A") is True

    def test_a_to_a_qm_is_valid(self):
        assert is_valid_decomposition("A", "A", "QM") is True

    def test_a_to_b_qm_is_invalid(self):
        assert is_valid_decomposition("A", "B", "QM") is False


class TestDescribeDecomposition:
    def test_describe_d_contains_all_options(self):
        desc = describe_decomposition("D")
        assert "ASIL D" in desc
        assert "B" in desc
        assert "QM" in desc

    def test_describe_qm_says_no_decomposition(self):
        desc = describe_decomposition("QM")
        assert "No decomposition possible" in desc
