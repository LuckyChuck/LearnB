# -*-coding: utf-8 -*-
# 对txt文件进行中文分词
import jieba
import os
from utils import files_processing
from gensim.models import word2vec
import multiprocessing

source_folder='./three_kingdoms/source'
segment_folder = './three_kingdoms/segment'
# 字词分割，对整个文件内容进行字词分割
def segment_lines(file_list,segment_out_dir,stopwords=[]):
    for i,file in enumerate(file_list):
        segment_out_name=os.path.join(segment_out_dir,'segment_{}.txt'.format(i))
        with open(file, 'rb') as f:
            document = f.read()
            document_cut = jieba.cut(document)
            sentence_segment=[]
            for word in document_cut:
                if word not in stopwords:
                    sentence_segment.append(word)
            result = ' '.join(sentence_segment)
            result = result.encode('utf-8')
            with open(segment_out_name, 'wb') as f2:
                f2.write(result)

# 对source中的txt文件进行分词，输出到segment目录中
file_list=files_processing.get_files_list(source_folder, postfix='*.txt')
segment_lines(file_list, segment_folder)

sentences = word2vec.PathLineSentences(segment_folder)
segment_folder='./three_kingdoms/segment'
sentences = word2vec.PathLineSentences(segment_folder)

# 设置模型参数，进行训练
model = word2vec.Word2Vec(sentences, size=64, window=3, min_count=2)
print("模型1找出跟曹操最相近的词top5:\n{}".format(model.most_similar("曹操", topn=10)))
print("-"*50)
print("模型1找出曹操+刘备-张飞：{}".format(model.wv.most_similar(positive=['曹操', '刘备'], negative=['张飞'])))
# 设置模型参数，进行训练
model2 = word2vec.Word2Vec(sentences, size=128, window=5, min_count=5, workers=multiprocessing.cpu_count())
# 保存模型
model2.save('./models/word2Vec.model')
print("-"*50)
print("模型2找出跟曹操最相近的词top5:\n{}".format(model2.most_similar("曹操", topn=10)))
print("-"*50)
print("模型2找出曹操+刘备-张飞：{}".format(model2.wv.most_similar(positive=['曹操', '刘备'], negative=['张飞'])))
