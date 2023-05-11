import os
import pandas as pd
from tqdm import tqdm
from langchain.llms import OpenAI
# from langchain.chat_models import ChatOpenAI
from chains.local_doc_qa import load_file
from configs.extract_model_config import *
from textsplitter import ChineseTextSplitter
from langchain import PromptTemplate, LLMChain
from langchain.docstore.document import Document
from langchain.document_loaders import UnstructuredFileLoader


def load_article_file(filepath, sentence_size=SENTENCE_SIZE):
    if filepath.lower().endswith(".md"):
        loader = UnstructuredFileLoader(filepath, mode="elements")
        docs = loader.load()
    elif filepath.lower().endswith(".pdf"):
        loader = UnstructuredFileLoader(filepath)
        # textsplitter = ChineseTextSplitter(pdf=True, sentence_size=sentence_size)
        # docs = loader.load_and_split(textsplitter)
        docs = loader.load()
    else:
        loader = UnstructuredFileLoader(filepath, mode="elements")
        # textsplitter = ChineseTextSplitter(pdf=False, sentence_size=sentence_size)
        # docs = loader.load_and_split(text_splitter=textsplitter)
        docs = loader.load()

    # print(docs[:3])
    return docs


def extract_text_relation(filepath):
    # 加载文件
    article_text = load_article_file(filepath=filepath)

    # 创建模板以及生成提示
    extract_prompt = PromptTemplate(template=extract_template, input_variables=["context"])
    # print(extract_prompt.format(context=article_text))

    # 初始化LLM模型和链式模型
    llm = OpenAI(model_name=openai_model_name, temperature=0)
    llm_chain = LLMChain(prompt=extract_prompt, llm=llm)

    #print(llm_chain.run(article_text))

    # 运行链式模型并返回结果
    return llm_chain.run(article_text)


def format_text_relation(text):
    formatted_list = []
    for line in text.split('\n'):
        if line.strip():
            formatted_list.append(line.split('，'))
    return formatted_list


def filter_list(input_list):
    result_list = []
    pmid = ''
    for item in input_list:
        if len(item) == 4 and '/' not in item[0] and '/' not in item[1] and '/' not in item[2] and '/' not in item[3]:
            if pmid == '':
                pmid = item[3]
            elif pmid != item[3]:
                item[3] = pmid
            result_list.append(item)
    return result_list


def process_file_batch(directory_path):
    # Check if the directory exists
    if not os.path.exists(directory_path):
        print(f"Warning: The directory '{directory_path}' does not exist.")
        return []

    # Get a list of all .txt files in the directory
    file_list = [f for f in os.listdir(directory_path) if f.endswith('.txt')]

    # Process each file with progress bar
    result = []
    for file_path in tqdm(file_list, desc="Processing files", unit="file"):
        try:
            text = extract_text_relation(os.path.join(directory_path, file_path))
            formatted = format_text_relation(text)
            formatted = filter_list(formatted)
            result.extend(formatted)
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    return result


def format_dblist(l):
    return [(x[2], x[1], x[0], x[3]) for x in l]


def save_to_excel(data, headers=['Herb', 'Effect', 'Gene', 'PMID'], file_name='result.xlsx'):
    """
    将数据存储到xlsx文件中

    参数：
        data：list类型的二维数组，包含要存储的数据
        headers：list类型的一维数组，包含表头字段名，默认值为['Herb', 'Effect', 'Gene', 'PMID']
        file_name：文件名，包含路径和扩展名，例如"/path/to/result.xlsx"，默认值为"result.xlsx"

    返回值：
        无返回值
    """
    # 将数据转化为DataFrame格式
    df = pd.DataFrame(data, columns=headers)

    # 将DataFrame保存到xlsx文件中
    with pd.ExcelWriter(file_name) as writer:
        df.to_excel(writer, index=False)


if __name__ == "__main__":
    text = """
    芪参益气滴丸，下调，CD68，22240383
    芪参益气滴丸，下调，transforming growth factor beta 1，22240383。
    """

    formatted_list = format_text_relation(text)
    print(formatted_list)

    data = [['芪参益气滴丸', '下调', 'CD68', '22240383'],
            ['芪参益气滴丸', '下调', 'transforming growth factor beta 1', '22240383'],
            ['芪参益气滴丸', '下调', 'VEGF', '19203810'],
            ['芪参益气滴丸', '下调', 'bFGF', '19203810'],
            ['芪参益气滴丸', '下调', 'PDGF-B', '19203810']]
    file_name = './result.xlsx'

    save_to_excel(data, file_name=file_name)