import googletrans


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

    print(f'Info > 目標語言 -> {targets}')

    print(f'Info > 句子 -> {txt} >>> {result.text}')

    return result
