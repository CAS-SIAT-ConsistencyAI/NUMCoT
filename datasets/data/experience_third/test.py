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


if __name__ == '__main__':
    # 测试函数
    test_strings = ["4133.0", "123",'0','0.00', "123.0", "123.456", "abc", "123.00", " 0.00100 "]
    test_results = [process_string(s) for s in test_strings]
    print(test_results)

