import googletrans


def translate_text(originlang, targetlang, txt):

    t = googletrans.Translator()

    if originlang is None:

        result = t.translate(
            txt,
            dest=targetlang
        )

    else:

        result = t.translate(
            txt,
            src=originlang,
            dest=targetlang
        )

    print('目標語言 -> '
          + str(targetlang)
          )

    print('句子 -> '
          + str(input)
          + ' >>> '
          + str(result.text)
          )

    return result
