# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 15:03:38 2021

@author: zaloginv
"""


import time
import os
import datetime

def follow(thefile):
    # поиск конца файла
    thefile.seek(0, os.SEEK_END)
    
    # запуск бесконечного цикла
    while True:
        
        try: # для прерывания цикла вручную, чтоб можно было сделать что-то с файлом
        
            # читаем последнюю строчку файла
            line = thefile.readline()
            # sleep если файл не обновляется
            if not line:
                time.sleep(0.1)
                continue
    
            yield line
            
        except KeyboardInterrupt:
            break



def main():
    ############## базовые значения #############
    ips = {} # словарь айпишников
    
    logfile = open("test-site.log","r")
    loglines = follow(logfile)
    
    mainurl = 'https://test-site.com/'
    
    site = [ # список страничек сайта
            'main','news','news/today','news/yesterday','help','contacts' 
            ]
    
    tab = '\t' # разделитель
    dateformat = '%Y-%m-%d %H:%M:%S.%f' # формат даты
    
    for url in range(len(site)): # обновляем список до прямых ссылок
        site[url] = str(mainurl + site[url] + '/')
        
        
        
    ############## обработка строк #####################   
    
    ''' описание некоторых переменных
    req - количество запросов всего
    time - время, в которое пользователь что-то сделал
    url - запрашиваемая строка url
    dos - счётчик возможной dos-атаки
    '''
    
    # итерация через генератор
    for line in loglines:
        
        ip = str(line.split(tab)[1])
        
        # если такого ip ещё нет в словаре
        if ip not in ips:
            ips.update({ip:{'req':0, 'time':None, 'url':''}}) # добавляем ip как ключ 
            ips[ip]['req'] = 1
            ips[ip]['dos'] = 0
            ips[ip]['time'] = datetime.datetime.strptime((line.split(tab)[0]), dateformat)
            ips[ip]['url'] = str(line.split(tab)[3])
            
            
            
        # если такой ip есть в словаре
        elif ip in ips:
            ips[ip]['req'] += 1
            newtime = datetime.datetime.strptime((line.split(tab)[0]), dateformat)
            if abs((ips[ip]['time'] - newtime)) < datetime.timedelta(seconds = 2): # сравниваем, сколько секунд прошло с предыдущего запроса
                   ips[ip]['dos'] += 1 # если прошло меньше 2, то счётчик дос-атак увеличиается
                   
                   # dos-атака
                   if ips[ip]['dos'] > 2:
                        print('DOS-атака. IP-адрес атакующего: ' + str(ip) +
                              '\n' + 'Количество атак: ' + str(ips[ip]['dos']) + '\n' + '\n' )
                        
            ips[ip]['time'] = newtime # присваивается новое время
            ips[ip]['url'] = str(line.split(tab)[3]) # присваивается новый IP
        
        # SQL-атака
        if str(ips[ip]['url']) not in site:
            print('SQL-атака. Сайт атакован по ссылке: ' + str(ips[ip]['url']) +
                 '\n' + 'IP-адрес атакующего: ' + str(ip) +
                 '\n' + 'Время атаки: ' + str(ips[ip]['time']) + '\n' + '\n' )
            


if __name__ == '__main__':
    main();

        
        
        
        
        
        
        
        