import os
import re
import sys

sys.path.insert(0, os.path.abspath("../.."))

import litellm


def test_no_nonexistent_litellm_vars_in_logging_docs() -> None:
    docs_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "docs",
        "my-website",
        "docs",
        "proxy",
        "logging.md",
    )
    try:
        with open(docs_path, encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Docs file not found at {docs_path}. Ensure BerriAI/litellm-docs is checked out at docs/my-website."
        )

    referenced = set(re.findall(r"litellm\.([a-z_]+message_logging\b)", content))
    nonexistent = {name for name in referenced if not hasattr(litellm, name)}
    assert not nonexistent, (
        f"The logging docs reference litellm attribute(s) that do not exist: {nonexistent}. "
        "Check docs/my-website/docs/proxy/logging.md for typos."
    )
