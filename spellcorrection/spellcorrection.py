import numpy as np
from nltk.corpus import reuters  # 用于导入语料库

# 读取'vocab.txt'文件，生成词典库，转换成set，降低in方法的时间复杂度
# list的in方法的时间复杂度为O(n)，set的in方法的时间复杂度为O(1)
vocab = set([line.rstrip() for line in open('vocab.txt')])


# 定义一个生成候选单词集合的函数
def generate_candidates(word):
    """
    :param word: 给定的输入（错误的输入）
    :return: 返回所有（valid）候选集合
    """
    # 生成边际距离为1的单词
    # 1.insert 2.delete 3.replace
    # e.g. appl: replace:bppl,cppl,aapl,
    #            insert:bappl,cappl,abppl
    #            delete:ppl,apl,app
    letters = 'abcdefghijklmnopqrstuvwxyz'
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    inserts = [L + c + R for L, R in splits for c in letters]
    deletes = [L + R[1:] for L, R in splits if R]
    replaces = [L + c + R[1:] for L, R in splits for c in letters]
    candidates = set(inserts + deletes + replaces)
    # 过滤掉不在词典库的单词
    return [word for word in candidates if word in vocab]


# 导入语料库
categories = reuters.categories()
corpus = reuters.sents(categories=categories)
# 构建语言模型：bigram
term_count = {}
bigram_count = {}
for doc in corpus:
    doc = ['<s>'] + doc
    for i in range(0, len(doc) - 1):
        # bigram:[i:i+1]
        term = doc[i]
        bigram = doc[i:i + 2]
        if term in term_count:
            term_count[term] += 1
        else:
            term_count[term] = 1
        bigram = ' '.join(bigram)
        if bigram in bigram_count:
            bigram_count[bigram] += 1
        else:
            bigram_count[bigram] = 1

# 用户犯错的概率统计--channel probability
channel_prob = {}
for line in open('spell-errors.txt'):
    items = line.split(':')
    correct = items[0].strip()
    mistakes = [item.strip() for item in items[1].strip().split(',')]
    channel_prob[correct] = {}
    for mis in mistakes:
        channel_prob[correct][mis] = 1 / len(mistakes)
V = len(term_count.keys())
file = open('testdata.txt', 'r')
for line in file:
    items = line.rstrip().split('\t')
    line = items[2].split()
    # line=["I","like","playing"]
    for word in line:
        if word not in vocab:
            # 需要替换word成正确的单词
            # step1：生成所有的（valid）候选集合
            candidates = generate_candidates(word)
            probs = []
            # 对于每一个candidate，计算它的score
            # score=P(correct)*P(mistake|correct)
            #      =log P(correct)+log p(mistake|correct)
            # 返回score最大的candidate
            for candi in candidates:
                prob = 0
                # a.计算channel probability
                if candi in channel_prob and word in channel_prob[candi]:
                    prob += np.log(channel_prob[candi][word])
                else:
                    prob += np.log(0.0001)

                # b.计算语言模型的概率
                idx = items[2].index(word) + 1
                if items[2][idx - 1] in bigram_count and candi in bigram_count[items[2][idx - 1]]:
                    prob += np.log((bigram_count[items[2][idx - 1]][candi] + 1.0) / (
                            term_count[bigram_count[items[2][idx - 1]]] + V
                    ))
                else:
                    prob += np.log(1.0 / V)
                probs.append(prob)
            # max_idx = probs.index(max(probs))
            # print(word, candidates[max_idx])
            # print(probs)
