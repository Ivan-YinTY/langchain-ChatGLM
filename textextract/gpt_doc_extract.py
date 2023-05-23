import os
import re
import time
import json
import pandas as pd
from tqdm import tqdm
from langchain.llms import OpenAI
# from langchain.chat_models import ChatOpenAI
from configs.extract_model_config import *
from textsplitter import ChineseTextSplitter
from langchain import PromptTemplate, LLMChain
from langchain.docstore.document import Document
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


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

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=50
    )
    docs = text_splitter.split_documents(docs)
    # print(docs[:3])
    return docs


def extract_text_relation(filepath, temperature=0):
    # 加载文件
    article_text = load_article_file(filepath=filepath)

    # 创建模板以及生成提示
    extract_prompt = PromptTemplate(template=extract_template, input_variables=["text"], template_format="jinja2")
    # print(extract_prompt.format(context=article_text))

    # 初始化LLM模型和链式模型
    if openai_model_name == "gpt-3.5-turbo":
        from langchain.chat_models import ChatOpenAI
        llm = ChatOpenAI(model_name=openai_model_name, temperature=temperature)
    else:
        llm = OpenAI(model_name=openai_model_name, temperature=temperature)

    llm_chain = LLMChain(prompt=extract_prompt, llm=llm)
    time.sleep(2)

    print(llm_chain.run(article_text))

    # 运行链式模型并返回结果
    return llm_chain.run(article_text), filepath


def format_text_relation(text, fp):
    formatted_list = []
    for line in text.split('\n'):
        if line.strip():
            formatted_list.append(line.split('，'))
    return formatted_list


def fix_json(json_str):
    if json_str.endswith(']'):
        return json_str
    elif json_str.endswith('}'):
        return json_str[:-1] + ']'
    else:
        for i in range(len(json_str) - 1, -1, -1):
            if json_str[i] == '}':
                return json_str[:i+1] + ']'


def test_fix_json():
    print(fix_json('[{"drug": "QSDP", "gene": "PLA2", "effect": "down-regulation"}, {"drug": "QSDP", "gene": "COX1", "effect": "down-regulation"}, {"drug": "QSDP", "gene": '))


def format_json_relation(json_data, fp):
    json_data = fix_json(json_data)

    try:
        data = json.loads(json_data)
    except Exception as e:
        print(f"Error: {e}")
        return []

    filename = os.path.basename(fp)  # 使用os.path.basename()函数获取文件名
    filename = filename.split('.')[0]  # 使用split()函数按照点号分割字符串并获取第一部分

    formatted_list = []
    for item in data:
        try:
            drug = item['drug']
            gene = item['gene']
            effect = item['effect']
            formatted_list.append((drug, effect, gene, filename))
        except Exception as e:
            print(f"Error: {e}. Skipping item.")
            continue

    return formatted_list


def test_format_json_relation():
    # json_data = '[{"drug": "QSDP", "gene": "PLA2", "effect": "down-regulation"}, {"drug": "QSDP", "gene": "COX1", "effect": "down-regulation"}, {"drug": "QSDP", "gene": "COX2", "effect": "down-regulation"}, {"drug": "QSDP", "gene": "MMP2", "effect": "down-regulation"}, {"drug": "QSDP", "gene": "MMP9", "effect": "down-regulation"}, {"drug": "QSDP", "gene": "AT1", "effect": "down-regulation"}, {"drug": "QSDP", "gene": "AT2", "effect": "up-regulation"}, {"drug": "QSDP", "gene": "NF-κB", "effect": "down-regulation"}, {"drug": "QSDP", "gene": "JAK1/STAT3", "effect": "down-regulation"}, {"drug": "QSDP", "gene": "Akt", "effect": "down-regulation"}]'
    json_data = '[{"drug": "QSDP", "gene": "PLA2", "effect": "down-regulation"}, {"drug": "QSDP", "gene": "COX1", "effect": "down-regulation"}, {"drug": "QSDP", "gene": "COX2", "effect": "down-regulation"}, {"drug": "QSDP", "gene": "AT1", "effect": "down-regulation"}, {"drug": "QSDP", "gene": "AT2", "effect": "up-regulation"}, {"drug": "QSDP", "gene": "NF-κB", "effect": "down-regulation"}, {"drug": "QSDP", "gene": "JAK1/STAT3", "effect": "down-regulation"}, {"drug": "QSDP", "gene": "Akt", "effect": "down-regulation"}]'
    fp = '/Output/19203810.txt'
    expected_output = [('QSDP', 'down-regulation', 'PLA2', '19203810'), ('QSDP', 'down-regulation', 'COX1', '19203810'), ('QSDP', 'up-regulation', 'AT2', '19203810')]
    print(format_json_relation(json_data, fp))
    # assert format_text_relation(json_data, fp) == expected_output, f'Error: {format_text_relation(json_data, fp)} != {expected_output}'


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

def filter_list_simple(input_list):
    result_list = []
    pmid = ''
    for item in input_list:
        if len(item) == 4:
            if pmid == '':
                pmid = item[3]
            elif pmid != item[3]:
                item[3] = pmid
            result_list.append(item)
    return result_list



def process_file_batch(directory_path, temperature=0):
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
            text, fp = extract_text_relation(os.path.join(directory_path, file_path), temperature=temperature)
            formatted = format_json_relation(text, fp)
            formatted = filter_list_simple(formatted)
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
    # text = """
    # 芪参益气滴丸，下调，CD68，22240383
    # 芪参益气滴丸，下调，transforming growth factor beta 1，22240383。
    # """
    #
    # formatted_list = format_text_relation(text)
    # print(formatted_list)
    #
    # data = [['芪参益气滴丸', '下调', 'CD68', '22240383'],
    #         ['芪参益气滴丸', '下调', 'transforming growth factor beta 1', '22240383'],
    #         ['芪参益气滴丸', '下调', 'VEGF', '19203810'],
    #         ['芪参益气滴丸', '下调', 'bFGF', '19203810'],
    #         ['芪参益气滴丸', '下调', 'PDGF-B', '19203810']]
    # file_name = './result.xlsx'
    #
    # save_to_excel(data, file_name=file_name)

    # print(filter_list_simple([['芪参益气滴丸', '下调', 'CD/68', '22240383'],
    #         ['芪参益气滴丸', '下调', 'transforming growth factor beta 1', '22240383'],
    #         ['芪参益气滴丸', '下调', '/', '22240383'],
    #         ['芪参益气滴丸', '下调', 'bFGF', '/'],
    #         ['芪参益气滴丸', '下调', 'bFGF', '2224'],
    #         ['芪参益气滴丸', '下调', 'PDGF-B', '22240383']]))

    # test_format_json_relation()

    test_fix_json()
