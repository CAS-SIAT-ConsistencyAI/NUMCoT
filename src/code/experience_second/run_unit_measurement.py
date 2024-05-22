import csv
import datetime
from utils_of_num_to_word import *
from commmon import *
import queue
import threading

# 假设这些函数已经被定义
def score(correct_answer, api_response, level, language):
    api_response = api_response.replace(",", "").replace("，", "").replace(" ", "").replace(" ", "")
    if level == 'easy' or level == 'medium':
        pattern = rf"(?<!\d){re.escape(correct_answer)}(?!\d)(?!\.\d)"
        if re.search(pattern, api_response):
            return '1'
        else:
            print(f'为什么不匹配？correct:{correct_answer}, api_response:{api_response}')
            return '0'
    else:
        tuple = eval(correct_answer)
        num1 = str(tuple[0])
        num2 = str(tuple[1])
        pattern1 = rf"(?<!\d){re.escape(num1)}(?!\d)(?!\.\d)"
        pattern2 = rf"(?<!\d){re.escape(num2)}(?!\d)(?!\.\d)"
        if re.search(pattern1, api_response) and re.search(pattern2, api_response):
            return '1'
        else:
            print(f'为什么不匹配？correct:{correct_answer}, api_response:{api_response}')
            return '0'

def generate_exist_data(exist_row, language, level='medium'):
    result = []
    filename = f'C:/unit_measurement_{level}_{language}.csv'
    print(f"filename is :{filename}")
    with open(filename, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        datas = [row for row in reader][0:]
    for index, row in enumerate(datas):
        if (index + 1) <= exist_row:
            continue
        temp = {row['question']: row['answer']}
        result.append(temp)
    return result

def process_data_subset(data_subset, model, result_queue, subset_index, language, level):
    new_data_subset = []
    for index, item in enumerate(data_subset):
        for question, answer in item.items():
            need_handle = 20
            while(need_handle > 0):
                response = ''
                zeroshot_quesion = format_unit_measurement(language, 'zeroshot', question)
                cot_zeroshot_quesion = format_unit_measurement(language, 'cot_zeroshot', question)
                fewshot_quesion = format_unit_measurement(language, 'fewshot', question)
                cot_fewshot_quesion = format_unit_measurement(language, 'cot_fewshot', question)
                numcot_quesion = format_unit_measurement(language, 'numcot', question)

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

                time.sleep(1)
                numcot_response = call_api(model, numcot_quesion, True)
                response += numcot_response
                print(f'{index + 1}-numcot_quesion:{numcot_quesion}\n{numcot_response}')
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
                question,
                answer,
                f"{zeroshot_quesion}",
                f"{zeroshot_response}",
                score(answer, zeroshot_response, level, language),
                f"{cot_zeroshot_quesion}",
                f"{cot_zeroshot_response}",
                score(answer, cot_zeroshot_response, level, language),
                f"{fewshot_quesion}",
                f"{fewshot_response}",
                score(answer, fewshot_response, level, language),
                f"{cot_fewshot_quesion}",
                f"{cot_fewshot_response}",
                score(answer, cot_fewshot_response, level, language),
                f"{numcot_quesion}",
                f"{numcot_response}",
                score(answer, numcot_response, level, language),
            ]
            print(f">>>>>>{index + 1}<<<<<<<", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), new_row)
        new_data_subset.append(new_row)
    result_queue.put((subset_index, new_data_subset))

def process_data(model, machine_num, language, level):
    try:
        datas = generate_exist_data(0, language, level)
        data_subsets = [datas[i::machine_num] for i in range(machine_num)]

        threads = []
        result_queue = queue.Queue()

        for i, data_subset in enumerate(data_subsets):
            thread = threading.Thread(target=process_data_subset, args=(data_subset, model, result_queue, i, language, level))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        new_data = [None] * machine_num
        while not result_queue.empty():
            subset_index, subset_data = result_queue.get()
            new_data[subset_index] = subset_data

        new_data = [row for subset in new_data for row in subset]

        with open(f'{model}_{level}_{language}_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}_{len(new_data)}.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # 写入列名
            writer.writerow(['level', 'number', 'answer',
                             f'{model}_zeroshot_quesion', f'{model}_zeroshot_answer', f'{model}_zeroshot_score',
                             f'{model}_cot_zeroshot_quesion', f'{model}_cot_zeroshot_answer', f'{model}_cot_zeroshot_score',
                             f'{model}_fewshot_quesion', f'{model}_fewshot_answer', f'{model}_fewshot_score',
                             f'{model}_cot_fewshot_quesion', f'{model}_cot_fewshot_answer', f'{model}_cot_fewshot_score',
                             f'{model}_numcot_quesion', f'{model}_numcot_answer', f'{model}_numcot_score'])
            # 写入数据
            writer.writerows(new_data)
        print(f"success. Data saved to '{model}_{level}_{language}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{len(new_data)}.csv'")
    except Exception as e:
        # 如果发生错误，保存已处理的数据
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        with open(f'{model}_{level}_{language}_{timestamp}_{len(new_data)}.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['level', 'number', 'answer',
                             f'{model}_zeroshot_quesion', f'{model}_zeroshot_answer', f'{model}_zeroshot_score',
                             f'{model}_cot_zeroshot_quesion', f'{model}_cot_zeroshot_answer', f'{model}_cot_zeroshot_score',
                             f'{model}_fewshot_quesion', f'{model}_fewshot_answer', f'{model}_fewshot_score',
                             f'{model}_cot_fewshot_quesion', f'{model}_cot_fewshot_answer', f'{model}_cot_fewshot_score'])
            writer.writerows(new_data)
        print(f"An error occurred: {e}. Data saved to '{model}_{level}_{language}_{timestamp}_{len(new_data)}.csv'")

# 调用处理数据的函数
process_data('chatglm26b', 20, 'zh', 'easy')
process_data('chatglm26b', 20, 'zh', 'medium')
process_data('chatglm26b', 20, 'zh', 'hard')

process_data('chatglm26b', 20, 'en', 'easy')
process_data('chatglm26b', 20, 'en', 'medium')
process_data('chatglm26b', 20, 'en', 'hard')
