import codecs
import configparser
import datetime
import os
import enum

import keyboard
import sys
from colorama import Fore, Back, Style, init, AnsiToWin32
from lxml import etree


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
    """ Get file in size in given unit like KB, MB or GB"""
    size = os.path.getsize(file_name)
    return convert_unit(size, size_type)


def writelogfile(logfile, message):
    with codecs.open(logfile, 'a', encoding='utf-8') as f:
        f.write(f"{message}\n")


def validate(xsdfile, xmlfile, logfile):
    msg = f'{xsdfile=}\n' \
          f'{xmlfile=}' \
          f'; Size={round(get_file_size(xmlfile, size_unit.KB), 2)}KB' \
          f'; Size={round(get_file_size(xmlfile, size_unit.MB), 2)}MB'
    print(f'{Fore.LIGHTBLUE_EX}{msg}', file=stream)
    writelogfile(logfile, msg)

    try:
        xmlschema_doc = etree.parse(xsdfile)
        xmlschema = etree.XMLSchema(xmlschema_doc)
        doc = etree.parse(xmlfile)
        strquery = f'count({xpath_count})'
        try:
            msg = f"Count ({xpath_count}): {int(doc.xpath(strquery))}"
            print(f'{Fore.LIGHTBLUE_EX}{msg}', file=stream)
            writelogfile(logfile, msg)
        except Exception as ex:
            msg = f'Ошибка запроса Count ({xpath_count}): {ex}'
            print(f'{Fore.RED}{msg}', file=stream)
            writelogfile(logfile, msg)

        if xmlschema.validate(doc):
            msg = 'OK'
            print(f'{Fore.GREEN}{msg}', file=stream)
            writelogfile(logfile, msg)
        else:
            msg = f'Error validate:'
            print(f"{Fore.RED}{msg}", file=stream)
            writelogfile(logfile, msg)
            for error in xmlschema.error_log:
                msg = "ERROR ON LINE %s: %s" % (error.line, error.message.encode("utf-8"))
                print(f'{Fore.RED}{msg}', file=stream)
                writelogfile(logfile, msg)
    except Exception as ex:
        msg = f'Error file struct:\n{ex}'
        print(f'{Fore.RED}{msg}', file=stream)
        writelogfile(logfile, msg)


def main():
    print(Style.RESET_ALL, file=stream)
    for in_file in os.listdir(cur_dir):
        if os.path.isfile(in_file) and in_file.endswith(".xml"):
            in_filename = in_file.split('.')[0]
            xml_file = f'{cur_dir}\\{in_filename}.xml'
            schema_file = f'{cur_dir}\\{in_filename}.xsd'
            log_file = f'{cur_dir}\\{in_filename}.log'
            if os.path.exists(schema_file):
                msg = f"==Start: '{in_file}' == {datetime.datetime.now()}"
                print(f"{Fore.YELLOW}{msg}", file=stream)
                writelogfile(log_file, msg)
                validate(schema_file, xml_file, log_file)
                msg = f"==End: '{in_file}' ==== {datetime.datetime.now()}"
                print(f"{Fore.YELLOW}{msg}", file=stream)
                writelogfile(log_file, msg)
                print(Style.RESET_ALL, file=stream)
    writelogfile(log_file, '______________________________________________\n\n')


def readconfigfile(filename):
    if os.path.exists(filename):
        try:
            config = configparser.ConfigParser()
            config.read(filename)
            config.sections()
            global xpath_count
            xpath_count = str(config.get("Settings", "xpath"))
        except Exception as ex:
            print(f'{Fore.RED}{ex}', file=stream)
            xpath_count = f'.//item/item'
    else:
        config = configparser.ConfigParser()
        config.add_section("Settings")
        config.set('Settings', '; comment here', './/item[@itemid="kated"]/item')
        config.set("Settings", "xpath", f'.//item/item')
        with open(filename, "w") as f:
            config.write(f)


if __name__ == "__main__":
    init(wrap=False)
    stream = AnsiToWin32(sys.stderr).stream
    cur_dir = os.getcwd()

    print(f"{Fore.CYAN}Last update: Cherepanov Maxim masygreen@gmail.com (c), 05.2021", file=stream)
    print(f"{Fore.CYAN}Find file the same name in current folder (*.xml; *.xsd)", file=stream)

    _config_file = f'{cur_dir}\\config.ini'
    xpath_count = f'.//item/item'
    if readconfigfile(_config_file):
        print(f"{Fore.CYAN}{xpath_count=}", file=stream)

    print(f"{Fore.CYAN}======================PROCESS==================", file=stream)

    main()
    print(f'{Fore.CYAN}All Process done\nPress Space to Exit... It the longest shortcut \\_(o0)_\\...', file=stream)
    keyboard.wait("space")
