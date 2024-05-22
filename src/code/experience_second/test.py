from generate_data import *
import pandas as pd


def process_csv_files(directory="C:/"):
    counts = {}  # 用于存储文件名和对应的计数
    problem_details = {}  # 存储问题单元格的详细信息

    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            var_name = os.path.splitext(filename)[0]
            count = 0  # 为当前文件初始化计数器

            # 读取CSV文件
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path)

            # 遍历每一行
            for index, row in df.iterrows():
                # 对每一行中的每个元素进行检查
                for col_name, element in row.items():
                    if "出现问题，需要重跑" in str(element):
                        count += 1
                        # 记录问题单元格的详细信息
                        if var_name not in problem_details:
                            problem_details[var_name] = []
                        problem_details[var_name].append((index + 1, col_name, row['question'], row['answer']))

            # 将计数值存储在字典中
            counts[var_name] = count

    # 按计数值从大到小排序并输出
    for file, count in sorted(counts.items(), key=lambda item: item[1], reverse=True):
        print(f"{file}: {count}")
        if file in problem_details:
            for row_index, col_name, number_value, answer in problem_details[file]:
                response = ''
                score = ''
                # model = 'chatGPT'
                # if 'word2num' in file:
                #     task = 'word2num'
                # else:
                #     task = 'num2word'
                # if '_zh_' in file:
                #     language = 'zh'
                # else:
                #     language = 'en'
                # if 'cot_zeroshot' in col_name:
                #     shot = 'cot_zeroshot'
                # elif 'zeroshot' in col_name:
                #     shot = 'zeroshot'
                # elif 'cot_fewshot' in col_name:
                #     shot = 'cot_fewshot'
                # else:
                #     shot = 'fewshot'
                # quesion = format_quesion(language, task, 'integer', number_value, shot)
                # response = call_api(model, quesion, True)
                # score = score_function(str(answer), response, task, language)
                print(f"    - Problem at Row {row_index}, Column '{col_name}', question: {number_value}, Response: {response}, score: {score}")


process_csv_files()