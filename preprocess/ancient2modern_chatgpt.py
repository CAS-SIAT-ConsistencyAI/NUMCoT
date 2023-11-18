import argparse

import opencc
import pandas as pda
from tqdm import tqdm

from numcot.model import ChatGPT

CHINESE_CONVERTERS = {
    't2s': opencc.OpenCC(f't2s.json'),
    's2t': opencc.OpenCC(f's2t.json'),
}


def main(opts):
    data = []
    df = pda.read_csv(opts.input_file)#.sample(10)
    print(df.head())
    for item in tqdm(df.itertuples()):
        l = item.problem
        if opts.opencc:
            l = CHINESE_CONVERTERS[opts.opencc].convert(l)

        if pda.isna(item.problem_ancient):
            messages = [
                {"role": "system", "content": "你数学能力和古汉语能力都很不错。"},
                {"role": "user", "content": f"给古文添加标点符号：{l.strip()}"}
            ]
            problem_ancient = ChatGPT.GPT(messages)
        else:
            problem_ancient = item.problem_ancient

        if pda.isna(item.problem_modern):
            messages = [
                {"role": "system", "content": "你数学能力和古汉语能力都很不错。"},
                {"role": "user", "content": f"将古汉语翻译成现代汉语：{l.strip()}"}
            ]
            problem_modern = ChatGPT.GPT(messages)
        else:
            problem_modern = item.problem_modern

        data.append([l.strip(), problem_ancient, problem_modern])

    df = pda.DataFrame(data, columns=['problem', 'problem_ancient', 'problem_modern'])
    df.to_csv(f'{opts.input_file}_converted.csv')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', required=True, help='annotation JSON')
    parser.add_argument('--opencc', default=None, choices=['t2s', 's2t'], help='annotation JSON')
    args = parser.parse_args()
    main(args)
