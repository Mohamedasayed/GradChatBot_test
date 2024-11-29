import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

# Load environment variables
load_dotenv()
google_api = st.secrets['GOOGLE_API_KEY']
google_api = os.getenv("GOOGLE_API_KEY")

# Check if Google API key is available
if google_api:
    genai.configure(api_key=google_api)
else:
    st.error("Google API key is not correct or found")

# Initialize session state for conversation history
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Define the tourism and museum-specific prompt with history


def get_prompt(user_input):
    # Build a history prompt from previous messages
    conversation = "\n".join(
        f"User: {entry['user']}\nBot: {entry['bot']}" for entry in st.session_state.conversation_history
    )
    # Add the current question to the conversation history
    return f"""
        if he ask in english:
        You are an expert travel guide and museum information assistant. 
        Answer user questions breifly  exclusively related to tourism, travel destinations, cultural sites, museums, 
        historical landmarks, art exhibitions, and travel tips. Provide detailed information on popular tourist spots, 
        museum exhibits, local history, cultural facts, and recommendations for travelers.
        
        If the user asks questions outside of tourism or museums, politely redirect them back to relevant topics 
        by saying, 'I’m here to assist you with questions about tourism, museums, and cultural sites.', also if he asking about anything related to ancient egyptian history pls reply breifly with details


        else if he ask in arabic 
        أنت مرشد سياحي خبير ومساعد معلومات المتاحف. أجب على أسئلة المستخدم بإيجاز تتعلق حصريًا بالسياحة، وجهات السفر، المواقع الثقافية، المتاحف، المعالم التاريخية، المعارض الفنية، ونصائح السفر. قدم معلومات مفصلة عن الأماكن السياحية الشهيرة، المعروضات في المتاحف، التاريخ المحلي، الحقائق الثقافية، والتوصيات للمسافرين.

إذا طرح المستخدم أسئلة خارج نطاق السياحة أو المتاحف، قم بتحويله بلطف إلى المواضيع ذات الصلة بقولك: "أنا هنا لمساعدتك في أسئلة حول السياحة والمتاحف والمواقع الثقافية."، وإذا كان يسأل عن أي شيء يتعلق بتاريخ مصر القديمة، يرجى الرد بإيجاز مع تفاصيل

        Conversation History:
        {conversation}

        Question: {user_input}
    """

# Function to generate text using Google Generative AI with the custom prompt


def generate_text(user_input):
    # Get the customized prompt with conversation history
    prompt = get_prompt(user_input)
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

# Function to display chat history in a conversation-style format


def display_chat_history():
    for entry in st.session_state.conversation_history:
        with st.chat_message("User"):
            st.write(entry["user"])
        with st.chat_message("Bot"):
            st.write(entry["bot"])


# Streamlit app UI
st.title("🏛️Tourism & Museum Chatbot")
url = "E:\Route assignment\wallpaperflare.com_wallpaper.jpg"
st.image(url)


# Display chat history
display_chat_history()

# Chat input box for new questions using st.chat_input
user_input = st.chat_input("Ask a question about tourism or museums:")

# Generate and display response when there is input
if user_input:
    response = generate_text(user_input)

    # Add the current question and response to the conversation history
    st.session_state.conversation_history.append(
        {"user": user_input, "bot": response})

    # Display new response immediately after user input
    with st.chat_message("User"):
        st.write(user_input)
    with st.chat_message("Bot"):
        st.write(response)
