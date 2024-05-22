import random
import re
import csv
import os

def length_decimal(num_str):
    # 分割字符串以小数点为界
    parts = num_str.split(".")

    # 检查是否有小数点及小数点后的位数
    if len(parts) > 1:
        return len(parts[1])
    else:
        # 如果没有小数点，返回0
        return 0

def generate_easy_question():
    # 单位转换关系
    random_seed = random.randint(1, 4)
    units = []
    if random_seed % 4 == 0:
        units = ['吨', '千克', '克', '毫克']
    elif random_seed % 4 == 1:
        units = ['周', '天', '小时', '分钟', '秒钟', '毫秒']
    elif random_seed % 4 == 2:
        units = ['千米', '米', '分米', '厘米', '毫米']
    elif random_seed % 4 == 3:
        units = ['元', '角', '分钱']
    # 随机选择两个不同的单位
    unit1 = random.choice(units)
    units.remove(unit1)
    unit2 = random.choice(units)
    # 生成随机数
    number = random.randint(100, 10000)
    # 构造转换公式
    question = f"{number}{unit1}=？{unit2}"
    return question
def solve_easy_question(question):
    # 单位转换关系
    if '克' in question:
        conversions = {"吨": 1000000000, "千克": 1000000, "克": 1000, "毫克": 1}
    elif '天' in question or '周' in question or '小时' in question or '分钟' in question or '秒' in question:
        conversions = {"周": 7 * 24 * 60 * 60 * 1000, "天": 24 * 60 * 60 * 1000, "小时": 60 * 60 * 1000, "分钟": 60 * 1000, "秒钟": 1000, "毫秒": 1}
    elif '米' in question:
        conversions = {"千米": 1000 * 1000, "米": 1000, "分米": 100, "厘米": 10, "毫米": 1}
    elif '元' in question or '角' in question or '分钱' in question:
        conversions = {"元": 100, "角": 10, "分钱": 1}
    parts = question.split('=')
    number_part = parts[0].strip()
    # 使用正则表达式匹配数字
    match = re.search(r'\d+', number_part)
    if match:
        value = int(match.group())
    else:
        raise ValueError("无法解析数字")
    # 提取单位
    unit1 = number_part.replace(str(value), '').strip()
    unit2 = parts[1].strip().replace('？', '').strip()
    # 计算转换
    conversion_factor = conversions[unit1] / conversions[unit2]
    result = value * conversion_factor

    # 检查结果是否为整数
    if result.is_integer():
        return int(result)
    else:
        return result

def generate_medium_question():
    # 定义转换关系
    conversions =  [("吨", "千克", 1000), ("千克", "克", 1000), ("克", "毫克", 1000),
                    ("周", "天", 7), ("天", "小时", 24), ("小时", "分钟", 60), ("分钟", "秒钟", 60), ("秒钟", "毫秒", 1000),
                    ("千米", "米", 1000), ("米", "分米", 10), ("分米", "厘米", 10), ("厘米", "毫米", 10),
                    ("元","角",10), ("角","分钱",10)]
    # 随机选择一个转换条件
    unit1, unit2, factor = random.choice(conversions)
    # 生成两个随机整数
    num1 = random.randint(1, 1000)
    num2 = random.randint(1, 1000)
    # 随机选择加号或减号
    operation = random.choice(["+", "-"])
    # 生成第一部分的表达式
    expression = f"{num1}{unit1} {operation} {num2}{unit2}"
    # 从两个单位中随机选择一个作为最终单位
    final_unit = random.choice([unit1, unit2])
    # 生成完整的等式
    full_expression = f"{expression} = ?{final_unit}"
    return full_expression
def solve_medium_question(question):
    # 定义转换关系
    conversion_factors = {
        "吨": {"千克": 1000},"千克": {"吨": 1/1000, "克": 1000},"克": {"千克": 1/1000, "毫克": 1000},
        "毫克": {"克": 1/1000},"周": {"天": 7},"天": {"周": 1/7, "小时": 24},"小时":{"天": 1/24, "分钟": 60},
        "分钟":{"小时": 1/60, "秒钟": 60},"秒钟":{"分钟":1/60, "毫秒": 1000},"毫秒":{"秒钟":1/1000},
        "千米": {"米":1000},"米":{"千米":1/1000, "分米": 10},"分米":{"米":1/10, "厘米": 10},
        "厘米":{"分米":1/10, "毫米": 10},"毫米": {"厘米": 1/10},
        "元":{"角": 10}, "角":{"元": 1/10, "分钱": 10}, "分钱":{"角": 1/10}
    }
    # 解析输入字符串
    parts = question.split()
    match1 = re.match(r"(\d+)(\D+)", parts[0])
    num1, unit1 = int(match1.group(1)), match1.group(2).strip()
    operation = parts[1]
    match2 = re.match(r"(\d+)(\D+)", parts[2])
    num2, unit2 = int(match2.group(1)), match2.group(2).strip()
    final_unit = parts[-1][1:]
    # 转换第一个数值到目标单位
    while unit1 != final_unit:
        num1 *= conversion_factors[unit1][final_unit]
        unit1 = final_unit
    # 转换第二个数值到目标单位
    while unit2 != final_unit:
        num2 *= conversion_factors[unit2][final_unit]
        unit2 = final_unit
    # 计算结果
    if operation == "+":
        result = num1 + num2
    else:
        result = num1 - num2

    # 检查结果是否为整数
    if float(result).is_integer():
        return int(result)
    else:
        return result


