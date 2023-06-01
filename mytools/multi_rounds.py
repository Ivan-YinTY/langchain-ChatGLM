import openai
import time
import os
# from configs.extract_model_config import *

openai.api_key = ""


def ask_gpt3(prompt, temperature=0, engine="text-davinci-003", retry=5):
    try_count = 0  # 已经尝试次数
    while True:
        try:
            if engine == "text-davinci-003":
                response = openai.Completion.create(
                    engine=engine,
                    prompt=prompt,
                    max_tokens=2048,
                    n=1,
                    stop=None,
                    temperature=temperature,
                )
                message = response.choices[0].text.strip()
            else:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}]
                )
                message = response['choices'][0]['message']['content'].strip()
            return message
        except Exception as e:
            if try_count >= retry:  # 判断是否已达到最大尝试次数
                raise e
            try_count += 1
            print(f"请求失败，正在进行第{try_count}次重试...")
            time.sleep(4)
            continue


def generate_prompt(prompt, questions, answers):
    num = len(answers)
    for i in range(num):
        prompt += "\n Q : " + questions[i]
        prompt += "\n A : " + answers[i]
    prompt += "\n Q : " + questions[num] + "\n A : "
    return prompt


def ask(question, questions, answers):
    questions.append(question)
    prompt = generate_prompt("", questions, answers)
    answer = ask_gpt3(prompt)
    answers.append(answer)
    return answer


def get_relation(abstract):
    questions = []
    answers = []

    prompt1 = f"""
     list abbreviation of gene/protein,which Qishen Yiqi , also called QSYQ has effect of inhibit or improve by follow:
    {abstract} 
    """

    ans1 = ask(prompt1, questions, answers)
    print(ans1)

    prompt2 = f"""
    isn't there others? output,again
    """

    ans2 = ask(prompt2, questions, answers)
    print(ans2)

    prompt3 = f"""
    just only list Gene or Proteins (format: 1.xxx 2.xxx) ,in belows:
    "{ans1}

    {ans2}"
    """

    ans3 = ask(prompt3, questions, answers)
    print(ans3)

    prompt4 = f"""
    is the effect of Qishen Yiqi , also called QSYQ, to those Gene/Protein(in belows) inhibit or improve expression? please only tell me inhibit or improve expression ,don't show other informations(format: 1.xxx 2.xxx):
    {ans3}
    """

    ans4 = ask(prompt4, questions, answers)
    print(ans4)


if __name__ == "__main__":
    abstract = """
        QiShenYiQi pill (QSYQ), a traditional Chinese medicine, is used to treat cardiovascular diseases. However, the dose-effect relationship of its intervention in the reactive myocardial fibrosis is elusive. In this work, rat models of reactive myocardial fibrosis induced by partial abdominal aortic coarctation were constructed and randomly classified into the model group, 3-methyladenine group, rapamycin group, QSYQ low-dose group, QSYQ medium-dose group, QSYQ high-dose group, and sham-operated rats (control group). We revealed that QSYQ lowered the heart mass index (HMI), left ventricular mass index (LVMI), and myocardial collagen volume fraction (CVF) levels in a dose-dependent mechanism. Additionally, QSYQ increased the number of autophagosomes, and the expression of myocardial Beclin-1 and LC3B. In contrast, it reduced the expression of myocardial p62 and decreased the ratios of myocardial p-PI3K/PI3K, p-Akt/Akt, and p-mTOR/mTOR. In conclusion, our results have revealed that QSYQ impacts anti-reactive myocardial fibrosis in a dose-dependent mechanism which is mediated by the activation of myocardial autophagy via the PI3K/AKT/mTOR pathway.
        """
    get_relation(abstract=abstract)