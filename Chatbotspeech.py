import streamlit as st
import speech_recognition as sr
from nltk.chat.util import Chat, reflections
import os

# Chatbot data
data = [
    [r"(.*hi|.*hello|.*hey)", ["Hello! How can I assist you today?", "Hi there! What can I help with?"]],
    [r"(.*name)", ["My name is Oluwaseun.", "I am Oluwaseun, your chatbot."]],
    [r"(.*age|.*old)", ["I am 23 years old."]],
    [r"(.*language)", ["I speak English and Yoruba."]],
    [r"(.*sports)", ["I enjoy football and basketball."]],
    [r"(.*hobbies)", ["I like taking walks and listening to music."]],
    [r"(.*work)", ["I am currently learning Data Science."]],
    [r"(.*skills)", ["I am average in Python and decent in SQL."]],
    [r"(.*expertise)", ["I am focusing on machine learning."]],
    [r"(.*food)", ["I love eating meat."]],
    [r"(.*pets|.*pet)", ["I do not have any pets."]],
    [r"(.*goals)", ["I aim to create models that solve real-world problems."]],
    [r"(.*books|.*reading)", ["I enjoy reading sci-fi and fantasy books."]],
    [r"(.*music)", ["I am a big fan of R&B music."]],
    [r"(.*data science|.*what is data science)", ["Data science uses scientific methods to extract insights from data."]],
    [r"(.*machine learning|.*ML|.*what is machine learning)", ["Machine learning enables computers to learn from data without explicit programming."]],
    [r"(.*artificial intelligence|.*AI|.*what is AI)", ["AI is the simulation of human intelligence by machines."]],
    [r"(.*big data|.*what is big data)", ["Big data refers to large datasets analyzed for patterns and trends."]],
    [r"(.*exit|.*bye)", ["Goodbye! Have a great day!"]],
]

chatbot = Chat(data, reflections)

# Speech recognition function
def transcribe_speech(api_choice, language_choice):
    r = sr.Recognizer()
    st.info("Recording... Speak now.")

    # Use microphone to record audio
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio_text = r.listen(source)
            st.info("Processing the audio...")
            # Transcribe the speech
            if api_choice == "Google Speech Recognition":
                text = r.recognize_google(audio_text, language=language_choice)
            elif api_choice == "Sphinx":
                text = r.recognize_sphinx(audio_text, language=language_choice)
            else:
                text = "Unsupported API"
            return text
    except Exception as e:
        return f"An error occurred: {e}"

# Main Streamlit app
def main():
    st.title("Speech-Enabled Chatbot")
    st.write("Click the button to speak to the chatbot. Say 'exit' to end the conversation.")

    # Display chatbot conversation
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # Button to trigger speech recognition
    if st.button("Start Talking"):
        user_input = transcribe_speech("Google Speech Recognition", "en-US")
        if user_input:
            st.session_state["chat_history"].append(f"You: {user_input}")
            if user_input.lower() == "exit":
                st.session_state["chat_history"].append("Chatbot: Goodbye!")
            else:
                response = chatbot.respond(user_input)
                if response:
                    st.session_state["chat_history"].append(f"Chatbot: {response}")
                else:
                    st.session_state["chat_history"].append("Chatbot: I couldn't understand that. Please rephrase.")

    # Display chat history
    for line in st.session_state["chat_history"]:
        st.write(line)

if __name__ == "__main__":
    main()

