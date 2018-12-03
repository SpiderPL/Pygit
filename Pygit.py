#!/usr/bin/env python3


import collections
import os
import hashlib
import shutil
import platform
import sys

############
# Unit tests
############

class Test: # Testy poszczegolnych funkcji

    def start_test(main_dest):
        test_dest = main_dest + '/testing'
        os.makedirs(test_dest)
        open(test_dest + '/test1.dat', 'a').close()
        open(test_dest + '/test2.dat', 'a').close()


    def test_check_files(main_dest):
        files.check_files(main_dest+'/testing')
        path1 = main_dest + '/testing/Pygit/stage_file/'
        path2 = main_dest + '/testing/Pygit/commit/'
        file = main_dest + '/testing/Pygit/commit/pygitdata.dat'
        assert os.path.exists(path1) and os.path.exists(path2) and os.path.isfile(file) == True


    def test_metadata(main_dest):
        test_dest = main_dest + '/testing/'
        logfile = open(test_dest + '/Pygit/commit/pygitdata.dat', 'w')
        logfile.write(str('2' + ' ' + 'c' + ' ' + 'test1.dat' + ' \n'))
        logfile.close()
        data_files, number_of_lines = files.metadata(test_dest)
        assert data_files[0][0] == '2' and data_files[0][1] == 'c' and number_of_lines == 1


    def test_check_sum(main_dest):
        test_dest1 = main_dest + '/testing/test1.dat'
        test_dest2 = main_dest + '/testing/test2.dat'
        assert files.check_sum(test_dest1) == 'd41d8cd98f00b204e9800998ecf8427e' and files.check_sum(test_dest2) == 'd41d8cd98f00b204e9800998ecf8427e'


    def test_move(main_dest):
        src = main_dest + '/testing/test1.dat'
        dest =main_dest + '/testing/Pygit/commit/test1.dat'
        move(src, dest)
        assert os.path.isfile(src) == False and os.path.isfile(dest) == True


    def test_copy(main_dest):
        src = main_dest + '/testing/test2.dat'
        dest = main_dest + '/testing/Pygit/stage_file/test2.dat'
        copy_files_list=[]
        copy(src, dest, copy_files_list)
        assert os.path.isfile(dest) == True


    def test_delete_files(main_dest):
        copy_files=[]
        copy_files.append(main_dest + '/testing/Pygit/stage_file/test2.dat')
        delete_files(copy_files)
        assert os.path.isfile(main_dest + '/testing/Pygit/stage_file/test2.dat') == False


    def end_test(main_dest):
        test_dest = main_dest + '/testing'
        os.system('rm -rf {}'.format(test_dest))



def Test_run(destination): # Funkcja wykonujaca wszystkie napisane testy jednostkowe
    Test.start_test(destination)
    Test.test_check_files(destination)
    Test.test_metadata(destination)
    Test.test_check_sum(destination)
    Test.test_move(destination)
    Test.test_copy(destination)
    Test.test_delete_files(destination)
    Test.end_test(destination)


########
#Funkcje
########


class files:
    def check_files(main_dest):  # Sprawdza czy foldery i plik z metadanymi istnieja
        if not os.path.exists(
                main_dest + '/Pygit/stage_file/'):
            os.makedirs(main_dest + '/Pygit/stage_file/')
        if not os.path.exists(main_dest + '/Pygit/commit/'):
            os.makedirs(main_dest + '/Pygit/commit/')
            open(main_dest + '/Pygit/commit/pygitdata.dat', 'a').close()


    def metadata(main_dest):  # Pobiera dane z plikow metadanych
        try:
            with open(main_dest + '/Pygit/commit/pygitdata.dat', 'r') as data_lines:
                number_of_lines = (len([line.rstrip('\n') for line in data_lines]))

            with open(main_dest + '/Pygit/commit/pygitdata.dat') as plik:
                data_file = [list(map(str, werse.split(' '))) for werse in plik]
            return data_file, number_of_lines
        except IOError:
            print('File not found')
            exit(0)
        except (MemoryError, RuntimeError):
            print('Not enough ram')
            exit(0)


    def show_status(name, status, version): # Funkcja do wyswietlania statusu plikow
        Status_name = collections.namedtuple('status_name', ['n', 's', 'm', 'c'],
                                             rename=False)  # określenia statusu plików
        status_name = Status_name(n='(new file)', s='(staged file)', m='(modified file)', c='')
        if not name == 'n' and not name == 's' and not name == 'c':
            status_file = 'file error'  # nieokreślony stan w przypadku
            if status == 'n':
                status_file = status_name.n
            elif status == 's':
                status_file = status_name.s
            elif status == 'c':
                status_file = status_name.c
            elif status == 'm':
                status_file = status_name.m
            print(name, status_file, ' version: ',
                  version)  # możliwość rozszerzenia informacji o numer commitowanej wersji
        else:
            print('Metafile error')  # wyświetla błąd informujący o nieprawidłowym statusie pliku
            exit(0)


    def check_sum(filepath): # Funkcja do zestawiania sumy kontrolnej plikow o tej samej nazwie
        with open(filepath, 'rb') as fh:
            m = hashlib.md5()
            while True:
                file = fh.read(8192)
                if not file:
                    break
                m.update(file)
            return m.hexdigest()







