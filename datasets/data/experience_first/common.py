import json
from chat_api import *

def get_json(json_file_path):
    # 打开并读取 JSON 文件
    with open(json_file_path, 'r', encoding='utf-8-sig') as json_file:
        # 将 JSON 数据加载为 Python 字典
        data = json.load(json_file)
    return data

def call_api(model, quesion, format=False):
    if model == 'chatGPT':
        return chat_gpt35(quesion, format)
    if model == 'chatglm26b':
        return chat_chatglm26b(quesion, format)
    if model == 'wenxinyy':
        return chat_wenxinyy(quesion, format)
    if model == 'zhipu':
        return chat_zhipu(quesion, format)
    return f"model错误，传入的是{model}，出现问题，需要重跑"

"""将提供的带有角色的文本转换为 JSON 格式。
参数:text (str): 包含 user 和 assistant 角色的文本
返回:list: 包含角色和内容的 JSON 结构列表"""
def text_to_json_with_roles(text):
    # 首先按照 "题目：" 分割整个文本
    segments = text.strip().split("题目：")
    json_output = []

    for segment in segments[1:]:  # 跳过第一个空元素
        # 再按照 "答案：" 分割每个段落
        question, answer = segment.split("答案：")
        json_output.append({"role": "user", "content": "题目：" + question.strip()})
        json_output.append({"role": "assistant", "content": "答案：" + answer.strip()})

    return json_output


