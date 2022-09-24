import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import date, timedelta, datetime
from catboost import CatBoostRegressor, Pool,CatBoostClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn import metrics
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from sklearn import preprocessing
import time
from datetime import date, timedelta
from openpyxl import Workbook, load_workbook
#WebPriceId     tDateObserve        tStockStatus        tCurrentPrice


start_time = time.time()
chunksize = 10000 #батч
Id_corr = []
file_name = 'DS_train(2020-06--2022-06-01).csv'
array = np.array([]) # Массив для
cor_array = None #Массив CPI

id = 1 #Переменная которая содержит id признака которого сейчас рассматриваем
num=1
flag = False

#
def data_exel_read(filename_read):

    exel = load_workbook(filename_read) #загружаем ексель файл как объект
    sheet = exel.sheetnames #получаем в виде списка названия листов
    ws = exel[sheet[0]]
    data = ws.values
    Data = pd.DataFrame(data).to_numpy()
    return Data[2][1:]

date_df_y = data_exel_read('Y_train.xlsx')
date_df_y = date_df_y.astype(float)


def CPI(dataframe,id):
    #cor_array = np.array([])
    dataframe_array = dataframe.to_numpy()
    dataframe['CPI'] = np.zeros(dataframe.shape[0])
    #dataframe = dataframe[['price','CPI']].to_numpy()
    #price_first = 0
    #price_second = 0
    CPI = np.array([])

    if ((dataframe_array[0][0]).date()).day == 10:
        dataframe_array = dataframe_array[1:]
        print(dataframe_array)

    for i in range(0,dataframe.shape[0]-1,2):
        CPI = np.append(CPI,(((dataframe_array[i+1][1]/dataframe_array[i][1])*100)-100))
        dataframe['CPI'] = np.where((dataframe.Data == pd.to_datetime((dataframe_array[i+2][0]).date())), ((dataframe_array[i+1][1]/dataframe_array[i][1])*100)-100, dataframe.CPI)
    #print(sum(CPI))
    if CPI.shape[0] == 23 and sum(CPI)!=0 and (np.corrcoef(CPI, date_df_y[1:])[0][1]) > 0.8:
        #cor_array = np.append(cor_array,(np.corrcoef(CPI, date_df_y[1:])[0][1]))
        #cor_array = np.append(cor_array,(np.array([CPI])))
        print('Корреляция равна = ',np.corrcoef(CPI, date_df_y[1:])[0][1], 'id = ', id)
        print(CPI)
        return CPI


