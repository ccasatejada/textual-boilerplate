from __future__ import annotations

from pathlib import PurePath
from typing import ClassVar

from textual.app import App


class MainApp(App[None]):
    theme: str = "textual-light"
    CSS_PATH: ClassVar[str | PurePath | list[str | PurePath] | None] = []


if __name__ == "__main__":
    MainApp().run()
