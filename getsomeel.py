import codecs
import configparser
import datetime
import os
import enum

import keyboard
import sys
from colorama import Fore, Back, Style, init, AnsiToWin32

import xml.etree.ElementTree as ET


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


def main():
    print(f'XPath: {xpath_str=}; Начальный эл.: {ind_start=}; Последний эл.: {ind_end=}', file=stream)
    print(Style.RESET_ALL, file=stream)

    for in_file in os.listdir(cur_dir):
        if os.path.isfile(in_file) and in_file.endswith(".xml") and not in_file.endswith("_part.xml"):
            in_filename = in_file.split('.')[0]
            xml_file = f'{cur_dir}\\{in_filename}.xml'
            log_file = f'{cur_dir}\\{in_filename}_part.xml'
            print(f'{Fore.CYAN}Обработка: {xml_file=}', file=stream)
            tree = ET.parse(xml_file)
            root = tree.getroot()
            _items = root.findall(xpath_str)
            curind = 0
            newroot = ET.Element("root")
            for _item in _items:
                curind = curind + 1
                if curind >= ind_start and curind <= ind_end:
                    newroot.append(_item)
                    print(f'{Fore.GREEN}Result {curind}: {_item.attrib}', file=stream)

            tree = ET.ElementTree(newroot)
            tree.write(log_file,"utf-8")

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

        except Exception as ex:
            print(f'{Fore.RED}{ex}; Delete file:{filename}', file=stream)
            xpath_str = f'.//item/item'
            ind_start = 1
            ind_end = 1
    else:
        config = configparser.ConfigParser()
        config.add_section("Settings")
        config.set('Settings', '; comment here', './/item[@itemid="kated"]/item')
        config.set("Settings", "xpath", f'.//item/item')
        config.set("Settings", "indstart", f'0')
        config.set("Settings", "indend", f'0')
        with open(filename, "w") as f:
            config.write(f)


if __name__ == "__main__":
    init(wrap=False)
    stream = AnsiToWin32(sys.stderr).stream
    cur_dir = os.getcwd()

    # print(f"{Fore.CYAN}Last update: Cherepanov Maxim masygreen@gmail.com (c), 06.2021", file=stream)
    # print(f"{Fore.CYAN}Get some count element ftom *.xml;", file=stream)

    _config_file = f'{cur_dir}\\config.ini'
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

    print(f"{Fore.CYAN}======================PROCESS==================", file=stream)

    main()
    print(f'{Fore.CYAN}All Process done\nPress Space to Exit... It the longest shortcut \\_(o0)_\\...', file=stream)
    keyboard.wait("space")
