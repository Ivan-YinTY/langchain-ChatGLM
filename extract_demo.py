from langchain.llms import OpenAI
from configs.extract_model_config import *
from textextract.gpt_doc_extract import *
from langchain.callbacks import get_openai_callback
from mysqlx.llm_store_abstract_extract_info import insert_data

if "OPENAI_API_KEY" not in os.environ or not os.environ["OPENAI_API_KEY"]:
    os.environ["OPENAI_API_KEY"] = input("Please enter your OPENAI_API_KEY: ")

OpenAI.api_key = os.getenv("OPENAI_API_KEY")

if __name__ == "__main__":
    with get_openai_callback() as cb:
        temp = process_file_batch("./PubMed/Output", temperature=LLM_TEMPERATURE)
        save_to_excel(temp, headers=['Herb', 'Effect', 'Gene', 'PMID'], file_name='./result.xlsx')
        print(temp)
        temp = format_dblist(temp)
        print(temp)

        print(f"Total Tokens: {cb.total_tokens}")
        print(f"Prompt Tokens: {cb.prompt_tokens}")
        print(f"Completion Tokens: {cb.completion_tokens}")
        print(f"Total Cost (USD): ${cb.total_cost}")

        # 询问用户是否写入数据库
        user_input = input("是否将结果写入数据库？(y/n)")

        if user_input.lower() == "y":
            insert_data(temp)
            print("数据库写入成功！")
        else:
            print("已取消写入数据库。")

