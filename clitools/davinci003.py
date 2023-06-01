import openai
import time
import sys
import os

api_key = sys.argv[1]
openai.api_key = api_key


def ask_gpt3(prompt):
    for i in range(5):  # 最大尝试次数为5次
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=512,
                n=1,
                stop=None,
                temperature=0.5,
            )
            message = response.choices[0].text.strip()
            return message
        except Exception as e:
            print("Error:", e)
            if i < 4:
                print(f"Retrying in 4 seconds... (Attempt {i+1}/5)")
                time.sleep(4)  # 每次间隔4秒
            else:
                print("Max retries reached, giving up.")
    return None



questions = []
answers = []


def generate_prompt(prompt, questions, answers):
    num = len(answers)
    for i in range(num):
        prompt += "\n Q : " + questions[i]
        prompt += "\n A : " + answers[i]
    prompt += "\n Q : " + questions[num] + "\n A : "
    return prompt


def ask(question):
    questions.append(question)
    prompt = generate_prompt("", questions, answers)
    answer = ask_gpt3(prompt)
    answers.append(answer)
    return answer

abstract = sys.argv[2]

prompt1 = f"""
 list abbreviation of gene/protein,which Qishen Yiqi , also called QSYQ has effect of inhibit or improve by follow:
{abstract} 
"""

ans1 = ask(prompt1)
# print(ans1)


prompt2 = f"""
isn't there others? output,again
"""

ans2 = ask(prompt2)
# print(ans2)


prompt3 = f"""
just only list Gene or Proteins (format: 1.xxx 2.xxx) ,in belows:
"{ans1}

{ans2}"
"""

ans3 = ask(prompt3)
# print(ans3)


prompt4 = f"""
is the effect of Qishen Yiqi , also called QSYQ, to those Gene/Protein(in belows) inhibit or improve expression? please only tell me inhibit or improve expression:
{ans3}
"""

ans4 = ask(prompt4)
print(ans4)