import os

OPENAI_API_KEY= ''

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

openai_model_name = "gpt-3.5-turbo" #gpt-3.5-turbo / text-davinci-003

# 语言模型温度
LLM_TEMPERATURE = 0

# 多轮对话提取模式
MULTI_ROUND_CONVERSATION = True

# 文本分句长度
SENTENCE_SIZE = 100

# 文本分割块长度
CHUNK_SIZE = 1050

# 文本分割块交集长度
CHUNK_OVERLAP = 150


# extract_template = """
# Extracts drug gene relationships from the text below delimited by three backslashes and return them in JSON format with the following keys: drug, effect, gene. You are asked to follow the following steps.
# Step 1, extract all contained gene name entities from each sentences. Note that '/' will not appear in the gene name, e.g. 'MMP-1/TIMP-1' is actually two genes 'MMP-1' and 'TIMP-1', splitting them.
# Step 2, try to find possible interactions between each gene obtained in the previous step and QiShenYiQi Pills, defined only in terms of up- or down-regulation, the more the better. Note that the aliases or abbreviations Qishenyiqi Dropping Pill, QSDP, QYDP, QSYQ, etc. all refer to QiShenYiQi Pills.
# Step 3, summarize the result of step 2, de-duplicate and return in the specified JSON format. Usually you will find 2 to 20 groups of drug-gene correspondences, as many as possible.
# Here are some examples,
# 1.if the text is "Expressions of phospholipase A2 (PLA2), cyclooxygenase 1 (COX1) and COX2 were also down-regulated in the QSDP-treated group. All in all the expression of COX1and COX2 could not be enhanced by QSDP.", the output should be "[{"drug": "QSDP", "gene": "PLA2", "effecf": "down-regulation"}, {"drug": "QSDP", "gene": "COX1", "effecf": "down-regulation"}, {"drug": "QSDP", "gene": "COX2", "effecf": "down-regulation"}]".
# 2.if the text is "Downregulation of FOXO3a by QSYQ promotes breast cancer stem cell properties and tumorigenesis.", the output should be "[{"drug": "QSYQ", "gene": "FOXO3a", "effecf": "down-regulation"}]".
# 3.if the text is "Age-related upregulation of Drosophila caudal gene via QSDP in the adult posterior midgut.", the output should be "[{"drug": "QSDP", "gene": "caudal", "effecf": "up-regulation"}]".
# ```{{text}}```
# """

extract_template = """
Extracts drug(herb) gene relationships from the text below delimited by three backslashes and return them in JSON format with the following keys: drug(herb), effect, gene. You are asked to follow the following steps.
Step 1, extract all contained gene name entities from each sentences. Note that '/' will not appear in the gene name, e.g. 'MMP-1/TIMP-1' is actually two genes 'MMP-1' and 'TIMP-1', splitting them.
Step 2, try to find possible interactions between each gene obtained in the previous step and astragalus membranaceus(AM), defined only in terms of up- or down-regulation, the more the better. Note that the aliases or abbreviations huangqi, astragalus, astragaloside, astragali, astragali radix (AR), astragalus polysaccharide (APS), milkvetch, etc. all refer to astragalus membranaceus(AM).
Step 3, summarize the result of step 2, de-duplicate and return in the specified JSON format. Usually you will find 2 to 20 groups of drug-gene correspondences, as many as possible.
Here are some examples,
1.if the text is "Expressions of phospholipase A2 (PLA2), cyclooxygenase 1 (COX1) and COX2 were also down-regulated in the AM-treated group. All in all the expression of COX1and COX2 could not be enhanced by huangqi.", the output should be "[{"drug": "AM", "gene": "PLA2", "effecf": "down-regulation"}, {"drug": "AM", "gene": "COX1", "effecf": "down-regulation"}, {"drug": "AM", "gene": "COX2", "effecf": "down-regulation"}]".
2.if the text is "Downregulation of FOXO3a by huangqi promotes breast cancer stem cell properties and tumorigenesis.", the output should be "[{"drug": "huangqi", "gene": "FOXO3a", "effecf": "down-regulation"}]".
3.if the text is "Age-related upregulation of Drosophila caudal gene via astragalus membranaceus(AM) in the adult posterior midgut.", the output should be "[{"drug": "astragalus membranaceus(AM)", "gene": "caudal", "effecf": "up-regulation"}]".
```{{text}}```
"""

