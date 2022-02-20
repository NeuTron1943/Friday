from gtts import gTTS
import os

text = "Здарова"

language = 'ru'

narrator = gTTS(text=text, lang=language, slow=False)

narrator.save('content/audio/tmp/voicelinetest.mp3')
os.system("mpg321 content/audio/tmp/voicelinetest.mp3")