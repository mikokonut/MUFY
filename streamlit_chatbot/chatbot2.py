import streamlit as st
from google import genai

# Configure Gemini API Client
GOOGLE_API_KEY = "AIzaSyAqLIZsviW4CitQWbbBnf2XL-NU8Ma2Spo"
client = genai.Client(api_key=GOOGLE_API_KEY)

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def get_gemini_response(prompt):
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    return response.text

def main():
    st.title("Gemini AI Chatbot")
    
    initialize_session_state()

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("Chat with Gemini"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.write(prompt)
        
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get Gemini response
        response = get_gemini_response(prompt)
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.write(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()