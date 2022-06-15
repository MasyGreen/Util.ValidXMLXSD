import codecs
import datetime
import configparser
import enum
import os
import sys
import xml.etree.ElementTree as ET

import keyboard
from colorama import Fore, Style, init, AnsiToWin32


# Enum for size units
class size_unit(enum.Enum):
    BYTES = 1
    KB = 2
    MB = 3
    GB = 4


def convert_unit(size_in_bytes, unit):
    """ Convert the size from bytes to other units like KB, MB or GB"""
    if unit == size_unit.KB:
        return size_in_bytes / 1024
    elif unit == size_unit.MB:
        return size_in_bytes / (1024 * 1024)
    elif unit == size_unit.GB:
        return size_in_bytes / (1024 * 1024 * 1024)
    else:
        return size_in_bytes


def get_file_size(file_name, size_type=size_unit.BYTES):
    size = 0
    """ Get file in size in given unit like KB, MB or GB"""
    if os.path.exists(file_name):
        size = os.path.getsize(file_name)
    return convert_unit(size, size_type)


def writelogfile(logfile, message):
    with codecs.open(logfile, 'a', encoding='utf-8') as f:
        f.write(f"{message}\n")


def generatesubroot(xpath_str, updroot, log_file):
    if createtree == 1:
        split_xpath = xpath_str.split('/')
        maxcount_split = len(split_xpath)

        msg = f'Генерация структуры: {split_xpath=}; {maxcount_split=}'
        print(f'{Fore.YELLOW}{msg}', file=stream)
        writelogfile(log_file, msg)

        if maxcount_split > 2:
            ind = 0
            for _item in split_xpath:
                ind = ind + 1
                if _item != '.' and _item != '' and ind <= maxcount_split - 1:
                    # поиск атрибутов
                    if _item.find('[') == -1:
                        updroot = ET.SubElement(updroot, _item)
                    else:
                        attr_split = _item.split('[')
                        msg = f'Структура + атрибуты: {attr_split=}'
                        print(f'{Fore.YELLOW}{msg}', file=stream)
                        writelogfile(log_file, msg)

                        if len(attr_split) == 2:
                            updroot = ET.SubElement(updroot, attr_split[0])
                            attr_s = attr_split[1].replace('@', '').replace(']', '').replace('\"', '')
                            attr_l = attr_s.split('=')

                            msg = f'Атрибуты: {attr_l=}'
                            print(f'{Fore.YELLOW}{msg}', file=stream)
                            writelogfile(log_file, msg)
                            updroot.set(attr_l[0], attr_l[1])

                    msg = f'Step {ind}: [{_item}]'
                    print(f'{Fore.YELLOW}{msg}', file=stream)
                    writelogfile(log_file, msg)

    return updroot


def main():
    print(f'XPath: {xpath_str=}; Начальный эл.: {ind_start=}; Последний эл.: {ind_end=}', file=stream)
    print(Style.RESET_ALL, file=stream)

    for in_file in os.listdir(cur_dir):
        if os.path.isfile(in_file) and in_file.endswith(".xml") and not in_file.endswith("_result.xml"):
            in_filename = in_file.split('.')[0]
            xml_file = os.path.join(cur_dir, f'{in_filename}.xml')
            result_file = os.path.join(cur_dir, f'{in_filename}_result.xml')
            log_file = os.path.join(cur_dir, f'{in_filename}.log')

            msg = f"==Start: '{xml_file}'; Size={round(get_file_size(xml_file, size_unit.KB), 2)}{size_unit.KB.name}; {datetime.datetime.now()}"
            print(f'{Fore.CYAN}{msg}', file=stream)
            writelogfile(log_file, msg)

            tree = ET.parse(xml_file)
            root = tree.getroot()
            _items = root.findall(xpath_str)

            msg = f"Кол-во элементов: {len(_items)=}; {datetime.datetime.now()}"
            print(f'{Fore.CYAN}{msg}', file=stream)
            writelogfile(log_file, msg)

            curind: int = 0
            newroot = ET.Element('root')
            subroot = generatesubroot(xpath_str, newroot, log_file)
            for _item in _items:
                curind = curind + 1
                if curind >= ind_start and curind <= ind_end:
                    subroot.append(_item)
                    # print(f'{Fore.GREEN}Result {curind}: {_item.attrib}', file=stream)

            tree = ET.ElementTree(newroot)
            tree.write(result_file, xml_declaration=True, method="xml", encoding="utf-8")

            msg = f"==End: '{result_file}'; Size={round(get_file_size(result_file, size_unit.KB), 2)}{size_unit.KB.name}; {datetime.datetime.now()}"
            print(f'{Fore.CYAN}{msg}', file=stream)
            writelogfile(log_file, msg)


def readconfigfile(filename):
    if os.path.exists(filename):
        try:
            config = configparser.ConfigParser()
            config.read(filename)
            config.sections()
            global xpath_str
            xpath_str = str(config.get("Settings", "xpath"))

            global ind_start
            varstr = str(config.get("Settings", "indstart"))
            ind_start = int(varstr)

            global ind_end
            varstr = str(config.get("Settings", "indend"))
            ind_end = int(varstr)

            global createtree
            varstr = str(config.get("Settings", "createtree"))
            createtree = int(varstr)

        except Exception as ex:
            print(f'{Fore.RED}{ex}; Delete file:{filename}', file=stream)
            xpath_str = f'.//item/item'
            ind_start = 1
            ind_end = 1
    else:
        config = configparser.ConfigParser()
        config.add_section("Settings")
        config.set('Settings', '; Шаблон xpath', './/item[@itemid="kated"]/item')
        config.set("Settings", "xpath", f'.//item/item')
        config.set('Settings', '; Диапазон', 'с 1 по ...')
        config.set("Settings", "indstart", f'0')
        config.set("Settings", "indend", f'0')
        config.set('Settings', '; Шаблон createtree', '0 - False, 1 - True')
        config.set("Settings", "createtree", f'0')
        with open(filename, "w") as f:
            config.write(f)


if __name__ == "__main__":
    init(wrap=False)
    stream = AnsiToWin32(sys.stderr).stream
    cur_dir = os.getcwd()

    print(f"{Fore.CYAN}Last update: Cherepanov Maxim masygreen@gmail.com (c), 06.2021", file=stream)
    print(f"{Fore.CYAN}Get some count element from *.xml;", file=stream)

    _config_file = os.path.join(cur_dir, "config.ini")
    xpath_str = f'.//item/item'
    ind_start = 1
    ind_end = 1
    if readconfigfile(_config_file):
        print(f"{Fore.CYAN}{xpath_str=}", file=stream)

    if ind_end < ind_start:
        ind_start = 0
        ind_end = 0

    if ind_start == 0:
        ind_start = int(input('Начало: '))

    if ind_end == 0:
        ind_end = int(input('Окончание: '))

    if ind_end < ind_start:
        ind_start = 1
        ind_end = 1

    print(f"{Fore.CYAN}Отбор с {ind_start} по {ind_end} ;", file=stream)
    print(f"{Fore.CYAN}======================PROCESS==================", file=stream)

    main()
    print(f'{Fore.CYAN}All Process done\nPress Space to Exit... It the longest shortcut \\_(o0)_\\...', file=stream)
    keyboard.wait("space")