def generate_hard_question():
    #随机决定要产生哪种单位的问题, 预设单位转换条件
    random_seed = random.randint(1, 4)
    conditions = []
    if random_seed % 4 == 0:
        conditions = [("吨", "千克", 1000), ("千克", "克", 1000), ("克", "毫克", 1000)]
    elif random_seed % 4 == 1:
        conditions = [("周", "天", 7), ("天", "小时", 24), ("小时", "分钟", 60), ("分钟", "秒钟", 60), ("秒钟", "毫秒", 1000)]
    elif random_seed % 4 == 2:
        conditions = [("千米", "米", 1000), ("米", "分米", 10), ("分米", "厘米", 10), ("厘米", "毫米", 10)]
    elif random_seed % 4 == 3:
        conditions = [("元", "角", 10), ("角", "分钱", 10)]
    # 随机选择一组条件
    unit1, unit2, _ = random.choice(conditions)
    # 生成随机数
    num1 = random.randint(1, 10)
    num2 = random.randint(10, 1000)
    # 第三步随机选择单位和生成num3
    chosen_unit = random.choice([unit1, unit2])
    num3 = random.randint(10, 100)
    # 构建拼接单位
    combined_units_1 = f"{num1}{unit1}{num2}{unit2}"
    combined_units_2 = f"{num3}{chosen_unit}"
    # 随机选择加号或减号
    operator = random.choice(["+", "-"])
    # 构建表达式
    expression = f"{combined_units_1} {operator} {combined_units_2}"
    # 构建问号表示的转换条件
    conversion = f"?{unit1}?{unit2}"
    # 最终结果
    result = f"{expression} = {conversion}"
    return result

def solve_hard_question(expression):
    matches = []
    conversion_rates = []
    if '克'  in expression :
        # 正则表达式匹配数字和单位
        matches = re.findall(r'(\d+)([吨千克克毫克]+)', expression)
        # 预设转换条件
        conversion_rates = {"吨": 1000000000, "千克": 1000000, "克": 1000, "毫克": 1}
    elif  '天' in expression or '周' in expression or'小时' in expression or '分钟' in expression or '秒' in expression:
        matches = re.findall(r'(\d+)([周天小时分钟秒钟毫秒]+)', expression)
        conversion_rates = {"周": 7*24*60*60*1000, "天": 24*60*60*1000, "小时": 60*60*1000, "分钟": 60*1000, "秒钟": 1000, "毫秒": 1}
    elif '米' in expression:
        matches = re.findall(r'(\d+)([千米米分米厘米毫米]+)', expression)
        conversion_rates = {"千米": 1000*1000, "米": 1000, "分米": 100, "厘米": 10, "毫米": 1}
    elif '元' in expression or '角' in expression or '分钱' in expression:
        matches = re.findall(r'(\d+)([元角分钱"]+)', expression)
        conversion_rates = {"元": 100, "角": 10, "分钱": 1}
    # 解析数值和单位，并进行转换
    total_milligrams = 0
    for num, unit in matches:
        total_milligrams += int(num) * conversion_rates[unit]
    # 检查是否有减法操作
    if '-' in expression:
        tuple = matches[2]
        num = tuple[0]
        unit = tuple[1]
        second_value = int(num) * conversion_rates[unit]
        total_milligrams -= 2*second_value
    # 转换回原始单位
    original_units = re.findall(r'\?(\w+)', expression)
    unit1, unit2 = original_units[0], original_units[1]
    value1 = total_milligrams // conversion_rates[unit1]
    remaining_milligrams = total_milligrams % conversion_rates[unit1]
    value2 = remaining_milligrams // conversion_rates[unit2]
    return value1, value2, unit1, unit2




#读取指定的CSV文件，将文件中的特定字符串替换为其他字符串，然后将修改后的内容保存到一个新的CSV文件中
def replace_in_csv(file_path):
    # 预设的替换规则
    replacements = {
        '？': ' ? ',
        '吨': ' tons ',
        '千克': ' kilograms ',
        '毫克': ' milligrams ',
        '周': ' weeks ',
        '天': ' days ',
        '小时': ' hours ',
        '分钟': ' minutes ',
        '秒钟': ' seconds ',
        '毫秒': ' milliseconds ',
        '千米': ' kilometers ',
        '分米': ' decimeters ',
        '厘米': ' centimeters ',
        '毫米': ' millimeters ',
        '元': ' yuan ',
        '角': ' jiao ',
        '分钱': ' fen '
    }

    # 生成新文件的路径
    file_dir, file_name = os.path.split(file_path)
    name_part, ext = os.path.splitext(file_name)
    output_path = os.path.join(file_dir, f"{name_part}_new{ext}")

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            rows = list(csv.reader(file))

            for row in rows:
                for i, cell in enumerate(row):
                    for key, value in replacements.items():
                        # 检查并替换所有关键词
                        cell = cell.replace(key, value)
                    row[i] = cell

        # 将修改后的数据写入新的CSV文件
        with open(output_path, 'w', encoding='utf-8', newline='') as new_file:
            writer = csv.writer(new_file)
            writer.writerows(rows)

        print(f"文件已成功保存到 {output_path}")

    except FileNotFoundError:
        print("指定的文件未找到。")
    except Exception as e:
        print(f"处理文件时出现错误: {e}")
