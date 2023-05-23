import os

OPENAI_API_KEY= ''

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

openai_model_name = "text-davinci-003" #gpt-3.5-turbo / text-davinci-003

# 文本分句长度
SENTENCE_SIZE = 100

# 匹配后单段上下文长度
CHUNK_SIZE = 1500

# extract_template = """
# Extracts drug gene relationships from the text below delimited by three backslashes and return them in JSON format with the following keys: drug, effect, gene. You are asked to follow the following steps.
# Step 1, extract all contained gene name entities.
# Step 2, filter out the gene name entities related to QiShenYiQi Pills (also known as QSYQ, Qishenyiqi Dropping Pill, QSDP, etc.) based on the results of the previous step.
# Step 3, identify the relationship, such as up-regulation or down-regulation, between the gene entities screened in step 2 and QiShenYiQi Pills. If the relationship cannot be determined, the action relationship is defined as regulatory.
# Step 4, summarize the result of step 3, de-duplicate and return in the specified JSON format. Usually you will find 2 to 20 groups of drug-gene correspondences, as many as possible.
# Example, if the text is "Expressions of phospholipase A2 (PLA2), cyclooxygenase 1 (COX1) and COX2 were also down-regulated in the QSDP-treated group.", the output should be "[{"drug": "QSDP", "gene": "PLA2", "effecf": "down-regulation"}, {"drug": "QSDP", "gene": "COX1", "effecf": "down-regulation"}, {"drug": "QSDP", "gene": "COX2", "effecf": "down-regulation"}]".
#
# ```{{text}}```
# """

extract_template = """
Extracts drug gene relationships from the text below delimited by three backslashes and return them in JSON format with the following keys: drug, effect, gene. You are asked to follow the following steps.
Step 1, extract all contained gene name entities from each sentences.
Step 2, filter out the gene name entities related to QiShenYiQi Pills (also known as QSYQ, Qishenyiqi Dropping Pill, QSDP, etc.) based on the results of the previous step.
Step 3, identify the relationship, such as up-regulation or down-regulation, between the gene entities screened in step 2 and QiShenYiQi Pills. If the relationship cannot be determined, the action relationship is defined as regulatory.
Step 4, summarize the result of step 3, de-duplicate and return in the specified JSON format. Usually you will find 2 to 20 groups of drug-gene correspondences, as many as possible.
Example, if the text is "Expressions of phospholipase A2 (PLA2), cyclooxygenase 1 (COX1) and COX2 were also down-regulated in the QSDP-treated group.", the output should be "[{"drug": "QSDP", "gene": "PLA2", "effecf": "down-regulation"}, {"drug": "QSDP", "gene": "COX1", "effecf": "down-regulation"}, {"drug": "QSDP", "gene": "COX2", "effecf": "down-regulation"}]".

```{{text}}```
"""


# extract_template = """已知信息：
# {context}
#
# 根据上述已知信息总结所包含的芪参益气滴丸药物实体对应靶点及其相互作用关系，以(药物名称，关系，基因名，文件名)的格式返回，例如(芪参益气滴丸，下调，，19203810)。关系只能是上调或下调。文件名从'filename'中查找，如'filename': '/content/langchain-ChatGLM/PubMed/Output/19203810.txt'，则文件名为19203810。多组关系用换行分割，不允许插入其他字符。如果无法从中得到答案，用‘/’填充对应位置，如回答(/，/，/),不允许编造。"""
