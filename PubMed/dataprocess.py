import os
import pandas as pd

def save_abstract_to_txt(excel_path, output_folder):
    # 读取Excel文件
    df = pd.read_excel(excel_path)

    # 创建Output文件夹
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    # 遍历DataFrame的每一行，并保存abstract内容到对应的txt文件中
    for index, row in df.iterrows():
        pmid = str(row['pmid'])
        abstract = str(row['abstract']).strip()

        # 将abstract内容保存到txt文件中
        txt_filename = output_folder + '/' + pmid + '.txt'
        with open(txt_filename, 'w', encoding='utf-8') as f:
            f.write(abstract)

if __name__ == "__main__":
    # 调用save_abstract_to_txt函数
    excel_path = './pubmed.xlsx'
    output_folder = './Output'
    save_abstract_to_txt(excel_path, output_folder)
