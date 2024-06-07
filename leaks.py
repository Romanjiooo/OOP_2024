import tkinter as tk
from tkinter import filedialog, messagebox, ttk, Text
from PIL import Image,  ImageGrab
import cv2
import numpy as np
from cryptography.fernet import Fernet
import os
import piexif
import logging
import urllib.request

# Настройка логирования
logging.basicConfig(filename='security_app.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

class EncryptionManager:
    """
    Класс для управления шифрованием и дешифрованием данных
    """
    def __init__(self, key=None):
        self.key = key or self.generate_key()
        self.fernet = Fernet(self.key)

    @staticmethod
    def generate_key():
        """Генерация ключа шифрования"""
        return Fernet.generate_key()

    def encrypt_data(self, data):
        """Шифрование данных"""
        return self.fernet.encrypt(data)

    def decrypt_data(self, encrypted_data):
        """Дешифрование данных"""
        return self.fernet.decrypt(encrypted_data)


class ImageManager:
    """
    Класс для управления изображениями и их шифрованием
    """
    def __init__(self, encryption_manager):
        self.encryption_manager = encryption_manager

    def encrypt_image(self, image_path, encrypted_image_path):
        """Шифрование изображения"""
        try:
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError("Неверный формат изображения.")
            _, encoded_image = cv2.imencode('.png', image)
            encrypted_data = self.encryption_manager.encrypt_data(encoded_image.tobytes())
            with open(encrypted_image_path, 'wb') as file:
                file.write(encrypted_data)
            logging.info(f"Изображение зашифровано: {image_path}")
        except Exception as e:
            logging.error(f"Ошибка при шифровании изображения: {e}")
            messagebox.showerror("Ошибка", f"Не удалось зашифровать изображение: {e}")

    def decrypt_image(self, encrypted_image_path, output_image_path):
        """Дешифрование изображения"""
        try:
            with open(encrypted_image_path, 'rb') as file:
                encrypted_data = file.read()
            decrypted_data = self.encryption_manager.decrypt_data(encrypted_data)
            nparr = np.frombuffer(decrypted_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if image is None:
                raise ValueError("Не удалось декодировать изображение.")
            cv2.imwrite(output_image_path, image)
            logging.info(f"Изображение дешифровано: {encrypted_image_path}")
        except Exception as e:
            logging.error(f"Ошибка при дешифровании изображения: {e}")
            messagebox.showerror("Ошибка", f"Не удалось расшифровать изображение: {e}")

    def extract_metadata(self, image_path):
        """Извлечение метаданных изображения"""
        try:
            image = Image.open(image_path)
            metadata = image.info
            exif_data = piexif.load(image.info['exif']) if 'exif' in image.info else {}
            return metadata, exif_data
        except Exception as e:
            return str(e)


class VideoManager:
    """
    Класс для управления видео и его шифрованием
    """
    def __init__(self, encryption_manager):
        self.encryption_manager = encryption_manager

    def encrypt_video(self, video_path, encrypted_video_path):
        """Шифрование видео"""
        try:
            with open(video_path, 'rb') as file:
                video_data = file.read()
            encrypted_data = self.encryption_manager.encrypt_data(video_data)
            with open(encrypted_video_path, 'wb') as file:
                file.write(encrypted_data)
            logging.info(f"Видео зашифровано: {video_path}")
        except Exception as e:
            logging.error(f"Ошибка при шифровании видео: {e}")
            messagebox.showerror("Ошибка", f"Не удалось зашифровать видео: {e}")

    def decrypt_video(self, encrypted_video_path, output_video_path):
        """Дешифрование видео"""
        try:
            with open(encrypted_video_path, 'rb') as file:
                encrypted_data = file.read()
            decrypted_data = self.encryption_manager.decrypt_data(encrypted_data)
            with open(output_video_path, 'wb') as file:
                file.write(decrypted_data)
            logging.info(f"Видео дешифровано: {encrypted_video_path}")
        except Exception as e:
            logging.error(f"Ошибка при дешифровании видео: {e}")
            messagebox.showerror("Ошибка", f"Не удалось расшифровать видео: {e}")

    def extract_metadata(self, video_path):
        """Извлечение метаданных видео"""
        try:
            cap = cv2.VideoCapture(video_path)
            metadata = {
                "Ширина кадра": cap.get(cv2.CAP_PROP_FRAME_WIDTH),
                "Высота кадра": cap.get(cv2.CAP_PROP_FRAME_HEIGHT),
                "Количество кадров": cap.get(cv2.CAP_PROP_FRAME_COUNT),
                "FPS": cap.get(cv2.CAP_PROP_FPS),
                "Кодек": cap.get(cv2.CAP_PROP_FOURCC),
                "Длительность (сек)": cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
            }
            cap.release()
            return metadata
        except Exception as e:
            return str(e)


class WebcamManager:
    """
    Класс для управления веб-камерой и шифрования снимков с веб-камеры
    """
    def __init__(self, encryption_manager):
        self.encryption_manager = encryption_manager

    def capture_and_encrypt_image(self, output_path):
        """Захват и шифрование изображения с веб-камеры"""
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            _, encoded_image = cv2.imencode('.png', frame)
            encrypted_data = self.encryption_manager.encrypt_data(encoded_image.tobytes())
            with open(output_path, 'wb') as file:
                file.write(encrypted_data)
            logging.info(f"Изображение с веб-камеры захвачено и зашифровано: {output_path}")
        cap.release()

    def decrypt_and_show_image(self, encrypted_image_path):
        """Дешифрование и отображение изображения с веб-камеры"""
        with open(encrypted_image_path, 'rb') as file:
            encrypted_data = file.read()
        decrypted_data = self.encryption_manager.decrypt_data(encrypted_data)
        nparr = np.frombuffer(decrypted_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        cv2.imshow('Дешифрованное изображение с веб-камеры', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


class DroneManager:
    """
    Класс для управления видео с дрона и его шифрования
    """
    def __init__(self, encryption_manager):
        self.encryption_manager = encryption_manager

    def download_video(self, url, save_path):
        """Загрузка видео по URL"""
        try:
            urllib.request.urlretrieve(url, save_path)
            logging.info(f"Видео с дрона загружено: {save_path}")
        except Exception as e:
            logging.error(f"Ошибка при загрузке видео: {e}")
            messagebox.showerror("Ошибка", f"Не удалось загрузить видео: {e}")

    def encrypt_video(self, video_path, encrypted_video_path):
        """Шифрование видео"""
        with open(video_path, 'rb') as file:
            video_data = file.read()
        encrypted_data = self.encryption_manager.encrypt_data(video_data)
        with open(encrypted_video_path, 'wb') as file:
            file.write(encrypted_data)
        logging.info(f"Видео с дрона зашифровано: {video_path}")

    def decrypt_and_play_video(self, encrypted_video_path):
        """Дешифрование и воспроизведение видео"""
        with open(encrypted_video_path, 'rb') as file:
            encrypted_data = file.read()
        decrypted_data = self.encryption_manager.decrypt_data(encrypted_data)
        temp_video_path = 'temp_decrypted_video.mp4'
        with open(temp_video_path, 'wb') as file:
            file.write(decrypted_data)
        cap = cv2.VideoCapture(temp_video_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                cv2.imshow('Дешифрованное видео', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
        cap.release()
        cv2.destroyAllWindows()
        os.remove(temp_video_path)


class ScreenshotManager:
    """
    Класс для захвата снимков экрана и их шифрования
    """
    def __init__(self, encryption_manager):
        self.encryption_manager = encryption_manager

    def capture_and_encrypt_screenshot(self, output_path):
        """Захват и шифрование снимка экрана"""
        screenshot = ImageGrab.grab()
        screenshot_np = np.array(screenshot)
        _, encoded_image = cv2.imencode('.png', screenshot_np)
        encrypted_data = self.encryption_manager.encrypt_data(encoded_image.tobytes())
        with open(output_path, 'wb') as file:
            file.write(encrypted_data)
        logging.info(f"Снимок экрана захвачен и зашифрован: {output_path}")

    def decrypt_and_show_screenshot(self, encrypted_image_path):
        """Дешифрование и отображение снимка экрана"""
        with open(encrypted_image_path, 'rb') as file:
            encrypted_data = file.read()
        decrypted_data = self.encryption_manager.decrypt_data(encrypted_data)
        nparr = np.frombuffer(decrypted_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        cv2.imshow('Дешифрованный снимок экрана', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


class GUIApplication:
    """
    Класс для создания графического интерфейса приложения
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Приложение для шифрования")

        self.encryption_manager = EncryptionManager()

        self.image_manager = ImageManager(self.encryption_manager)
        self.video_manager = VideoManager(self.encryption_manager)
        self.webcam_manager = WebcamManager(self.encryption_manager)
        self.drone_manager = DroneManager(self.encryption_manager)
        self.screenshot_manager = ScreenshotManager(self.encryption_manager)

        self.setup_ui()

    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        self.setup_image_tab()
        self.setup_video_tab()
        self.setup_webcam_tab()
        self.setup_drone_tab()
        self.setup_screenshot_tab()

    def setup_image_tab(self):
        """Настройка вкладки для работы с изображениями"""
        self.image_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.image_tab, text="Шифрование изображений")

        self.image_path_label = tk.Label(self.image_tab, text="Путь к изображению:")
        self.image_path_label.grid(row=0, column=0, padx=10, pady=10)

        self.image_path_entry = tk.Entry(self.image_tab, width=50)
        self.image_path_entry.grid(row=0, column=1, padx=10, pady=10)

        self.browse_image_button = tk.Button(self.image_tab, text="Обзор", command=self.browse_image)
        self.browse_image_button.grid(row=0, column=2, padx=10, pady=10)

        self.encrypt_image_button = tk.Button(self.image_tab, text="Зашифровать изображение", command=self.encrypt_image)
        self.encrypt_image_button.grid(row=1, column=1, pady=10)

        self.decrypt_image_button = tk.Button(self.image_tab, text="Расшифровать изображение", command=self.decrypt_image)
        self.decrypt_image_button.grid(row=2, column=1, pady=10)

        self.image_metadata_label = tk.Label(self.image_tab, text="Метаданные изображения:")
        self.image_metadata_label.grid(row=3, column=0, columnspan=3, pady=10)

        self.image_metadata_text = Text(self.image_tab, width=75, height=10)
        self.image_metadata_text.grid(row=4, column=0, columnspan=3)

    def setup_video_tab(self):
        """Настройка вкладки для работы с видео"""
        self.video_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.video_tab, text="Шифрование видео")

        self.video_path_label = tk.Label(self.video_tab, text="Путь к видео:")
        self.video_path_label.grid(row=0, column=0, padx=10, pady=10)

        self.video_path_entry = tk.Entry(self.video_tab, width=50)
        self.video_path_entry.grid(row=0, column=1, padx=10, pady=10)

        self.browse_video_button = tk.Button(self.video_tab, text="Обзор", command=self.browse_video)
        self.browse_video_button.grid(row=0, column=2, padx=10, pady=10)

        self.encrypt_video_button = tk.Button(self.video_tab, text="Зашифровать видео", command=self.encrypt_video)
        self.encrypt_video_button.grid(row=1, column=1, pady=10)

        self.decrypt_video_button = tk.Button(self.video_tab, text="Расшифровать видео", command=self.decrypt_video)
        self.decrypt_video_button.grid(row=2, column=1, pady=10)

        self.video_metadata_label = tk.Label(self.video_tab, text="Метаданные видео:")
        self.video_metadata_label.grid(row=3, column=0, columnspan=3, pady=10)

        self.video_metadata_text = Text(self.video_tab, width=75, height=10)
        self.video_metadata_text.grid(row=4, column=0, columnspan=3)

        self.play_video_button = tk.Button(self.video_tab, text="Воспроизвести видео", command=self.play_video)
        self.play_video_button.grid(row=5, column=1, pady=10)

    def setup_webcam_tab(self):
        """Настройка вкладки для работы с веб-камерой"""
        self.webcam_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.webcam_tab, text="Шифрование с веб-камеры")

        self.capture_webcam_button = tk.Button(self.webcam_tab, text="Захватить и зашифровать изображение", command=self.capture_and_encrypt_webcam_image)
        self.capture_webcam_button.grid(row=0, column=1, pady=10)

        self.decrypt_webcam_button = tk.Button(self.webcam_tab, text="Расшифровать и показать изображение", command=self.decrypt_and_show_webcam_image)
        self.decrypt_webcam_button.grid(row=1, column=1, pady=10)

        self.webcam_metadata_label = tk.Label(self.webcam_tab, text="Метаданные веб-камеры:")
        self.webcam_metadata_label.grid(row=2, column=0, columnspan=3, pady=10)

        self.webcam_metadata_text = Text(self.webcam_tab, width=75, height=10)
        self.webcam_metadata_text.grid(row=3, column=0, columnspan=3)

    def setup_drone_tab(self):
        """Настройка вкладки для работы с видео с дрона"""
        self.drone_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.drone_tab, text="Шифрование с дрона")

        self.drone_video_url_label = tk.Label(self.drone_tab, text="URL видео с дрона:")
        self.drone_video_url_label.grid(row=0, column=0, padx=10, pady=10)

        self.drone_video_url_entry = tk.Entry(self.drone_tab, width=50)
        self.drone_video_url_entry.grid(row=0, column=1, padx=10, pady=10)

        self.download_drone_video_button = tk.Button(self.drone_tab, text="Скачать и зашифровать видео с дрона", command=self.download_and_encrypt_drone_video)
        self.download_drone_video_button.grid(row=1, column=1, pady=10)

        self.decrypt_drone_video_button = tk.Button(self.drone_tab, text="Расшифровать и воспроизвести видео с дрона", command=self.decrypt_and_play_drone_video)
        self.decrypt_drone_video_button.grid(row=2, column=1, pady=10)

        self.drone_metadata_label = tk.Label(self.drone_tab, text="Метаданные видео с дрона:")
        self.drone_metadata_label.grid(row=3, column=0, columnspan=3, pady=10)

        self.drone_metadata_text = Text(self.drone_tab, width=75, height=10)
        self.drone_metadata_text.grid(row=4, column=0, columnspan=3)

    def setup_screenshot_tab(self):
        """Настройка вкладки для работы с снимками экрана"""
        self.screenshot_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.screenshot_tab, text="Шифрование скриншотов")

        self.capture_screenshot_button = tk.Button(self.screenshot_tab, text="Захватить и зашифровать скриншот", command=self.capture_and_encrypt_screenshot)
        self.capture_screenshot_button.grid(row=0, column=1, pady=10)

        self.decrypt_screenshot_button = tk.Button(self.screenshot_tab, text="Расшифровать и показать скриншот", command=self.decrypt_and_show_screenshot)
        self.decrypt_screenshot_button.grid(row=1, column=1, pady=10)

        self.screenshot_metadata_label = tk.Label(self.screenshot_tab, text="Метаданные скриншота:")
        self.screenshot_metadata_label.grid(row=2, column=0, columnspan=3, pady=10)

        self.screenshot_metadata_text = Text(self.screenshot_tab, width=75, height=10)
        self.screenshot_metadata_text.grid(row=3, column=0, columnspan=3)

    def browse_image(self):
        """Обзор и выбор изображения"""
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.image_path_entry.delete(0, tk.END)
            self.image_path_entry.insert(0, file_path)
            self.display_image_metadata(file_path, self.image_metadata_text)

    def browse_video(self):
        """Обзор и выбор видео"""
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi")])
        if file_path:
            self.video_path_entry.delete(0, tk.END)
            self.video_path_entry.insert(0, file_path)
            self.display_video_metadata(file_path, self.video_metadata_text)

    def download_and_encrypt_drone_video(self):
        """Скачать и зашифровать видео с дрона"""
        video_url = self.drone_video_url_entry.get()
        if video_url:
            video_path = "downloaded_drone_video.mp4"
            encrypted_video_path = filedialog.asksaveasfilename(defaultextension=".dat", filetypes=[("Encrypted Files", "*.dat")])
            if encrypted_video_path:
                self.drone_manager.download_video(video_url, video_path)
                self.drone_manager.encrypt_video(video_path, encrypted_video_path)
                os.remove(video_path)  # Удаление временного файла после шифрования
                messagebox.showinfo("Успех", f"Видео с дрона скачано, зашифровано и сохранено в {encrypted_video_path}")
                self.display_video_metadata(video_path, self.drone_metadata_text)

    def decrypt_and_play_drone_video(self):
        """Расшифровать и воспроизвести видео с дрона"""
        encrypted_video_path = filedialog.askopenfilename(filetypes=[("Encrypted Files", "*.dat")])
        if encrypted_video_path:
            self.drone_manager.decrypt_and_play_video(encrypted_video_path)

    def encrypt_image(self):
        """Зашифровать изображение"""
        image_path = self.image_path_entry.get()
        if image_path:
            encrypted_image_path = filedialog.asksaveasfilename(defaultextension=".dat",
                                                                filetypes=[("Encrypted Files", "*.dat")])
            if encrypted_image_path:
                self.image_manager.encrypt_image(image_path, encrypted_image_path)
                messagebox.showinfo("Успех", f"Изображение зашифровано и сохранено в {encrypted_image_path}")
                self.display_encrypted_metadata(encrypted_image_path, self.image_metadata_text)
        else:
            messagebox.showwarning("Внимание", "Пожалуйста, выберите файл изображения.")

    def decrypt_image(self):
        """Расшифровать изображение"""
        encrypted_image_path = filedialog.askopenfilename(filetypes=[("Encrypted Files", "*.dat")])
        if encrypted_image_path:
            output_image_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                             filetypes=[("Image Files", "*.png")])
            if output_image_path:
                self.image_manager.decrypt_image(encrypted_image_path, output_image_path)
                self.display_image_metadata(output_image_path, self.image_metadata_text)
                messagebox.showinfo("Успех", f"Изображение дешифровано и сохранено в {output_image_path}")
        else:
            messagebox.showwarning("Внимание", "Пожалуйста, выберите зашифрованный файл изображения.")

    def encrypt_video(self):
        """Зашифровать видео"""
        video_path = self.video_path_entry.get()
        if video_path:
            encrypted_video_path = filedialog.asksaveasfilename(defaultextension=".dat",
                                                                filetypes=[("Encrypted Files", "*.dat")])
            if encrypted_video_path:
                self.video_manager.encrypt_video(video_path, encrypted_video_path)
                messagebox.showinfo("Успех", f"Видео зашифровано и сохранено в {encrypted_video_path}")
                self.display_encrypted_metadata(encrypted_video_path, self.video_metadata_text)
        else:
            messagebox.showwarning("Внимание", "Пожалуйста, выберите видеофайл.")

    def decrypt_video(self):
        """Расшифровать видео"""
        encrypted_video_path = filedialog.askopenfilename(filetypes=[("Encrypted Files", "*.dat")])
        if encrypted_video_path:
            output_video_path = filedialog.asksaveasfilename(defaultextension=".mp4",
                                                             filetypes=[("Video Files", "*.mp4")])
            if output_video_path:
                self.video_manager.decrypt_video(encrypted_video_path, output_video_path)
                self.display_video_metadata(output_video_path, self.video_metadata_text)
                messagebox.showinfo("Успех", f"Видео дешифровано и сохранено в {output_video_path}")

    def play_video(self):
        """Воспроизвести видео"""
        video_path = self.video_path_entry.get()
        if video_path:
            cap = cv2.VideoCapture(video_path)
            while cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    cv2.imshow('Видео', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    break
            cap.release()
            cv2.destroyAllWindows()

    def capture_and_encrypt_webcam_image(self):
        """Захватить и зашифровать изображение с веб-камеры"""
        encrypted_image_path = filedialog.asksaveasfilename(defaultextension=".dat",
                                                            filetypes=[("Encrypted Files", "*.dat")])
        if encrypted_image_path:
            self.webcam_manager.capture_and_encrypt_image(encrypted_image_path)
            messagebox.showinfo("Успех", f"Изображение с веб-камеры захвачено и зашифровано в {encrypted_image_path}")
            self.display_encrypted_metadata(encrypted_image_path, self.webcam_metadata_text)

    def decrypt_and_show_webcam_image(self):
        """Расшифровать и показать изображение с веб-камеры"""
        encrypted_image_path = filedialog.askopenfilename(filetypes=[("Encrypted Files", "*.dat")])
        if encrypted_image_path:
            self.webcam_manager.decrypt_and_show_image(encrypted_image_path)

    def capture_and_encrypt_screenshot(self):
        """Захватить и зашифровать скриншот"""
        encrypted_image_path = filedialog.asksaveasfilename(defaultextension=".dat",
                                                            filetypes=[("Encrypted Files", "*.dat")])
        if encrypted_image_path:
            self.screenshot_manager.capture_and_encrypt_screenshot(encrypted_image_path)
            messagebox.showinfo("Успех", f"Скриншот захвачен и зашифрован в {encrypted_image_path}")
            self.display_encrypted_metadata(encrypted_image_path, self.screenshot_metadata_text)

    def decrypt_and_show_screenshot(self):
        """Расшифровать и показать скриншот"""
        encrypted_image_path = filedialog.askopenfilename(filetypes=[("Encrypted Files", "*.dat")])
        if encrypted_image_path:
            self.screenshot_manager.decrypt_and_show_screenshot(encrypted_image_path)

    def display_image_metadata(self, file_path, text_widget):
        """Отображение метаданных изображения"""
        text_widget.delete(1.0, tk.END)
        if file_path.endswith('.dat'):
            text_widget.insert(tk.END, "Зашифрованный файл: метаданные недоступны.")
        else:
            metadata, exif_data = self.image_manager.extract_metadata(file_path)
            formatted_metadata = self.format_metadata(metadata, exif_data)
            text_widget.insert(tk.END, formatted_metadata)

    def display_video_metadata(self, file_path, text_widget):
        """Отображение метаданных видео"""
        text_widget.delete(1.0, tk.END)
        if file_path.endswith('.dat'):
            text_widget.insert(tk.END, "Зашифрованный файл: метаданные недоступны.")
        else:
            metadata = self.video_manager.extract_metadata(file_path)
            formatted_metadata = self.format_video_metadata(metadata)
            text_widget.insert(tk.END, formatted_metadata)

    def display_encrypted_metadata(self, file_path, text_widget):
        """Отображение метаданных зашифрованного файла"""
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, "Зашифрованный файл: метаданные недоступны.")

    @staticmethod
    def format_metadata(metadata, exif_data):
        """Форматирование метаданных изображения"""
        formatted = "Метаданные:\n"
        for key, value in metadata.items():
            formatted += f"{key}: {value}\n"
        formatted += "\nEXIF данные:\n"
        for key, value in exif_data.items():
            formatted += f"{key}: {value}\n"
        return formatted

    @staticmethod
    def format_video_metadata(metadata):
        """Форматирование метаданных видео"""
        formatted = "Метаданные:\n"
        for key, value in metadata.items():
            formatted += f"{key}: {value}\n"
        return formatted

if __name__ == "__main__":
    root = tk.Tk()
    app = GUIApplication(root)
    root.mainloop()