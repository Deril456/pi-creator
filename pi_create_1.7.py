from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import threading

# Функция для сохранения изображения в формате .pi
def save_pi(image, filename):
    width, height = image.size
    pixels = image.load()

    with open(filename, 'wb') as f:
        f.write(width.to_bytes(4, byteorder='big'))
        f.write(height.to_bytes(4, byteorder='big'))

        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                f.write(r.to_bytes(1, byteorder='big'))
                f.write(g.to_bytes(1, byteorder='big'))
                f.write(b.to_bytes(1, byteorder='big'))

# Функция для создания 3D модели
def create_3d_model(image, model_filename):
    width, height = image.size
    pixels = np.array(image)

    with open(model_filename, 'w') as f:
        f.write('o Model\n')
        for y in range(height):
            for x in range(width):
                z = int(np.clip((pixels[y, x][0] + pixels[y, x][1] + pixels[y, x][2]) / 3, 0, 255))
                f.write(f'v {x} {y} {z}\n')
        for y in range(height - 1):
            for x in range(width - 1):
                f.write(f'f {x + y * width + 1} {x + (y + 1) * width + 1} {(x + 1) + (y + 1) * width + 1}\n')
                f.write(f'f {x + y * width + 1} {(x + 1) + (y + 1) * width + 1} {(x + 1) + y * width + 1}\n')

# Функция для восстановления старого фото
def restore_old_photo(image):
    image = image.filter(ImageFilter.SHARPEN)
    image = image.filter(ImageFilter.MedianFilter(size=3))
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.5)
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1.2)
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(1.3)
    return image

# Функция для сохранения аудио в формате .pi
def save_audio_as_pi(audio_path, output_filename):
    try:
        with open(audio_path, 'rb') as audio_file:
            audio_data = audio_file.read()
            with open(output_filename, 'wb') as pi_file:
                pi_file.write(audio_data)
        print(f"Audio saved to {output_filename}")
    except Exception as e:
        print(f"Failed to save audio: {e}")

# Основная функция обработки изображения
def process_image(input_filename, output_filename, model_filename, audio_path, new_size=(256, 256), restore=False):
    try:
        image = Image.open(input_filename).convert('RGB')
        image = image.resize(new_size, Image.BICUBIC)

        if restore:
            image = restore_old_photo(image)

        save_pi(image, output_filename)
        create_3d_model(image, model_filename)

        # Сохранение аудио
        audio_output_path = output_filename.replace('.pi', '_audio.pi')
        save_audio_as_pi(audio_path, audio_output_path)

        print(f"Image converted and saved to {output_filename}")
        print(f"3D model created and saved to {model_filename}")
    except Exception as e:
        print(f"Failed to process image: {e}")

# Функция для запуска в отдельном потоке
def convert_image(input_filename, output_pi_filename, output_model_filename, audio_path, new_size=(256, 256), restore=False):
    thread = threading.Thread(target=process_image, args=(input_filename, output_pi_filename, output_model_filename, audio_path, new_size, restore))
    thread.start()
    thread.join()

# Укажите путь к входному изображению и аудио
input_image_path = '/storage/emulated/0/Pictures/starinnoe_foto_semejnaja_para_obshchedostupnaja_fotografija_i_n_zubkova_s_peterburg.jpg'
output_pi_path = '/storage/emulated/0/Download/RESTORED_PHOTO.pi'
output_model_path = '/storage/emulated/0/Download/model_restored5.obj'
audio_path = '/storage/emulated/0/Music/Telegram/EVERYTHING_IS_DIFFICULT_AT_FIRST_😈🔥_By_Elon_Musk_😈__#qoutes_#shorts.mp3'
resize_to = (519, 519)

# Конвертация изображения с восстановлением старого фото
convert_image(input_image_path, output_pi_path, output_model_path, audio_path, new_size=resize_to, restore=True)