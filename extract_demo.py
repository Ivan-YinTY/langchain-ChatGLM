from langchain.llms import OpenAI
from textextract.gpt_doc_extract import *
from mysqlx.llm_store_abstract_extract_info import insert_data

OpenAI.api_key = os.getenv("OPENAI_API_KEY")

if __name__ == "__main__":
    temp = process_file_batch("./PubMed/Output")
    save_to_excel(temp, headers=['Herb', 'Effect', 'Gene', 'PMID'], file_name='./result.xlsx')
    print(temp)
    temp = format_dblist(temp)
    print(temp)
    # 询问用户是否写入数据库
    user_input = input("是否将结果写入数据库？(y/n)")

    if user_input.lower() == "y":
        insert_data(temp)
        print("数据库写入成功！")
    else:
        print("已取消写入数据库。")

