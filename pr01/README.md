# Практическая работа №1 — Вариант B

## 1. Информация о системе

whoami:
rayasha

pwd:
/home/rayasha

uname -a:
Linux ubuntu 7.0.0-34-generic #34-Ubuntu SMP PREEMPT_DYNAMIC Wed Sep 2 14:34:54 UTC 2026 aarch64 GNU/Linux

lsb_release -a:
Distributor ID: Ubuntu
Description: Ubuntu 26.04.1 LTS
Release: 26.04
Codename: resolute

## 2. Пользователь и группа

Была создана группа developers.

Был создан пользователь student2.

Пользователь student2 был добавлен в группу developers.

Результат команды groups student2:

student2 : student2 users developers

## 3. Каталог /srv/shared

Был создан каталог /srv/shared.

Владелец: root
Группа: developers

Права:

drwxrwsr-x

## 4. Проверка прав

От имени student2 был создан файл student2.txt.

Результат:

-rw-rw-r-- 1 student2 developers 0 student2.txt

Основной пользователь rayasha попытался удалить файл без sudo.

Система запросила подтверждение удаления защищённого от записи файла. После выбора n файл не был удалён.

## 5. Разница между su и sudo

su — переключает текущую сессию на другого пользователя.

sudo — позволяет выполнить отдельную команду с правами администратора.

В Ubuntu постоянный вход под root по умолчанию ограничен из соображений безопасности.

## 6. Настройка .bashrc

В файл ~/.bashrc были добавлены:

alias ll='ls -la'
alias cpr='cd ~/os-course/pr01'
export MY_NAME="rayasha"

Переменная окружения была проверена командой:

echo $MY_NAME

Результат:

rayasha
