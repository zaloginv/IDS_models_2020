﻿### unervsity-project-IDS-models (2021)
в этом репозитории находятся три программы, имитирующие работу системы обнаружения вторжений. первые две программы выполняют аналогичные функции разными способами. речь о **generator.py** и **generator-new.py**

**generator.py** формирует логи, имитирующие логи реального веб-сервера, то есть, записываются посещения страничек сайта пользователей, включая нарушителей, использующих DOS-атаку или SQLi. у программы есть существенный минус - пользователи не работают параллельно. данные записываются в файл test-site.log

эта проблема решается в **generator-new.py**, где используется модуль симуляций, что позволяет работать функциям параллельно, а значит, создавать более реалистичную картину "посещений" сайта

**auditor.py** же является моделью СОВ, которая подключается на проверку к test-site.log, анализируя его на предмет вторжений (DOS и SQLi), предупреждения об атаках выносятся в консоль

данный каталог в общем представляет собой тестовую систему, опыт работы с которой позволил написать свою IPS

   
