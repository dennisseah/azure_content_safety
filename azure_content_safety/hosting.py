"""Defines our top level DI container.
Utilizes the Lagom library for dependency injection, see more at:

- https://lagom-di.readthedocs.io/en/latest/
- https://github.com/meadsteve/lagom
"""

import logging

from dotenv import load_dotenv
from lagom import Container, dependency_definition

from azure_content_safety.protocols.i_content_safety import IContentSafety

load_dotenv(dotenv_path=".env")


container = Container()
"""The top level DI container for our application."""


# Register our dependencies ------------------------------------------------------------


@dependency_definition(container, singleton=True)
def _() -> logging.Logger:
    return logging.getLogger("studio_board")


@dependency_definition(container, singleton=True)
def _(c: Container) -> IContentSafety:
    from azure_content_safety.services.content_safety import ContentSafety

    return c[ContentSafety]
