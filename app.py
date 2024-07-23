import streamlit as st
import pandas as pd
from operations import chat, visualChat

groq_api_key = st.secrets["general"]["GROQ_API_KEY"]


def display_chat_history(messages):
    for message in messages:
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        else:
            st.markdown(f"**Bot:** {message['content']}")

def upload_page():
    st.title("ExcelWay")
    st.divider()
    st.subheader("Upload a Excel file to Continue")

    uploaded_file = st.file_uploader("", type=["xlsx", "xls"])

    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        st.write("File uploaded successfully.")
        st.dataframe(df.head())

        if st.button("Proceed"):
            st.session_state.uploaded_file = uploaded_file
            st.session_state.messages = []
            st.experimental_rerun()
def chat_page():
    st.title('Chat with your Excel')

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    uploaded_file = st.session_state.uploaded_file

    language_options = ["English", "Hindi", "Marathi", "Gujrati", "Other"]
    selected_language = st.selectbox("Select Language", language_options)

    if selected_language == "Other":
        selected_language = st.text_input("Enter your language")

    user_input = st.text_input("You:", "")
    if st.button("Send"):
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})

            response = chat(uploaded_file, user_input, language=selected_language, api_key=groq_api_key)

            if "error" in response:
                st.subheader(f"**Bot:** {response['error']}",divider="red")
            else:
                st.subheader(f"**Bot:** {response['answer']}", divider="rainbow")

def visualize_page():
    st.title('Visualization')

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    uploaded_file = st.session_state.uploaded_file

    language_options = ["English", "Hindi", "Marathi", "Gujrati", "Other"]
    selected_language = st.selectbox("Select Language", language_options)

    if selected_language == "Other":
        selected_language = st.text_input("Enter your language")

    user_input = st.text_input("You:", "")
    if st.button("Send"):
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})

            response = visualChat(uploaded_file, user_input, language=selected_language, api_key=groq_api_key)

            if "error" in response:
                st.session_state.messages.append({"role": "bot", "content": response["error"]})
            else:
                if "data" in response and "chart_type" in response and "title" in response and "summary" in response:
                    data = response["data"]
                    chart_type = response["chart_type"]
                    title = response["title"]
                    summary = response["summary"]

                    st.session_state.messages.append({"role": "bot", "content": f"**Chart Type:** {chart_type}\n**Chart Title:** {title}\n**Summary:** {summary}"})

                    st.markdown(f"### {title}")
                    if chart_type.lower() == "bar":
                        st.bar_chart(data)
                    elif chart_type.lower() == "line":
                        st.line_chart(data)
                    elif chart_type.lower() == "pie":
                        st.write("Pie charts are not directly supported by Streamlit. Here is the data for the pie chart:")
                        st.write(data)
                    else:
                        st.table(data)
                    st.subheader(f"**Summary:** :blue[{summary}]")
                elif "question" in response and "answer" in response:
                    st.session_state.messages.append({"role": "bot", "content": response["answer"]})

    # display_chat_history(st.session_state.messages)


def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Upload and Choose Function", "Chat", "Visualize"])

    if page == "Upload and Choose Function":
        upload_page()
    elif page == "Chat":
        if 'uploaded_file' not in st.session_state:
            st.warning("Please upload a file and select 'Chat' on the previous page.")
        else:
            chat_page()
    elif page == "Visualize":
        if 'uploaded_file' not in st.session_state:
            st.warning("Please upload a file and select 'Visualize' on the previous page.")
        else:
            visualize_page()

if __name__ == "__main__":
    main()
