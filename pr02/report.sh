#!/bin/bash

if [ $# -lt 2 ]; then
    echo "Использование: $0 <каталог> <уровень> [--top N]"
    echo "Уровень: ERROR или WARN"
    exit 1
fi

DIR="$1"
LEVEL="$2"

if [ ! -d "$DIR" ]; then
    echo "Ошибка: каталог не существует"
    exit 1
fi

if [ "$LEVEL" != "ERROR" ] && [ "$LEVEL" != "WARN" ]; then
    echo "Ошибка: уровень должен быть ERROR или WARN"
    exit 1
fi

TOP=0

if [ "$3" = "--top" ]; then
    if [ -z "$4" ]; then
        echo "Ошибка: укажите N после --top"
        exit 1
    fi
    TOP="$4"
fi

RESULT=$(grep -h "$LEVEL" "$DIR"/*.log 2>/dev/null |
    sed -n 's/.*module=\([^ ]*\).*/\1/p' |
    sort |
    uniq -c |
    sort -nr)

echo "Модуль        Количество"
echo "------------------------"

if [ "$TOP" -gt 0 ]; then
    echo "$RESULT" | head -n "$TOP" |
    awk '{printf "%-14s %d\n", $2, $1}'
else
    echo "$RESULT" |
    awk '{printf "%-14s %d\n", $2, $1}'
fi
