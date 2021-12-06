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

    print('目標語言 -> '
          + str(targets)
          )

    print('句子 -> '
          + str(input)
          + ' >>> '
          + str(result.text)
          )

    return result
