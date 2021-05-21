import codecs
import datetime
import os

import keyboard
import sys
from colorama import Fore, Back, Style, init, AnsiToWin32
from lxml import etree


def writelog(logfile, message):
    with codecs.open(logfile, 'a', encoding='utf-8') as f:
        f.write(f"{message}\n")


def validate(xsdfile, xmlfile, logfile):
    msg = f'Process: {datetime.datetime.now()}\n{xmlfile=}\n{xsdfile=}\n'
    print(f'{Fore.LIGHTBLUE_EX}{msg}', file=stream)
    writelog(logfile, msg)

    xmlschema_doc = etree.parse(xsdfile)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    doc = etree.parse(xmlfile)
    if xmlschema.validate(doc):
        msg = 'OK'
        print(f'{Fore.GREEN}{msg}', file=stream)
        writelog(logfile, msg)
    else:
        msg = f'Error:'
        print(f"{Fore.RED}{msg}", file=stream)
        writelog(logfile, msg)
        for error in xmlschema.error_log:
            msg = "ERROR ON LINE %s: %s" % (error.line, error.message.encode("utf-8"))
            print(f'{Fore.RED}{msg}', file=stream)
            writelog(logfile, msg)
        writelog(logfile, '______________________________________________\n\n')


def main():
    print(Style.RESET_ALL, file=stream)
    for in_file in os.listdir(os.getcwd()):
        if os.path.isfile(in_file) and in_file.endswith(".xml"):
            in_filename = in_file.split('.')[0]
            xml_file = f'{cur_dir}\\{in_filename}.xml'
            schema_file = f'{cur_dir}\\{in_filename}.xsd'
            log_file = f'{cur_dir}\\{in_filename}.log'
            if os.path.exists(schema_file):
                print(f"{Fore.YELLOW}==Start: '{in_file}' ==", file=stream)
                validate(schema_file, xml_file, log_file)
                print(f"{Fore.YELLOW}==End: '{in_file}' ====", file=stream)
                print(Style.RESET_ALL, file=stream)


if __name__ == "__main__":
    init(wrap=False)
    stream = AnsiToWin32(sys.stderr).stream

    print(f"{Fore.CYAN}Last update: Cherepanov Maxim masygreen@gmail.com (c), 05.2021", file=stream)
    print(f"{Fore.CYAN}Find file the same name in current folder (*.xml; *.xsd)", file=stream)
    print(f"{Fore.CYAN}======================PROCESS==================", file=stream)
    cur_dir = os.getcwd()
    main()
    print(f'{Fore.CYAN}*All Process done\n*Press Space to Exit... It the longest shortcut \_(o0)_\...', file=stream)
    keyboard.wait("space")