mr_summary_template = """
Summarize the following text delimited by three backslashes into compressed JSON format with the following keys: drug(herb), effect, gene, e.g. "[{"drug": "huangqi", "gene": "caudal", "effecf": "up-regulation"}]".
```{{text}}```
"""


# extract_template = """
# Extracts drug gene relationships from the text below delimited by three backslashes and return them in JSON format with the following keys: drug, effect, gene. You are asked to follow the following steps.
# Step 1, extract all contained gene name entities from each sentences. Note that '/' will not appear in the gene name, e.g. 'MMP-1/TIMP-1' is actually two genes 'MMP-1' and 'TIMP-1', splitting them.
# Step 2, try to find possible interactions between each gene obtained in the previous step and QiShenYiQi Pills, defined only in terms of up- or down-regulation, the more the better. Note that the aliases or abbreviations Qishenyiqi Dropping Pill, QSDP, QYDP, QSYQ, etc. all refer to QiShenYiQi Pills.
# Step 3, summarize the result of step 2, de-duplicate and return in the specified JSON format. Usually you will find 2 to 20 groups of drug-gene correspondences, as many as possible.
# Here are some examples,
# 1.if the text is "Expressions of phospholipase A2 (PLA2), cyclooxygenase 1 (COX1) and COX2 were also down-regulated in the QSDP-treated group. All in all the expression of COX1and COX2 could not be enhanced by QSDP.", the output should be "[{"drug": "QSDP", "gene": "PLA2", "effecf": "down-regulation"}, {"drug": "QSDP", "gene": "COX1", "effecf": "down-regulation"}, {"drug": "QSDP", "gene": "COX2", "effecf": "down-regulation"}]".
# 2.if the text is "Downregulation of FOXO3a by QSYQ promotes breast cancer stem cell properties and tumorigenesis.", the output should be "[{"drug": "QSYQ", "gene": "FOXO3a", "effecf": "down-regulation"}]".
# 3.if the text is "Age-related upregulation of Drosophila caudal gene via QSDP in the adult posterior midgut.", the output should be "[{"drug": "QSDP", "gene": "caudal", "effecf": "up-regulation"}]".
# ```{{text}}```
# """


# extract_template = """已知信息：
# {context}
#
# 根据上述已知信息总结所包含的芪参益气滴丸药物实体对应靶点及其相互作用关系，以(药物名称，关系，基因名，文件名)的格式返回，例如(芪参益气滴丸，下调，，19203810)。关系只能是上调或下调。文件名从'filename'中查找，如'filename': '/content/langchain-ChatGLM/PubMed/Output/19203810.txt'，则文件名为19203810。多组关系用换行分割，不允许插入其他字符。如果无法从中得到答案，用‘/’填充对应位置，如回答(/，/，/),不允许编造。"""


# multi_round_conversation_template_1 = """
# List abbreviation of gene/protein,which Qishen Yiqi , also called QSYQ has effect of inhibit or improve by the following text delimited by three backslashes.
# ```{{text}}```
# """
#
# multi_round_conversation_template_2 = """
# Previously I gave you the following text delimited by three backslashes and asked you to "List abbreviation of gene/protein, which Qishen Yiqi , also called QSYQ has effect of inhibit or improve."
# Your previous answer was "{{STEP1}}" Now I want to ask you "Isn't there another gene name or protein name? Output,again."
#
# ```{{text}}```
# """
#
# multi_round_conversation_template_3 = """
# I will give you two sentences and ask you to summarize the names of all the genes and proteins that appear in these two sentences, separated by commas.
# Sentence 1, "{{STEP1}}"
# Sentence 2, "{{STEP2}}"
# """
#
# multi_round_conversation_template_4 = """
# Answer the question based on the entity name and text delimited by three backslashes I gave you below. Note that you must use the compressed JSON string format I give you below for the output.
# ENTITY NAME:```{{STEP3}}```
# TEXT:```{{text}}```
# QUESTION:Is the effect of Qishen Yiqi (aka QSYQ) on these genes/proteins inhibit or improve expression? Please just tell me whether it is inhibit or improve expression and do not answer other information.
# OUTPUT FORMAT:"[{"drug": "QSDP", "gene": "PLA2", "effecf": "up-regulation"}, {"drug": "QSDP", "gene": "COX2", "effecf": "down-regulation"}]"
# """