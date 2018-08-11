'''
Срипт автозапуска сервера и приложений
'''

from subprocess import Popen

process_list = []

while True:
    user = input("1 Запустить сервер и клиентов\n"
                 "2 Выйти и закрыть соединения\n"
                 "Выберите пункт меню =")

    if user == '1':
        process_list.append(Popen('python server.py'))
        print('Сервер запущен')

        menu = input('Сколько читающих клиентов запустить? =')
        print('Запуск {} читающих клиентов'.format(menu))
        for i in range(int(menu)):
            process_list.append(Popen('python client.py localhost 8888 r'))

        menu = input('Сколько пишущих клиентов запустить? =')
        print('Запуск {} пишущих клиентов'.format(menu))
        for i in range(int(menu)):
            process_list.append(Popen('python client.py localhost 8888 w'))

    elif user == '2':
        for process in process_list:
            print('Закрываю {}'.format(p))
            process.kill()
        process_list.clear()
        print('Гудбай')
        break
