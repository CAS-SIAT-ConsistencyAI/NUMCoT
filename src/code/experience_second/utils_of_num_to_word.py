import csv
import os
import random
import cn2an
import num2words
import re

# 生成require_number个介于10亿到100亿之间的整数
def generate_integer_lower_10B(require_number):
    numbers = [random.randint(1_000_000_000, 10_000_000_000) for _ in range(require_number)]
    return numbers

# 生成require_number个分子和分母都不超过max_limit的分数，返回的是字符串list
def generate_fraction(require_number, max_limit):
    fractions = []
    for index in range(require_number):
        numerator = random.randint(1, max_limit)
        denominator = random.randint(1, max_limit)
        fractions.append(f"{numerator}/{denominator}")
    return fractions

# 生成require_number个整数和小数都不超过max_limit的浮点数据，返回的是字符串list
def generate_decimal(require_number, max_limit):
    decimals = []
    for index in range(require_number):
        int_part = random.randint(1, max_limit)
        decimal_part = random.randint(1, max_limit)
        decimals.append(f"{int_part}.{decimal_part}")
    return decimals

def remove_0_bewteen_wan_and_qian(text):
    index = 0
    while index < len(text) - 2:
        substring = text[index:index + 4]  # 获取当前字符及之后的两个字符
        if '亿' == text[index:index+1] and '千' == text[index+3:index+4] and '零' in substring:
            zero_index = substring.find('零')
            index_to_replace = zero_index + index
            text = text[:index_to_replace] + text[index_to_replace + 1:]
        if '万' == text[index:index+1] and '千' == text[index+3:index+4] and '零' in substring:
            zero_index = substring.find('零')
            index_to_replace = zero_index + index
            text = text[:index_to_replace] + text[index_to_replace + 1:]
        index += 1
    return text

# 将数字转为中文表达
def num_to_chinese(number):
    text = cn2an.an2cn(str(number))
    return remove_0_bewteen_wan_and_qian(text)

# 将数字转为英文表达，全小写
def num_to_english(number):
    result = num2words.num2words(number).replace(",", "").replace("-", " ").replace(" and ", " ")
    return result

# 将分数转为中文表达
def fraction_num_to_chinese(number):
    nums = str(number).split("/")
    return f"{remove_0_bewteen_wan_and_qian(cn2an.an2cn(nums[1]))}分之{remove_0_bewteen_wan_and_qian(cn2an.an2cn(nums[0]))}"

# 将分数转为英文表达，全小写
def fraction_num_to_english(number):
    nums = str(number).split("/")
    return f"{num_to_english(int(nums[0]))} over {num_to_english(int(nums[1]))}"

# 将百分比转为中文表达
def percent_num_to_chinese(number):
    nums = str(number).split("%")
    return f"百分之{remove_0_bewteen_wan_and_qian(cn2an.an2cn(nums[0].rstrip('0')))}"

# 将百分比转为英文表达
def percent_num_to_english(number):
    nums = str(number).split("%")
    return f"{num_to_english(nums[0].rstrip('0'))} percent"

# 繁体中文数字到简体中文数字的映射
def traditional_to_simplified(chinese_number):
    trad_to_simp_map = {'壹': '一', '貳': '二','贰': '二', '两': '二', '叁': '三', '肆': '四',
        '伍': '五', '陸': '六', '陆': '六', '柒': '七', '捌': '八', '玖': '九',
        '拾': '十', '佰': '百', '仟': '千', '萬': '万', '億': '亿'}
    # 将繁体中文数字转换为简体
    simplified_number = "".join(trad_to_simp_map.get(char, char) for char in chinese_number)
    return simplified_number

