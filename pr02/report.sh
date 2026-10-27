
#!/bin/bash
set -euo pipefail

if [ "$#" -lt 2 ]; then
    echo "Использование: $0 <каталог> <уровень> [--top N]"
    echo "Уровень: ERROR, WARN или INFO"
    exit 1
fi

DIR="$1"
LEVEL="$2"
TOP=0

if [ ! -d "$DIR" ]; then
    echo "Ошибка: каталог не существует"
    exit 1
fi

if [[ ! "$LEVEL" =~ ^(ERROR|WARN|INFO)$ ]]; then
    echo "Ошибка: уровень должен быть ERROR, WARN или INFO"
    exit 1
fi

if [ "$#" -gt 2 ]; then
    if [ "$#" -ne 4 ] || [ "$3" != "--top" ] ||
       ! [[ "$4" =~ ^[1-9][0-9]*$ ]]; then
        echo "Использование: $0 <каталог> <уровень> [--top N]"
        exit 1
    fi
    TOP="$4"
fi

shopt -s nullglob
FILES=("$DIR"/*.log)

if [ "${#FILES[@]}" -eq 0 ]; then
    echo "Ошибка: в каталоге нет файлов .log"
    exit 1
fi

RESULT=$(
    awk -v level="$LEVEL" '
    {
        # Старый формат: module=net
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

        # Формат Linux.log: дата время host service: сообщение
        if (level == "ERROR" && tolower($0) ~ /(error|failed|failure|fatal|alert)/)
            count["linux-log"]++
        else if (level == "WARN" && tolower($0) ~ /(warn|warning|alert)/)
            count["linux-log"]++
        else if (level == "INFO" && tolower($0) ~ /(info|succeeded|initialized|starting|started)/)
            count["linux-log"]++
    }
    END {
        for (module in count)
            printf "%d %s\n", count[module], module
    }' "${FILES[@]}" |
    sort -nr
)

echo "Модуль        Количество"
echo "------------------------"

if [ "$TOP" -gt 0 ]; then
    printf '%s\n' "$RESULT" | head -n "$TOP" |
        awk '{printf "%-14s %d\n", $2, $1}'
else
    printf '%s\n' "$RESULT" |
        awk '{printf "%-14s %d\n", $2, $1}'
fi
