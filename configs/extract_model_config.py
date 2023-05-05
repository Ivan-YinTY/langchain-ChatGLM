import os

OPENAI_API_KEY= ''

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

openai_model_name = "text-davinci-003"


extract_template = """已知信息：
{context} 

根据上述已知信息总结所包含的药物实体、基因实体及其相互作用关系，以(药物名称，关系，基因名，文件名)的格式返回，例如(芪参益气滴丸，下调，，19203810)。关系只能是上调或下调。文件名从'filename'中查找，如'filename': '/content/langchain-ChatGLM/PubMed/Output/19203810.txt'，则文件名为19203810。多组关系用换行分割，不允许插入其他字符。如果无法从中得到答案，用‘/’填充对应位置，如回答(/，/，/),不允许编造。"""
