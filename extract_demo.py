from langchain.llms import OpenAI
from textextract.gpt_doc_extract import *
#from mysql.llm_store_abstract_extract_info import insert_data


OpenAI.api_key = os.getenv("OPENAI_API_KEY")

if __name__ == "__main__":
    temp = process_file_batch("./PubMed/Output")
    save_to_excel(temp, headers=['Herb', 'Effect', 'Gene', 'PMID'], file_name='./result.xlsx')
    print(temp)
    temp = format_dblist(temp)
    print(temp)
    #insert_data(temp)