def move(src, dest):  # Przeniesienie plikow w postaci zmiany kilku bitow
    shutil.move(src, dest)


def copy(src, dest, copy_files_list): # Kopiowanie plikow z poziomu powloki linuksa jest nieporownywalnie szybsze
    try:
        os.system('cp -a {} {}'.format(src, dest))
    except IOError:
        print('Disk is full')
        delete_files(copy_files_list)
        exit(0)


def delete_files(copy_files): # Funkcja do usuwania skopiowanych plikow w przypadku np; braku miejsa na dysku
    for i in range(len(copy_files)):
        os.system('rm -f {}'.format(copy_files[i]))


def clean_input(command):
    command = command.replace(' ', '')
    return (command)


def check_is_file(dest,main_dest):
    for i in range(len(dest)):
        path1 = main_dest + '/Pygit/stage_file/' + os.path.basename(dest[i][2])
        path2 = main_dest + '/Pygit/commit/' + dest[i][2]
        if (os.path.isfile(path1)) != True and dest[i][1] == 's':
            print('Error, file: {} not exist'.format(dest[i][2]))
            exit(0)
        if (os.path.isfile(path2)) != True and dest[i][1] == 'c' or (os.path.isfile(path2)) != True and dest[i][
            1] == 'm':
            print('Error, file: {} not exist'.format(dest[i][2]))
            exit(0)


def save_data(destination, number_oflines, data_file):
    try:
        logfile = open(destination, 'w')
        for i in range(number_oflines):
            logfile.write(str(data_file[i][0]) + ' ' + str(data_file[i][1]) + ' ' + str(data_file[i][2]) + ' \n')
        logfile.close()
    except IOError:
        print('Cannot open the datafile')
        exit(0)


def read_data(destination, number_oflines, data_file):
    try:
        logfile = open(destination, 'r')

        for i in range(number_oflines):
            data_file[i] = logfile.readline()
            data_file[i] = data_file[i].split(' ', 3)
        logfile.close()
        return (data_file)
    except IOError:
        print('Cannot open the datafile')
        exit(0)




###############
#Główne komendy
###############




def command_input_function(main_dest):  # Komenda status
    files.check_files(main_dest)
    data_file, number_of_lines = files.metadata(main_dest)
    data_stage = os.listdir(main_dest)
    for k in range(len(os.listdir(main_dest))):
        for i in range(number_of_lines):
            if data_stage[k] == data_file[i][2] and data_file[i][1] == 'c' or data_stage[k] == data_file[i][2] and \
                    data_file[i][1] == 'm':
                # Funkcja sprawdza czy istnieje plik o tej samej nazwie w stanie commitowanym lub modyfikowanym
                if not files.check_sum(main_dest + '/Pygit/commit/' + data_file[i][2]) == files.check_sum(
                        main_dest + '/' + data_stage[k]):
                    data_file[i][0] = str(
                        int(data_file[i][0]) + 1)  # Podwyższa poziom wersji dla danego zapisu pliku w pliku metadanych
                    data_file[i][1] = 'm'
    if number_of_lines > 1:  # Sprawdza czy został dodany jakikolwiek plik do Pygit
        for i in range(number_of_lines):  # Wyświetla stan plików zapisanych w pliku metadanych
            files.show_status(data_file[i][2], data_file[i][1], data_file[i][0])
    else:
        print('file without stage, commit and new file')
    dest = './Pygit/commit/pygitdata.dat'
    save_data(dest, number_of_lines, data_file)





def command_input_commit(main_dest):  # Komenda commit
    files.check_files(main_dest)
    data_file, number_of_lines = files.metadata(main_dest)

    for i in range(number_of_lines):
        if data_file[i][1] == 's':  # Wyszukuje wszystkie pliki o stanie stage do zmiany na commit w pliku metadanych
            move(main_dest + '/Pygit/stage_file/' + data_file[i][2], main_dest + '/Pygit/commit/' + data_file[i][2])
            data_file[i][1] = 'c'  # Zmienia stan tylko przekopiowanych plików w pliku metadanych na commit
    dest = main_dest + '/Pygit/commit/pygitdata.dat'
    save_data(dest, number_of_lines, data_file)




