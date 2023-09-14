# BackDoor on Python
Проект в технопарк на курс "информационная безопасность"<br><br>

## Предыстория | О проекте | Подробнее о функциях, интерфейсе | Используемые технологии
<img src="assets/cyberstalker.jpg">

## |- Предыстория 🎲 -|
Совсем недавно я пересматривал сериал "Кибер Сталкер" 1 и 2 сезоны. И в голову пришла мысль: "А что если воссоздать подобную программу, которая может подключиться к устройствам на расстоянии, копировать данные, транслировать экран или вебку, записывать звук и т. д.? ".

Начало разработки 03.09.2023 - ...

## |- О проекте (14.09.2023) 🍀 -|
Целью проекта было максимально воссоздать программу для слежки, как в сериале. Для создания программы которой можно управлять на большом расстоянии я использовал Библиотеку Telebot.

На данный момент программа умеет: <b>выполнять комманды в cmd, скачивать файлы <= 50мб с устройства, безопастно записывать звук с микрофона, записывать видео, транслировать экран в реальном времени</b>.

## |- Подробнее о функциях, интерфейсе (14.09.2023) 📃 -|

#### Всего рабочих функций в проекте 10шт
* __cd__ - вывести текущий каталог
* __chdir__ - сменить каталог
* __dir__ - вывести файлы в каталоге
* __rm_file__ - удалить файл
* __exec_cmd__ - выполнить комманду в cmd
* __get_file__ - скачать файл

* __record_audio__ - включить запись микрофона
* __get_audio__ - Отправить из дампа последнюю запись микрофона (После отправления удаляет очищает dump)

* __record_video__ - включить запись экрана (Запускает "бесконечный" цикл записи видео по 70 секунд. 70сек. ~ 30-40мб. Запись прекращается, когда выключается программа либо пк клиента)
* __get_video__ - скачать записанное видео

* __get_screen__ - включить трансляцию экрана (При включении одновременно транслирует экран клиента и записывает транслируемое видео в .avi)


### Интерфейс 
<b>Основное управление осуществляется при помощи Телеграм бота</b>

При запуске функций, кроме:
* __exec_cmd__
* __record_audio__
* __get_audio__
* __record_video__
* __get_screen__

Появляются кнопки с названием файлов в каталоге. При нажатии отправляется название файла и выполняется функция.
Для отмены действия присутствует кнопка "EXIT"

При запуске функций __exec_cmd__, __record_audio__ и __get_screen__ требуется ввод параметров:
* __exec_cmd__ - 1. Выполняемая комманда

* __record_audio__ - 1. Кол-во секунд 2. Кол-во итераций. Вводится одним сообщением. Пример: "5 2" включение записи 2 раза по 5 секунд

* __get_screen__ - 1. Порт 2. ip адрес сервера на который будет транслироваться экран(server.py). Вводится одним сообщением. Пример: "8080 192.158.1.38". 

---

<b>В данный момент в программе ведётся разработка нового функционала...</b><br>
<b>Полное описание работы функций будет в конце завершения проекта...</b>

## Используемые технологии 💻
<div>
    <img src="assets/python.svg" width="60" heigth="60">
    <img src="assets/git.svg" width="60" heigth="60">
</div>