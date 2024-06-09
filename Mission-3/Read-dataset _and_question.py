import json
import pdfplumber


questions = json.load(open("Mission-3\questions.json", "r", encoding="utf-8"))
#print(questions[0])


pdf = pdfplumber.open("Mission-3\初赛训练数据集.pdf")
#print(pdf.pages[0].extract_text())


pdf_content = []
for page_idx in range(len(pdf.pages)):
    pdf_content.append({
        'page': 'page_' + str(page_idx + 1),
        'content': pdf.pages[page_idx].extract_text()
    })

print(len(pdf_content))