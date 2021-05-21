# Назначение
Проверка соответствия XML схеме XSD
XML Validator Against XSD Schema

# Алгоритм
1) Поиск в текущей директории файлов *.xml
   Find *.xml in current folder
2) Для каждого файла XML поиск файла *.xsd с тем же именем
   Find *.xsd same name
3) В случае ошибки создается файл *.log с тем же именем (файл пополняется с каждым запуском)
   If have error appended *.log same name

