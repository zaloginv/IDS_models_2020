# -*- coding: utf-8 -*-
"""
Created on Tue Nov 30 16:22:05 2021

@author: zaloginv
"""

import random
import simpy
import numpy as np
import datetime



class Server( object ):
    
    log_file = 'test-site.log' # текстовый файл, куда будет записываться лог
    
    site = [ # список страничек сайта
            'main','news','news/today','news/yesterday','help','contacts' 
            ]
    
    SQLi = [
            ' SELECT ',' OR 1 = 1'," 0; 'AND ",'= '
            ]

    def __init__( self, env ):
        self.env = env

    def request( self, client_ip, method, url ):
        
        Server.log = open(Server.log_file, 'a')
        print( f"{datetime.datetime.now()}\t{client_ip}\t{method}\thttps://test-site.com/{url}\t" , file = Server.log) # итоговая строка под запись в лог
        Server.log.close()
        



class ip_make( object ): # создание списка с IP-адресами

    def __init__( self, number, num_bad_sqli, num_bad_dos ):
        self.number = number # общее число ip
        self.num_bad_sqli = num_bad_sqli # число ip, с которых идёт атака sqli
        self.num_bad_dos = num_bad_dos # число ip, с которых идёт dos атака
        
        self.ips_good = []
        self.ips_bad_sqli = []
        self.ips_bad_dos = []

        for i in range( self.number ):
            self.ips_good.append( f"{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}" ) # формируем строчку ip
        
        self.ips_bad_sqli.extend( self.ips_good[ 0:self.num_bad_sqli ] ) # формируем список с ip, с которых идёт атака sqli
        del self.ips_good[ 0:self.num_bad_sqli ] # удаляем скопированные ip из общего списка
        
        self.ips_bad_dos.extend( self.ips_good[ 0:self.num_bad_dos ] ) # формируем список с ip, с которых идёт dos атака
        del self.ips_good[ 0:self.num_bad_dos ]  # удаляем скопированные ip из общего списка
        






def good_client( env, rng, client_ip, server ):

    while True:
        yield env.timeout( rng.uniform( 10, 15 ) ) # вероятность срабатывания по времени (раз в от и до) в секундах
        server.request( client_ip, 'GET', f"{random.choice(Server.site)}/" )


def bad_client_SQLi( env, rng, client_ip, server ):
    
    while True:
        yield env.timeout( rng.uniform( 30, 60 ) ) # вероятность срабатывания по времени (раз в от и до) в секундах
        server.request( client_ip, 'GET', f"{random.choice(Server.site)}/{random.choice(Server.SQLi)}" )

        
def bad_client_dos( env, rng, client_ip, server ):
    attack = 0
    repeats = 7
    while True:
        if attack < repeats:
            attack += 1
            yield env.timeout( rng.uniform( 0, 1 ) ) # вероятность срабатывания по времени (раз в от и до) в секундах
        else:
            attack -= random.randint( repeats, 10)
            yield env.timeout( rng.uniform( 10, 15 ) )
        server.request( client_ip, 'GET', f"{random.choice(Server.site)}/" )





def main():
    
    rng = np.random.default_rng( 0 ) # генератор случайных чисел
#    env = simpy.Environment() # мгновенно
    env = simpy.rt.RealtimeEnvironment() # в реальном времени
    server = Server( env )


    ips = ip_make(10,2,1) # первое число - общее количество ip, второе - атаки sqli, третье - dos
    
    


    for i in range(len( ips.ips_good )):
        (env.process( good_client( env, rng, ips.ips_good[i], server )) )
        
    for i in range(len( ips.ips_bad_sqli )):
        (env.process( bad_client_SQLi( env, rng, ips.ips_bad_sqli[i], server )) )
        
    for i in range(len( ips.ips_bad_dos )):
        (env.process( bad_client_dos( env, rng, ips.ips_bad_dos[i], server )) )

    env.run( until=100 )


if __name__ == '__main__':
	print(main())