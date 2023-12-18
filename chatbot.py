from flask import Flask, render_template, request, Blueprint
import openai
import time
import pdfplumber
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("api_key")

# Initialize the OpenAI client
client = openai.Client(api_key=api_key)

chatbot_app = Blueprint('chatbot', __name__)

@chatbot_app.route('/', methods=['GET', 'POST'])
def assistant_chatbot():
    if request.method == 'POST':
        file = request.files.get('file')  # Get the file if it's uploaded
        user_query = request.form['query']

        pdf_text = ""
        if file:  # Check if the user uploaded a file
            # Read the PDF content
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    pdf_text += page.extract_text()

        # Create a new thread
        thread = client.beta.threads.create()

        # Create a message from the user
        # Combine user query and PDF content if PDF is uploaded
        content = user_query + "\n" + pdf_text if pdf_text else user_query
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=content,
        )

        # Create a run
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id="asst_6o7w7E8I6m0cVfM3zFzePcb9",  # Assuming you have an assistant object
            instructions="you are a helpful assistant if the user asks you a normal question, then give a normal answer. If the user asks according to the file, then give an answer from the file.",
        )

        # Wait for the run to complete
        while not run.completed_at:
            time.sleep(5)
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

        # Retrieve and display the assistant's response
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        last_message = messages.data[0]
        response = last_message.content[0].text.value
        return render_template('chatbot.html', response=response)

    return render_template('chatbot.html')





# import streamlit as st
# from bot import supertec_bot
#
#
# didx_chatbot = supertec_bot()
#
# st.title("SuperTech Bot")
# user_input = st.text_input('How can I help you?')
# with st.spinner('Sit back and relax.'):
#     if st.button('Ask'):
#         if user_input:
#             answer = didx_chatbot.user_chat(user_input)
#             st.write(answer)





# -*- coding: utf-8 -*-
# """cv reader.ipynb
#
# Automatically generated by Colaboratory.
#
# Original file is located at
#     https://colab.research.google.com/drive/10wL6gfx7JQPZD4RWscyeKxyc211cZ9Co
# """

# import openai
# import time
#
# api_key = "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"  # Replace with your actual API key
# client = openai.Client(api_key=api_key)
#
#
# file_loc =input("Enter file location")
#
# # Upload a file with an "assistants" purpose
# file = client.files.create(
#   file=open(file_loc, "rb"),
#   purpose='assistants'
# )
#
# print(file.id)
#
# # assistant = client.beta.assistants.create(
# #     name="Thread Level Assistant",
# #     instructions="You are a helpful analyst.You help people to thier queries",
# #     tools=[{"type": "retrieval"}],
# #     model="gpt-4-1106-preview",
# #     # file_ids=[file.id]
# # )
#
# thread = client.beta.threads.create()
#
# message = "How many MCQs in this file?"
#
# message = client.beta.threads.messages.create(
#     thread_id=thread.id,
#     role="user",
#     content=message,
#     file_ids=[file.id]
# )
#
# run = client.beta.threads.runs.create(
#     thread_id = thread.id,
#     assistant_id = "asst_6o7w7E8I6m0cVfM3zFzePcb9",
#     instructions = "Please address the user queries based upon the document."
# )
#
# def wait_for_run_completion(client, thread_id, run_id, sleep_interval=5):
#     """
#     Waits for a run to complete and prints the elapsed time.:param client: The OpenAI client object.
#     :param thread_id: The ID of the thread.
#     :param run_id: The ID of the run.
#     :param sleep_interval: Time in seconds to wait between checks.
#     """
#     while True:
#         try:
#             run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
#             if run.completed_at:
#                 elapsed_time = run.completed_at - run.created_at
#                 formatted_elapsed_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
#                 print(f"Run completed in {formatted_elapsed_time}")
#                 break
#         except Exception as e:
#             print(f"An error occurred while retrieving the run: {e}")
#             break
#         print("Waiting for run to complete...")
#         time.sleep(sleep_interval)
#
#
# wait_for_run_completion(client, thread.id, run.id)
#
# messages = client.beta.threads.messages.list(
#     thread_id=thread.id
#     )
#
# last_message = messages.data[0]
# response = last_message.content[0].text.value
# print(response)

# import streamlit as st
# import openai
# import time
#
# # Set your OpenAI API key
# api_key = "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"  # Replace with your actual API key
# client = openai.Client(api_key=api_key)
#
# # Streamlit UI
# st.title("Assistant Chatbot")
#
# # Upload a file with an "assistants" purpose
# file = st.file_uploader("Upload a PDF file", type=["pdf"])
#
# if file is not None:
#     st.write("File uploaded successfully!")
#
#     # User input
#     user_query = st.text_input("Enter Your Query", "")
#
#     if st.button("Submit Query"):
#         try:
#             # Create a new thread
#             thread = client.beta.threads.create()
#
#             # Create a file using OpenAI's client
#             openai_file = client.files.create(
#                 file=file,
#                 purpose='assistants',
#             )
#
#             # Check if the file was created successfully
#             if not openai_file:
#                 st.write("Error in file creation. Please try again.")
#                 raise Exception("File creation failed")
#
#             # Create a message from the user with the uploaded file
#             message = client.beta.threads.messages.create(
#                 thread_id=thread.id,
#                 role="user",
#                 content=user_query,
#                 file_ids=[openai_file.id],  # Include the file ID in the message
#             )
#
#             if not message:
#                 st.write("Error in message creation. Please try again.")
#                 raise Exception("Message creation failed")
#
#             # Create a run
#             run = client.beta.threads.runs.create(
#                 thread_id=thread.id,
#                 assistant_id="asst_6o7w7E8I6m0cVfM3zFzePcb9",
#                 instructions="Please address the user queries based on the document.",
#             )
#
#             if not run:
#                 st.write("Error in creating the run. Please try again.")
#                 raise Exception("Run creation failed")
#
#             # Wait for the run to complete
#             while not run.completed_at:
#                 st.write("Waiting for the assistant's response...")
#                 time.sleep(5)
#                 run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
#
#             # Retrieve and display the assistant's response
#             messages = client.beta.threads.messages.list(thread_id=thread.id)
#             if messages and messages.data:
#                 last_message = messages.data[-1]  # Get the latest message
#
#                 # Assuming last_message.content is a list and we need the first element
#                 if last_message.content and isinstance(last_message.content, list):
#                     response_content = last_message.content[0]
#                     if 'text' in response_content and 'value' in response_content['text']:
#                         response = response_content['text']['value']
#                         st.write(f"Assistant's Response: {response}")
#                     else:
#                         st.write("No text value found in response.")
#                 else:
#                     st.write("Invalid response format.")
#             else:
#                 st.write("Error in retrieving messages. Please try again.")
#
#         except Exception as e:
#             st.write(f"An error occurred: {str(e)}")
