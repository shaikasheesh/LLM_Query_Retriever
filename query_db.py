from langchain.llms import GooglePalm
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma,faiss
from langchain.prompts import FewShotPromptTemplate
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt
from langchain.prompts.prompt import PromptTemplate
import os
from dotenv import load_dotenv
from few_shot import few_shots
load_dotenv()  # take environment variables from .env (especially openai api key)


def query_from_db():
    llm = GooglePalm(google_api_key=os.getenv('google_api_key'), temperature=0.2)
    db_user = "root"
    db_password = "password"
    db_host = "127.0.0.1"
    db_name = "atliq_tshirts"
    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}",sample_rows_in_table_info=3)
    #create embeddings using HuggingFace
    HFembeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    values_to_vectorize = [" ".join(i.values())for i in few_shots] #converting to single big string
    faiss_db = faiss.FAISS.from_texts(values_to_vectorize,HFembeddings,few_shots)

    example_selector = SemanticSimilarityExampleSelector(
                        vectorstore=faiss_db,
                        k=2,
                            )
    
    example_prompt = PromptTemplate(
    input_variables=["Question", "SQLQuery", "SQLResult","Answer",],
    template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
                )
    

    few_shot_prompt = FewShotPromptTemplate(
    example_selector=example_selector,
    example_prompt=example_prompt,
    prefix=_mysql_prompt,
    suffix=PROMPT_SUFFIX,
    input_variables=["input", "table_info", "top_k"], #These variables are used in the prefix and suffix
        )
    
    sql_db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True,prompt=few_shot_prompt)
    return sql_db_chain



#chain = query_from_db()
#print(chain.run("how many total white shirts are available ?"))

