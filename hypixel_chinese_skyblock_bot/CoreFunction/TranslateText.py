import logging

import googletrans

from CoreFunction.Logger import Logger

bot_logger = Logger(__name__)


def translate_text(originals: str, targets: str, txt: str):
    t = googletrans.Translator()

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
    bot_logger.log_message(logging.INFO, f'Translate > {txt} --> {result.text} ({targets})')

    return result
