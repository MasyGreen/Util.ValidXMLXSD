# Назначение
Набор утилит для работы с XML

## 1 validxmlxsd
Проверка соответствия XML схеме XSD
XML Validator Against XSD Schema

### Алгоритм
1) Поиск в текущей директории файлов *.xml
   Find *.xml in current folder
2) Для каждого файла XML поиск файла *.xsd с тем же именем
   Find *.xsd same name
3) В случае ошибки создается файл *.log с тем же именем (файл пополняется с каждым запуском)
   If have error appended *.log same name

## 2 conminify
Переформатирует все файлы *.xml в текущей директории в pretty
Format all *.xml file in current folder (add prefix _)

### Алгоритм
1) Поиск в текущей директории файлов *.xml
   
2) Каждый файла XML конвертируется в XML с разделителями, к имени файла добавляется префикс "_"
   
3) Создается файл *.log с тем же именем (файл пополняется с каждым запуском)

