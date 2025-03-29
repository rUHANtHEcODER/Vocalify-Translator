import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import io
import textwrap
import speech_recognition as sr

# Language dictionary
languages = {
    "Afrikaans": "af",
    "Albanian": "sq",
    "Amharic": "am",
    "Arabic": "ar",
    "Basque": "eu",
    "Bengali": "bn",
    "Bosnian": "bs",
    "Bulgarian": "bg",
    "Catalan": "ca",
    "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW",
    "Croatian": "hr",
    "Czech": "cs",
    "Danish": "da",
    "Dutch": "nl",
    "English": "en",
    "Estonian": "et",
    "Filipino": "tl",
    "Finnish": "fi",
    "French": "fr",
    "Galician": "gl",
    "German": "de",
    "Greek": "el",
    "Gujarati": "gu",
    "Hausa": "ha",
    "Hebrew": "iw",
    "Hindi": "hi",
    "Hungarian": "hu",
    "Icelandic": "is",
    "Indonesian": "id",
    "Italian": "it",
    "Japanese": "ja",
    "Javanese": "jv",
    "Kannada": "kn",
    "Khmer": "km",
    "Korean": "ko",
    "Latin": "la",
    "Latvian": "lv",
    "Lithuanian": "lt",
    "Malay": "ms",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Nepali": "ne",
    "Norwegian": "no",
    "Polish": "pl",
    "Portuguese": "pt",
    "Punjabi": "pa",
    "Romanian": "ro",
    "Russian": "ru",
    "Serbian": "sr",
    "Sinhala": "si",
    "Slovak": "sk",
    "Spanish": "es",
    "Sundanese": "su",
    "Swahili": "sw",
    "Swedish": "sv",
    "Tamil": "ta",
    "Telugu": "te",
    "Thai": "th",
    "Turkish": "tr",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Vietnamese": "vi",
    "Welsh": "cy"
}


# Function to translate long text in chunks
def translate_large_text(text, source, target, chunk_size=50):
    chunks = textwrap.wrap(text,
                           width=chunk_size)  # Break text into smaller chunks
    translated_chunks = [
        GoogleTranslator(source=source, target=target).translate(chunk)
        for chunk in chunks
    ]
    return " ".join(translated_chunks)  # Combine translated parts


# UI Header
st.markdown(
    "<h1 style='text-align: left; color: #4194cb;'>🎙️Vocalify: Next Generation of Translation</h1>",
    unsafe_allow_html=True)

tabs = ["Text-to-Speech", "Text-to-Text", "Speech-to-Speech", "Speech-to-Text"]
tab = st.sidebar.selectbox("Select a tab", tabs)

if tab == "Text-to-Speech":
    st.markdown("**Text-to-Speech**")
    st.caption("Enter your language & text below")

    input_text = st.text_area("Enter your text here")

    language_from = st.selectbox("Select or type a language",
                                 options=list(languages.keys()),
                                 index=0)
    language_to = st.selectbox("Select or type a language",
                               options=list(languages.keys()),
                               index=1)

    if st.button(f"🎤 Speak in {language_to}"):
        translated_text = translate_large_text(input_text,
                                               languages[language_from],
                                               languages[language_to])

        language_code_to = languages[language_to]
        tts = gTTS(text=translated_text, lang=language_code_to, slow=False)
        audio = io.BytesIO()
        tts.write_to_fp(audio)
        audio.seek(0)

        st.write(
            f"Translated Text: {translated_text}")  # Display translated text
        st.audio(audio, format="audio/mp3")  # Play audio

elif tab == "Text-to-Text":
    st.markdown("**Text-to-Text**")
    st.caption("Enter your language & text below")

    input_text = st.text_area("Enter your text here")

    language_from = st.selectbox("Select or type a language",
                                 options=list(languages.keys()),
                                 index=0)
    language_to = st.selectbox("Select or type a language",
                               options=list(languages.keys()),
                               index=1)

    if st.button(f"㊗️ Translate to {language_to}"):
        translated_text = translate_large_text(input_text,
                                               languages[language_from],
                                               languages[language_to])
        st.write(f"Translated Text: {translated_text}")
elif tab == "Speech-to-Speech":
  st.markdown("**Speech-to-Speech**")
  st.caption("Record your message and translate it to another language.")

  input_audio = st.audio_input("Record your message")

  language_from = st.selectbox("Select input language", options=list(languages.keys()))
  language_to = st.selectbox("Select output language", options=list(languages.keys()))

  if st.button(f"💬 Translate to {language_to}"):
      audio_bytes = io.BytesIO(input_audio.read())  # Read recorded audio into BytesIO

      recognizer = sr.Recognizer()
      
      try:
          with sr.AudioFile(audio_bytes) as source:
              audio = recognizer.record(source)

          # Convert Speech to Text
          recognized_text = recognizer.recognize_google(audio, language=languages[language_from])
          

          # Translate the text
          translated_text = translate_large_text(recognized_text, languages[language_from], languages[language_to])

          # Convert Translated Text to Speech
          tts = gTTS(text=translated_text, lang=languages[language_to], slow=False)
          audio_output = io.BytesIO()
          tts.write_to_fp(audio_output)
          audio_output.seek(0)

          # Play Translated Speech
          st.audio(audio_output, format="audio/mp3")

      except sr.UnknownValueError:
          st.warning("Speech Recognition could not understand the audio.")
      except sr.RequestError as e:
          st.warning(f"Could not process results due to {e}")
elif tab == "Speech-to-Text":
  st.markdown("**Speech-to-Text**")
  st.caption("Record your message and translate it to another language.")

  input_audio = st.audio_input("Record your message")

  language_from = st.selectbox("Select input language", options=list(languages.keys()))
  language_to = st.selectbox("Select output language", options=list(languages.keys()))

  if st.button(f"🉐 Translate to {language_to}"):
      audio_bytes = io.BytesIO(input_audio.read())  # Read recorded audio into BytesIO

      recognizer = sr.Recognizer()
      
      try:
          with sr.AudioFile(audio_bytes) as source:
              audio = recognizer.record(source)

          # Convert Speech to Text
          recognized_text = recognizer.recognize_google(audio, language=languages[language_from])
          

          # Translate the text
          translated_text = translate_large_text(recognized_text, languages[language_from], languages[language_to])

          # Convert Translated Text to Speech
          tts = gTTS(text=translated_text, lang=languages[language_to], slow=False)
          audio_output = io.BytesIO()
          tts.write_to_fp(audio_output)
          audio_output.seek(0)

          # Play Translated Speech
          st.write(f"Translated Text: {translated_text}")

      except sr.UnknownValueError:
          st.warning("Speech Recognition could not understand the audio.")
      except sr.RequestError as e:
          st.warning(f"Could not process results due to {e}")