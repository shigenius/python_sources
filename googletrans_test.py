from googletrans import Translator
translator = Translator()
translated = translator.translate('a man riding a wave on top of a surfboard .', dest='ja')
print(translated.text)
