# 使用最大双向匹配算法实现中文分词
# 导入已经写好的FMM和BMM
from tokenization.maxmatching import BMM
from tokenization.maxmatching import FMM


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


# 实现双向匹配算法中的分词方法
def cut_word(raw_sentence, words_dic):
    bmm_word_list = BMM.cut_word(raw_sentence, words_dic)
    fmm_word_list = FMM.cut_word(raw_sentence, words_dic)
    bmm_word_list_size = len(bmm_word_list)
    fmm_word_list_size = len(fmm_word_list)
    if bmm_word_list_size != fmm_word_list_size:
        if bmm_word_list_size < fmm_word_list_size:
            return bmm_word_list
        else:
            return fmm_word_list
    else:
        bsingle = 0
        fsingle = 0
        isSame = True
        for i in range(bmm_word_list_size):
            if fmm_word_list[i] not in bmm_word_list:
                isSame = False
            if fmm_word_list_size == 1:
                fsingle == 1
            if bmm_word_list_size == 1:
                bsingle += 1
        if isSame and bsingle < fsingle:
            return bmm_word_list
        else:
            return fmm_word_list


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
