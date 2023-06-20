import openai
import time
import sys
import os

api_key = sys.argv[1]
openai.api_key = api_key


def ask_gpt3(prompt):
    attempts = 0
    while attempts < 5:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=prompt
            )
            message = response['choices'][0]['message']['content'].strip()
            return message
        except Exception as e:
            attempts += 1
            print(f"Error: {e}. Retrying in 4 seconds...")
            time.sleep(4)
    raise Exception("Failed to get response from OpenAI API after 5 attempts.")



questions = []
answers = []


def generate_prompt(prompt, questions, answers):
    # num = len(answers)
    # for i in range(num):
    #     prompt += "\n Q : " + questions[i]
    #     prompt += "\n A : " + answers[i]
    # prompt += "\n Q : " + questions[num] + "\n A : "
    # return prompt
    prompt_list = []
    num = len(answers)
    for i in range(num):
        prompt_list.append({"role": "user", "content": f"{questions[i]}"})
        prompt_list.append({"role": "assistant", "content": f"{answers[i]}"})
    prompt_list.append({"role": "user", "content": f"{questions[num]}"})
    return prompt_list


def ask(question):
    questions.append(question)
    prompt = generate_prompt("", questions, answers)
    answer = ask_gpt3(prompt)
    answers.append(answer)
    return answer

abstract = sys.argv[2]

# prompt1 = f"""
#  list abbreviation of gene/protein,which Qishen Yiqi , also called QSYQ has effect of inhibit or improve by follow:
# {abstract}
# """

prompt1 = f"""
 list abbreviation of gene/protein,which astragalus membranaceus(AM) , also called huangqi, milkvetch, astragalus, has effect of inhibit or improve by follow:
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


# prompt4 = f"""
# is the effect of Qishen Yiqi , also called QSYQ, to those Gene/Protein(in belows) inhibit or improve expression? please only tell me inhibit or improve expression:
# {ans3}
# """

prompt4 = f"""
is the effect of astragalus membranaceus(AM) , also called huangqi, milkvetch, astragalus, to those Gene/Protein(in belows) inhibit or improve expression? please only tell me inhibit or improve expression:
{ans3}
"""

ans4 = ask(prompt4)
print(ans4)