import datetime
import os

import keyboard
from lxml import etree


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def writelog(logfile, message):
    with open(logfile, 'a') as f:
        f.write(f"{datetime.datetime.now()}: {message}\n")


def validate(xsdfile, xmlfile, logfile):
    print(f'{bcolors.OKBLUE}Process: {xsdfile=}; {xmlfile=}')
    xmlschema_doc = etree.parse(xsdfile)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    doc = etree.parse(xmlfile)
    if xmlschema.validate(doc):
        print(f'{bcolors.OKGREEN}OK')
    else:
        log = xmlschema.error_log
        writelog(logfile, log)
        print(f'{bcolors.FAIL}Error: {log.last_error}')


def main():
    for in_file in os.listdir(os.getcwd()):
        if os.path.isfile(in_file) and in_file.endswith(".xml"):
            in_filename = in_file.split('.')[0]
            xml_file = f'{cur_dir}\\{in_filename}.xml'
            schema_file = f'{cur_dir}\\{in_filename}.xsd'
            log_file = f'{cur_dir}\\{in_filename}.log'
            if os.path.exists(schema_file):
                print(f"{bcolors.HEADER}{bcolors.BOLD}File: {in_file}")
                validate(schema_file, xml_file, log_file)
                print(f"{bcolors.OKBLUE}______________________________")


if __name__ == "__main__":
    print(f"{bcolors.HEADER}Last update: Cherepanov Maxim masygreen@gmail.com (c), 05.2021")
    print(f"{bcolors.HEADER}Find file the same name in current folder (*.xml; *.xsd)")
    cur_dir = os.getcwd()
    main()
    print(f'{bcolors.HEADER}\n\n*All Process done\n*Press Space to Exit... It the longest shortcut \_(o0)_\...')
    keyboard.wait("space")