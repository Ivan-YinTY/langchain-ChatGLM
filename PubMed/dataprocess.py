import os
import pandas as pd

def save_abstract_to_txt(excel_path, output_folder, num_files=1):
    # 读取Excel文件
    df = pd.read_excel(excel_path)

    # 创建Output文件夹
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    # 根据 num_files 将 DataFrame 分成多个子集
    subsets = [df[i:i+num_files] for i in range(0, len(df), num_files)]

    # 遍历 DataFrame 的每个子集，将 abstract 合并后保存到对应的 txt 文件中
    for subset in subsets:
        pmids = '_'.join(map(str, subset['pmid'].tolist()))
        abstracts = '\n'.join(map(str.strip, subset['abstract'].tolist()))

        # 将合并后的 abstract 内容保存到 txt 文件中
        txt_filename = f"{output_folder}/{pmids}.txt"
        with open(txt_filename, 'w', encoding='utf-8') as f:
            f.write(abstracts)

if __name__ == "__main__":
    # 调用save_abstract_to_txt函数
    excel_path = './pubmed.xlsx'
    output_folder = './Output'
    save_abstract_to_txt(excel_path, output_folder, num_files=1)
