import csv
import datetime
from utils_of_num_to_word import *
from common import *
import queue
import threading

# 假设这些函数已经被定义
def score(correct_answer, api_response, task, language):
    if task == 'word2num':
        api_response = api_response.replace(",", "").replace("，", "").replace(" ", "").replace(" ", "")
        pattern = rf"(?<!\d){re.escape(correct_answer)}(?!\d)(?!\.\d)"
        if re.search(pattern, api_response):
            return '1'
        else:
            print(f'为什么不匹配？correct:{correct_answer}, api_response:{api_response}')
            return '0'
    if language == 'zh':
        correct_answer = traditional_to_simplified(correct_answer)
        api_response = traditional_to_simplified(api_response)
        if (correct_answer in api_response):
            return '1'
        else:
            print(f'为什么不匹配？correct:{correct_answer}, api_response:{api_response}')
            return '0'
    if language == 'en':
        correct_answer = correct_answer.lower().replace(" and ", " ").replace(",", "").replace("-", "").replace(" ", "")
        api_response = api_response.lower().replace(" and ", " ").replace(",", "").replace("-", "").replace(" ", "")
        if (traditional_to_simplified(correct_answer) in traditional_to_simplified(api_response)):
            return '1'
        else:
            print(f'为什么不匹配？correct:{correct_answer}, api_response:{api_response}')
            return '0'

def generate_exist_data(exist_row, task, language, type, level='medium'):
    result = []
    if level == 'hard':
        if type == 'decimal':
            level += f"_point"
        else:
            level += f"_{type}"
    filename = f'C:/{task}_{level}_{language}.csv'
    print(f"filename is :{filename}")
    with open(filename, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        datas = [row for row in reader][0:]
    for index, row in enumerate(datas):
        if (index + 1) <= exist_row:
            continue
        temp = {row['number']: row['answer']}
        result.append(temp)
    return result

def process_data_subset(data_subset, model, result_queue, subset_index, task, language, type, level):
    new_data_subset = []
    for index, item in enumerate(data_subset):
        for number, answer in item.items():
            need_handle = 20
            while(need_handle > 0):
                response = ''
                number = str(number)
                zeroshot_quesion = format_quesion(language, task, type, number, shot='zeroshot')
                cot_zeroshot_quesion = format_quesion(language, task, type, number, shot='cot_zeroshot')
                fewshot_quesion = format_quesion(language, task, type, number, shot='fewshot')
                cot_fewshot_quesion = format_quesion(language, task, type, number, shot='cot_fewshot')

                time.sleep(1)
                zeroshot_response = call_api(model, zeroshot_quesion, True)
                response += zeroshot_response
                print(f'{index + 1}-zeroshot_quesion:{zeroshot_quesion}\n{zeroshot_response}')

                time.sleep(1)
                cot_zeroshot_response = call_api(model, cot_zeroshot_quesion, True)
                response += cot_zeroshot_response
                print(f'{index + 1}-cot_zeroshot_quesion:{cot_zeroshot_quesion}\n{cot_zeroshot_response}')

                time.sleep(1)
                fewshot_response = call_api(model, fewshot_quesion, True)
                response += fewshot_response
                print(f'{index + 1}-fewshot_quesion:{fewshot_quesion}\n{fewshot_response}')

                time.sleep(1)
                cot_fewshot_response = call_api(model, cot_fewshot_quesion, True)
                response += cot_fewshot_response
                print(f'{index + 1}-cot_fewshot_quesion:{cot_fewshot_quesion}\n{cot_fewshot_response}')
                if "出现问题，需要重跑" in response:
                    if need_handle < 10:
                        sleeptime = 20
                    else:
                        sleeptime = 5
                    print(f'暂停{sleeptime}s')
                    time.sleep(sleeptime)
                    need_handle -= 1
                else:
                    need_handle = 0
            new_row = [
                level,
                number,
                answer,
                zeroshot_quesion,
                zeroshot_response,
                score(answer, zeroshot_response, task, language),
                cot_zeroshot_quesion,
                cot_zeroshot_response,
                score(answer, cot_zeroshot_response, task, language),
                fewshot_quesion,
                fewshot_response,
                score(answer, fewshot_response, task, language),
                cot_fewshot_quesion,
                cot_fewshot_response,
                score(answer, cot_fewshot_response, task, language),
            ]
            print(f">>>>>>{index + 1}<<<<<<<", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), new_row)
        new_data_subset.append(new_row)
    result_queue.put((subset_index, new_data_subset))

def process_data(model, machine_num, task, language, type, level):
    try:
        datas = generate_exist_data(0, task, language, type, level)
        data_subsets = [datas[i::machine_num] for i in range(machine_num)]

        threads = []
        result_queue = queue.Queue()

        for i, data_subset in enumerate(data_subsets):
            thread = threading.Thread(target=process_data_subset, args=(data_subset, model, result_queue, i, task, language, type, level))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        new_data = [None] * machine_num
        while not result_queue.empty():
            subset_index, subset_data = result_queue.get()
            new_data[subset_index] = subset_data

        new_data = [row for subset in new_data for row in subset]

        with open(f'{task}_{model}_{level}_{type}_{language}_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}_{len(new_data)}.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # 写入列名
            writer.writerow(['level', 'number', 'answer',
                             f'{model}_zeroshot_quesion', f'{model}_zeroshot_answer', f'{model}_zeroshot_score',
                             f'{model}_cot_zeroshot_quesion', f'{model}_cot_zeroshot_answer', f'{model}_cot_zeroshot_score',
                             f'{model}_fewshot_quesion', f'{model}_fewshot_answer', f'{model}_fewshot_score',
                             f'{model}_cot_fewshot_quesion', f'{model}_cot_fewshot_answer', f'{model}_cot_fewshot_score'])
            # 写入数据
            writer.writerows(new_data)
        print(f"success. Data saved to '{task}_{model}_{level}_{type}_{language}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{len(new_data)}.csv'")
    except Exception as e:
        # 如果发生错误，保存已处理的数据
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        with open(f'{task}_{model}_{level}_{type}_{language}_{timestamp}_{len(new_data)}.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['level', 'number', 'answer',
                             f'{model}_zeroshot_quesion', f'{model}_zeroshot_answer', f'{model}_zeroshot_score',
                             f'{model}_cot_zeroshot_quesion', f'{model}_cot_zeroshot_answer', f'{model}_cot_zeroshot_score',
                             f'{model}_fewshot_quesion', f'{model}_fewshot_answer', f'{model}_fewshot_score',
                             f'{model}_cot_fewshot_quesion', f'{model}_cot_fewshot_answer', f'{model}_cot_fewshot_score'])
            writer.writerows(new_data)
        print(f"An error occurred: {e}. Data saved to '{task}_{model}_{level}_{type}_{language}_{timestamp}_{len(new_data)}.csv'")

# 调用处理数据的函数
# process_data('chatglm26b', 100, 'num2word', 'zh', 'integer', 'medium')
