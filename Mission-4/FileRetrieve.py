import json
import pdfplumber
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize

questions = json.load(open("questions.json", "r", encoding="utf-8"))
#print(questions[0])


pdf = pdfplumber.open("初赛训练数据集.pdf")
#print(pdf.pages[0].extract_text())


pdf_content = []
for page_idx in range(len(pdf.pages)):
    pdf_content.append({
        'page': 'page_' + str(page_idx + 1),
        'content': pdf.pages[page_idx].extract_text()
    })

questions_word = [' '.join(jieba.lcut(x['question'])) for x in questions]
pdf_content_word = [' '.join(jieba.lcut(x['content'])) for x in pdf_content]

tfidf = TfidfVectorizer()
tfidf.fit(questions_word + pdf_content_word)

# 提取TFIDF
question_feat = tfidf.transform(questions_word)
pdf_content_feat = tfidf.transform(pdf_content_word)

# 进行归一化
question_feat = normalize(question_feat)
pdf_content_feat = normalize(pdf_content_feat)

# 检索进行排序
for query_idx, feat in enumerate(question_feat):
    score = feat @ pdf_content_feat.T
    score = score.toarray()[0]
    max_score_page_idx = score.argsort()[-1] + 1
    questions[query_idx]['reference'] = 'page_' + str(max_score_page_idx)

with open('submit.json', 'w', encoding='utf8') as up:
    json.dump(questions, up, ensure_ascii=False, indent=4)