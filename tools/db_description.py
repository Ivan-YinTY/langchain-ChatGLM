import os
import pandas as pd
from tqdm import tqdm
from time import sleep
from typing import List
from langchain.chat_models import ChatOpenAI
from langchain.chains import SQLDatabaseSequentialChain
from langchain import OpenAI, SQLDatabase, SQLDatabaseChain

if "OPENAI_API_KEY" not in os.environ or not os.environ["OPENAI_API_KEY"]:
    os.environ["OPENAI_API_KEY"] = input("Please enter your OPENAI_API_KEY: ")


def table_info_summary(username: str = 'ionadmin', password: str = 'ionadmin', host: str = '', database: str = '',
                    charset: str = 'utf8', table: str = '') -> List[str]:
    uri = f"mysql+pymysql://{username}:{password}@{host}/{database}?charset={charset}"
    include_tables = [table]
    sample_rows_in_table_info = 2

    db = SQLDatabase.from_uri(uri, include_tables=include_tables, sample_rows_in_table_info=sample_rows_in_table_info)
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    chain = SQLDatabaseSequentialChain.from_llm(llm, db, verbose=False)
    result = chain.run(f"用中文概括一下{table}表包含的信息，最多选取五条示例数据。")

    return result


def test_table_info_summary():
    username = 'ionadmin'
    password = 'ionadmin'
    host = '10.9.17.7'
    database = 'tcmsystem_db_v2'
    charset = 'utf8'
    table = 'tcm_ingredient_targets_stitch'

    print(table_info_summary(username, password, host, database, charset, table))


#无中断恢复
def db_info_summary_simple(xlsx_path: str = 'db_info_10.9.17.7.xlsx', username: str = 'ionadmin', password: str = 'ionadmin', host: str = '10.9.17.7',
                    charset: str = 'utf8', max_retry: int = 3) -> None:

    df = pd.read_excel(xlsx_path)
    df['表内容'] = ''

    for i in tqdm(range(len(df))):
        database = df.loc[i, '数据库名称']
        table = df.loc[i, '表名称']
        # print(database, table)

        for j in range(max_retry):
            try:
                result = table_info_summary(username=username, password=password, host=host, database=database, charset=charset, table=table)
                break
            except Exception as e:
                print(f"第{i+1}行数据重试{j+1}次失败，错误信息：{e}")
                if j == max_retry - 1:
                    print(f"第{i+1}行数据全部尝试失败，跳过处理。")
                    continue
                else:
                    sleep(1)

        df.loc[i, '表内容'] = result + '\n'
        sleep(2)

    df.to_excel(xlsx_path, index=False)

    print("跑完了！")


#中断恢复
def db_info_summary_interruption(xlsx_path: str = 'db_info_10.9.17.7.xlsx', username: str = 'ionadmin', password: str = 'ionadmin',
                    host: str = '10.9.17.7',
                    charset: str = 'utf8', max_retry: int = 2) -> None:
    df = pd.read_excel(xlsx_path)

    if '表内容' not in df.columns:
        df['表内容'] = ''
        null_content_indices = df.index.tolist()
    else:
        null_content_indices = df[df['表内容'].isnull()].index.tolist()

    if len(null_content_indices) == 0:
        print("所有记录都已经处理过了！")
        return

    for i in tqdm(null_content_indices):
        database = df.loc[i, '数据库名称']
        table = df.loc[i, '表名称']
        result = ''

        for j in range(max_retry):
            try:
                result = table_info_summary(username=username, password=password, host=host, database=database,
                                            charset=charset, table=table)
                break
            except Exception as e:
                print(f"第{i + 1}行数据重试{j + 1}次失败，错误信息：{e}")
                if j == max_retry - 1:
                    print(f"第{i + 1}行数据重试依旧失败，跳过处理。")
                    break
                else:
                    sleep(1)

        df.loc[i, '表内容'] = result + '\n'
        df.to_excel(xlsx_path, index=False) # 每处理完一条数据就保存一次excel文件
        sleep(2)

    print("跑完了！")


if __name__ == "__main__":
    # test_table_info_summary()
    db_info_summary_interruption()