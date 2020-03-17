import os
import re
from docutils import nodes


def setup(app):
    app.add_config_value('is_i18n', None, 'env')
    app.add_role("api", role_api)


def role_api(name, rawtext, text, lineno, inliner, options={}, content=[]):
    """
    Converts ":api:`class_SomeClass`" or ":api:`SomeClass <class_SomeClass>`"
    to ":ref:`class_SomeClass`" for non-i18n docs and ":ref:`api:class_SomeClass`"
    otherwise (the `api` cross-reference is defined by Intersphinx).

    See https://docutils.sourceforge.io/docs/howto/rst-roles.html
    rawtext: ":api:`SomeClass <class_SomeClass>`" or ":api:`class_SomeClass`"
    text: "SomeClass <class_SomeClass>" or "class_SomeClass"
    """
    match = re.search("([^<]*)?<?([^>]*)?>?", text)
    if match is None or len(match.groups()) != 2:
        raise ValueError
    ref = match.group(2 if "<" in text else 1)

    crossref = "api:" if inliner.document.settings.env.app.config.is_i18n else ""
    ref = f":ref:`{crossref}{ref}`"

    node = nodes.reference(rawtext, text, refuri=ref, **options)

    return [node], []
