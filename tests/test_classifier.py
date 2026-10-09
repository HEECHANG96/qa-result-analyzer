
import pytest

from analyzer.classifier import classify_failure


@pytest.mark.parametrize(
    "error_message, expected",
    [
        ("AssertionError: assert False", "ASSERTION"),
        ("TimeoutError: Locator.click failed", "TIMEOUT"),
        ("ConnectionError: Connection refused", "NETWORK"),
        ("Unknown exception", "UNKNOWN"),
        ("", "UNKNOWN"),
    ],
)
def test_classify_failure(error_message, expected):
    assert classify_failure(error_message) == expected
