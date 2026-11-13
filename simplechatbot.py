import os
import getpass

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI                       
import streamlit as st   
st.title("Karnika's Show Chat Bot")                                                 
input_txt=st.text_input("Please enter your queries here...")  
os.environ["GOOGLE_API_KEY"] = getpass.getpass(
    "Enter your Gemini API key: "
)
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7
)
  
prompt=ChatPromptTemplate.from_messages(                                                  
    [("system","you are a helpful AI assistant.Your name is karnika's Assistant"),
     ("user","user query:{query}")     
    ])                     
output_parser = StrOutputParser()

chain = prompt | llm | output_parser
while True:
    input_txt = input("Enter your query (type exit to stop): ")

    if input_txt.lower() == "exit":
        print("Chatbot stopped.")
        break

    response = chain.invoke({"query": input_txt})

    print("\nKarnika's Assistant:", response)