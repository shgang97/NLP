tag2id, id2tag = {}, {}  # {'NNP': 0, ',': 1, 'VBG': 2, 'TO': 3, 'VB': 4...}
word2id, id2word = {}, {}  # word2id:{'Newsweek': 0, ',': 1, 'trying': 2, 'to': 3, 'keep': 4...}
for line in open('traindata.txt'):
    items = line.split('/')
    word, tag = items[0], items[1].rstrip()
    if word not in word2id:
        word2id[word] = len(word2id)
        id2word[len(id2word)] = word
    if tag not in tag2id:
        tag2id[tag] = len(tag2id)
        id2tag[len(id2tag)] = tag
M = len(word2id)  # M：词典的大小
N = len(tag2id)  # N：词性的种类个数
# 构建pi，A，B
import numpy as np

pi = np.zeros(N)  # 每个词性出现在句子第一个位置的概率
A = np.zeros((N, M))  # A[i][j]:给定tag i，出现单词j的概率
B = np.zeros((N, N))  # B[i][j]:之前的状态是i，之后转换成状态j的概率
prev_tag = ''
for line in open('traindata.txt'):
    items = line.split('/')
    wordId, tagId = word2id[items[0]], tag2id[items[1].rstrip()]
    if prev_tag == '':
        pi[tagId] += 1
        A[tagId][wordId] += 1
    else:
        A[tagId][wordId] += 1
        B[tag2id[prev_tag]][tagId] += 1
    if items[0] == '.':
        prev_tag = ''
    else:
        prev_tag = items[1].rstrip()
pi /= sum(pi)
for i in range(N):
    A[i] /= sum(A[i])
    B[i] /= sum(B[i])


def log(v):
    if v == 0:
        return np.log(v + 0.000001)
    return np.log(v)


def viterbi(x, pi, A, B):
    """

    :param x: user input string/sentence
    :param pi: initial probability of tags
    :param A: 给定tag，每个单词出现的概率
    :param B: tag之间的转移概率
    :return:
    """
    x = [word2id.get(word) for word in x.split(' ')]
    T = len(x)
    dp = np.zeros((T, N))
    ptr = np.array([[0 for x in range(N)] for y in range(T)])
    for j in range(N):
        dp[0][j] = log(pi[j]) + log(A[j][x[0]])
    for i in range(1, T):  # 每个单词
        for j in range(N):  # 每个词性
            dp[i][j] = -99999
            for k in range(N):  # 从每一个k可以到达j
                score = dp[i - 1][k] + log(B[k][j]) + log(A[j][x[i]])
                if score > dp[i][j]:
                    dp[i][j] = score
                    ptr[i][j] = k
    # decoding:把最好的tag sequence打印出来
    best_seq = [0] * T
    # step1：找出对应于最后一个单词的词性
    best_seq[T - 1] = np.argmax(dp[T - 1])
    # step2:通过从后到前的循环依次求出每个单词的词性
    for i in range(T - 2, -1, -1):
        best_seq[i] = ptr[i + 1][best_seq[i + 1]]
    # 到目前位置，best_seq存放了对应于x的词性序列
    for i in range(len(best_seq)):
        print(id2tag[best_seq[i]])


x = 'However , none of the big three weeklies recorded circulation gains recently'
viterbi(x, pi, A, B)
