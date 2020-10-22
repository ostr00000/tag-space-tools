import logging
import sys
from pathlib import Path

from tag_space_tools.core.fix_tagspace import TagSpaceSearch

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.DEBUG)

    if len(sys.argv) >= 2:
        loc = Path(sys.argv[1])
    else:
        loc = Path().absolute().parent.parent / 'test'

    logger.debug(f"search path: '{loc}'")
    tss = TagSpaceSearch(loc)
    tss.match()