# 生成一个类似于Num2Words_integer的csv文件
'''
data = [['easy', 'identity', '123456', '你是谁1', 'helloworld1', '你是谁21', '1/0', 'good morning1', '0/1'],
['hard', 'identity', '223456', '你是谁2', 'helloworld2', '你是谁22', '2/0', 'good morning2', '0/2']],
column_names = ['level', 'operation', 'number', 'zh', 'en', 'chatchat_ZH', 'chatchat_ZH_Score', 'chatchat_EN', 'chatchat_EN_Score']
'''
def create_csv_from_nested_list(data, column_names, file_name='world.csv', directory='.'):
    # 检查数据是否合法
    if not all(len(row) == len(column_names) for row in data):
        raise ValueError("所有行的长度必须与列名数量相同")
    # 构造完整的文件路径
    full_path = os.path.join(directory, file_name)
    # 创建目录（如果不存在）
    if not os.path.exists(directory):
        os.makedirs(directory)
    # 将数据写入CSV文件
    with open(full_path , 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(column_names)  # 写入列名
        writer.writerows(data)  # 写入数据
    print(f"文件 '{file_name}' 已成功创建。")

# 接受 'subtraction', 'addition', 或 'shifting'，对整数进行操作
def process_number(number, operation):
    if operation == 'identity':
        return number
    if operation == 'subtraction':
        return number - 1
    elif operation == 'addition':
        return number + 1
    elif operation == 'shifting':
        return number * 10
    elif operation == 'progression':
        num_str = str(number)
        shifted = num_str[1:] + num_str[0]
        shifted_no_leading_zeros = int(shifted)
        return shifted_no_leading_zeros
    else:
        raise ValueError("无效的操作。只接受 'subtraction', 'addition', 'shifting' 或 'progression'。")

def generate_random_int_data(start, end, int_time, is_need_easy_set, operators, num2words_complete_nums):
    for i in range(int_time):
        num = random.randint(start, end)
        for op in operators:
            row = []
            new_num = process_number(num, op)
            row.append("medium")
            row.append(op)
            row.append(str(new_num))
            row.append(num_to_chinese(new_num))
            row.append(num_to_english(new_num))
            for _ in range(32):
                row.append("")
            num2words_complete_nums.append(row)

    if is_need_easy_set:
        step = start
        easy_num = start
        for i in range(3):
            for j in range(9):
                row = []
                row.append("easy")
                row.append("identity")
                row.append(str(easy_num))
                row.append(num_to_chinese(easy_num))
                row.append(num_to_english(easy_num))
                for _ in range(32):
                    row.append("")
                num2words_complete_nums.append(row)
                easy_num += step
            step *= 10
            easy_num = step
    return num2words_complete_nums

def generate_random_fraction_data(fraction_time, decimal_time, num2words_fracture_nums):
    for i in range(fraction_time):
        numerator = random.randint(1, 10000000)
        denominator = random.randint(1, 10000000)
        row = []
        fractional_num = f"{numerator}/{denominator}"
        row.append("hard")
        row.append("identity")
        row.append(fractional_num)
        row.append(fraction_num_to_chinese(fractional_num))
        row.append(fraction_num_to_english(fractional_num))
        for _ in range(32):
            row.append("")
        num2words_fracture_nums.append(row)
    for index in range(decimal_time):
        int_part = random.randint(1, 100000)
        decimal_part = random.randint(100000, 1000000000)
        while decimal_part % 10 == 0:
            decimal_part = random.randint(100000, 1000000000)
        row = []
        decimal_num = f"{int_part}.{decimal_part}"
        row.append("hard")
        row.append("identity")
        row.append(decimal_num)
        row.append(num_to_chinese(decimal_num))
        row.append(num_to_english(decimal_num))
        for _ in range(32):
            row.append("")
        num2words_fracture_nums.append(row)
    return num2words_fracture_nums

# 按照论文的3.1实验生成数据
def generate_data_in_num2word():
    num2words_complete_plus_fracture_nums = []
    operators = ['identity', 'subtraction', 'addition', 'shifting', 'progression']
    # 整数
    num2words_complete_plus_fracture_nums = generate_random_int_data(1, 999, 15, True, operators, num2words_complete_plus_fracture_nums)
    num2words_complete_plus_fracture_nums = generate_random_int_data(1000, 999999, 15, True, operators, num2words_complete_plus_fracture_nums)
    num2words_complete_plus_fracture_nums = generate_random_int_data(1000000, 999999999, 15, True, operators, num2words_complete_plus_fracture_nums)
    num2words_complete_plus_fracture_nums = generate_random_int_data(1000000000, 999999999999, 15, True, operators, num2words_complete_plus_fracture_nums)
    # 分数
    num2words_complete_plus_fracture_nums = generate_random_fraction_data(150, 150, num2words_complete_plus_fracture_nums)
    #混合
    num2words_complete_plus_fracture_nums = generate_random_int_data(1, 999, 10, False, operators, num2words_complete_plus_fracture_nums)
    num2words_complete_plus_fracture_nums = generate_random_int_data(1000, 999999, 10, False, operators, num2words_complete_plus_fracture_nums)
    num2words_complete_plus_fracture_nums = generate_random_int_data(1000000, 999999999, 10, False, operators, num2words_complete_plus_fracture_nums)
    num2words_complete_plus_fracture_nums = generate_random_int_data(1000000000, 999999999999, 10, False, operators, num2words_complete_plus_fracture_nums)
    num2words_complete_plus_fracture_nums = generate_random_fraction_data(50, 50, num2words_complete_plus_fracture_nums)
    return num2words_complete_plus_fracture_nums