import codecs
import datetime
import enum
import os
import sys
import xml.dom.minidom
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

def savepretty(infile, outfile):
    tree = ET.parse(infile)
    root = tree.getroot()
    xmlstr = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
    with open(outfile, "w", encoding="utf-8") as f:
        f.write(xmlstr)


def main():
    print(Style.RESET_ALL, file=stream)
    for in_file in os.listdir(cur_dir):
        if os.path.isfile(in_file) and in_file.endswith(".xml") and not in_file.endswith("_result.xml"):
            in_filename = in_file.split('.')[0]
            xml_file = f'{cur_dir}\\{in_filename}.xml'
            xml_filepretty = f'{cur_dir}\\{in_filename}_result.xml'
            log_file = f'{cur_dir}\\{in_filename}.log'

            msg = f"==Start: '{xml_file}'; Size={round(get_file_size(xml_file, size_unit.KB), 2)}{size_unit.KB.name}; {datetime.datetime.now()}"
            print(f"{Fore.YELLOW}{msg}", file=stream)
            writelogfile(log_file, msg)
            try:
                savepretty(xml_file, xml_filepretty)
            except Exception as ex:
                print(f'{Fore.RED}{ex}', file=stream)
                writelogfile(log_file, ex)

            msg = f"==End: '{xml_filepretty}'; Size={round(get_file_size(xml_filepretty, size_unit.KB), 2)}{size_unit.KB.name}; {datetime.datetime.now()}"
            print(f"{Fore.YELLOW}{msg}\n", file=stream)
            writelogfile(log_file, msg)


if __name__ == "__main__":
    init(wrap=False)
    stream = AnsiToWin32(sys.stderr).stream
    cur_dir = os.getcwd()

    print(f"{Fore.CYAN}Last update: Cherepanov Maxim masygreen@gmail.com (c), 06.2021", file=stream)
    print(f"{Fore.CYAN}Format all *.xml file in current folder (add prefix _)", file=stream)

    print(f"{Fore.CYAN}======================PROCESS==================", file=stream)

    main()
    print(f'{Fore.CYAN}All Process done\nPress Space to Exit... It the longest shortcut \\_(o0)_\\...', file=stream)
    keyboard.wait("space")
