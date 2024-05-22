import threading
import datetime
from chat_api import *
from utils_of_num_to_word import *
from common import *
import queue

# 假设这些函数已经被定义
def score(correct_answer, api_response):
    correct_answer = traditional_to_simplified(correct_answer)
    api_response = traditional_to_simplified(api_response)
    if (correct_answer in api_response):
        return '1'
    else:
        print(f'为什么不匹配？correct:{correct_answer}, api_response:{api_response}')
        return '0'

def generate_exist_data(exist_row):
    result = []
    with open('C:/num2word_medium_en.csv', 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        datas = [row for row in reader][0:]
    for index, row in enumerate(datas):
        if (index + 1) <= exist_row:
            continue
        temp = {row['number']: row['answer']}
        result.append(temp)
    return result

def process_data_subset(data_subset, model, result_queue, subset_index):
    new_data_subset = []
    for index, item in enumerate(data_subset):
       # quesion = "以下是关于整数转为中文读法的题目，请根据题目的数字，给出正确的答案。\n题目：123 \n答案：让我们一步一步思考。\n1、首先将这个整数进行划分，使用如下的伪代码\nfunction split_and_reverse_sort_number(number):\n    number_str = str(number)\n    parts = []\n    while number_str:\n        part, number_str = number_str[-4:], number_str[:-4]\n        parts.insert(0, part)\n    parts.sort(reverse=True)\n    return parts\n这个函数代码可以将这个整数划分为一个部分「123」；\n2、只有一个部分，所以直接写出它的中文读法即可；\n3、从左到右依次可以写出一百二十三。\n所以答案是一百二十三。\n题目：123456 \n答案：让我们一步一步思考。\n1、首先将这个整数进行划分，使用如下的伪代码\nfunction split_and_reverse_sort_number(number):\n    number_str = str(number)\n    parts = []\n    while number_str:\n        part, number_str = number_str[-4:], number_str[:-4]\n        parts.insert(0, part)\n    parts.sort(reverse=True)\n    return parts\n这个函数代码可以将这个整数划分为2个部分「12」和「3456」；\n2、有2个部分，所以第一个部分写出它的中文读法后要在后面加上一个「万」字，第二个部分直接写出它的中文读法即可；\n3、从左到右依次可以写出十二万三千四百五十六。\n所以答案是十二万三千四百五十六。\n题目：123456789 \n答案：让我们一步一步思考。\n1、首先将这个整数进行划分，使用如下的伪代码\nfunction split_and_reverse_sort_number(number):\n    number_str = str(number)\n    parts = []\n    while number_str:\n        part, number_str = number_str[-4:], number_str[:-4]\n        parts.insert(0, part)\n    parts.sort(reverse=True)\n    return parts\n这个函数代码可以将这个整数划分为3个部分「1」和「2345」和「6789」；\n2、有3个部分，所以第一个部分写出它的中文读法后要在后面加上一个「亿」字，第二个部分写出它的中文读法后要在后面加上一个「万」字，第三个部分直接写出它的中文读法即可；\n3、从左到右依次可以写出一亿二千三百四十五万六千七百八十九。\n所以答案是一亿二千三百四十五万六千七百八十九。\n题目：123456789012 \n答案：让我们一步一步思考。\n1、首先将这个整数进行划分，使用如下的伪代码\nfunction split_and_reverse_sort_number(number):\n    number_str = str(number)\n    parts = []\n    while number_str:\n        part, number_str = number_str[-4:], number_str[:-4]\n        parts.insert(0, part)\n    parts.sort(reverse=True)\n    return parts\n这个函数代码可以将这个整数划分为3个部分「1234」和「5678」和「9012」；\n2、有3个部分，所以第一个部分写出它的中文读法后要在后面加上一个「亿」字，第二个部分写出它的中文读法后要在后面加上一个「万」字，第三个部分直接写出它的中文读法即可；\n3、从左到右依次可以写出一千二百三十四亿五千六百七十八万九千零一十二。\n所以答案是一千二百三十四亿五千六百七十八万九千零一十二。\n题目：XXX\n答案：让我们一步一步思考。"
        #quesion = "以下是关于整数转为中文读法的题目，请根据题目的数字，给出正确的答案。\n题目：123 \n答案：让我们一步一步思考。1、首先将这个整数进行从低位到高位按顺序的划分，每四位数字组成一个级别，可以将这个整数划分为一个级别123，只有一个级别，所以123是个级；2、每级末尾不管有几个0，都不用读这个0，其他数位上有一个0或连续几个0，都只读一次\"零\"；3、个级的123，读作一百二十三；所以答案是一百二十三。\n题目：123456 \n答案：让我们一步一步思考。1、首先将这个整数进行从低位到高位按顺序的划分，每四位数字组成一个级别，可以将这个整数划分为两个级别12和3456，其中3456是个级，12是万级；2、先读万级，再读个级。每级末尾不管有几个0，都不用读这个0，其他数位上有一个0或连续几个0，都只读一次\"零\"；3、万级的数，要按照个级的数的读法来读，再在后面加上一个\"万\"字，所以万级的12读作十二万；4、个级则不用加，所以个级的3456读作三千四百五十六；所以答案是十二万三千四百五十六。\n题目：123456789 \n答案：让我们一步一步思考。1、首先将这个整数进行从低位到高位按顺序的划分，每四位数字组成一个级别，可以将这个整数划分为三个级别1和2345和6789，其中6789是个级，2345是万级，1是亿级；2、先读亿级，再读万级，最后读个级。每级末尾不管有几个0，都不用读这个0，其他数位上有一个0或连续几个0，都只读一次\"零\"；3、亿级的数，要按照个级的数的读法来读，再在后面加上一个\"亿\"字，所以亿级的1读作一亿；4、万级的数，要按照个级的数的读法来读，再在后面加上一个\"万\"字，所以万级的2345读作二千三百四十五万；5、个级则不用加，所以个级的6789读作六千七百八十九；所以答案是一亿二千三百四十五万六千七百八十九。\n题目：123456789012 \n答案：让我们一步一步思考。1、首先将这个整数进行从低位到高位按顺序的划分，每四位数字组成一个级别，可以将这个整数划分为三个级别1234和5678和9012，其中9012是个级，5678是万级，1234是亿级；2、先读亿级，再读万级，最后读个级。每级末尾不管有几个0，都不用读这个0，其他数位上有一个0或连续几个0，都只读一次\"零\"；3、亿级的数，要按照个级的数的读法来读，再在后面加上一个\"亿\"字，所以亿级的1234读作一千二百三十四亿；4、万级的数，要按照个级的数的读法来读，再在后面加上一个\"万\"字。所以万级的5678读作五千六百七十八万；5、个级则不用加，所以个级的9012读作九千零一十二；所以答案是一千二百三十四亿五千六百七十八万九千零一十二。\n题目：XXX\n答案：让我们一步一步思考。"
        #quesion = "以下是关于整数转为中文读法的题目，请根据题目的数字，给出正确的答案。\n题目：XXX\n答案：让我们一步一步思考。"
        #quesion = "以下是关于整数转为中文读法的题目，请根据题目的数字，给出正确的答案。题目：123456 答案：让我们一步一步思考。首先，我们可以将数字123456分解为十万位、万位、千位、百位、十位和个位的数字。然后，根据中文读法，将每个位上的数字转换为对应的中文数字。对于123456来说，它的十万位是1，万位是2，千位是3，百位是4，十位是5，个位是6。因此，它的中文读法是：十万位：一十、万位：二万、千位：三千、百位：四百、十位：五十、个位：六。将这些部分组合起来，答案是：十二万三千四百五十六。以下是关于整数转为中文读法的题目，请根据题目的数字，给出正确的答案。题目：930042210 答案：让我们一步一步思考。首先，我们可以将数字930042210分解为亿位、千万位、百万位、十万位、万位、千位、百位、十位和个位的数字。然后，根据中文读法，将每个位上的数字转换为对应的中文数字。对于930042210来说，它的亿位是9，千万位是3，百万位是0，十万位是0，万位是4，千位是2，百位是2，十位是1，个位是0。因此，它的中文读法是：亿位：九亿、千万位：三千、百万位：零、十万位：零、万位：四万、千位：二千、百位：二百、十位：一十、个位：零。将这些部分组合起来，答案是：九亿三千零四万二千二百一十。以下是关于整数转为中文读法的题目，请根据题目的数字，给出正确的答案。题目：930042210692 答案：让我们一步一步思考。首先，我们可以将数字930042210692分解为千亿位、百亿位、十亿位、亿位、千万位、百万位、十万位、万位、千位、百位、十位、个位的数字。然后，根据中文读法，将每个位上的数字转换为对应的中文数字。对于930042210692来说，它的千亿位是9，百亿位是3，十亿位是0，亿位是0，千万位是4，百万位是2，十万位是2，万位是1，千位是0，百位是6，十位是9，个位是2。因此，它的中文读法是：千亿位：九千、百亿位：三百、十亿位：零、亿位：零、千万位：四千、百万位：二百、十万位：二十、万位：一万、千位：零、百位：六百、十位：九十、个位：二。将这些部分组合起来，答案是：九千三百亿四千二百二十一万零六百九十二。以下是关于整数转为中文读法的题目，请根据题目的数字，给出正确的答案。 题目：XXX 答案：让我们一步一步思考。"
        #quesion = "以下是关于整数转为中文读法的题目，请根据题目的数字，给出正确的答案。\n题目：123 \n答案：让我们一步一步思考。\n1、这个整数的长度一共是3位，按照中文的语法，3位数字是百级别的数字；\n2、从左到右依次可以写出一百二十三。\n所以答案是一百二十三。\n题目：123456 \n答案：让我们一步一步思考。\n1、这个整数的长度一共是6位，按照中文的语法，6位数字是十万级别的数字；\n2、从左到右依次可以写出十二万三千四百五十六。\n所以答案是十二万三千四百五十六。\n题目：123456789 \n答案：让我们一步一步思考。\n1、这个整数的长度一共是9位，按照中文的语法，9位数字是亿级别的数字；\n2、从左到右依次可以写出一亿二千三百四十五万六千七百八十九。\n所以答案是一亿二千三百四十五万六千七百八十九。\n题目：123456789012 \n答案：让我们一步一步思考。\n1、这个整数的长度一共是12位，按照中文的语法，12位数字是千亿级别的数字；\n2、从左到右依次可以写出一千二百三十四亿五千六百七十八万九千零一十二。\n所以答案是一千二百三十四亿五千六百七十八万九千零一十二。\n题目：XXX\n答案：让我们一步一步思考。\n"
        #quesion = "以下是关于整数转为中文读法的题目，请根据题目的数字，给出正确的答案。\n题目：930042210692 \n答案：让我们一步一步思考。\n1、首先，我们可以将数字930042210692分解为千亿位、百亿位、十亿位、亿位、千万位、百万位、十万位、万位、千位、百位、十位、个位的数字。\n2、然后，根据中文读法，将每个位上的数字转换为对应的中文数字。对于930042210692来说，它的千亿位是9，百亿位是3，十亿位是0，亿位是0，千万位是4，百万位是2，十万位是2，万位是1，千位是0，百位是6，十位是9，个位是2。\n3、因此，它的中文读法是：千亿位：九千、百亿位：三百、十亿位：零、亿位：零、千万位：四千、百万位：二百、十万位：二十、万位：一万、千位：零、百位：六百、十位：九十、个位：二。\n4、将这些部分组合起来，答案是：九千三百亿四千二百二十一万零六百九十二。\n以下是关于整数转为中文读法的题目，请根据题目的数字，给出正确的答案。 \n题目：XXX \n答案：让我们一步一步思考。"
        #quesion = "以下是关于整数转为中文读法的题目，请根据题目的数字，给出正确的答案。\n题目：123456 \n答案：1、首先，我们可以将数字123456分解为十万位、万位、千位、百位、十位和个位的数字。\n2、然后，根据中文读法，将每个位上的数字转换为对应的中文数字。对于123456来说，它的十万位是1，万位是2，千位是3，百位是4，十位是5，个位是6。\n3、因此，它的中文读法是：十万位：一十、万位：二万、千位：三千、百位：四百、十位：五十、个位：六。\n4、将这些部分组合起来，答案是：十二万三千四百五十六。\n\n以下是关于整数转为中文读法的题目，请根据题目的数字，给出正确的答案。\n题目：930042210 \n答案：1、首先，我们可以将数字930042210分解为亿位、千万位、百万位、十万位、万位、千位、百位、十位和个位的数字。\n2、然后，根据中文读法，将每个位上的数字转换为对应的中文数字。对于930042210来说，它的亿位是9，千万位是3，百万位是0，十万位是0，万位是4，千位是2，百位是2，十位是1，个位是0。\n3、因此，它的中文读法是：亿位：九亿、千万位：三千、百万位：零、十万位：零、万位：四万、千位：二千、百位：二百、十位：一十、个位：零。\n4、将这些部分组合起来，答案是：九亿三千零四万二千二百一十。\n\n以下是关于整数转为中文读法的题目，请根据题目的数字，给出正确的答案。\n题目：930042210692 \n答案：1、首先，我们可以将数字930042210692分解为千亿位、百亿位、十亿位、亿位、千万位、百万位、十万位、万位、千位、百位、十位、个位的数字。\n2、然后，根据中文读法，将每个位上的数字转换为对应的中文数字。对于930042210692来说，它的千亿位是9，百亿位是3，十亿位是0，亿位是0，千万位是4，百万位是2，十万位是2，万位是1，千位是0，百位是6，十位是9，个位是2。\n3、因此，它的中文读法是：千亿位：九千、百亿位：三百、十亿位：零、亿位：零、千万位：四千、百万位：二百、十万位：二十、万位：一万、千位：零、百位：六百、十位：九十、个位：二。\n4、将这些部分组合起来，答案是：九千三百亿四千二百二十一万零六百九十二。\n\n以下是关于整数转为中文读法的题目，请根据题目的数字，给出正确的答案。 \n题目：XXX \n答案："
        # quesion = "以下是关于整数转为中文读法的题目，请根据题目的数字，给出正确的答案。\n题目：XXX\n答案："
        prompt_json = get_json("prompt.json")
        quesion = prompt_json['zeroshot']['num2word_en_integer']
        for number, answer in item.items():
            need_handle = 10
            while(need_handle > 0):
                time.sleep(3)
                number = str(number)
                quesion = quesion.replace("XXX", number)
                response = call_api(model, quesion)
                print(f'{index + 1}-quesion:{quesion}{response}')
                if "出现问题，需要重跑" in response:
                    need_handle -= 1
                else:
                    need_handle = 0
            new_row = [
                'medium',
                number,
                answer,
                response,  # chatGPT_answer
                score(answer, response),  # chatGPT_answer_score
            ]
            print(">>>>>>>>>>>>>>>", index + 1, "<<<<<<<<<<<<<<<<",
                  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), new_row)
        new_data_subset.append(new_row)
    result_queue.put((subset_index, new_data_subset))