def format_quesion(language='zh', task='num2word', type='integer', quesion='', shot='zeroshot'):
    prompt = ''
    if task == 'num2word':
        if language == "zh":
            if type == 'integer':
                prompt = [{"role": "system", "content": "你是一个数学优秀的中文人工智能助手，以下是关于整数转为中文读法的题目，请根据题目的数字，给出正确的答案。"}]
                if shot == 'zeroshot':
                    prompt += [{"role": "user", "content":f"以下是关于整数转为中文读法的题目，请根据题目的数字，给出正确的答案。 题目：{quesion} 答案："}]
                if shot == 'cot_zeroshot':
                    prompt += [{"role": "user", "content":f"以下是关于整数转为中文读法的题目，请根据题目的数字，给出正确的答案。 题目：{quesion} 答案：让我们一步一步思考，"}]
                if shot == 'fewshot':
                    prompt += [{"role": "user", "content": "以下是关于整数转为中文读法的题目，请根据题目的数字，给出正确的答案。 题目：123 答案："},
                               {"role": "assistant", "content": "一百二十三"},
                               {"role": "user", "content": "以下是关于整数转为中文读法的题目，请根据题目的数字，给出正确的答案。 题目：123456 答案："},
                               {"role": "assistant", "content": "十二万三千四百五十六"},
                               {"role": "user", "content": "以下是关于整数转为中文读法的题目，请根据题目的数字，给出正确的答案。 题目：123456789 答案："},
                               {"role": "assistant", "content": "一亿二千三百四十五万六千七百八十九"},
                               {"role": "user", "content": "以下是关于整数转为中文读法的题目，请根据题目的数字，给出正确的答案。 题目：123456789012 答案："},
                               {"role": "assistant", "content": "一千二百三十四亿五千六百七十八万九千零一十二"},
                               {"role": "user", "content":f"以下是关于整数转为中文读法的题目，请根据题目的数字，给出正确的答案。 题目：{quesion} 答案："}]
                if shot == 'cot_fewshot':
                    prompt += [{"role": "user", "content": "以下是关于整数转为中文读法的题目，请根据题目的数字，给出正确的答案。 题目：123 答案：让我们一步一步思考，"},
                               {"role": "assistant", "content": "1、这个整数的长度一共是3位，按照中文的语法，3位数字是百级别的数字；2、这个数字从高到低，各级别分别读作：一百、二十、三；3、从左到右依次可以写出一百二十三。所以答案是一百二十三。"},
                               {"role": "user", "content": "以下是关于整数转为中文读法的题目，请根据题目的数字，给出正确的答案。 题目：123456 答案：让我们一步一步思考，"},
                               {"role": "assistant", "content": "1、这个整数的长度一共是6位，按照中文的语法，6位数字是十万级别的数字；2、这个数字从高到低，各级别分别读作：十万、二万、三千、四百、五十、六；3、从左到右依次可以写出十二万三千四百五十六。所以答案是十二万三千四百五十六。"},
                               {"role": "user", "content": "以下是关于整数转为中文读法的题目，请根据题目的数字，给出正确的答案。 题目：123456789 答案：让我们一步一步思考，"},
                               {"role": "assistant", "content": "1、这个整数的长度一共是9位，按照中文的语法，9位数字是亿级别的数字；2、这个数字从高到低，各级别分别读作：一亿、二千万、三百万、四十万、五万、六千、七百、八十、九；3、从左到右依次可以写出一亿二千三百四十五万六千七百八十九。所以答案是一亿二千三百四十五万六千七百八十九。"},
                               {"role": "user", "content": "以下是关于整数转为中文读法的题目，请根据题目的数字，给出正确的答案。 题目：123456789012 答案：让我们一步一步思考，"},
                               {"role": "assistant", "content": "1、这个整数的长度一共是12位，按照中文的语法，12位数字是千亿级别的数字；2、这个数字从高到低，各级别分别读作：一千亿、二百亿、三十亿、四亿、五千万、六百万、七十万、八万、九千、零、零、二；3、出现了连续两个零，那么只写一个零；4、从左到右依次可以写出一千二百三十四亿五千六百七十八万九千零二。所以答案是一千二百三十四亿五千六百七十八万九千零二。"},
                               {"role": "user", "content":f"以下是关于整数转为中文读法的题目，请根据题目的数字，给出正确的答案。 题目：{quesion} 答案：让我们一步一步思考，"}]
            if type == 'decimal':
                prompt = [{"role": "system", "content": "你是一个数学优秀的中文人工智能助手，以下是关于小数转为中文读法的题目，请根据题目的数字，给出正确的答案。"}]
                if shot == 'zeroshot':
                    prompt += [{"role": "user", "content":f"以下是关于小数转为中文读法的题目，请根据题目的数字，给出正确的答案。题目：{quesion} 答案："}]
                if shot == 'cot_zeroshot':
                    prompt += [{"role": "user", "content":f"以下是关于小数转为中文读法的题目，请根据题目的数字，给出正确的答案。题目：{quesion} 答案：让我们一步一步思考，"}]
                if shot == 'fewshot':
                    prompt += [{"role": "user", "content": "以下是关于小数转为中文读法的题目，请根据题目的数字，给出正确的答案。题目：123.456 答案："},
                               {"role": "assistant", "content": "一百二十三点四五六"},
                               {"role": "user", "content": "以下是关于小数转为中文读法的题目，请根据题目的数字，给出正确的答案。题目：123456.789012 答案："},
                               {"role": "assistant", "content": "十二万三千四百五十六点七八九零一二"},
                               {"role": "user", "content": "以下是关于小数转为中文读法的题目，请根据题目的数字，给出正确的答案。题目：123456789.987654321 答案："},
                               {"role": "assistant", "content": "一亿二千三百四十五万六千七百八十九点九八七六五四三二一"},
                               {"role": "user", "content": "以下是关于小数转为中文读法的题目，请根据题目的数字，给出正确的答案。题目：123456789012.210987654321 答案："},
                               {"role": "assistant", "content": "一千二百三十四亿五千六百七十八万九千零一十二点二一零九八七六五四三二一"},
                               {"role": "user", "content":f"以下是关于小数转为中文读法的题目，请根据题目的数字，给出正确的答案。题目：{quesion} 答案："}]
                if shot == 'cot_fewshot':
                    prompt += [{"role": "user", "content": "以下是关于小数转为中文读法的题目，请根据题目的数字，给出正确的答案。题目：123.456 答案：让我们一步一步思考，"},
                               {"role": "assistant", "content": "1、这个数字有小数点，所以这是一个小数；2、小数点左侧的整数部分是123，这是一个长度为3的整数，按照中文的语法，3位数字是百级别的数字；3、所以整数部分从左到右依次可以写出一百二十三；4、小数右侧的小数部分是456，按照中文的语法，小数部分一个一个数字写出来即可；5、所以小数部分从左到右依次可以写出四五六；6、小数点读作点；所以答案是一百二十三点四五六。"},
                               {"role": "user", "content": "以下是关于小数转为中文读法的题目，请根据题目的数字，给出正确的答案。题目：123456.789012 答案：让我们一步一步思考，"},
                               {"role": "assistant", "content": "1、这个数字有小数点，所以这是一个小数；2、小数点左侧的整数部分是123456，这是一个长度为6的整数，按照中文的语法，6位数字是十万级别的数字；3、所以整数部分从左到右依次可以写出十二万三千四百五十六；4、小数右侧的小数部分是789012，按照中文的语法，小数部分一个一个数字写出来即可；5、所以小数部分从左到右依次可以写出七八九零一二；6、小数点读作点；所以答案是十二万三千四百五十六点七八九零一二。"},
                               {"role": "user", "content": "以下是关于小数转为中文读法的题目，请根据题目的数字，给出正确的答案。题目：123456789.987654321 答案：让我们一步一步思考，"},
                               {"role": "assistant", "content": "1、这个数字有小数点，所以这是一个小数；2、小数点左侧的整数部分是123456789，这是一个长度为9的整数，按照中文的语法，9位数字是亿级别的数字；3、所以整数部分从左到右依次可以写出一亿二千三百四十五万六千七百八十九；4、小数右侧的小数部分是987654321，按照中文的语法，小数部分一个一个数字写出来即可；5、所以小数部分从左到右依次可以写出九八七六五四三二一；6、小数点读作点；所以答案是一亿二千三百四十五万六千七百八十九点九八七六五四三二一。"},
                               {"role": "user", "content": "以下是关于小数转为中文读法的题目，请根据题目的数字，给出正确的答案。题目：123456789012.210987654321 答案：让我们一步一步思考，"},
                               {"role": "assistant", "content": "1、这个数字有小数点，所以这是一个小数；2、小数点左侧的整数部分是123456789012，这是一个长度为12的整数，按照中文的语法，12位数字是千亿级别的数字；3、所以整数部分从左到右依次可以写出一千二百三十四亿五千六百七十八万九千零一十二；4、小数右侧的小数部分是210987654321，按照中文的语法，小数部分一个一个数字写出来即可；5、所以小数部分从左到右依次可以写出二一零九八七六五四三二一；6、小数点读作点；所以答案是一千二百三十四亿五千六百七十八万九千零一十二点二一零九八七六五四三二一。"},
                               {"role": "user", "content":f"以下是关于小数转为中文读法的题目，请根据题目的数字，给出正确的答案。题目：{quesion} 答案：让我们一步一步思考，"}]
            if type == 'fraction':
                prompt = [{"role": "system", "content": "你是一个数学优秀的中文人工智能助手，以下是关于分数转为中文读法的题目，请根据题目的数字，给出正确的答案。"}]
                if shot == 'zeroshot':
                    prompt += [{"role": "user", "content":f"以下是关于分数转为中文读法的题目，请根据题目的数字，给出正确的答案。题目：{quesion} 答案："}]
                if shot == 'cot_zeroshot':
                    prompt += [{"role": "user", "content":f"以下是关于分数转为中文读法的题目，请根据题目的数字，给出正确的答案。题目：{quesion} 答案：让我们一步一步思考，"}]
                if shot == 'fewshot':
                    prompt += [{"role": "user", "content": "以下是关于分数转为中文读法的题目，请根据题目的数字，给出正确的答案。题目：123/456 答案："},
                               {"role": "assistant", "content": "四百五十六分之一百二十三"},
                               {"role": "user", "content": "以下是关于分数转为中文读法的题目，请根据题目的数字，给出正确的答案。题目：123456/789012 答案："},
                               {"role": "assistant", "content": "七十八万九千零一十二分之十二万三千四百五十六"},
                               {"role": "user", "content": "以下是关于分数转为中文读法的题目，请根据题目的数字，给出正确的答案。题目：123456789/987654321 答案："},
                               {"role": "assistant", "content": "九亿八千七百六十五万四千三百二十一分之一亿二千三百四十五万六千七百八十九"},
                               {"role": "user", "content": "以下是关于分数转为中文读法的题目，请根据题目的数字，给出正确的答案。题目：123456789012/210987654321 答案："},
                               {"role": "assistant", "content": "二千一百零九亿八千七百六十五万四千三百二十一分之一千二百三十四亿五千六百七十八万九千零一十二"},
                               {"role": "user", "content":f"以下是关于分数转为中文读法的题目，请根据题目的数字，给出正确的答案。题目：{quesion} 答案："}]
                if shot == 'cot_fewshot':
                    prompt += [{"role": "user", "content": "以下是关于分数转为中文读法的题目，请根据题目的数字，给出正确的答案。题目：123/456 答案：让我们一步一步思考，"},
                               {"role": "assistant", "content": "1、这个数字有斜杠，所以这是一个分数；2、斜杠左侧的分子是123，这个整数的长度一共是3位，按照中文的语法，3位数字是百级别的数字；3、所以分子从左到右依次可以写出一百二十三；4、斜杠右侧的分母是456，这个整数的长度一共是3位，按照中文的语法，3位数字是百级别的数字；5、所以分子从左到右依次可以写出四百五十六；6、斜杠读作分之；7、中文的语法里，要先读分母，再读斜杠，再读分子；所以答案是四百五十六分之一百二十三。"},
                               {"role": "user", "content": "以下是关于分数转为中文读法的题目，请根据题目的数字，给出正确的答案。题目：123456/789012 答案：让我们一步一步思考，"},
                               {"role": "assistant", "content": "1、这个数字有斜杠，所以这是一个分数；2、斜杠左侧的分子是123456，这个整数的长度一共是6位，按照中文的语法，6位数字是十万级别的数字；3、所以分子从左到右依次可以写出十二万三千四百五十六；4、斜杠右侧的分母是789012，这个整数的长度一共是6位，按照中文的语法，6位数字是十万级别的数字；5、所以分子从左到右依次可以写出七十八万九千零一十二；6、斜杠读作分之；7、中文的语法里，要先读分母，再读斜杠，再读分子；所以答案是七十八万九千零一十二分之十二万三千四百五十六。"},
                               {"role": "user", "content": "以下是关于分数转为中文读法的题目，请根据题目的数字，给出正确的答案。题目：123456789/987654321 答案：让我们一步一步思考，"},
                               {"role": "assistant", "content": "1、这个数字有斜杠，所以这是一个分数；2、斜杠左侧的分子是123456789，这个整数的长度一共是9位，按照中文的语法，9位数字是亿级别的数字；3、所以分子从左到右依次可以写出一亿二千三百四十五万六千七百八十九；4、斜杠右侧的分母是987654321，这个整数的长度一共是9位，按照中文的语法，9位数字是亿级别的数字；5、所以分子从左到右依次可以写出九亿八千七百六十五万四千三百二十一；6、斜杠读作分之；7、中文的语法里，要先读分母，再读斜杠，再读分子；所以答案是九亿八千七百六十五万四千三百二十一分之一亿二千三百四十五万六千七百八十九。"},
                               {"role": "user", "content": "以下是关于分数转为中文读法的题目，请根据题目的数字，给出正确的答案。题目：123456789012/210987654321 答案：让我们一步一步思考，"},
                               {"role": "assistant", "content": "1、这个数字有斜杠，所以这是一个分数；2、斜杠左侧的分子是123456789012，这个整数的长度一共是12位，按照中文的语法，12位数字是千亿级别的数字；3、所以分子从左到右依次可以写出一千二百三十四亿五千六百七十八万九千零一十二；4、斜杠右侧的分母是210987654321，这个整数的长度一共是12位，按照中文的语法，12位数字是千亿级别的数字；5、所以分子从左到右依次可以写出二千一百零九亿八千七百六十五万四千三百二十一；6、斜杠读作分之；7、中文的语法里，要先读分母，再读斜杠，再读分子；所以答案是二千一百零九亿八千七百六十五万四千三百二十一分之一千二百三十四亿五千六百七十八万九千零一十二。"},
                               {"role": "user", "content":f"以下是关于分数转为中文读法的题目，请根据题目的数字，给出正确的答案。题目：{quesion} 答案：让我们一步一步思考，"}]
        if language == "en":
            if type == 'integer':
                prompt = [{"role": "system", "content": "You are an excellent English artificial intelligence assistant in mathematics, the following is a question about how to convert integers into English pronunciation. Please provide the correct answer based on the numbers in the question."}]
                if shot == 'zeroshot':
                    prompt += [{"role": "user", "content":f"The following is a question about how to convert integers into English pronunciation. Please provide the correct answer based on the numbers in the question. Question:{quesion} Answer: "}]
                if shot == 'cot_zeroshot':
                    prompt += [{"role": "user", "content":f"The following is a question about how to convert integers into English pronunciation. Please provide the correct answer based on the numbers in the question. Question:{quesion} Answer: Let's think step by step, "}]
                if shot == 'fewshot':
                    prompt += [{"role": "user", "content": "The following are questions about converting integers into their English reading forms. Please give the correct answers based on the numbers in the questions.  Question: 123 Answer: "},
                               {"role": "assistant", "content": "One hundred twenty-three"},
                               {"role": "user", "content": "The following are questions about converting integers into their English reading forms. Please give the correct answers based on the numbers in the questions.  Question: 123456 Answer: "},
                               {"role": "assistant", "content": "One hundred twenty-three thousand four hundred fifty-six"},
                               {"role": "user", "content": "The following are questions about converting integers into their English reading forms. Please give the correct answers based on the numbers in the questions.  Question: 123456789 Answer: "},
                               {"role": "assistant", "content": "One hundred twenty-three million four hundred fifty-six thousand seven hundred eighty-nine"},
                               {"role": "user", "content": "The following are questions about converting integers into their English reading forms. Please give the correct answers based on the numbers in the questions.  Question: 123456789012 Answer: "},
                               {"role": "assistant", "content": "One hundred twenty-three billion four hundred fifty-six million seven hundred eighty-nine thousand twelve"},
                               {"role": "user", "content":f"The following are questions about converting integers into their English reading forms. Please give the correct answers based on the numbers in the questions.  Question: {quesion} Answer: "}]
                if shot == 'cot_fewshot':
                    prompt += [{"role": "user", "content": "The following are questions about converting integers into their English reading forms. Please give the correct answers based on the numbers in the questions.  Question: 123 Answer: Let's think step by step, "},
                               {"role": "assistant", "content": "1. The length of this integer is 3 digits, which in English grammar is a number at the hundred level; 2. From high to low, each level of this number reads as: one hundred, twenty, three; 3. From left to right, it can be written as one hundred twenty-three. So, the answer is one hundred twenty-three."},
                               {"role": "user", "content": "The following are questions about converting integers into their English reading forms. Please give the correct answers based on the numbers in the questions.  Question: 123456 Answer: Let's think step by step, "},
                               {"role": "assistant", "content": "1. The length of this integer is 6 digits, which in English grammar is a number at the hundred thousand level; 2. From high to low, each level of this number reads as: one hundred thousand, twenty thousand, three thousand, four hundred, fifty, six; 3. From left to right, it can be written as one hundred twenty-three thousand four hundred fifty-six. So, the answer is one hundred twenty-three thousand four hundred fifty-six."},
                               {"role": "user", "content": "The following are questions about converting integers into their English reading forms. Please give the correct answers based on the numbers in the questions.  Question: 123456789 Answer: Let's think step by step, "},
                               {"role": "assistant", "content": "1. The length of this integer is 9 digits, which in English grammar is a number at the hundred million level; 2. From high to low, each level of this number reads as: one hundred million, twenty million, three million, four hundred thousand, fifty thousand, six thousand, seven hundred, eighty, nine; 3. From left to right, it can be written as one hundred twenty-three million four hundred fifty-six thousand seven hundred eighty-nine. So, the answer is one hundred twenty-three million four hundred fifty-six thousand seven hundred eighty-nine."},
                               {"role": "user", "content": "The following are questions about converting integers into their English reading forms. Please give the correct answers based on the numbers in the questions.  Question: 123456789002 Answer: Let's think step by step, "},
                               {"role": "assistant", "content": "1. The length of this integer is 12 digits, which in English grammar is a number at the hundred billion level; 2. From high to low, each level of this number reads as: one hundred billion, twenty billion, three billion, four hundred million, fifty million, six million, seven hundred thousand, eighty thousand, nine thousand, zero, zero, two; 3. From left to right, it can be written as one hundred and twenty-three billion four hundred and fifty-six million seven hundred and eighty-nine thousand and two. So, the answer is one hundred and twenty-three billion four hundred and fifty-six million seven hundred and eighty-nine thousand and two."},
                               {"role": "user", "content":f"The following are questions about converting integers into their English reading forms. Please give the correct answers based on the numbers in the questions.  Question: {quesion} Answer: Let's think step by step, "}]
            if type == 'decimal':
                prompt = [{"role": "system", "content": "You are an excellent English artificial intelligence assistant in mathematics, the following is a question about how to convert decimals into English pronunciation. Please provide the correct answer based on the numbers in the question."}]
                if shot == 'zeroshot':
                    prompt += [{"role": "user", "content":f"The following is a question about how to convert decimals into English pronunciation. Please provide the correct answer based on the numbers in the question. Question:{quesion} Answer: "}]
                if shot == 'cot_zeroshot':
                    prompt += [{"role": "user", "content":f"The following is a question about how to convert decimals into English pronunciation. Please provide the correct answer based on the numbers in the question. Question:{quesion} Answer: Let's think step by step, "}]
                if shot == 'fewshot':
                    prompt += [{"role": "user", "content": "The following are questions about how to convert decimals into English pronunciation. Please provide the correct answer based on the numbers in the question. Question:123.456 Answer: "},
                               {"role": "assistant", "content": "one hundred twenty three point four five six"},
                               {"role": "user", "content": "The following are questions about how to convert decimals into English pronunciation. Please provide the correct answer based on the numbers in the question. Question: 123456.789012 Answer: "},
                               {"role": "assistant", "content": "one hundred twenty three thousand four hundred fifty six point seven eight nine zero one two"},
                               {"role": "user", "content": "The following are questions about how to convert decimals into English pronunciation. Please provide the correct answer based on the numbers in the question. Question: 123456789.987654321 Answer: "},
                               {"role": "assistant", "content": "one hundred twenty three million four hundred fifty six thousand seven hundred eighty nine point nine eight seven six five four three two one"},
                               {"role": "user", "content": "The following are questions about how to convert decimals into English pronunciation. Please provide the correct answer based on the numbers in the question. Question: 123456789012.210987654321 Answer: "},
                               {"role": "assistant", "content": "one hundred twenty three billion four hundred fifty six million seven hundred eighty nine thousand twelve point two one zero nine eight seven six five four three two one"},
                               {"role": "user", "content":f"The following are questions about how to convert decimals into English pronunciation. Please provide the correct answer based on the numbers in the question. Question: {quesion} Answer:"}]
                if shot == 'cot_fewshot':
                    prompt += [{"role": "user", "content": "The following are questions about how to convert decimals into English pronunciation. Please provide the correct answer based on the numbers in the question. Question:123.456 Answer: Let's think step by step, "},
                               {"role": "assistant", "content": "1. This number has a decimal point, so it's a decimal.2. The integer part to the left of the decimal point is 123, which is a 3-digit integer. According to English grammar, a 3-digit number is at the hundred level.3. So, the integer part from left to right can be written as one hundred twenty three.4. The decimal part to the right of the decimal point is 456, which according to English grammar, is written out one digit at a time.5. So the decimal part from left to right can be written as four five six.6. The decimal point is read as 'point'.So the answer is one hundred twenty three point four five six."},
                               {"role": "user", "content": "The following are questions about how to convert decimals into English pronunciation. Please provide the correct answer based on the numbers in the question. Question: 123456.789012 Answer: Let's think step by step, "},
                               {"role": "assistant", "content": "1. This number has a decimal point, so it's a decimal.2. The integer part to the left of the decimal point is 123456, which is a 6-digit integer. According to English grammar, a 6-digit number is at the hundred-thousand level.3. So, the integer part from left to right can be written as one hundred twenty three thousand four hundred fifty six.4. The decimal part to the right of the decimal point is 789012, which according to English grammar, is written out one digit at a time.5. So the decimal part from left to right can be written as seven eight nine zero one two.6. The decimal point is read as 'point'.So the answer is one hundred twenty three thousand four hundred fifty six point seven eight nine zero one two."},
                               {"role": "user", "content": "The following are questions about how to convert decimals into English pronunciation. Please provide the correct answer based on the numbers in the question. Question: 123456789.987654321 Answer: Let's think step by step, "},
                               {"role": "assistant", "content": "1. This number has a decimal point, so it's a decimal.2. The integer part to the left of the decimal point is 123456789, which is a 9-digit integer. According to English grammar, a 9-digit number is at the hundred-million level.3. So, the integer part from left to right can be written as one hundred twenty-three million four hundred fifty-six thousand seven hundred eighty-nine.4. The decimal part to the right of the decimal point is 987654321, which according to English grammar, is written out one digit at a time.5. So the decimal part from left to right can be written as nine eight seven six five four three two one.6. The decimal point is read as 'point'.So the answer is one hundred twenty-three million four hundred fifty-six thousand seven hundred eighty-nine point nine eight seven six five four three two one."},
                               {"role": "user", "content": "The following are questions about how to convert decimals into English pronunciation. Please provide the correct answer based on the numbers in the question. Question: 123456789012.210987654321 Answer: Let's think step by step, "},
                               {"role": "assistant", "content": "1. This number has a decimal point, so it's a decimal.2. The integer part to the left of the decimal point is 123456789012, which is a 12-digit integer. According to English grammar, a 12-digit number is at the hundred-billion level.3. So, the integer part from left to right can be written as one hundred twenty-three billion four hundred fifty-six million seven hundred eighty-nine thousand twelve.4. The decimal part to the right of the decimal point is 210987654321, which according to English grammar, is written out one digit at a time.5. So the decimal part from left to right can be written as two one zero nine eight seven six five four three two one.6. The decimal point is read as 'point'.So the answer is one hundred twenty-three billion four hundred fifty-six million seven hundred eighty-nine thousand twelve point two one zero nine eight seven six five four three two one."},
                               {"role": "user", "content":f"The following are questions about how to convert decimals into English pronunciation. Please provide the correct answer based on the numbers in the question. Question: {quesion} Answer: Let's think step by step, "}]
            if type == 'fraction':
                prompt = [{"role": "system", "content": "You are an excellent English artificial intelligence assistant in mathematics, the following is a question about how to convert fractions into English pronunciation. Please provide the correct answer based on the numbers in the question."}]
                if shot == 'zeroshot':
                    prompt += [{"role": "user", "content": f"The following is a question about how to convert fractions into English pronunciation. Please provide the correct answer based on the numbers in the question.Question:{quesion} Answer: "}]
                if shot == 'cot_zeroshot':
                    prompt += [{"role": "user", "content": f"The following is a question about how to convert fractions into English pronunciation. Please provide the correct answer based on the numbers in the question.Question:{quesion} Answer: Let's think step by step, "}]
                if shot == 'fewshot':
                    prompt += [{"role": "user", "content":  "The following are questions about how to convert fractions into English pronunciation. Please provide the correct answer based on the numbers in the question.Question:123/456 Answer: "},
                               {"role": "assistant", "content": "one hundred twenty three over four hundred fifty six"},
                               {"role": "user", "content":  "The following are questions about how to convert fractions into English pronunciation. Please provide the correct answer based on the numbers in the question.Question:123456/789012 Answer: "},
                               {"role": "assistant", "content": "one hundred twenty three thousand four hundred fifty six over seven hundred eighty nine thousand twelve"},
                               {"role": "user", "content":  "The following are questions about how to convert fractions into English pronunciation. Please provide the correct answer based on the numbers in the question.Question:123456789/987654321 Answer: "},
                               {"role": "assistant", "content": "one hundred twenty three million four hundred fifty six thousand seven hundred eighty nine over nine hundred eighty seven million six hundred fifty four thousand three hundred twenty one"},
                               {"role": "user", "content":  "The following are questions about how to convert fractions into English pronunciation. Please provide the correct answer based on the numbers in the question.Question:123456789012/210987654321 Answer: "},
                               {"role": "assistant", "content": "one hundred twenty three billion four hundred fifty six million seven hundred eighty nine thousand twelve over two hundred ten billion nine hundred eighty seven million six hundred fifty four thousand three hundred twenty one"},
                               {"role": "user", "content": f"The following are questions about how to convert fractions into English pronunciation. Please provide the correct answer based on the numbers in the question.Question:{quesion} Answer: "}]
                if shot == 'cot_fewshot':
                    prompt += [{"role": "user", "content":  "The following are questions about how to convert fractions into English pronunciation. Please provide the correct answer based on the numbers in the question.Question:123/456 Answer: Let's think step by step, "},
                               {"role": "assistant", "content": "1. This number has a slash, so it's a fraction.2. The numerator to the left of the slash is 123, which is a 3-digit integer. According to English grammar, a 3-digit number is at the hundred level.3. So the numerator from left to right can be written as one hundred twenty-three.4. The denominator to the right of the slash is 456, which is also a 3-digit integer. According to English grammar, a 3-digit number is at the hundred level.5. So the denominator from left to right can be written as four hundred fifty-six.6. The slash is read as 'over'.So the answer is one hundred twenty-three over four hundred fifty-six."},
                               {"role": "user", "content":  "The following are questions about how to convert fractions into English pronunciation. Please provide the correct answer based on the numbers in the question.Question:123456/789012 Answer: Let's think step by step, "},
                               {"role": "assistant", "content": "1. This number has a slash, so it's a fraction.2. The numerator to the left of the slash is 123456, which is a 6-digit integer. According to English grammar, a 6-digit number is at the hundred-thousand level.3. So the numerator from left to right can be written as one hundred twenty-three thousand four hundred fifty-six.4. The denominator to the right of the slash is 789012, which is also a 6-digit integer. According to English grammar, a 6-digit number is at the hundred-thousand level.5. So the denominator from left to right can be written as seven hundred eighty-nine thousand twelve.6. The slash is read as 'over'.So the answer is one hundred twenty-three thousand four hundred fifty-six over seven hundred eighty-nine thousand twelve."},
                               {"role": "user", "content":  "The following are questions about how to convert fractions into English pronunciation. Please provide the correct answer based on the numbers in the question.Question:123456789/987654321 Answer: Let's think step by step, "},
                               {"role": "assistant", "content": "1. This number has a slash, so it's a fraction.2. The numerator to the left of the slash is 123456789, which is a 9-digit integer. According to English grammar, a 9-digit number is at the hundred-million level.3. So the numerator from left to right can be written as one hundred twenty-three million four hundred fifty-six thousand seven hundred eighty-nine.4. The denominator to the right of the slash is 987654321, which is also a 9-digit integer. According to English grammar, a 9-digit number is at the hundred-million level.5. So the denominator from left to right can be written as nine hundred eighty-seven million six hundred fifty-four thousand three hundred twenty-one.6. The slash is read as 'over'.So the answer is one hundred twenty-three million four hundred fifty-six thousand seven hundred eighty-nine over nine hundred eighty-seven million six hundred fifty-four thousand three hundred twenty-one."},
                               {"role": "user", "content":  "The following are questions about how to convert fractions into English pronunciation. Please provide the correct answer based on the numbers in the question.Question:123456789012/210987654321 Answer: Let's think step by step, "},
                               {"role": "assistant", "content": "1. This number has a slash, so it's a fraction.2. The numerator to the left of the slash is 123456789012, which is a 12-digit integer. According to English grammar, a 12-digit number is at the hundred-billion level.3. So the numerator from left to right can be written as one hundred twenty-three billion four hundred fifty-six million seven hundred eighty-nine thousand twelve.4. The denominator to the right of the slash is 210987654321, which is also a 12-digit integer. According to English grammar, a 12-digit number is at the hundred-billion level.5. So the denominator from left to right can be written as two hundred ten billion nine hundred eighty-seven million six hundred fifty-four thousand three hundred twenty-one.6. The slash is read as 'over'.So the answer is one hundred twenty-three billion four hundred fifty-six million seven hundred eighty-nine thousand twelve over two hundred ten billion nine hundred eighty-seven million six hundred fifty-four thousand three hundred twenty-one."},
                               {"role": "user", "content": f"The following are questions about how to convert fractions into English pronunciation. Please provide the correct answer based on the numbers in the question.Question:{quesion} Answer: Let's think step by step, "}]
    if task == 'word2num':
        if language == "zh":
            if type == 'integer':
                prompt = [{"role": "system",  "content": "你是一个数学优秀的中文人工智能助手，以下是关于中文转为整数的题目，请根据题目的中文，给出正确的答案。"}]
                if shot == 'zeroshot':
                    prompt += [{"role": "user", "content":f"以下是关于中文转为整数的题目，请根据题目的中文，给出正确的答案。 题目：{quesion} 答案："}]
                if shot == 'cot_zeroshot':
                    prompt += [{"role": "user", "content":f"以下是关于中文转为整数的题目，请根据题目的中文，给出正确的答案。 题目：{quesion} 答案：让我们一步一步思考，"}]
                if shot == 'fewshot':
                    prompt += [{"role": "user", "content": "以下是关于中文转为整数的题目，请根据题目的中文，给出正确的答案。 题目：一百二十三 答案："},
                              {"role": "assistant", "content": "123"},
                              {"role": "user", "content":  "以下是关于中文转为整数的题目，请根据题目的中文，给出正确的答案。 题目：十二万三千四百五十六 答案："},
                              {"role": "assistant", "content": "123456"},
                              {"role": "user", "content":  "以下是关于中文转为整数的题目，请根据题目的中文，给出正确的答案。 题目：一亿二千三百四十五万六千七百八十九 答案："},
                              {"role": "assistant", "content": "123456789"},
                              {"role": "user", "content":  "以下是关于中文转为整数的题目，请根据题目的中文，给出正确的答案。 题目：一千二百三十四亿五千六百七十八万九千零一十二 答案："},
                              {"role": "assistant", "content": "123456789012"},
                              {"role": "user", "content": f"以下是关于中文转为整数的题目，请根据题目的中文，给出正确的答案。 题目：{quesion} 答案："}]
                if shot == 'cot_fewshot':
                    prompt += [{"role": "user", "content": "以下是关于中文转为整数的题目，请根据题目的中文，给出正确的答案。 题目：一百二十三 答案：让我们一步一步思考，"},
                               {"role": "assistant", "content": "1、按照顺序从左到右写下来，一百写作100，二十写作20，三写作3；2、上面所有的数字相加，100+20+3=123；所以答案是123。"},
                               {"role": "user", "content": "以下是关于中文转为整数的题目，请根据题目的中文，给出正确的答案。 题目：十二万三千四百五十六  答案：让我们一步一步思考，"},
                               {"role": "assistant", "content": "1、按照顺序从左到右写下来，十二万写作120000，三千四百五十六写作3456；2、上面所有的数字相加，120000+3456=123456所以答案是123456。"},
                               {"role": "user", "content": "以下是关于中文转为整数的题目，请根据题目的中文，给出正确的答案。 题目：一亿二千三百四十五万六千七百八十九  答案：让我们一步一步思考，"},
                               {"role": "assistant", "content": "1、按照顺序从左到右写下来，一亿写作100000000，二千三百四十五万写作23450000，六千七百八十九写作6789；2、上面所有的数字相加，100000000+23450000+6789=123456789；所以答案是123456789。"},
                               {"role": "user", "content": "以下是关于中文转为整数的题目，请根据题目的中文，给出正确的答案。 题目：一千二百三十四亿五千六百七十八万九千零一十二  答案：让我们一步一步思考，"},
                               {"role": "assistant", "content": "1、按照顺序从左到右写下来，一千二百三十四亿写作123400000000，五千六百七十八万写作56780000，九千零一十二写作9012；2、上面所有的数字相加，123400000000+56780000+9012=123456789012；所以答案是123456789012。"},
                               {"role": "user", "content":f"以下是关于中文转为整数的题目，请根据题目的中文，给出正确的答案。 题目：{quesion} 答案：让我们一步一步思考，"}]
            if type == 'decimal':
                prompt = [{"role": "system", "content": "你是一个数学优秀的中文人工智能助手，以下是关于中文转为小数的题目，请根据题目的中文，给出正确的答案。"}]
                if shot == 'zeroshot':
                    prompt += [{"role": "user", "content":f"以下是关于中文转为小数的题目，请根据题目的中文，给出正确的答案。 题目：{quesion} 答案："}]
                if shot == 'cot_zeroshot':
                    prompt += [{"role": "user", "content":f"以下是关于中文转为小数的题目，请根据题目的中文，给出正确的答案。 题目：{quesion} 答案：让我们一步一步思考，"}]
                if shot == 'fewshot':
                    prompt += [{"role": "user", "content": "以下是关于中文转为小数的题目，请根据题目的中文，给出正确的答案。 题目：一百二十三点四五六 答案："},
                               {"role": "assistant", "content": "123.456"},
                               {"role": "user", "content": "以下是关于中文转为小数的题目，请根据题目的中文，给出正确的答案。 题目：十二万三千四百五十六点七八九零一二 答案："},
                               {"role": "assistant", "content": "123456.789012"},
                               {"role": "user", "content": "以下是关于中文转为小数的题目，请根据题目的中文，给出正确的答案。 题目：一亿二千三百四十五万六千七百八十九点九八七六五四三二一 答案："},
                               {"role": "assistant", "content": "123456789.987654321"},
                               {"role": "user", "content": "以下是关于中文转为小数的题目，请根据题目的中文，给出正确的答案。 题目：一千二百三十四亿五千六百七十八万九千零一十二点二一零九八七六五四三二一 答案："},
                               {"role": "assistant", "content": "123456789012.210987654321"},
                               {"role": "user", "content":f"以下是关于中文转为小数的题目，请根据题目的中文，给出正确的答案。 题目：{quesion} 答案："}]
                if shot == 'cot_fewshot':
                    prompt += [{"role": "user", "content": "以下是关于中文转为小数的题目，请根据题目的中文，给出正确的答案。 题目：一百二十三点四五六 答案：让我们一步一步思考，"},
                               {"role": "assistant", "content": "1、题目里出现了'点'这个汉字，说明这是一个小数；2、'点'字左边'一百二十三'的是整数部分，写作123；3、'点'字右边'四五六'的是小数部分，写作456；4、'点'字写作. ；所以答案是123.456。"},
                               {"role": "user", "content": "以下是关于中文转为小数的题目，请根据题目的中文，给出正确的答案。 题目：十二万三千四百五十六点七八九零一二 答案：让我们一步一步思考，"},
                               {"role": "assistant", "content": "1、题目里出现了'点'这个汉字，说明这是一个小数；2、'点'字左边'十二万三千四百五十六'的是整数部分，写作123456；3、'点'字右边'七八九零一二'的是小数部分，写作789012；4、'点'字写作. ；所以答案是123456.789012。"},
                               {"role": "user", "content": "以下是关于中文转为小数的题目，请根据题目的中文，给出正确的答案。 题目：一亿二千三百四十五万六千七百八十九点九八七六五四三二一 答案：让我们一步一步思考，"},
                               {"role": "assistant", "content": "1、题目里出现了'点'这个汉字，说明这是一个小数；2、'点'字左边'一亿二千三百四十五万六千七百八十九'的是整数部分，写作123456789；3、'点'字右边'九八七六五四三二一'的是小数部分，写作987654321；4、'点'字写作. ；所以答案是123456789.987654321。"},
                               {"role": "user", "content": "以下是关于中文转为小数的题目，请根据题目的中文，给出正确的答案。 题目：一千二百三十四亿五千六百七十八万九千零一十二点二一零九八七六五四三二一 答案：让我们一步一步思考，"},
                               {"role": "assistant", "content": "1、题目里出现了'点'这个汉字，说明这是一个小数；2、'点'字左边'一千二百三十四亿五千六百七十八万九千零一十二'的是整数部分，写作123456789012；3、'点'字右边'二一零九八七六五四三二一'的是小数部分，写作210987654321；4、'点'字写作. ；所以答案是123456789012.210987654321。"},
                               {"role": "user", "content":f"以下是关于中文转为小数的题目，请根据题目的中文，给出正确的答案。 题目：{quesion} 答案：让我们一步一步思考，"}]
            if type == 'fraction':
                prompt = [{"role": "system", "content": "你是一个数学优秀的中文人工智能助手，以下是关于中文转为分数的题目，请根据题目的中文，给出正确的答案。"}]
                if shot == 'zeroshot':
                    prompt += [{"role": "user", "content": f"以下是关于中文转为分数的题目，请根据题目的中文，给出正确的答案。 题目：{quesion} 答案："}]
                if shot == 'cot_zeroshot':
                    prompt += [{"role": "user", "content": f"以下是关于中文转为分数的题目，请根据题目的中文，给出正确的答案。 题目：{quesion} 答案：让我们一步一步思考，"}]
                if shot == 'fewshot':
                    prompt += [{"role": "user", "content": f"以下是关于中文转为分数的题目，请根据题目的中文，给出正确的答案。 题目：四百五十六分之一百二十三 答案："},
                               {"role": "assistant", "content": "123/456"},
                               {"role": "user", "content": f"以下是关于中文转为分数的题目，请根据题目的中文，给出正确的答案。 题目：七十八万九千零一十二分之十二万三千四百五十六 答案："},
                               {"role": "assistant", "content": "123456/789012"},
                               {"role": "user", "content": f"以下是关于中文转为分数的题目，请根据题目的中文，给出正确的答案。 题目：九亿八千七百六十五万四千三百二十一分之一亿二千三百四十五万六千七百八十九 答案："},
                               {"role": "assistant", "content": "123456789/987654321"},
                               {"role": "user", "content": f"以下是关于中文转为分数的题目，请根据题目的中文，给出正确的答案。 题目：二千一百零九亿八千七百六十五万四千三百二十一分之一千二百三十四亿五千六百七十八万九千零一十二 答案："},
                               {"role": "assistant", "content": "123456789012/210987654321"},
                               {"role": "user", "content": f"以下是关于中文转为分数的题目，请根据题目的中文，给出正确的答案。 题目：{quesion} 答案："}]
                if shot == 'cot_fewshot':
                    prompt += [{"role": "user", "content": f"以下是关于中文转为分数的题目，请根据题目的中文，给出正确的答案。 题目：四百五十六分之一百二十三 答案：让我们一步一步思考，"},
                               {"role": "assistant", "content": "1、题目里出现了'分之'这个词，说明这是一个分数；2、'分之'左边的'四百五十六'是分母，写作456；3、'分之'右边的'一百二十三'是分子，写作123；4、'分之'写作/ ；5、写为分数的时候，从左到右要先写分子，再写/，最后写分母；所以答案是123/456。"},
                               {"role": "user", "content": f"以下是关于中文转为分数的题目，请根据题目的中文，给出正确的答案。 题目：七十八万九千零一十二分之十二万三千四百五十六 答案：让我们一步一步思考，"},
                               {"role": "assistant", "content": "1、题目里出现了'分之'这个词，说明这是一个分数；2、'分之'左边的'七十八万九千零一十二'是分母，写作789012；3、'分之'右边的'十二万三千四百五十六'是分子，写作123456；4、'分之'写作/ ；5、写为分数的时候，从左到右要先写分子，再写/，最后写分母；所以答案是123456/789012。"},
                               {"role": "user", "content": f"以下是关于中文转为分数的题目，请根据题目的中文，给出正确的答案。 题目：九亿八千七百六十五万四千三百二十一分之一亿二千三百四十五万六千七百八十九 答案：让我们一步一步思考，"},
                               {"role": "assistant", "content": "1、题目里出现了'分之'这个词，说明这是一个分数；2、'分之'左边的'九亿八千七百六十五万四千三百二十一'是分母，写作987654321；3、'分之'右边的'一亿二千三百四十五万六千七百八十九'是分子，写作123456789；4、'分之'写作/ ；5、写为分数的时候，从左到右要先写分子，再写/，最后写分母；所以答案是123456789/987654321。"},
                               {"role": "user", "content": f"以下是关于中文转为分数的题目，请根据题目的中文，给出正确的答案。 题目：二千一百零九亿八千七百六十五万四千三百二十一分之一千二百三十四亿五千六百七十八万九千零一十二 答案：让我们一步一步思考，"},
                               {"role": "assistant", "content": "1、题目里出现了'分之'这个词，说明这是一个分数；2、'分之'左边的'二千一百零九亿八千七百六十五万四千三百二十一'是分母，写作210987654321；3、'分之'右边的'一千二百三十四亿五千六百七十八万九千零一十二'是分子，写作123456789012；4、'分之'写作/ ；5、写为分数的时候，从左到右要先写分子，再写/，最后写分母；所以答案是123456789012/210987654321。"},
                               {"role": "user", "content": f"以下是关于中文转为分数的题目，请根据题目的中文，给出正确的答案。 题目：{quesion} 答案：让我们一步一步思考，"}]
        if language == "en":
            if type == 'integer':
                prompt = [{"role": "system", "content": "You are an excellent English artificial intelligence assistant in mathematics, the following is a question about how to convert English pronunciation into integers. Please provide the correct answer based on the numbers in the question."}]
                if shot == 'zeroshot':
                    prompt += [{"role": "user", "content":f"The following is a question about how to convert English pronunciation into integers. Please provide the correct answer based on the numbers in the question.  Question: {quesion}  Answer:"}]
                if shot == 'cot_zeroshot':
                    prompt += [{"role": "user", "content":f"The following is a question about how to convert English pronunciation into integers. Please provide the correct answer based on the numbers in the question.  Question: {quesion}  Answer: Let's think step by step, "}]
                if shot == 'fewshot':
                    prompt += [{"role": "user", "content": "The following are questions about how to convert English pronunciation into integers. Please provide the correct answer based on the numbers in the question.  Question: One hundred twenty-three  Answer: "},
                               {"role": "assistant", "content": "123"},
                               {"role": "user", "content": "The following are questions about how to convert English pronunciation into integers. Please provide the correct answer based on the numbers in the question.  Question: One hundred twenty-three thousand four hundred fifty-six  Answer: "},
                               {"role": "assistant", "content": "123456"},
                               {"role": "user", "content": "The following are questions about how to convert English pronunciation into integers. Please provide the correct answer based on the numbers in the question.  Question: One hundred twenty-three million four hundred fifty-six thousand seven hundred eighty-nine  Answer: "},
                               {"role": "assistant", "content": "123456789"},
                               {"role": "user", "content": "The following are questions about how to convert English pronunciation into integers. Please provide the correct answer based on the numbers in the question.  Question: One hundred twenty-three billion four hundred fifty-six million seven hundred eighty-nine thousand twelve  Answer: "},
                               {"role": "assistant", "content": "123456789012"},
                               {"role": "user", "content":f"The following are questions about how to convert English pronunciation into integers. Please provide the correct answer based on the numbers in the question.  Question: {quesion}  Answer: "}]
                if shot == 'cot_fewshot':
                    prompt += [{"role": "user", "content": "The following are questions about how to convert English pronunciation into integers. Please give the correct answers based on the English words in the questions.  Question: One hundred twenty-three  Answer: Let's think step by step, "},
                               {"role": "assistant", "content": "1. Write it down in order from left to right, one hundred is written as 100, twenty is written as 20, three is written as 3; 2. Add all the numbers above, 100 + 20 + 3 = 123; So, the answer is 123."},
                               {"role": "user", "content": "The following are questions about how to convert English pronunciation into integers. Please give the correct answers based on the English words in the questions.  Question: One hundred twenty-three thousand four hundred fifty-six  Answer: Let's think step by step, "},
                               {"role": "assistant", "content": "1. Write it down in order from left to right, one hundred twenty-three thousand is written as 123000, four hundred fifty-six is written as 456; 2. Add all the numbers above, 123000 + 456 = 123456; So, the answer is 123456."},
                               {"role": "user", "content": "The following are questions about how to convert English pronunciation into integers. Please give the correct answers based on the English words in the questions.  Question: One hundred twenty-three million four hundred fifty-six thousand seven hundred eighty-nine  Answer: Let's think step by step, "},
                               {"role": "assistant", "content": "1. Write it down in order from left to right, one hundred twenty-three million is written as 123000000, four hundred fifty-six thousand is written as 456000, seven hundred eighty-nine is written as 789; 2. Add all the numbers above, 123000000 + 456000 + 789 = 123456789; So, the answer is 123456789."},
                               {"role": "user", "content": "The following are questions about how to convert English pronunciation into integers. Please give the correct answers based on the English words in the questions.  Question: One hundred twenty-three billion four hundred fifty-six million seven hundred eighty-nine thousand and twelve  Answer: Let's think step by step, "},
                               {"role": "assistant", "content": "1. Write it down in order from left to right, one hundred twenty-three billion is written as 123000000000, four hundred fifty-six million is written as 456000000, seven hundred eighty-nine thousand is written as 789000, twelve is written as 12; 2. Add all the numbers above, 123000000000 + 456000000 + 789000 + 12 = 123456789012; So, the answer is 123456789012."},
                               {"role": "user", "content":f"The following are questions about how to convert English pronunciation into integers. Please give the correct answers based on the English words in the questions.  Question: {quesion}  Answer: Let's think step by step, "}]
            if type == 'decimal':
                prompt = [{"role": "system", "content": "You are an excellent English artificial intelligence assistant in mathematics, the following is a question about how to convert English pronunciation into decimals. Please provide the correct answer based on the numbers in the question."}]
                if shot == 'zeroshot':
                    prompt += [{"role": "user", "content":f"The following is a question about how to convert English pronunciation into decimals. Please provide the correct answer based on the numbers in the question.  Question: {quesion}  Answer:"}]
                if shot == 'cot_zeroshot':
                    prompt += [{"role": "user", "content":f"The following is a question about how to convert English pronunciation into decimals. Please provide the correct answer based on the numbers in the question.  Question: {quesion}  Answer: Let's think step by step, "}]
                if shot == 'fewshot':
                    prompt += [{"role": "user", "content": "The following are questions about how to convert English pronunciation into decimals. Please provide the correct answer based on the numbers in the question.  Question: one hundred twenty three point four five six  Answer:"},
                               {"role": "assistant", "content": "123.456"},
                               {"role": "user", "content": "The following are questions about how to convert English pronunciation into decimals. Please provide the correct answer based on the numbers in the question.  Question: one hundred twenty three thousand four hundred fifty six point seven eight nine zero one two  Answer:"},
                               {"role": "assistant", "content": "123456.789012"},
                               {"role": "user", "content": "The following are questions about how to convert English pronunciation into decimals. Please provide the correct answer based on the numbers in the question.  Question: one hundred and twenty-three million four hundred and fifty-six thousand seven hundred and eighty-nine point nine eight seven six five four three two one  Answer:"},
                               {"role": "assistant", "content": "123456789.987654321"},
                               {"role": "user", "content": "The following are questions about how to convert English pronunciation into decimals. Please provide the correct answer based on the numbers in the question.  Question: one hundred twenty three billion four hundred fifty six million seven hundred eighty nine thousand twelve point two one zero nine eight seven six five four three two one  Answer:"},
                               {"role": "assistant", "content": "123456789012.210987654321"},
                               {"role": "user", "content":f"The following are questions about how to convert English pronunciation into decimals. Please provide the correct answer based on the numbers in the question.  Question: {quesion}  Answer:"}]
                if shot == 'cot_fewshot':
                    prompt += [{"role": "user", "content": "The following are questions about how to convert English pronunciation into decimals. Please provide the correct answer based on the numbers in the question.  Question: one hundred twenty three point four five six  Answer: Let's think step by step, "},
                               {"role": "assistant", "content": "1. The presence of the character 'point' in the problem indicates that this is a decimal number;2. To the left of 'point', 'one hundred and twenty-three' is the integer part, written as 123;3. To the right of 'point', 'four five six' is the decimal part, written as 456;4. The 'point' is written as '.';So the answer is 123.456."},
                               {"role": "user", "content": "The following are questions about how to convert English pronunciation into decimals. Please provide the correct answer based on the numbers in the question.  Question: one hundred twenty three thousand four hundred fifty six point seven eight nine zero one two  Answer: Let's think step by step, "},
                               {"role": "assistant", "content": "1. The presence of the character 'point' in the problem indicates that this is a decimal number;2. To the left of 'point', 'one hundred twenty-three thousand four hundred fifty-six' is the integer part, written as 123456;3. To the right of 'point', 'seven eight nine zero one two' is the decimal part, written as 789012;4. The 'point' is written as '.';So the answer is 123456.789012."},
                               {"role": "user", "content": "The following are questions about how to convert English pronunciation into decimals. Please provide the correct answer based on the numbers in the question.  Question: one hundred and twenty-three million four hundred and fifty-six thousand seven hundred and eighty-nine point nine eight seven six five four three two one  Answer: Let's think step by step, "},
                               {"role": "assistant", "content": "1. The presence of the character 'point' in the problem indicates that this is a decimal number;2. To the left of 'point', 'one hundred twenty-three million four hundred fifty-six thousand seven hundred eighty-nine' is the integer part, written as 123456789;3. To the right of 'point', 'nine eight seven six five four three two one' is the decimal part, written as 987654321;4. The 'point' is written as '.';So the answer is 123456789.987654321."},
                               {"role": "user", "content": "The following are questions about how to convert English pronunciation into decimals. Please provide the correct answer based on the numbers in the question.  Question: one hundred twenty three billion four hundred fifty six million seven hundred eighty nine thousand twelve point two one zero nine eight seven six five four three two one  Answer: Let's think step by step, "},
                               {"role": "assistant", "content": "1. The presence of the character 'point' in the problem indicates that this is a decimal number;2. To the left of 'point', 'one hundred twenty-three billion four hundred fifty-six million seven hundred eighty-nine thousand twelve' is the integer part, written as 123456789012;3. To the right of 'point', 'two one zero nine eight seven six five four three two one' is the decimal part, written as 210987654321;4. The 'point' is written as '.';So the answer is 123456789012.210987654321."},
                               {"role": "user", "content":f"The following are questions about how to convert English pronunciation into decimals. Please provide the correct answer based on the numbers in the question.  Question: {quesion}  Answer: Let's think step by step, "}]
            if type == 'fraction':
                prompt = [{"role": "system", "content": "You are an excellent English artificial intelligence assistant in mathematics, the following is a question about how to convert English pronunciation into fractions. Please provide the correct answer based on the numbers in the question."}]
                if shot == 'zeroshot':
                    prompt += [{"role": "user", "content":f"The following is a question about how to convert English pronunciation into fractions. Please provide the correct answer based on the numbers in the question.  Question: {quesion}  Answer:"}]
                if shot == 'cot_zeroshot':
                    prompt += [{"role": "user", "content":f"The following is a question about how to convert English pronunciation into fractions. Please provide the correct answer based on the numbers in the question.  Question: {quesion}  Answer: Let's think step by step, "}]
                if shot == 'fewshot':
                    prompt += [{"role": "user", "content": "The following is a question about how to convert English pronunciation into fractions. Please provide the correct answer based on the numbers in the question.  Question: one hundred twenty three over four hundred fifty six  Answer:"},
                               {"role": "assistant", "content": "123/456"},
                               {"role": "user", "content": "The following is a question about how to convert English pronunciation into fractions. Please provide the correct answer based on the numbers in the question.  Question: one hundred twenty three thousand four hundred fifty six over seven hundred eighty nine thousand twelve  Answer:"},
                               {"role": "assistant", "content": "123456/789012"},
                               {"role": "user", "content": "The following is a question about how to convert English pronunciation into fractions. Please provide the correct answer based on the numbers in the question.  Question: one hundred twenty three million four hundred fifty six thousand seven hundred eighty nine over nine hundred eighty seven million six hundred fifty four thousand three hundred twenty one  Answer:"},
                               {"role": "assistant", "content": "123456789/987654321"},
                               {"role": "user", "content": "The following is a question about how to convert English pronunciation into fractions. Please provide the correct answer based on the numbers in the question.  Question: one hundred twenty three billion four hundred fifty six million seven hundred eighty nine thousand twelve over two hundred ten billion nine hundred eighty seven million six hundred fifty four thousand three hundred twenty one  Answer:"},
                               {"role": "assistant", "content": "123456789012/210987654321"},
                               {"role": "user", "content":f"The following is a question about how to convert English pronunciation into fractions. Please provide the correct answer based on the numbers in the question.  Question: {quesion}  Answer:"}]
                if shot == 'cot_fewshot':
                    prompt += [{"role": "user", "content": "The following is a question about how to convert English pronunciation into fractions. Please provide the correct answer based on the numbers in the question.  Question: one hundred twenty three over four hundred fifty six  Answer: Let's think step by step, "},
                               {"role": "assistant", "content": "1. The appearance of the term 'over' in the problem indicates that this is a fraction;2. To the left of 'over', 'four hundred fifty-six' is the denominator, written as 456;3. To the right of 'over', 'one hundred twenty-three' is the numerator, written as 123;4. 'over' is written as '/';5. When written as a fraction, the numerator is written first, followed by '/', and then the denominator;So the answer is 123/456."},
                               {"role": "user", "content": "The following is a question about how to convert English pronunciation into fractions. Please provide the correct answer based on the numbers in the question.  Question: one hundred twenty three thousand four hundred fifty six over seven hundred eighty nine thousand twelve  Answer: Let's think step by step, "},
                               {"role": "assistant", "content": "1. The appearance of the term 'over' in the problem indicates that this is a fraction;2. To the left of 'over', 'seven hundred eighty-nine thousand twelve' is the denominator, written as 789012;3. To the right of 'over', 'one hundred twenty-three thousand four hundred fifty-six' is the numerator, written as 123456;4. 'over' is written as '/';5. When written as a fraction, the numerator is written first, followed by '/', and then the denominator;So the answer is 123456/789012."},
                               {"role": "user", "content": "The following is a question about how to convert English pronunciation into fractions. Please provide the correct answer based on the numbers in the question.  Question: one hundred twenty three million four hundred fifty six thousand seven hundred eighty nine over nine hundred eighty seven million six hundred fifty four thousand three hundred twenty one  Answer: Let's think step by step, "},
                               {"role": "assistant", "content": "1. The appearance of the term 'over' in the problem indicates that this is a fraction;2. To the left of 'over', 'nine hundred eighty-seven million six hundred fifty four thousand three hundred twenty-one' is the denominator, written as 987654321;3. To the right of 'over', 'one hundred twenty-three million four hundred fifty-six thousand seven hundred eighty-nine' is the numerator, written as 123456789;4. 'over' is written as '/';5. When written as a fraction, the numerator is written first, followed by '/', and then the denominator;So the answer is 123456789/987654321."},
                               {"role": "user", "content": "The following is a question about how to convert English pronunciation into fractions. Please provide the correct answer based on the numbers in the question.  Question: one hundred twenty three billion four hundred fifty six million seven hundred eighty nine thousand twelve over two hundred ten billion nine hundred eighty seven million six hundred fifty four thousand three hundred twenty one  Answer: Let's think step by step, "},
                               {"role": "assistant", "content": "1. The appearance of the term 'over' in the problem indicates that this is a fraction;2. To the left of 'over', 'two hundred ten billion nine hundred eighty-seven million six hundred fifty-four thousand three hundred twenty-one' is the denominator, written as 210987654321;3. To the right of 'over', 'one hundred twenty-three billion four hundred fifty-six million seven hundred eighty-nine thousand twelve' is the numerator, written as 123456789012;4. 'over' is written as '/';5. When written as a fraction, the numerator is written first, followed by '/', and then the denominator;So the answer is 123456789012/210987654321."},
                               {"role": "user", "content":f"The following is a question about how to convert English pronunciation into fractions. Please provide the correct answer based on the numbers in the question.  Question: {quesion}  Answer: Let's think step by step, "}]
    return prompt