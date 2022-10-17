# Black Desert

> Bot and automation for Black Desert Online


## 

## Composition
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
    config.example.ini
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
