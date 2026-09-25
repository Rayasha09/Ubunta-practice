#!/usr/bin/env bash
set -euo pipefail

TOP=0

if [[ "${1:-}" == "--top" ]]; then
    if [[ $# -ne 4 ]] || ! [[ "$2" =~ ^[1-9][0-9]*$ ]]; then
        echo "Использование: $0 [--top N] <каталог> <ERROR|WARN|INFO>"
        exit 1
    fi
    TOP="$2"
    DIR="$3"
    LEVEL="$4"
else
    if [[ $# -ne 2 && $# -ne 4 ]]; then
        echo "Использование: $0 <каталог> <ERROR|WARN|INFO> [--top N]"
        exit 1
    fi
    DIR="$1"
    LEVEL="$2"

    if [[ $# -eq 4 ]]; then
        if [[ "$3" != "--top" ]] || ! [[ "$4" =~ ^[1-9][0-9]*$ ]]; then
            echo "Неверный параметр --top"
            exit 1
        fi
        TOP="$4"
    fi
fi

if [[ ! -d "$DIR" ]]; then
    echo "Ошибка: каталог не существует: $DIR"
    exit 1
fi

if [[ ! "$LEVEL" =~ ^(ERROR|WARN|INFO)$ ]]; then
    echo "Ошибка: уровень должен быть ERROR, WARN или INFO"
    exit 1
fi

shopt -s nullglob
FILES=("$DIR"/*.log)

if [[ ${#FILES[@]} -eq 0 ]]; then
    echo "Ошибка: в каталоге нет файлов .log"
    exit 1
fi

RESULT=$(
    awk -v level="$LEVEL" '
    {
        if ($0 ~ ("(^|[[:space:]])" level "([[:space:]]|$)")) {
            module = ""
            for (i = 1; i <= NF; i++) {
                if ($i ~ /^module=/) {
                    module = $i
                    sub(/^module=/, "", module)
                    break
                }
            }
            if (module != "") count[module]++
        }

        lower = tolower($0)
        if (level == "ERROR" && lower ~ /(error|failed|failure|fatal|alert)/)
            count["linux-log"]++
        else if (level == "WARN" && lower ~ /(warn|warning|alert)/)
            count["linux-log"]++
        else if (level == "INFO" && lower ~ /(info|succeeded|initialized|starting|started)/)
            count["linux-log"]++
    }
    END {
        for (module in count)
            printf "%d %s\n", count[module], module
    }' "${FILES[@]}" | sort -k1,1nr
)

echo "Модуль        Количество"
echo "------------------------"

if [[ -n "$RESULT" ]]; then
    if [[ "$TOP" -gt 0 ]]; then
        printf '%s\n' "$RESULT" | head -n "$TOP" |
            awk '{printf "%-14s %d\n", $2, $1}'
    else
        printf '%s\n' "$RESULT" |
            awk '{printf "%-14s %d\n", $2, $1}'
    fi
else
    echo "Совпадений не найдено"
fi
