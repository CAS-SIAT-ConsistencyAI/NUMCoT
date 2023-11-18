import openai
import time


def GPT(prompt):
    error_cnt = 1
    response = '__error__'
    cnt = 0
    while error_cnt == 1 and cnt < 3:
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0301",
                max_tokens=1000,
                temperature=0,
                n=1,
                messages=prompt
            )
            error_cnt = 0
        except Exception as e:
            print(e)
            time.sleep(3)
            cnt += 1
    if cnt == 3:
        time.sleep(3)
        response = '__error__'
    else:
        response = completion.choices[0].message['content']
    time.sleep(2)
    return response
