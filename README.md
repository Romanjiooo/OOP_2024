# OOP_2024 — BMSTU Projects (Python)

Учебный репозиторий с двумя курсовыми работами МГТУ им. Н. Э. Баумана:

- **BMSTU RPG** — 2D-игра на **Pygame** (ООП, сцены, NPC, боёвка, столкновения).
- **Encryption GUI** — настольное **Tkinter/OpenCV** приложение для шифрования/дешифрования изображений, видео, веб-камеры и скриншотов с логированием и метаданными.

> Если вы здесь из резюме: ключевые файлы — `git.py` и `classes.py` (игра) и `leaks.py` (GUI).

## Быстрый старт

### Вариант A — через venv + requirements.txt

# Клонировать
git clone https://github.com/Romanjiooo/OOP_2024.git
cd OOP_2024

# Создать и активировать виртуальное окружение
# Windows
python -m venv .venv
.venv\Scripts\activate
# macOS/Linux
# python3 -m venv .venv
# source .venv/bin/activate

# Установить зависимости
pip install -r requirements.txt

<img width="1223" height="699" alt="image" src="https://github.com/user-attachments/assets/b8c09c30-7e2c-4404-96c3-c6c324ad4910" />
<img width="1402" height="782" alt="image" src="https://github.com/user-attachments/assets/2a1e842e-df26-405d-a279-70b342b58087" />

<img width="1382" height="762" alt="image" src="https://github.com/user-attachments/assets/b5136900-6762-4eba-9987-eb5914479698" />

Также была сделана вторая курсовая работа в файле leaks.py
это GUI-приложение на Tkinter, которое шифрует/дешифрует изображения, видео, скриншоты и кадры с веб-камеры с помощью Fernet (сохраняет как .dat), может скачивать видео по URL (дрон), извлекает EXIF/видеометаданные, воспроизводит расшифрованное медиа и ведёт лог в security_app.log.
Для windows скачать все библиотеки:
py -m pip install --upgrade pip && py -m pip install pillow opencv-python numpy cryptography piexif
после чего увидите окно
<img width="717" height="465" alt="image" src="https://github.com/user-attachments/assets/e9ad50fd-6545-452f-9fbc-1f96187d2c71" />