def process_data(model, machine_num):
    try:
        datas = generate_exist_data(0)
        data_subsets = [datas[i::machine_num] for i in range(machine_num)]

        threads = []
        result_queue = queue.Queue()

        for i, data_subset in enumerate(data_subsets):
            thread = threading.Thread(target=process_data_subset, args=(data_subset, model, result_queue, i))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        new_data = [None] * machine_num
        while not result_queue.empty():
            subset_index, subset_data = result_queue.get()
            new_data[subset_index] = subset_data

        new_data = [row for subset in new_data for row in subset]

        with open(f'num2word_{model}_medium_zh{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}_{len(new_data)}.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # 写入列名
            writer.writerow(['level', 'number', 'answer','chatGPT_numcot_answer', 'chatGPT_numcot_score'])
            # 写入数据
            writer.writerows(new_data)
        print(f"success. Data saved to 'num2word_{model}_medium_zh{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{len(new_data)}.csv'")
    except Exception as e:
        # 如果发生错误，保存已处理的数据
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        with open(f'num2word_{model}_medium_zh{timestamp}_{len(new_data)}.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['level', 'number', 'answer','chatGPT_numcot_answer', 'chatGPT_numcot_score'])
            writer.writerows(new_data)
        print(f"An error occurred: {e}. Data saved to 'num2word_{model}_medium_zh{timestamp}_{len(new_data)}.csv'")

# 调用函数
process_data('chatGPT', 20)
