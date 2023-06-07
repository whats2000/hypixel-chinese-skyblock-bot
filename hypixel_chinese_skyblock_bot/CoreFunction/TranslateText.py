import logging

import googletrans
from googletrans.models import Translated

from CoreFunction.Logger import Logger

bot_logger = Logger(__name__)


def translate_text(originals: str, targets: str, txt: str):
    t = googletrans.Translator()

    try:
        if originals is None:

            result = t.translate(
                txt,
                dest=targets
            )

        else:
            result = t.translate(
                txt,
                src=originals,
                dest=targets
            )
        bot_logger.log_message(logging.DEBUG, f'Translate > {txt} --> {result.text} ({targets})')

    except TypeError:
        bot_logger.log_message(logging.ERROR, 'Translator Fail')

        return Translated(src=None ,dest=targets, origin=originals, text=txt, parts=[], pronunciation=None)

    return result
