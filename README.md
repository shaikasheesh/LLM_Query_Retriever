# LLM_SQL_Database_Query_Retriever

# Requirement:
we have an database for t-shirts stock. let us say if we want to know some details about the stock for eg how many white shirts are available, we need to write a SQL query to get this answer but end users may not always know sql queries.

so instead we make use of LLMs to query from database and get the answers to our questions

This seems simple at first glance. but think about the complex queries that you might have and this LLM models are not trained on your SQL database , they are just using their general knowledge to get the answers for simple queries.

to make LLM comfortable with your SQL database, we need to give certain questions and answers (queries) to the LLM so that when a similar query comes in it will understand from these examples and give you the right answer

to make this happen, we need the concept of EMbeddings, Vector databases, sentence similarity and custom prompt templates using few shot method

# Output Screen Shot
![image](https://github.com/shaikasheesh/LLM_Query_Retriever/assets/63601317/5b6e20d9-ca57-4f91-968a-100ca64b1ab9)

in short, the question is converted to embeddings then it takes in similar vectors from the vector store and return the most similar query to query from SQL database and provides the answer

# Consumption:

built a streamlit powered UI to ask the question and retrive the answer

