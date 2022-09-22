import logging

import googletrans

from hypixel_chinese_skyblock_bot.Core.Logger import Logger


def translate_text(originals, targets, txt):

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
    bot_logger = Logger(__name__)

    bot_logger.log_message(logging.INFO, f'Translate > {txt} --> {result.text} ({targets})')

    return result
