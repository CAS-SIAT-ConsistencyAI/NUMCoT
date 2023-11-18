import argparse

import opencc
import pandas as pda
from transformers import AutoTokenizer, AutoModel


CHINESE_CONVERTERS = {
    't2s': opencc.OpenCC(f't2s.json'),
    's2t': opencc.OpenCC(f's2t.json'),
}

tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm2-6b", trust_remote_code=True)
model = AutoModel.from_pretrained("THUDM/chatglm2-6b", trust_remote_code=True, device='cuda')
model = model.eval()


def main(args):
    translations = []
    df = pda.read_csv(args.input_file)
    print(df.head())
    for item in df.itertuples():
        l = item.problem
        if args.opencc:
            l = CHINESE_CONVERTERS[args.opencc].convert(l)
        response, history = model.chat(tokenizer, f"将古文翻译成现代文：{l.strip()}", history=[])
        print(response)
        translations.append([l.strip(), response])
    from numcot.model import ChatGPT
    from numcot.utils import load_GPTapi

    if __name__ == "__main__":
        api = load_GPTapi()

        df = pda.read_csv("算经十书-Num2Words.csv")
        print(df)
        for item in tqdm(df.itertuples()):
            print(item)
            messages = []
            dic_1 = {"role": "system", "content": "你是一个具有数数能力的人，现在要做百亿以内数的写法。"}
            dic_2 = {"role": "user", "content": f"‘{item.words}’写作什么? "}
            messages += [dic_1, dic_2]
            # result[idiom] = {}
            # result[idiom]['correct_sentiment'] = data[idiom][0]['json']['sentiment']
            # if args.experiment_type == 'direct_inquiry':
            #     prompt = en_pt.direct_inquiry(args, idiom=idiom)
            ret = ChatGPT.GPT(api, messages)
            print(ret)
            #     result[idiom]['infer_sentiment'] = sentiment

    df = pda.DataFrame(translations, columns=['problem', 'translation'])
    df.to_csv(f'{args.input_file}_translation.csv')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', required=True, help='annotation JSON')
    parser.add_argument('--opencc', default=None, choices=['t2s', 's2t'], help='annotation JSON')
    args = parser.parse_args()
    main(args)
