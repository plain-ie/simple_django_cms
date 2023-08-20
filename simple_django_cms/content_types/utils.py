from typing import List


def get_translated_content(
    translatable_contents: List[dict],
    language: str,
    default_language: str,
) -> dict:

    _content = None
    _default_content = None

    for translatable_content in translatable_contents:

        if translatable_content['language'] == language:
            _content = translatable_content

        if translatable_content['language'] == default_language:
            _default_content = translatable_content

    if language == default_language:
        return _default_content

    if _content is not None:
        return _content

    return _default_content