def command_input_init(main_dest):  # Komenda init
    files.check_files(main_dest)
    data_file, number_of_lines = files.metadata(main_dest)
    data_stage = os.listdir(main_dest)  # Pobiera nazwy plików w repozytorium
    check_is_file(data_file,main_dest)
    add = 0
    for k in range(len(os.listdir(main_dest))):
        # Wykonuje tyle cykli ile jest plików i folderów w bierzącym folderze
        is_file_in_data_file = 0
        for j in range(number_of_lines):
            if str(data_file[j][2]) == str(
                    data_stage[k]):  # Sprawdza czy dany plik został już zapisany do pliku metadanych
                is_file_in_data_file = 1

        if (os.path.isfile(data_stage[k])) == True and not data_stage[k] == 'main.py' and is_file_in_data_file == 0:
            # Informacje o pliku zostają zapisane jeśli nie został znaleziony w pliku metadanych
            number_of_lines = number_of_lines + 1
            data_file.append('1' + ' ' + 'n' + ' ' + str(data_stage[k]))
            add += 1
    dest = './Pygit/commit/pygitdata.dat'
    if add > 0:
        for i in range(number_of_lines - add, number_of_lines):
            data_file[i] = data_file[i].split(' ', 2)

    save_data(dest, number_of_lines, data_file)




def command_input_add(command_input,main_dest):  # Komenda add ścieżka_do_pliku
    files.check_files(main_dest)
    data_file, number_of_lines = files.metadata(main_dest)
    data_stage = command_input[3:]
    dest = './Pygit/commit/pygitdata.dat'
    data_file = read_data(dest, number_of_lines, data_file)

    for m in range(number_of_lines):
        if data_file[m][2] == data_stage and data_file[m][
            1] == 's':  # Sprawdzanie czy istnieje nazwa pliku w pliku metadanych
            continue

        if (os.path.isfile(data_stage)) == True and not data_stage == 'main.py' and data_file[m][
            1] == 'n':
            copy(main_dest + '/' + data_stage,
                 main_dest + '/Pygit/stage_file/' + os.path.basename(data_stage))
            data_file[m][1] = 'n'
            for j in range(number_of_lines):
                if str(data_file[j][2]) == str(data_stage) and str(data_file[j][1]) == 'n':
                    data_file[j][1] = 's'
                    continue
                elif data_file[j][2] == data_stage and data_file[j][1] == 'c' or data_file[j][2] == data_stage and \
                        data_file[j][1] == 'm':
                    if not md5_checksum(main_dest + '/Pygit/commit/' + data_file[j][2]) == md5_checksum(
                            main_dest + '/' + data_stage):
                        data_file[j][0] = str(int(data_file[i][0]) + 1)
                        data_file[j][1] = 'm'
                        continue
    dest = './Pygit/commit/pygitdata.dat'
    save_data(dest, number_of_lines, data_file)




def command_input_add_all(main_dest):  # Komenda add *
    files.check_files(main_dest)
    data_file, number_of_lines = files.metadata(main_dest)
    data_stage = os.listdir(main_dest)
    dest = './Pygit/commit/pygitdata.dat'
    data_file = read_data(dest, number_of_lines, data_file)
    copy_files = []
    for k in range(len(os.listdir(main_dest))):
        for m in range(number_of_lines):
            if data_file[m][2] == data_stage[k] and data_file[m][
                1] == 's':  # Sprawdzanie czy istnieje nazwa pliku w pliku metadanych
                continue
            if (os.path.isfile(data_stage[k])) == True and not data_stage[k] == 'main.py' and data_file[m][
                1] == 'n':

                copy(main_dest + '/' + data_stage[k],
                     main_dest + '/Pygit/stage_file/' + os.path.basename(data_stage[k]), copy_files)
                copy_files.append(main_dest + '/Pygit/stage_file/' + os.path.basename(data_stage[k]))
                data_file[m][1] = 's'
                break

                for j in range(number_of_lines):
                    if str(data_file[j][2]) == str(data_stage[k]) and str(data_file[j][1]) == 'n':
                        data_file[j][1] = 's'
                        continue
                    elif data_file[j][2] == data_stage[k] and data_file[j][1] == 'c' or data_file[j][2] == data_stage[
                        k] and data_file[j][1] == 'm':
                        if not md5_checksum(main_dest + '/Pygit/commit/' + data_file[j][2]) == md5_checksum(
                                main_dest + '/' + data_stage[k]):
                            data_file[j][0] = str(int(data_file[i][0]) + 1)
                            data_file[j][1] = 'm'
                            continue

    dest = './Pygit/commit/pygitdata.dat'
    save_data(dest, number_of_lines, data_file)




if __name__ == '__main__':  # Główna część programu

    assert ('Linux' == platform.system()), 'This code runs on Linux only. It is {}'.format(platform.system())

    destination = os.getcwd()

    #Uruchomienie testow jednostkowych
    Test_run(destination)

    try:
        #komendy: status, commit, init, add*, add sciezka_do_wskazanego_pliku
        command = clean_input(input())
    except:
        print('Unexpected error:', sys.exc_info()[0])
        exit(0)

    for i in range(len(command)):
        if command[i:i + 6] == 'status':
            command_input_function(destination)
            break
        elif command[i:i + 6] == 'commit':
            command_input_commit(destination)
            break
        elif command[i:i + 4] == 'init':
            command_input_init(destination)
            break
        elif command[i:i + 3] == 'add':
            if command[i:i + 4] == 'add*':
                command_input_add_all(destination)
                break
            else:
                # print('odpala else')
                command_input_add(command,destination)
                break
        if i + 1 == len(command):
            print('wrong command')

