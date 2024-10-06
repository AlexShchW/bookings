import os

from PIL import Image

from app.tasks.celery import celery_app


@celery_app.task
def process_pic(
    input_path: str,
):
    base_folder = os.path.dirname(input_path)
    
    with Image.open(input_path) as img:
        resized_img = img.convert('RGB').resize((1000, 500))
        output_path = os.path.join(base_folder, 
                                  f"resized_1000_500_{os.path.basename(input_path)}")
        resized_img.save(output_path, format='WEBP', quality=90)

    with Image.open(input_path) as img:
        resized_img = img.convert('RGB').resize((200, 100))
        output_path = os.path.join(base_folder, 
                                  f"resized_200_100_{os.path.basename(input_path)}")
        resized_img.save(output_path, format='WEBP', quality=90)