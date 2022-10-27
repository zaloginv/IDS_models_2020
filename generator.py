# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 16:22:05 2021

@author: zaloginv
"""

import random
import time


def ip_make(number): # создание списка с IP-адресами, number - количество IP
    ips = []
    for i in range(number):
        ips.append(str(random.randint(0,255)) + '.' + str(random.randint(0,255)) + '.'
                   + str(random.randint(0,255)) + '.' + str(random.randint(0,255)))
    return ips




def user_action(ips, func_text): # активная работа пользователя

    ######## базовые значения #########
    
    site = [ # список страничек сайта
            'main','news','news/today','news/yesterday','help','contacts' 
            ]
    use_time = 1511145956 # исходное время
    
    SQLi = [
            ' SELECT ',' OR 1 = 1'," 0; 'AND ",'= '
            ]
    
    default_user = 40 # вероятность, что сайтом пользуется обычный пользователь
    hack_user = default_user / 2 # вероятность (точнее, числовой отрезок), что пользователь атакует сервер
    dos_time = 1 # сколько секунд ждёт атакующий пользователь при атаке dos
    
    tab = '\t' # разделитель
    
    
    ########### бесконечный цикл ###########

    while True:
        
        try: # для прерывания цикла вручную, чтоб можно было сделать что-то с файлом
            
            func_log = open(func_text, 'a')
            percent_user = random.randint(0,100) # вероятность срабатывания атаки
            
            # действия обычного пользователя
            if percent_user >= default_user:
                use_time += random.randint(0,60) # увеличиваем время
                print( str ( ips[random.randrange(len(ips))] + tab + # добавление IP-адреса
                           time.ctime(use_time) + tab + # генерация времени, в которое пользовател что-то сделал
                           'GET' + tab +
                            'https://test-site.com/' + random.choice(site) + '/' + tab ) , # ссылка, по которой перешёл пользователь
                file = func_log ) # запись строки в файл
                time.sleep(random.randint(1,5)) # время ожидания генерации записи
        
            # атака SQLi
            elif percent_user < default_user and percent_user >= hack_user:
                use_time += random.randint(0,60) # увеличиваем время
                print( str ( ips[random.randrange(len(ips))] + tab + # добавление IP-адреса
                           time.ctime(use_time) + tab + # генерация времени, в которое пользовател что-то сделал
                           'GET' + tab + 
                            'https://test-site.com/' + random.choice(site) + random.choice(SQLi) + tab ) , # ссылка, по которой перешёл пользователь, включая SQLi
                file = func_log ) # запись строки в файл
                time.sleep(random.randint(1,5)) # время ожидания генерации записи
            
            # dos-атака
            else:
                dos_hacker = ips[random.randrange(len(ips))] # выбираем IP, с которого идёт атака
                for i in range(random.randint(5,10)): # для генерации сразу нескольких строчек
                    use_time += dos_time # увеличиваем время
                    print( str ( dos_hacker + tab + # добавление IP-адреса
                               time.ctime(use_time) + tab + # генерация времени, в которое пользовател что-то сделал
                               'GET' + tab +
                                'https://test-site.com/' + random.choice(site) + '/' + tab ) , # ссылка, по которой перешёл пользователь
                    file = func_log ) # запись строки в файл
                    time.sleep(dos_time) # время ожидания генерации записи (ускорено в сравнении с обычным пользователем)
                    
            func_log.close() # закрываем файл, чтобы он сохранился
            
        except KeyboardInterrupt:
            break
            
            






def main():
    all_ips = ip_make(5) # генерируем список с IP
    log = 'test-site.log' # текстовый файл, куда будет записываться лог
    (user_action(all_ips, log)) # запуск основной функции с генератором строк лога
    

if __name__ == '__main__':
    main()