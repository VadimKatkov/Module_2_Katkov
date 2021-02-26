import matplotlib
import pandas as pd
import numpy as np



students = pd.read_csv("D:\SkillFactory\stud_math.csv")
#print(students.info())
students.rename(columns={'studytime, granular':'granular'}, inplace=True) # just rename one column to more appropriate
#print(students.info())

'''
Согласно условию ряд категориальных признаков (Medu, Fedu, traveltime, studytime, failures) принимают значения от 1 до 4 включительно.
Превышение этих значений будет ошибкой. Проверим на наличие таких ошибок.
'''

for col in ['Medu', 'Fedu', 'traveltime', 'studytime', 'failures']:
    list(map(lambda item: print(col, item) if item > 4 else None, students[col]))

#только одно значение в поле Fedu не отвечает условию. Предполагаем, что это ошибка. Заменим его на 4.
students.Fedu.replace(40,4)

#тоже сделаем для признаков famrel, freetime, goout, health. Но проверим на не превышение 5
for col in ['famrel','freetime','goout','health']:
    list(map(lambda item: print(col, item) if item > 5 else None, students[col]))
#тут все хорошо

#проверим главный показатель score на диапазон 0 - 100
print('max значение %d,  min значение %d' % (students.score.min(), students.score.max()))
#тут тоже в ожидаемых пределах

print(students.age.value_counts())
#есть по одному студенту в возврасте 22 и 21 год. Эти наблюдения будут не репрезентативные в выборке. Мы их удалим
students = students[students.age <=20]

cols = ["schoolsup","famsup","paid","activities","nursery","higher","internet","romantic","score",'Medu',
         "Fedu", "traveltime", "studytime", "failures","famrel","freetime","goout","health"]
students.replace(to_replace={"schoolsup":{'yes': 1,'no':0},
                             "famsup":{'yes': 1,'no':0},
                             "paid":{'yes': 1,'no':0},
                             "activity":{'yes': 1,'no':0},
                             "nursery":{'yes': 1,'no':0},
                             "higher":{'yes': 1,'no':0},
                             "internet":{'yes': 1,'no':0},
                             "romantic":{'yes': 1,'no':0}}, inplace=True)

print(students.schoolsup.value_counts())
print(students[cols].corr())

for col in students.columns:
    pct_missing = students[col].isna().mean()
    print(f'{col} - {pct_missing :.1%}')

print(students.groupby(['school', 'higher'])['score'].mean())
print(students.groupby(['school', 'higher'])['score'].count())

