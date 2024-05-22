import csv
import datetime
from utils_of_num_to_word import *
from commmon import *
import queue
import threading
import time

#去掉小数部分多余的0
def process_string(s):
    try:
        # 尝试将字符串转换为浮点数
        float_val = float(s)

        # 尝试将字符串转换为整数
        int_val = int(float_val)

        # 如果转换为整数后与原浮点数相等，返回整数部分（转换为字符串）
        if int_val == float_val:
            return str(int_val)
        else:
            # 含有非零小数部分，使用字符串格式化去除多余的零
            return "{:.10g}".format(float_val)
    except ValueError:
        # 无法转换为浮点数，返回原字符串
        return s

# 假设这些函数已经被定义
def score(correct_answer, api_response):
    api_response = api_response.replace(",", "").replace("，", "").replace(" ", "").replace(" ", "")
    pattern = rf"(?<!\d){re.escape(correct_answer)}(?!\d)(?!\.\d)"
    if re.search(pattern, api_response):
        return '1'
    else:
        print(f'为什么不匹配？correct:{correct_answer}, api_response:{api_response}')
        if 'msorrybutyouhaven' in api_response:
            return '-1'
        return '0'

def generate_exist_data(exist_row, language, level, is_need_numcot):
    result = []

    filename = f'C:/Cross-lingual-MWP-{level}.csv'
    print(f"filename is :{filename}")
    with open(filename, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        datas = [row for row in reader][0:]
    for index, row in enumerate(datas):
        if (index + 1) <= exist_row:
            continue
        if is_need_numcot == True:
            question = row['problem_modern']
            answer = row['answer']
        else:
            if language == 'zh':
                question = row['zh']
            else:
                question = row['sQuestion']
            answer = row['lSolutions'].replace("[", "").replace("]", "").replace("'", "").replace("‘", "")
            answer = process_string(answer)
        temp = {question: answer}
        result.append(temp)
    return result

def process_data_subset(data_subset, model, result_queue, subset_index, language, level, is_need_numcot):
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

                time.sleep(3)
                zeroshot_response = call_api(model, zeroshot_quesion, True)
                response += zeroshot_response
                zeroshot_score = score(answer, zeroshot_response)
                if zeroshot_score == '-1':
                    print("出现问题需要处理")
                print(f'{index + 1}-zeroshot_quesion:{zeroshot_quesion}\n{zeroshot_response}')

                time.sleep(3)
                cot_zeroshot_response = call_api(model, cot_zeroshot_quesion, True)
                response += cot_zeroshot_response
                cot_zeroshot_score = score(answer, cot_zeroshot_response)
                if cot_zeroshot_score == '-1':
                    print("出现问题需要处理")
                print(f'{index + 1}-cot_zeroshot_quesion:{cot_zeroshot_quesion}\n{cot_zeroshot_response}')

                time.sleep(3)
                fewshot_response = call_api(model, fewshot_quesion, True)
                response += fewshot_response
                fewshot_score = score(answer, fewshot_response)
                if fewshot_score == '-1':
                    print("出现问题需要处理")
                print(f'{index + 1}-fewshot_quesion:{fewshot_quesion}\n{fewshot_response}')

                time.sleep(3)
                cot_fewshot_response = call_api(model, cot_fewshot_quesion, True)
                response += cot_fewshot_response
                cot_fewshot_score = score(answer, cot_fewshot_response)
                if cot_fewshot_score == '-1':
                    print("出现问题需要处理")
                print(f'{index + 1}-cot_fewshot_quesion:{cot_fewshot_quesion}\n{cot_fewshot_response}')

                if is_need_numcot == True:
                    numcot_quesion = format_unit_measurement(language, 'numcot', question)
                    time.sleep(3)
                    numcot_response = call_api(model, numcot_quesion, True)
                    response += numcot_response
                    numcot_score = score(answer, numcot_response)
                    if numcot_score == '-1':
                        print("出现问题需要处理")
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

            if is_need_numcot == True:
                new_row = [
                    level,
                    question,
                    answer,
                    f"{zeroshot_quesion}",
                    f"{zeroshot_response}",
                    zeroshot_score,
                    f"{cot_zeroshot_quesion}",
                    f"{cot_zeroshot_response}",
                    cot_zeroshot_score,
                    f"{fewshot_quesion}",
                    f"{fewshot_response}",
                    fewshot_score,
                    f"{cot_fewshot_quesion}",
                    f"{cot_fewshot_response}",
                    cot_fewshot_score,
                    f"{numcot_quesion}",
                    f"{numcot_response}",
                    numcot_score,
                ]
            else:
                new_row = [
                    level,
                    question,
                    answer,
                    f"{zeroshot_quesion}",
                    f"{zeroshot_response}",
                    zeroshot_score,
                    f"{cot_zeroshot_quesion}",
                    f"{cot_zeroshot_response}",
                    cot_zeroshot_score,
                    f"{fewshot_quesion}",
                    f"{fewshot_response}",
                    fewshot_score,
                    f"{cot_fewshot_quesion}",
                    f"{cot_fewshot_response}",
                    cot_fewshot_score,
                ]
            print(f">>>>>>{index + 1}<<<<<<<", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), new_row)
        new_data_subset.append(new_row)
    result_queue.put((subset_index, new_data_subset))

