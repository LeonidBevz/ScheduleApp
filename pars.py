from bs4 import BeautifulSoup as BS
import requests


class getRasp:
    urlok=False
    group=[]
    prof=[]
    block=[]
    aud=[]
    groupid=[]
    profid=[]
    blockid=[]
    audid=[]
    info = []
    offschedule =[]
    week = []
    weekstr=[]
    weekup=[]
    weekdown=[]


    def __init__(self):
        self.urlok=self.url_ok()
        if self.urlok:#--------проверка есть ли доступ к сайту-----------#
            r=requests.get("https://guap.ru/rasp/")
            html=BS(r.content,'html.parser')


            for el in html.select(".page > .rasp"):
                title = el.select(".form > span > select")

            self.group=str(title[0].text).split("\n")[1:len(self.group)-1]
            self.prof=str(title[1].text).split("\n")[1:len(self.prof)-1]
            self.block=str(title[2].text).split("\n")[1:len(self.block)-1]
            self.aud=str(title[3].text).split("\n")[1:len(self.aud)-1]
            self.groupid=str(title[0]).split('"')[1::2][2:]
            self.profid=str(title[1]).split('"')[1::2][2:]
            self.blockid=str(title[2]).split('"')[1::2][2:]
            self.audid=str(title[3]).split('"')[1::2][2:]
            #print(self.group,self.prof,self.block,self.aud,self.groupid,self.profid,self.blockid,self.audid,sep="\n")
            self.newRasp(0,0,0,0)

        else:
            self.legends = "Нет доступа к сайту"
            self.weekstr = [""] * 7
            self.weekup = [""] * 7
            self.weekdown = [""] * 7
            self.info = [""]
            self.offschedulestr = ""

    def newRasp(self,newGroup,newProf,newBlock,newAud):
        if self.urlok:
            #----------получение новых данных------------------#
            d=requests.get("https://guap.ru/rasp/" + "?g=" + self.groupid[newGroup] + "&p=" + self.profid[newProf] + "&b=" + self.blockid[newBlock] + "&r=" + self.audid[newAud])
            html1 = BS(d.content, 'html.parser')

            for el in html1.select(".page"):
                title = el.select(".result")
            rasp = title[0].get_text("\n").split("\n")

            #-----если расписание не найдено------#
            if rasp[0]=='' or "Нет данных, удовлетворяющих условиям поиска ..." in rasp[1]:
                self.legends = "Нет данных, удовлетворяющих условиям поиска ..."
                self.weekstr=[""]*7
                self.weekup = [""] * 7
                self.weekdown = [""] * 7
                self.info=[""]
                #if rasp[0]=='':
                #    self.info.append("")
                #else:
                #    self.info.append(rasp[0])
                self.offschedulestr=""
            else:
                legend = rasp[:14]
                self.legends = "\n\n"
                for i in range(len(legend)):
                    self.legends += legend[i]
                    if i % 2 == 1:
                        self.legends += '\n'
                legend = []

                # print(legends)
                rasp = rasp[14:]
                while rasp.count(' ') != 0:
                    rasp.remove(' ')

                ##for i in range(len(rasp) - 1, 0, -1):
                ##    if rasp[i] == '▼' or rasp[i] == '▲' or (
                ##            (rasp[i] == 'Л' or rasp[i] == 'ПР' or rasp[i] == 'ЛР') and rasp[i - 1] != '▼' and rasp[
                ##        i - 1] != '▲'):  # '▲'
                ##        rasp.insert(i, "\n")
                ##        rasp.insert(i - 1, "\n\n")

                #print(rasp)
                # for i in rasp:
                # print(i)

                #-------------------разделение на дни недели----------------------#
                weekid = [0] * 7
                if rasp.count("Понедельник") != 0:
                    weekid[0] = rasp.index("Понедельник")
                else:
                    weekid[0] = -1
                if rasp.count("Вторник") != 0:
                    weekid[1] = rasp.index("Вторник")
                else:
                    weekid[1] = -1
                if rasp.count("Среда") != 0:
                    weekid[2] = rasp.index("Среда")
                else:
                    weekid[2] = -1
                if rasp.count("Четверг") != 0:
                    weekid[3] = rasp.index("Четверг")
                else:
                    weekid[3] = -1
                if rasp.count("Пятница") != 0:
                    weekid[4] = rasp.index("Пятница")
                else:
                    weekid[4] = -1
                if rasp.count("Суббота") != 0:
                    weekid[5] = rasp.index("Суббота")
                else:
                    weekid[5] = -1

                if weekid[5] == -1:
                    weekid[5] = len(rasp) - 1
                while weekid.count(-1) != 0:
                    for i in range(len(weekid) - 2):
                        if weekid[i] == -1:
                            weekid[i] = weekid[i + 1]
                # print(weekid)

                #--------------------занятия вне сетки и информация----------------------------#
                self.info = rasp[0:weekid[0]]
                if 'Вне сетки расписания' in self.info:
                    self.offschedule = self.info[1:]
                    self.info = self.info[:1]
                    #while self.offschedule.count("\n\n")!=0:
                    #   self.offschedule.remove("\n\n")
                    self.offschedule.pop(1)
                    self.offschedule.insert(0,'\n')
                    #print(self.offschedule)
                    for i in range(len(self.offschedule) - 1, 0, -1):
                        if self.offschedule[i] in {'Л','ПР','ЛР','КП','КР'} :
                            self.offschedule.insert(i, '\n')

                    self.offschedulestr=" ".join(self.offschedule)
                # print(info)
                # print(offschedule)

                #----------расписание в строчку------------#
                self.week = []
                for i in range(len(weekid) - 2):
                    self.week.append(rasp[weekid[i]+1:weekid[i + 1]])#дни недели + удаление названия дня (+2)
                self.week.append(rasp[weekid[5]+1:len(rasp) - 1])
                self.week.append("")
                self.weekstr = [[""]] * 7
                #print(self.week)
                for i in range(len(self.week)):
                    self.weekstr[i] = " ".join(self.week[i])
                #print(self.info)


                #----------------Разделение на пары-----------------#
                parid = []
                for i in range(len(self.week)):
                    parid.append([])
                    for j in range(len(self.week[i])):
                        if " пара " in self.week[i][j]:
                            parid[i].append(j)
                    parid[i].append(len(self.week[i]))
                #print(self.week[1])
                #print(parid)

                #-------------Разделение на нижнюю и верхнюю учебную неделю---------------------#
                par=[]
                for i in range(len(parid)):
                    par.append([])
                    for j in range(len(parid[i])-1):
                        #print(parid[i][j],parid[i][j+1])
                        par[i].append(self.week[i][parid[i][j]:parid[i][j+1]])
                self.weekup = []
                self.weekdown = []

                for i in range(len(par)):
                    self.weekup.append([])
                    self.weekdown.append([])
                    for j in range(len(par[i])):
                        if "▼" in par[i][j] and "▲" in par[i][j]:
                            downid=par[i][j].index("▼")
                            self.weekup[i].append(par[i][j][:downid])
                            self.weekdown[i].append(par[i][j][downid:])
                            self.weekdown[i][len(self.weekdown[i])-1].insert(0,par[i][j][0])#Добавление номера и времени пары для нижней недели
                        elif "▼" in par[i][j]:
                            self.weekdown[i].append(par[i][j])
                            #print(par[0][0])
                        elif "▲" in par[i][j]:
                            self.weekup[i].append(par[i][j])
                        else:
                            self.weekup[i].append(par[i][j])
                            self.weekdown[i].append(par[i][j])

                for i in range(len(self.weekup)):
                    for j in range(len(self.weekup[i])):
                        self.weekup[i][j]=" ".join(self.weekup[i][j])
                for i in range(len(self.weekup)):
                    self.weekup[i] = "\n\n".join(self.weekup[i])
                for i in range(len(self.weekdown)):
                    for j in range(len(self.weekdown[i])):
                        self.weekdown[i][j]=" ".join(self.weekdown[i][j])
                for i in range(len(self.weekdown)):
                    self.weekdown[i] = "\n\n".join(self.weekdown[i])
                #-----------вывод пар-------------#
                #for i in range(len(self.weekup)):
                #    for j in range(len(self.weekup[i])):
                #        print(self.weekup[i][j])
                #    print("\n")

                #print(self.weekdown)
    def url_ok(self):
        try:
            r = requests.head("https://guap.ru/rasp/")
            return True
        except:
            return False



