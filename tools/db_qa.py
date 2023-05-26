import os
import openai
import platform
from langchain.prompts.prompt import PromptTemplate
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain
from langchain.chains import SQLDatabaseSequentialChain

if "OPENAI_API_KEY" not in os.environ or not os.environ["OPENAI_API_KEY"]:
    os.environ["OPENAI_API_KEY"] = input("Please enter your OPENAI_API_KEY: ")

_DEFAULT_TEMPLATE = """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Use the following format:

Question: "Question here"
SQLQuery: "SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"

Only use the following tables:

{table_info}

If someone asks for the table foobar, they really mean the employee table.

Question: {input}"""
PROMPT = PromptTemplate(
    input_variables=["input", "table_info", "dialect"], template=_DEFAULT_TEMPLATE
)

if __name__ == "__main__":
    # db = SQLDatabase.from_uri("mysql+pymysql://ionadmin:ionadmin@10.9.17.7/tcmsystem_db_v2?charset=utf8")
    db = SQLDatabase.from_uri(
        "mysql+pymysql://ionadmin:ionadmin@10.9.17.7/tcmsystem_db_v2?charset=utf8",
        include_tables=['tcm_ingredient_targets_stitch', 'tcm_ingredient_targets_chembl'],  # we include only one table to save tokens in the prompt :)
        sample_rows_in_table_info=2)
    llm = OpenAI(model_name="gpt-3.5-turbo", temperature=0.9)

    chain = SQLDatabaseSequentialChain.from_llm(llm, db, verbose=True)
    chain.run("描述一下tcm_ingredient_targets_stitch表，最多选取十条示例数据。")

    # db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, return_direct=True, top_k=3, return_intermediate_steps=True)
    # result = db_chain("PIK3CD的pchembl_value值是多少？")
    # result["intermediate_steps"]

    # db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, use_query_checker=True)
    # db_chain.run("PIK3CD的pchembl_value值是多少？")