def process_data(model, machine_num, language, level, is_need_numcot=False):
    datas = generate_exist_data(0, language, level, is_need_numcot)
    data_subsets = [datas[i::machine_num] for i in range(machine_num)]

    threads = []
    result_queue = queue.Queue()

    for i, data_subset in enumerate(data_subsets):
        thread = threading.Thread(target=process_data_subset, args=(data_subset, model, result_queue, i, language, level, is_need_numcot))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    new_data = [None] * machine_num
    while not result_queue.empty():
        subset_index, subset_data = result_queue.get()
        new_data[subset_index] = subset_data

    new_data = [row for subset in new_data for row in subset]
    if is_need_numcot == True:
        with open(
                f'{model}_{level}_{language}_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}_{len(new_data)}.csv',
                'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # 写入列名
            writer.writerow(['level', 'number', 'answer',
                             f'{model}_zeroshot_quesion', f'{model}_zeroshot_answer', f'{model}_zeroshot_score',
                             f'{model}_cot_zeroshot_quesion', f'{model}_cot_zeroshot_answer',
                             f'{model}_cot_zeroshot_score',
                             f'{model}_fewshot_quesion', f'{model}_fewshot_answer', f'{model}_fewshot_score',
                             f'{model}_cot_fewshot_quesion', f'{model}_cot_fewshot_answer', f'{model}_cot_fewshot_score',
                             f'{model}_numcot_quesion', f'{model}_numcot_answer', f'{model}_numcot_score'])
            # 写入数据
            writer.writerows(new_data)
    else:
        with open(f'{model}_{level}_{language}_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}_{len(new_data)}.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # 写入列名
            writer.writerow(['level', 'number', 'answer',
                             f'{model}_zeroshot_quesion', f'{model}_zeroshot_answer', f'{model}_zeroshot_score',
                             f'{model}_cot_zeroshot_quesion', f'{model}_cot_zeroshot_answer', f'{model}_cot_zeroshot_score',
                             f'{model}_fewshot_quesion', f'{model}_fewshot_answer', f'{model}_fewshot_score',
                             f'{model}_cot_fewshot_quesion', f'{model}_cot_fewshot_answer', f'{model}_cot_fewshot_score'])
            # 写入数据
            writer.writerows(new_data)
    print(f"success. Data saved to '{model}_{level}_{language}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{len(new_data)}.csv'")



if __name__ == '__main__':
    process_data('zhipu', 20, 'suanjing', 'suanjing', True)
