# BackDoor on Python
 Запасной проект на случай если не пройду в технопарк

## Предыстория | О проекте:
### |- Предыстория 🍀 -|
Совсем недавно я пересматривал сериал "Кибер Сталкер" 1 и 2 сезоны. И в голову пришла мысль: "А что если воссоздать подобную программу, которая может подключиться к устройствам на расстоянии, копировать данные, транслировать экран или вебку, записывать звук и т. д.? ".

03.09.2023 я стартовал разработку...

### |- О проекте 🎲 -|
Целью проекта было максимально воссоздать программу для слежки, как в сериале. И первая проблема, с которой столкнулся, была с подключением на расстоянии. Первым делом я полез в Google и всё, что я находил, было связанно с Socket/ами. Вроде не плохое решение проблемы, но! Подключится к устройству можно было только при условии, что вы находитесь в одной сети. И тогда мне пришла идея о использовании телеграм ботов.

#### Проект написан на Python, используемые библиотеки - subprocess, pyautogui, telebot, pyaudio, wave, os, socket.

И всё же: "Почему был добавлен сокет? ". К сожалению, я не придумал, как без сокета передавать данные(трансляция экрана и вебки) на большие расстояния. Была идея реализовать всю эту тему при помощи VidGear, но не срослось. Поэтому как есть. Можно будет подключиться, если вы в одной сети. А так: запись звука с микрофона, управление cmd, скриншот экрана, скачивание файлов с устройства доступны на расстоянии.

#### В проекте 2 файла. Main.py - запускается на устройстве жертвы и Server.py - отвечающий за подключение и трансляцию экрана жертвы и "вебки".