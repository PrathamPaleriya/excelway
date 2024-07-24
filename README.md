# ExcelWay 👩🏻‍💻

ExcelWay is a Streamlit application that allows users to interact with their Excel files using natural language. Powered by the Llama3 large language model and Groq API, ExcelWay simplifies data analysis and visualization by making Excel files easy to understand and manipulate through conversational AI.

## Application Link 🌐

Check out the live application: [ExcelWay](https://excelway.streamlit.app/)

## Usage 🚀

1. Upload your Excel file.
2. Select one of the two options: **Chat** or **Visualize**.
3. You can use any regional language to interact with the application.

## Features ✨

- **Natural Language Interaction**: Ask questions and get answers about your Excel data as if you were talking to a friend.
- **Data Visualization**: Generate visualizations based on your queries to better understand your data.
- **Multilingual Support**: Communicate in multiple languages and get responses tailored to your preferred language.
- **Intent Analysis**: Automatically detect if a question is analytical or personal and respond appropriately.

## Installation 💻

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/excelway.git
    cd excelway
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up environment variables by creating a `.env` file in the project root directory:
    ```env
    GROQ_API_KEY=your_groq_api_key
    ```

## Example 📊

Upload your Excel file, ask a question about the data, and get a response:

![image](https://github.com/user-attachments/assets/b99e2645-1997-4cac-84bb-fc3fd72bd60d)
![Screenshot 2024-07-24 062203](https://github.com/user-attachments/assets/6c26ea41-ad22-4b41-9150-a55cea2d23b7)
![Screenshot 2024-07-24 062246](https://github.com/user-attachments/assets/6aa40e92-ee31-4e01-ae34-24cd82b5546b)

## Project Structure 🗂️

- `app.py`: Main entry point for the Streamlit application.
- `core.py`: Core logic for interacting with the Excel file and the language model.
- `templates/`: Contains prompt templates for different tasks.
- `requirements.txt`: Python dependencies.

## How It Works ⚙️

1. **Model Initialization**: The `get_model` function initializes the Llama3 model using the Groq API.
2. **Excel Reading**: The `readExcel` function reads the uploaded Excel file into a Pandas DataFrame.
3. **Intent Analysis**: The `intend_prompt` template and the model determine if the user's question is analytical or personal.
4. **Response Generation**: Based on the intent, the application either processes the data with Pandas or generates a personalized response.

## Technologies Used 🛠️

- **Python**: Core programming language.
- **Pandas**: For data manipulation and analysis.
- **Streamlit**: For building the web application.
- **LangChain**: For creating pipelines and chains.
- **Groq API**: For accessing the Llama3 large language model.

## Contributing 🤝

Feel free to open issues or submit pull requests if you have any suggestions or improvements.

## Contact 📧

For any questions or feedback, please contact [paleriyapratham@gmail.com](mailto:paleriyapratham@gmail.com).
