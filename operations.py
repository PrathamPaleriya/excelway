import pandas as pd
import os
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import pandas as pd
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import logging
from dotenv import load_dotenv
import streamlit as st


def get_model(api_key):
    model = ChatGroq(
        temperature=0,
        model="llama3-70b-8192",
        api_key=api_key
    )

    return model

def readExcel(file):
    df = pd.read_excel(file)
    return df


intend_template = """Analyze the user question: "{question}" and determine the intent.

If the intent is analytical (related to data analysis, calculations, or insights based on uploaded Excel files with first few rows ad {context}), respond with '1'.

If the intent is personal (related to personal information, preferences, or general inquiries), respond with a tailored message based on the nature of the question as follows:

1. For questions about capabilities or identity (e.g., "What can you do?", "Who are you?", "What can you do for me?" or "What's up"), respond in {language} with:
   "Hello, my name is Excel Genie. My role is to assist you with your Excel file. You can ask me questions about the data, and I can perform calculations and visualize it for you."

2. For specific personal questions such as "What's the weather?" or other general inquiries not related to the Excel file, respond in {language} with:
   "I'm not equipped to provide information about that. Please ask questions related to your Excel file, and I'll be happy to assist."

3. For other types of personal questions, provide a contextually appropriate response in {language}, indicating that you specialize in Excel file-related queries.

Only respond with '1' or the tailored personal message and do not provide any extra information. Just the response.

"""

translate_template = """
    Translate the following sentence: "{sentence}" into {language}.

    Provide only the translated text without any additional information.
    """

# intent chain 
intend_prompt = ChatPromptTemplate.from_template(intend_template)



# translation chain
translate_prompt = ChatPromptTemplate.from_template(translate_template)



# _________ visual search
pandas_visualization_template = """
    Translate the following question into a Pandas query "{question}".

    The query should be based on a dataframe named 'df' with columns named {context}. Ensure that only the columns present in the dataframe are used in the query. Enclose the query in $$ and provide only the Pandas query without any additional information.

    Additionally, suggest the type of chart to create (e.g., bar, pie, line) based on the query. 

    Format: && query && chart type && chart short explanation && chart title &&
"""
pandas_prompt_visual = ChatPromptTemplate.from_template(pandas_visualization_template)




json_analysis_template = """Analyze the JSON context: {context} and provide a concise insight in {language}.

Provide insights such as trends, key points, anomalies, or summaries that are relevant to the context.

Only provide the concise insight and do not include any additional information. Just the insight.
"""

json_analysis_prompt = ChatPromptTemplate.from_template(json_analysis_template)



def chat(file, question, language='English', api_key=None):

    intend_chain = intend_prompt | model | StrOutputParser()
    translate_chain = translate_prompt | model | StrOutputParser()
    

    try:
        df = pd.read_excel(file)
    except Exception as e:
        return {"error": f"Failed to read file: {str(e)}"}
    
    model = get_model(api_key)

    try:
        intend = intend_chain.invoke({"question": question, "context": df.head(10), "language": language})

        if intend == "1":
            agent = create_pandas_dataframe_agent(
                llm=model,
                df=readExcel(file=file),
                verbose=False,
                allow_dangerous_code=True,
            )

            agent_response = agent.invoke(question)
            answer = agent_response["output"]

            if language != "English":
                answer = translate_chain({"sentence": answer, "language": language})

        else:
            answer = intend

        response = {
            "question": question,
            "answer": answer
        }

        return response

    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

def visualChat(file, question, language ="English",  api_key=None):

    pandas_query_visual_chain = pandas_prompt_visual | model | StrOutputParser()

    json_analysis_chain = json_analysis_prompt | model | StrOutputParser()

    intend_chain = intend_prompt | model | StrOutputParser()
    translate_chain = translate_prompt | model | StrOutputParser()

    try:
        df = pd.read_excel(file)
    except Exception as e:
        return {"error": f"Failed to read file: {str(e)}"}
    
    model = get_model(api_key)

    try:
        intend = intend_chain.invoke({"question": question, "context" : df.head(10), "language": language})

        if intend == "1":
            
            response = pandas_query_visual_chain.invoke({"question": question, "context": df.head(10)})

            response = response.split("&&")

            exe_query = response[1].strip()
            chart_type = response[2].strip()
            title = response[3].strip()

            data = eval(exe_query)

            summary = json_analysis_chain.invoke({"context": data, "language": language})

            response = {
                "data": data,
                "title": title,
                "chart_type": chart_type,
                "summary": summary
            }

            return response

        else:
            answer = intend
            response = {
                "question": question,
                "answer": answer
            }

            return response
        
    except Exception as e:
        return {"error": f"An error occurred: {str(e)}"}

    




if __name__ == "__main__":
    question = input("Enter you question >> ")
    # print(chat(file = "Historical_data.xlsx", question= question))
    # print(visualChat(file = "Historical_data.xlsx", question=question))