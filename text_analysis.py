import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,QGridLayout, QPlainTextEdit, QPushButton, QLabel, QListWidget,QLineEdit
from PyQt6.QtCore import Qt
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import string

class TextAnalysis(QMainWindow):
    def __init__(self):
        #setting application window size
        super().__init__()
        self.setWindowTitle("Text Analysis Tool")
        self.setGeometry(100,100,800,600)

        #downloading 
        nltk.download('punkt')
        nltk.download('punkt_tab')
        nltk.download('stopwords')

        self.central_widget=QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout=QGridLayout(self.central_widget)

        self.setup_ui()
    
    def setup_ui(self):

        self.text_input=QPlainTextEdit()
        self.text_input.setPlaceholderText("Enter your Text here...")
        self.main_layout.addWidget(self.text_input,0,0,1,2)

        button_widget = QWidget()
        button_layout = QVBoxLayout(button_widget)
        button_layout.setContentsMargins(0, 10, 10, 0)
        self.analyze_button = QPushButton("Analyze")
        self.analyze_button.clicked.connect(self.analyze_text)
        button_layout.addWidget(self.analyze_button, alignment=Qt.AlignmentFlag.AlignRight)
        self.main_layout.addWidget(button_widget, 0, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)


        k_input_widget=QWidget()
        k_input_layout=QHBoxLayout(k_input_widget)
        self.k_input_label=QLabel("Enter k for kth distinct word: ")
        self.k_input=QLineEdit()
        self.k_input.setFixedWidth(50)
        self.k_input.textChanged.connect(self.update_kth_distinct)
        k_input_layout.addWidget(self.k_input_label)
        k_input_layout.addWidget(self.k_input)
        k_input_layout.addStretch()
        self.main_layout.addWidget(k_input_widget,1,0,1,2)


        results_widget=QWidget()
        results_layout=QHBoxLayout(results_widget)

        left_column=QVBoxLayout()
        self.total_words_label=QLabel("Total words: ")
        self.total_intext_label=QLabel()
        self.unique_words_label=QLabel("Unique  words: ")
        self.kth_distinct_label=QLabel()
        left_column.addWidget(self.total_words_label)
        left_column.addWidget(self.total_intext_label)
        left_column.addWidget(self.unique_words_label)
        left_column.addWidget(self.kth_distinct_label)
        left_column.addStretch()

        right_column=QVBoxLayout()
        self.top_words_label=QLabel("Top 10 Words: ")
        self.top_words_list=QListWidget()
        right_column.addWidget(self.top_words_label)
        right_column.addWidget(self.top_words_list)

        results_layout.addLayout(left_column,1)
        results_layout.addLayout(right_column,1)

        self.main_layout.addWidget(results_widget,2,0,1,2)

    def numberToWords(self,num:int):
            if num==0:
                return "Zero"
            
            ones_map = {
                        1: "One",
                        2: "Two",
                        3: "Three",
                        4: "Four",
                        5: "Five",
                        6: "Six",
                        7: "Seven",
                        8: "Eight",
                        9: "Nine",
                        10: "Ten",
                        11: "Eleven",
                        12: "Twelve",
                        13: "Thirteen",
                        14: "Fourteen",
                        15: "Fifteen",
                        16: "Sixteen",
                        17: "Seventeen",
                        18: "Eighteen",
                        19: "Nineteen",
                    }
            tens_map = {
                        20: "Twenty",
                        30: "Thirty",
                        40: "Forty",
                        50: "Fifty",
                        60: "Sixty",
                        70: "Seventy",
                        80: "Eighty",
                        90: "Ninety"
                    }
            
            def get_string(n):
                res=[]
                hundreds=n//100
                if hundreds:
                    res.append(ones_map[hundreds]+ " hundreds")
                last2=n%100
                if last2>=20:
                    tens,ones=last2//10,last2%10
                    res.append(tens_map[tens*10])
                    if ones:
                        res.append(ones_map[ones])
                elif last2:
                    res.append(ones_map[last2])
                return " ".join(res)
            
            postfix=[""," Thousand"," Million"," Billion"]
            i=0
            res=[]
            while num:
                digits=num%1000
                s=get_string(digits)
                if s:
                    res.append(s+postfix[i])
                i+=1
                num=num//1000
            res.reverse()
            return " ".join(res)
    def update_kth_distinct(self):
        if not self.results:
            return
        
        try:
            if self.k_input.text()!="":
                k=int(self.k_input.text())
                kth_distinct,found=self.kthdistinct(self.results["all_words"],k)
                if found:
                    self.kth_distinct_label.setText(f"{k}th distinct word: {kth_distinct}")
                else:
                    self.kth_distinct_label.setText(f"{kth_distinct}")
        except ValueError:
            self.kth_distinct_label.setText("Please enter a valid number for k")
        

    def kthdistinct(self,arr,k):
        count=Counter(arr)
        distinct=0
        for i in arr:
            if count[i]==1:
                distinct+=1
            if distinct==k:
                return (i,1)
        return ("These number of distinct words do not exist in the document",0)
    def analyze_text(self):
        text=self.text_input.toPlainText()
        self.results=self._analyze_text(text)

        self.total_words_label.setText(f"Total words :{self.results['total_words']}")
        self.unique_words_label.setText(f"Total words :{self.results['unique_words']}")
        
        total_in_text=self.numberToWords(self.results["total_words"])
        self.total_intext_label.setText(f"{total_in_text}")

       
        self.top_words_list.clear()
        for word,count in self.results['top_words']:
            self.top_words_list.addItem(f"{word}: {count}")

        self.update_kth_distinct()

    def _analyze_text(self,text):

        tokens=word_tokenize(text.lower())

        stop_words=set(stopwords.words('english'))
        tokens=[word for word in tokens if word not in string.punctuation and word not in stop_words]

        word_freq=Counter(tokens)

        top_words=word_freq.most_common(10)

        total_words=len(tokens)
        unique_words=len(set(tokens))

        return {
            'top_words':top_words,
            'total_words':total_words,
            'unique_words':unique_words,
            'all_words':tokens
        }

if __name__=='__main__':
    app=QApplication(sys.argv)
    window=TextAnalysis()
    window.show()
    sys.exit(app.exec())