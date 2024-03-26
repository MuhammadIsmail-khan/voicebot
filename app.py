import streamlit as st
import speech_recognition as sr
from openai import OpenAI
import pyttsx3

api_key = "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"
client = OpenAI(api_key=api_key)

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Speak now...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        st.write("You said: " + text)
        return text
    except sr.UnknownValueError:
        st.write("Sorry, I couldn't understand audio")
    except sr.RequestError as e:
        st.write("Request failed; {0}".format(e))
    return None

def run_model(text):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are AI assistant help to get ANswers from given data"},
            {"role": "user", "content": make_prompt(text)}
        ]
    )
    return completion.choices[0].message.content

def convert_text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def make_prompt(text):
    return f"""
        You are AI Bot to answer question. It is crucial that you follow these guidelines for every question:
        - Your answer should be concise and to the point.
        - Answer should be less then 50 words
        Question:
        {text}
    """

def main():
    st.title("Voice Assistant")

    if st.button("Start Recording"):
        text = recognize_speech()
        if text:
            answer = run_model(text)
            st.write("AI Assistant says:")
            st.write(answer)
            convert_text_to_speech(answer)

if __name__ == "__main__":
    main()
