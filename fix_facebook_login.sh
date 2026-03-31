#!/bin/bash
# Поправка на Facebook Login - изчистване на cache и рестартиране

echo "======================================================================"
echo "FIX FACEBOOK LOGIN - Почистване на cache и проверки"
echo "======================================================================"

cd ~/repositories/bghrana

echo ""
echo "=== 1. Проверка на git версия ==="
git log --oneline -3

echo ""
echo "=== 2. Проверка на settings.py за Facebook ==="
if grep -q "'facebook'" products/settings.py; then
    echo "✓ Facebook е в settings.py"
    grep -n "'facebook'" products/settings.py | head -3
else
    echo "✗ Facebook ЛИПСВА в settings.py!"
fi

echo ""
echo "=== 3. Изтриване на Python cache ==="
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -name "*.pyc" -delete 2>/dev/null
find . -name "*.pyo" -delete 2>/dev/null
echo "✓ Cache изтрит"

echo ""
echo "=== 4. Рестартиране на app (3 пъти за сигурност) ==="
touch tmp/restart.txt
sleep 2
touch tmp/restart.txt
sleep 2
touch tmp/restart.txt
echo "✓ App рестартиран"

echo ""
echo "=== 5. Финална проверка на SOCIALACCOUNT_PROVIDERS ==="
grep -A 15 "SOCIALACCOUNT_PROVIDERS" products/settings.py | grep -E "(google|facebook)" --color=never

echo ""
echo "======================================================================"
echo "ГОТОВО! Изчакай 30 секунди и тествай:"
echo "1. https://bghrana.com/register - трябва да има Facebook бутон"
echo "2. Натисни Facebook бутона - трябва да отвори Facebook (не Google)"
echo "======================================================================"
