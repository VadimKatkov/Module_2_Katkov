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
students.Fedu = students.Fedu.replace(40,4)

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
students.replace(to_replace={"Pstatus":{'T':1,'A':0},
                             "schoolsup":{'yes': 1,'no':0},
                             "famsup":{'yes': 1,'no':0},
                             "paid":{'yes': 1,'no':0},
                             "activity":{'yes': 1,'no':0},
                             "nursery":{'yes': 1,'no':0},
                             "higher":{'yes': 1,'no':0},
                             "internet":{'yes': 1,'no':0},
                             "romantic":{'yes': 1,'no':0}}, inplace=True)

print(students.schoolsup.value_counts())

# описание аналитик Medu & Fedu содержит категорию  0-нет. Делаем предположение, что в 21-ом века начальное образование
# есть у всех то наблюдения должны принимать значения от 1до 4. Помиотрим сколько таких запмсей.
#print('Образование матери:\n',students.Medu.value_counts())
#print('Образование отца:\n',students.Fedu.value_counts())

# значений 0 не так много, но попробуем их заменить. Оценим как это раполагается в группах мать-отец
#print(students.pivot_table(index=['Medu'], columns=['Fedu'], values=['school'], aggfunc='count'))

students['Medu'] = students.apply(lambda row: row['Fedu'] if row['Medu'] == 0 or pd.isnull(row['Medu']) else row['Medu'], axis=1)
students['Fedu'] = students.apply(lambda row: row['Medu'] if row['Fedu'] == 0 or pd.isnull(row['Fedu']) else row['Fedu'], axis=1)
#print(students.pivot_table(index=['Medu'], columns=['Fedu'], values=['school'], aggfunc='count'))

# тепловая карта показывает, что наибольшую корреляцию score показывает со следующими категориями:
# age, higher, romantic, Medu, studityme, failures, goout, address Выделим их в отдельный датасет и опять построим heatmap
students_short = students[['score', 'age', 'higher', 'romantic', 'Medu', 'studytime', 'failures', 'goout', 'address']]
#пока не удалось понять назначение поля granular. Это дубликат поля studytime с коэффициентом -3.

# оценим пропуски в новом наборе
for col in students_short.columns:
    pct_missing = students_short[col].isna().mean()
    print(f'{col} - {pct_missing :.1%}')
'''
score_qunt_25 = students.score.quantile(q=0.25,  interpolation='linear')
score_qunt_75 = students.score.quantile(q=0.75,  interpolation='linear')
score_std = np.std(students.score)
for row in students.score:
    if row < score_qunt_25-score_std*1.5 or row > score_qunt_75+score_std*1.5:
        print(row)
'''
print(students.groupby(['romantic', 'studytime'])['score'].mean())
print(students.groupby(['address', 'internet'])['score'].mean())