def processing(array, id):
    df = pd.DataFrame(data = array, columns= ['WebPriceId','tDateObserve','tStockStatus','tCurrentPrice'])
    array_options = df.to_numpy()
    OutOfStock = 0
    for i in range(array_options.shape[0]-1): #Считаем Оутстоки
        if array_options[i][2] == 'OutOfStock':
            first_inst  = datetime.strptime(array_options[i][1], '%Y-%m-%d %H:%M:%S.%f').date()
            second_inst = datetime.strptime(array_options[i+1][1], '%Y-%m-%d %H:%M:%S.%f').date()
            OutOfStock += (second_inst-first_inst).days
    if OutOfStock < 210: #Если Инстоков < 30%
        #dt  = datetime.strptime(array[1][1], '%Y-%m-%d %H:%M:%S.%f').date()
        df = df[df['tStockStatus']=='InStock']
        #df['tCurrentPrice'] = np.where((df.tStockStatus == 'OutOfStock'), True, df.tCurrentPrice)
        array = df.to_numpy()
        #print(array)
        first_inst  = datetime.strptime(array[0][1], '%Y-%m-%d %H:%M:%S.%f').date()
        second_inst = datetime(2022, 5, 31).date()

        date_range = pd.Series(pd.date_range(first_inst, periods = (second_inst-first_inst).days+1, freq ='D'))
        #print(array)
        zero_array = np.zeros(date_range.shape[0])

        data_train = pd.DataFrame({'Data': date_range, 'price': zero_array, 'Bool': zero_array})
        data_train['price'] = np.where((data_train.price == 0.0), None, data_train.price)
        data_train['Bool'] = np.where((data_train.Bool == 0.0), None, data_train.Bool)

        munth = pd.to_datetime(data_train.Data[0]).month
        day = pd.to_datetime(data_train.Data[0]).day

        for i in range(array.shape[0]):
            data_train['price'] = np.where((data_train.Data == pd.to_datetime(datetime.strptime(array[i][1], '%Y-%m-%d %H:%M:%S.%f').date())), array[i][3], data_train.price)
            #print(array[i][1])

        data_train = data_train.fillna(method='ffill') #Получаем датафрейм с ценами и датами


        for i in range(zero_array.shape[0]):
            if pd.to_datetime(data_train.Data[i]).day == 10 or ((pd.to_datetime(data_train.Data[i])+timedelta(days=1)).day == 1):
                data_train['Bool'] = np.where((data_train.Data == pd.to_datetime(data_train.Data[i])), True, data_train.Bool)
                #print(pd.to_datetime(data_train.Data[i])+timedelta(days=1))

        data_train.dropna(subset=['Bool'], inplace=True)
        data_train = data_train.drop('Bool', axis=1)

        cpi = CPI(data_train,id)
        return cpi
        #print(data_train.to_string())
        #print(array.shape[0])





for chunk in pd.read_csv(file_name, sep='\t', chunksize=chunksize):
    #print(2)
    '''
    if chunk['WebPriceId'].to_numpy()[0] == id:
        array = np.append(array, (chunk.to_numpy()))
    else:
        id = chunk['WebPriceId'].to_numpy()[0] #Обновляем айдишник
        #print(array)
        array = np.array([]) #Очищаем массив
        array = np.append(array, (chunk.to_numpy())) #добавляем первое значение нового айдишника
        print(id)'''
    #print(id in chunk['WebPriceId'].to_numpy())

    #print(chunk['WebPriceId'].to_numpy())
    while id in chunk['WebPriceId'].to_numpy():
        if id-1 in chunk['WebPriceId'].to_numpy() and flag == True:
            #print(np.reshape(array, (int(array.shape[0]/4), 4)))
            array = np.append(array, (chunk[chunk['WebPriceId'] == id-1].to_numpy())) #Добавляем значения
            array = np.reshape(array, (int(array.shape[0]/4), 4))
            # Тут чёт делаем и потом очищаем массив и берём следующий батч
            cor_array = np.append(cor_array,(processing(array,id)))
            #print(np.reshape(array, (int(array.shape[0]/4), 4)))
            array = np.array([]) #Очищаем массив
            id+=1
            flag = False
            #break

        elif id+1 in chunk['WebPriceId'].to_numpy(): #Если следующее значение есть то обнуляем значение и меняем id
            array = np.append(array, (chunk[chunk['WebPriceId'] == id].to_numpy()))
            # Тут чёт делаем и потом очищаем массив и берём следующий батч
            array = np.reshape(array, (int(array.shape[0]/4), 4))
            #print(pd.DataFrame(data = array, columns= ['WebPriceId','tDateObserve','tStockStatus','tCurrentPrice'])['tStockStatus'].value_counts())
            cor_array = np.append(cor_array,(processing(array,id)))
            array = np.array([]) #Очищаем массив
            id+=1
            flag = False
            #break

        elif id+1 not in chunk['WebPriceId'].to_numpy():#Если следующего значения нет
            array = np.append(array, (chunk[chunk['WebPriceId'] == id].to_numpy()))
            id+=1
            flag = True
'''
    #print(id)
    print(cor_array)
    if cor_array.shape[0] == 4:
        print(cor_array)
        break'''



print("--- %s Время: ---" % (time.time() - start_time))
# 78 сек - 10 000
