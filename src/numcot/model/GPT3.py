import openai
import time


def GPT(prompt):
    # top_p = 1
    # frequency_penalty = 0
    # presence_penalty = 0
    # temperature = 0.7 if args.SC and max_length != 32 else 0.0
    # n = 10 if args.SC and max_length != 32 else 1
    # stop = ["\n\n"] if max_length == 32 else None
    error_cnt = 1
    response = '__error__'
    cnt = 0
    while error_cnt == 1 and cnt < 3:
        try:
            completion = openai.Completion.create(
                engine='text-davinci-003',
                prompt=prompt,
                # frequency_penalty=frequency_penalty,
                # presence_penalty=presence_penalty,
                n=1,
                max_tokens=500
            )
            error_cnt = 0
        except:
            print('error')
            time.sleep(5)
            cnt += 1
    if cnt == 3:
        time.sleep(10)
        response = '__error__'
    else:
        response = completion.choices[0]['text']
    return response

# def basic_runner(args, inputs, max_length, apikey, max_retry=3):
#     retry = 0
#     get_result = False
#     pred = [] if args.SC else ''
#     error_msg = ''
#     while not get_result:
#         try:
#             pred = decoder_for_gpt3(args, inputs, max_length, apikey)
#             get_result = True
#         except openai.error.RateLimitError as e:
#             if e.user_message == 'You exceeded your current quota, please check your plan and billing details.':
#                 raise e
#             elif retry < max_retry:
#                 time.sleep(args.api_time_interval)
#                 retry += 1
#             else:
#                 error_msg = e.user_message
#                 break
#         except Exception as e:
#             raise e
#     return get_result, pred, error_msg
