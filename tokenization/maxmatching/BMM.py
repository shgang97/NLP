# 使用最大逆向匹配算法实现中文分词


def loaddict(filename):
    """
    读取字典文件
    载入词典
    :return:
    """
    words_dic = []
    with open(filename, 'r', encoding='utf-8') as dic_input:
        for word in dic_input:
            words_dic.append(word.strip())
    return set(words_dic)


# 实现逆向匹配算法中的分词方法
def cut_word(raw_sentence, words_dic):
    # 统计词典中最长的词
    max_length = max(len(word) for word in words_dic)
    sentence = raw_sentence.strip()
    # 统计序列长度
    words_length = len(sentence)
    # 存储切分好的词语
    cut_word_list = []
    while words_length > 0:
        max_cut_length = min(max_length, words_length)
        subSentence = sentence[words_length - max_cut_length:]
        while max_cut_length > 0:
            if subSentence in words_dic:
                cut_word_list.insert(0, subSentence)
                break
            elif max_cut_length == 1:
                cut_word_list.insert(0, subSentence)
                break
            else:
                max_cut_length = max_cut_length - 1
                subSentence = subSentence[1:]
        sentence = sentence[0:words_length - max_cut_length]
        words_length = words_length - max_cut_length
    words = "/".join(cut_word_list)
    return words


if __name__ == '__main__':
    # 进行交互式测试
    def main():
        """
        用于交互接口
        :return:
        """
        words_dic = loaddict('dic.txt')
        while True:
            print("请输入您要分词的序列：")
            input_str = input()
            if not input_str:
                break
            result = cut_word(input_str, words_dic)
            print("分词结果为：" + result)


    main()
