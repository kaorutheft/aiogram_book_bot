import os
import logging

logger = logging.getLogger(__name__)


def _ger_part_text(path: str, start: int, size: int) -> tuple[str, int]:
