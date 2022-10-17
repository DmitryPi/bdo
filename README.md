# BDO
> Фарм бот и автоматизиция для игры Black Desert Online


## Стэк

    numpy
    openCV (cv2)
    win32api
    pytest


## Требования
- Разрешение: 1920x1080
- Графика: Очень низкая - Средняя
- Персонаж: Страж Пробуждение
- Минимальный Гир: 269 атаки, 350 защиты
- Интерфейс: избавление от всего лишнего, на что бот может навестись

## Архитектура

    | assets
        | buffs
        | foods
        | loot
        | ui
    | data
        *.json
    | modules
        bdo.py
        bot.py
        camera.py
        keys.py
        utils.py
        vision.py
        | tests
            test_bdo.py
            test_bot.py
            test_camera.py
            test_utils.py
            test_vision.py
    .editorconfig
    .gitignore
    main.py
    requirements.txt

## Tests
```sh
pytest (run all tests)
pytest -s (with i/o logging)
pytest modules/tests/test_db.py (run separate testcase)
pytest -v -m slow (run only decorated tag-mark: @pytest.mark.slow)
pytest -s -v -m "not slow" (inverse - exclude tests decorated with 'slow')
```
