import os
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from langchain.llms.openai import OpenAI
from langchain.agents import AgentExecutor

if "OPENAI_API_KEY" not in os.environ or not os.environ["OPENAI_API_KEY"]:
    os.environ["OPENAI_API_KEY"] = input("Please enter your OPENAI_API_KEY: ")

if __name__ == "__main__":
    db = SQLDatabase.from_uri(
        "mysql+pymysql://ionadmin:ionadmin@10.9.17.7/tcmsystem_db_v2?charset=utf8",
        include_tables=['tcm_ingredient_targets_stitch', 'tcm_ingredient_targets_chembl'],  # we include only one table to save tokens in the prompt :)
        sample_rows_in_table_info=2)

    llm = OpenAI(model_name="text-davinci-003", temperature=0)

    toolkit = SQLDatabaseToolkit(db=db,llm=llm)

    agent_executor = create_sql_agent(
        llm,
        toolkit=toolkit,
        verbose=True,
        max_iterations=5,
        early_stopping_method="generate"
    )

    agent_executor.run("描述一下tcm_ingredient_targets_stitch表.")