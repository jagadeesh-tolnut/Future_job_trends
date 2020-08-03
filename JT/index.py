from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import *
import sys
import webbrowser
from PyQt5 import QtWidgets
from PyQt5 import uic
from urllib.error import HTTPError
from requests.exceptions import ConnectionError
from urllib.error import URLError
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.arima_model import ARIMA
import os
import os.path


#importing the UI file
ui,_ = loadUiType('gui.ui')

class MainApp(QMainWindow, ui):
    def __init__(self,parent=None):
        super(MainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handle_Buttons()
        self.UI()

    def UI(self):
        self.tabWidget.tabBar().setVisible(False)
        self.comboBox_3.addItems(["2025","2024","2023","2022","2021"])
        # self.State.setStyleSheet("QGroupBox { background-color: rgb(0,255,0,20%); border:1px solid rgb(255, 170, 255); }")
        # self.style = self.State.stylesheet()
        self.Box_1()
        self.Box_2()


    def Handle_Buttons(self):
        self.pushButton.clicked.connect(self.Open_Home)
        self.pushButton_2.clicked.connect(self.Open_Search)
        self.pushButton_3.clicked.connect(self.Open_Import)
        self.pushButton_4.clicked.connect(self.Open_Settings)
        #self.pushButton_8.clicked.connect(self.Open_Settings)
        self.pushButton_5.clicked.connect(self.predict)
        self.pushButton_6.clicked.connect(self.import_browse)
        self.pushButton_12.clicked.connect(self.data_plot)
        self.pushButton_9.clicked.connect(self.acf_plot)
        self.pushButton_10.clicked.connect(self.pacf_plot)
        self.pushButton_11.clicked.connect(self.trend_plot)
        self.pushButton_7.clicked.connect(self.import_report)
        self.pushButton_8.clicked.connect(self.apply_blue_theme)
        self.pushButton_17.clicked.connect(self.apply_light_theme)


    def explore(self):
        a = self.lineEdit.text()
        wiki_link = "https://en.wikipedia.org/wiki/"
        wiki_job_link = wiki_link + a
        webbrowser.open(wiki_job_link)



    def import_report(self):
        df = pd.read_csv(self.lineEdit_3.text())
        x = df["Month"]
        self.y = df["jobs"]
        y = df["jobs"]

        p = 3
        d = 2
        q = 3
        if self.checkBox.isChecked():
            p = int(self.lineEdit_4.text())

        if self.checkBox_2.isChecked():
            d = int(self.lineEdit_5.text())

        if self.checkBox_3.isChecked():
            q = int(self.lineEdit_6.text())

        model = ARIMA(y, order=(p, d, q))
        model_fit = model.fit()
        output = model_fit.forecast(60)  # Predicting the next 5 yrs
        self.report_future_job = output[0]
        #print(self.report_Predict_val)
        # self.report_Predict_val = ("{:.2f}".format(self.report_Predict_val))
        self.report_conf = output[2]
        self.report = QDialog()
        self.report.setGeometry(250,50,500,650)
        self.report_job = self.lineEdit_8.text()
        self.report_loc = self.lineEdit_9.text()
        self.report_yr = self.comboBox_3.currentText()
        self.report_calculations()
        self.report_ui()

    def report_calculations(self):
        year = self.report_yr
        year = int(year) - 2020
        report_index_val = (year*12) - 1
        self.report_index = int(report_index_val)
        #print("Calculated")
        self.report_final_value = int(self.report_future_job[self.report_index])
        self.report_initial_value = int(self.y[143])
        self.rep_gr_val = (((self.report_final_value-self.report_initial_value)/self.report_initial_value)*100)
        self.rep_gr_val = float("{:.2f}".format(self.rep_gr_val))
        self.rep_gr_val_dis = str(self.rep_gr_val)+" %"
        self.rep_con_lvl_min = str(self.report_conf[self.report_index][0])
        self.rep_con_lvl_min = float("{:.2f}".format(float(self.rep_con_lvl_min)))
        self.rep_con_lvl_max = str(self.report_conf[self.report_index][1])
        self.rep_con_lvl_max = float("{:.2f}".format(float(self.rep_con_lvl_max)))
        self.rep_con_lvl_val = str(self.rep_con_lvl_min)+" - "+str(self.rep_con_lvl_max)
        self.report_final_value = str("{:.5f}".format(float(self.report_final_value)))



    def report_ui(self):
        title = str(self.report_job) + " trend in " + self.report_yr
        self.report_Title = QLabel(title,self.report)
        self.report_Title.setGeometry(10,15,481,21)
        self.report_Title.setFont(QFont('Times', 20))
        self.report_Title.setAlignment(Qt.AlignCenter)
        self.image = QLabel(self.report)
        if (float(self.rep_gr_val) < 0):
            self.image.setPixmap(QPixmap("pics/red.png"))
        else:
            self.image.setPixmap(QPixmap("pics/green.png"))
        self.image.setGeometry(75,50,350,350)
        self.rep_model = QLabel("Model : ",self.report)
        self.rep_model.setGeometry(40,430, 111, 31)
        self.rep_model.setFont(QFont('Times', 15))
        self.rep_loc = QLabel("Location : ", self.report)
        self.rep_loc.setGeometry(40, 470, 111, 31)
        self.rep_loc.setFont(QFont('Times', 15))
        self.rep_fv = QLabel("Forecasted Value : ", self.report)
        self.rep_fv.setGeometry(40, 510, 201, 31)
        self.rep_fv.setFont(QFont('Times', 15))
        self.rep_con = QLabel("Confidence : ", self.report)
        self.rep_con.setGeometry(40, 550, 141, 31)
        self.rep_con.setFont(QFont('Times', 15))
        self.rep_gr = QLabel("Growth rate : ", self.report)
        self.rep_gr.setGeometry(40, 590, 141, 31)
        self.rep_gr.setFont(QFont('Times', 15))
        self.rep_model_ans = QLabel("ARIMA model", self.report)
        self.rep_model_ans.setGeometry(240, 430, 241, 31)
        self.rep_model_ans.setFont(QFont('Times', 15))
        self.rep_loc_ans = QLabel(self.report_loc, self.report)
        self.rep_loc_ans.setGeometry(240, 470, 241, 31)
        self.rep_loc_ans.setFont(QFont('Times', 15))
        self.rep_fv_ans = QLabel(str(self.report_final_value), self.report)
        self.rep_fv_ans.setGeometry(240, 510, 241, 31)
        self.rep_fv_ans.setFont(QFont('Times', 15))
        self.rep_con_ans = QLabel(self.rep_con_lvl_val, self.report)
        print(str(self.report_conf[self.report_index][1]))
        self.rep_con_ans.setGeometry(240, 550, 241, 31)
        self.rep_con_ans.setFont(QFont('Times', 15))
        self.rep_gr_ans = QLabel(str(self.rep_gr_val_dis), self.report)
        self.rep_gr_ans.setGeometry(240, 590, 241, 31)
        self.rep_gr_ans.setFont(QFont('Times', 15))
        self.report.show()

    def predict(self):
        # Importing the required modules
        import requests
        import bs4
        from urllib.error import HTTPError
        from requests.exceptions import ConnectionError
        from urllib.error import URLError
        import lxml
        import re
        import io

        # creating a user defined function to check the errors before web scrapping
        def urlopen(url):
            try:
                var = "no error"
                read = requests.get(url)
                # requests.sessions().close()
            except HTTPError as e:
                var = "Error occured"
            except URLError as e:
                var = "Error occured"
            except ConnectionError as e:
                var = "Error occured"
            if var:
                return read
            else:
                return "error while openning"

        # Logic to generate the url
        job = self.lineEdit.text()
        loc = self.lineEdit_2.text()
        u1 = "https://www.indeed.co.in/jobs?q="
        u2 = job
        u3 = "&l="
        u4 = loc
        # url = "https://www.indeed.co.in/jobs?q=doctor&l=chennai"
        url = u1 + u2 + u3 + u4
        var = urlopen(url)
        read = bs4.BeautifulSoup(var.text, "lxml")
        # print(read)

        # Pharsing the div tag and taking the number of jobs availabe
        count = read.find("div", attrs={"id": "searchCountPages"}).text.strip()
        # print(count)

        # taking only the number of jobs
        count = re.sub("Page 1 of ", "", count)
        count = re.sub(" jobs", "", count)
        # print(count)

        # creating a new csv file
        with io.open("file1.csv", "w", encoding="utf8") as f1:
            f1.write("min_salary,max_salary\n")

        # loop to access all the pages
        for i in range(0, int(count), 10):
            url = url + "&start=" + str(i)
            var1 = urlopen(url)
            readfull = bs4.BeautifulSoup(var1.text, "lxml")
            # read1 = readfull.select(".salaryText")

            # loop to take all salaries from the page
            for sal in readfull.find_all("span", {"class": "salaryText"}):
                data = sal.text
                data = re.sub("₹", "", data)
                data = re.sub(",", "", data)
                # print(data)

                # classifying months and years
                if (data[-1] == "h"):
                    data = re.sub(" a month", "", data)
                    data = data.split()
                    #print(data)
                    if ("-" in data):
                        min = data[0]
                        max = data[-1]
                    else:
                        min = data[0]
                        max = min

                    max = int(max) * 12
                    min = int(min) * 12
                    #print("month")
                elif (data[-1] == "r"):
                    data = re.sub(" a year", "", data)
                    data = data.split()
                    if ("-" in data):
                        min = data[0]
                        max = data[-1]
                    else:
                        min = data[0]
                        max = max
                    #print("year")
                else:
                    pass
                    #print("differnt value")

                # print(data)
                # print(min)
                # print(max)
                fdata = str(min) + "," + str(max) + "\n"
                #print(fdata)
                # writing the datas to the created file
                with io.open("file1.csv", "a", encoding="utf8") as f1:
                    f1.write(fdata)



        import numpy as np
        import pandas as pd

        df = pd.read_csv("file1.csv", header=0)
        data = df.head(5)
        #print(data)

        experience = self.comboBox_4.currentText()

        min_sal = df["min_salary"]
        min_sal_d = min_sal.describe()
        if experience == "-":
            min_sal = np.median(min_sal)
        elif experience == "0-2 yrs":
            min_sal = min_sal_d["25%"]
        elif experience == "3-5 yrs":
            min_sal = min_sal_d["50%"]
        elif experience == "5+ yrs":
            min_sal = min_sal_d["75%"]
        else:
            min_sal = np.median(min_sal)
        print(min_sal)

        max_sal = df["max_salary"]
        max_sal_d = max_sal.describe()

        if experience == "-":
            max_sal = np.median(max_sal)
        elif experience == "0-2 yrs":
            max_sal = max_sal_d["25%"]
        elif experience == "3-5 yrs":
            max_sal = max_sal_d["50%"]
        elif experience == "5+ yrs":
            max_sal = max_sal_d["75%"]
        else:
            max_sal = np.median(max_sal)

        #max_sal = np.median(max_sal)
        print(max_sal)
        min_sal = int(min_sal)
        min_sal = str(min_sal)
        max_sal = int(max_sal)
        max_sal = str(max_sal)
        if len(min_sal)==5:
            min_sal = min_sal[0]+min_sal[1]+","+min_sal[2]+min_sal[3]+min_sal[4]
        elif len(min_sal) == 6:
            min_sal = min_sal[0] + "," + min_sal[1] + min_sal[2] + "," + min_sal[3] + min_sal[4] + min_sal[5]
        elif len(min_sal) == 7:
            min_sal = min_sal[0] + min_sal[1] + "," + min_sal[2] + min_sal[3] + "," + min_sal[4] + min_sal[5] + min_sal[6]
        elif len(min_sal) == 8:
            min_sal = min_sal[0]+min_sal[1] + min_sal[2] + "," + min_sal[3] + min_sal[4] + "," + min_sal[5] + min_sal[6] + min_sal[7]
        else:
            min_sal = min_sal

        if len(max_sal) == 5:
            max_sal = max_sal[0] + max_sal[1] + "," + max_sal[2] + max_sal[3] + max_sal[4]
        elif len(max_sal) == 6:
            max_sal = max_sal[0] + "," + max_sal[1] + max_sal[2] + "," + max_sal[3] + max_sal[4] + max_sal[5]
        elif len(max_sal) == 7:
            max_sal = max_sal[0] + max_sal[1] + "," + max_sal[2] + max_sal[3] + "," + max_sal[4] + max_sal[5] + max_sal[
                6]
        elif len(max_sal) == 8:
            max_sal = max_sal[0] + max_sal[1] + max_sal[2] + "," + max_sal[3] + max_sal[4] + "," + max_sal[5] + max_sal[
                6] + max_sal[7]
        else:
            max_sal = max_sal

        self.predicted_Salary = ("Salary: "+"₹"+min_sal+" - "+"₹"+max_sal)

        print("Salary: "+"₹"+str(min_sal)+"-"+"₹"+str(max_sal))

        ################ Wiki-Scraper ################

        wiki_title = self.lineEdit.text()
        wiki_link = "https://en.wikipedia.org/wiki/" + wiki_title

        wiki_source = urlopen(wiki_link)
        wiki_data = wiki_source

        self.wiki_soup = bs4.BeautifulSoup(wiki_data.text, "lxml")

        self.wiki_text = ""
        i = 0
        for paragraph in self.wiki_soup.find_all('p'):
            i = i + 1
            if i < 3:
                self.wiki_text = self.wiki_text + paragraph.text
            else:
                break
        pat = re.compile(r'\[\d*\]')
        list = pat.findall(self.wiki_text)
        for r in list:
            self.wiki_text = self.wiki_text.replace(r, '')
        print(self.wiki_text)
        self.sj()

    def sj(self):
        self.wid1 = QDialog()
        self.wid1.setGeometry(400,150,434,565)
        self.job_details = QLabel("Job Details",self.wid1)
        self.job_details.setGeometry(QtCore.QRect(150, 0, 141, 41))
        self.job_details.setFont(QFont('Times', 18))
        self.des = QLabel("Description : ",self.wid1)
        self.des.setGeometry(QtCore.QRect(10,60,131,31))
        self.des.setFont(QFont('Times', 13))
        self.destext = QTextEdit(self.wid1)
        self.destext.setGeometry(10,100,411,281)
        self.destext.setFont(QFont('Times', 13))
        self.destext.setText(self.wiki_text.strip())
        self.sal = QLabel("Package per year : ",self.wid1)
        self.sal.setGeometry(10,400,191,31)
        self.sal.setFont(QFont('Times', 14))
        self.salvalue = QLabel(self.predicted_Salary,self.wid1)
        self.salvalue.setGeometry(30,430,401,51)
        self.salvalue.setFont(QFont('Times', 22))
        self.explore_more = QPushButton("Explore More",self.wid1)
        self.explore_more.setGeometry(130,500,181,41)
        self.explore_more.setFont(QFont('Times',16))
        self.explore_more.clicked.connect(self.explore)
        self.wid1.show()


    def data_plot(self):
        df = pd.read_csv(self.lineEdit_3.text())
        x = df["Month"]
        y = df["jobs"]
        plt.plot(x, y)
        plt.show()

    def acf_plot(self):
        df = pd.read_csv(self.lineEdit_3.text())
        x = df["Month"]
        y = df["jobs"]
        plot_acf(y)
        plt.show()

    def pacf_plot(self):
        df = pd.read_csv(self.lineEdit_3.text())
        x = df["Month"]
        y = df["jobs"]
        plot_pacf(y, lags=15)
        plt.show()

    def trend_plot(self):
        df = pd.read_csv(self.lineEdit_3.text())
        x = df["Month"]
        y = df["jobs"]
        p = 3
        d = 2
        q = 3
        if self.checkBox.isChecked():
            p = int(self.lineEdit_4.text())

        if self.checkBox_2.isChecked():
            d = int(self.lineEdit_5.text())

        if self.checkBox_3.isChecked():
            q = int(self.lineEdit_6.text())

        model = ARIMA(y, order=(p, d, q))
        model_fit = model.fit()
        output = model_fit.forecast(60)  # Predicting the next 5 yrs
        future_job = output[0]
        plt.xlabel("Upcoming 5 years")
        plt.ylabel("No. of jobs")
        plt.plot(future_job, label = "Job line")
        #plt.fill_between(x,output[2][0],output[2][1])
        plt.legend()
        plt.show()



    def import_browse(self):
        data_location = QFileDialog.getOpenFileName(self)
        print(data_location[0])
        self.lineEdit_3.setText(str(data_location[0]))

    def Open_Home(self):
        self.tabWidget.setCurrentIndex(0)

    def Open_Search(self):
        self.tabWidget.setCurrentIndex(1)

    def Open_Import(self):
        self.tabWidget.setCurrentIndex(2)

    def Open_Expert(self):
        self.tabWidget.setCurrentIndex(3)

    def Open_Settings(self):
        self.tabWidget.setCurrentIndex(4)

    def apply_blue_theme(self):
        style = open('themes/blue.css')
        style = style.read()
        self.setStyleSheet(style)

    def apply_light_theme(self):
        style = open('themes/light.css')
        style = style.read()
        self.setStyleSheet(style)
    #
    # def apply_normal_theme(self):
    #     style = open('themes/normal.css')
    #     style = style.read()
    #     self.setStyleSheet(style)


    def Box_1(self):
        box_animation = QPropertyAnimation(self.groupBox, b"geometry")
        box_animation.setDuration(2000)
        box_animation.setStartValue(QRect(0,0,0,0))
        box_animation.setEndValue(QRect(50,140,451,401))
        box_animation.start()
        self.box_animation_1 = box_animation

    def Box_2(self):
        box_animation = QPropertyAnimation(self.groupBox_2, b"geometry")
        box_animation.setDuration(2000)
        box_animation.setStartValue(QRect(0,0,0,0))
        box_animation.setEndValue(QRect(560,140,451,401))
        box_animation.start()
        self.box_animation_2 = box_animation


def main():
    app=QApplication(sys.argv)
    window=MainApp()
    window.show()
    app.exec_()
if __name__ == '__main__':
    main()

