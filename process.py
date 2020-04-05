import sys
from bs4 import BeautifulSoup
import os
import pandas as pd

def extract_time(time=''):
    inputtime=time.split(' - ')
    starttime=int(inputtime[0].split(':')[0])
    Endtime=int(inputtime[1].split(':')[0])
    times=[]
    for i in range(starttime,Endtime,1):
        times.append(i)
    return times
def extract_weeks(week=''):
    inputweek=week.split(',')
    week=[]
    for i in inputweek:
        if i.find('-') >=0 :
            weeklong=i.split('-')
            startweek=int(weeklong[0])
            Endweek=int(weeklong[1])+1
            for j in range(startweek,Endweek,1):
                week.append(j)
        else:
            week.append(int(i))

    return week
def main():
    Dayofweek=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
    result={'year':[], 'course':[], 'room':[],'subject':[], 'week':[], 'hour':[] ,'dayofweek':[]}
    for filename in os.listdir('output/'):
        print("processing :"+ filename)
        file = open('output/' +filename).read()
        f=file.replace('<br/> <br/>','</font><font>')
        soup = BeautifulSoup(f, 'lxml')
        year=filename.split('.')[0][-1:]
        course=filename.split('.')[0][0:-1]

        for i in soup.find_all('tr'):
            week=-1
            for td in i.find_all('td'):
                week=week+1
                for f in td.find_all('font'):
                    if (len(f.contents) >1):
                        times=extract_time(f.contents[0])
                        weeks=extract_weeks(f.contents[-1])
                        subject=f.contents[2]
                        Lecturer=f.contents[4]
                        Room=f.contents[6]
                        for t in times:
                            for w in weeks:
                                result['hour'].append(t)
                                result['week'].append(w)
                                result['subject'].append(subject)
                                result['room'].append(str(Room))
                                result['year'].append(year)
                                result['course'].append(course)
                                result['dayofweek'].append(Dayofweek[week])
    df=pd.DataFrame(result)
    df.to_csv("output/final.csv",index=False)




if __name__ == '__main__':
    main();
