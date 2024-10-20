from PIL import Image
import os
import requests
import shutil
from io import BytesIO
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

class ImageRotator:
    def __init__(self, directory):
        self.directory = directory
        os.makedirs(self.directory, exist_ok=True)

    def rotate_and_save_gif(self, image_url):
        try:
            # 检查并清空目录
            if os.path.exists(self.directory) and os.listdir(self.directory):
                shutil.rmtree(self.directory)
                os.makedirs(self.directory)
                print(f"已清空目录: {self.directory}")

            response = requests.get(image_url)
            response.raise_for_status()
            im = Image.open(BytesIO(response.content))
            filename = os.path.basename(image_url)
            base_name, ext = os.path.splitext(filename)
            
            rotated_images = []
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeElapsedColumn()
            ) as progress:
                rotate_task = progress.add_task("正在旋转图像", total=24)
                for i in range(24):
                    angle = i * 15
                    rotated_im = im.rotate(angle)
                    rotated_images.append(rotated_im)
                    progress.update(rotate_task, advance=1)

            # 创建GIF
            gif_filename = f"rotation.gif"
            gif_path = os.path.join(self.directory, gif_filename)
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeElapsedColumn()
            ) as progress:
                gif_task = progress.add_task("正在创建GIF", total=1)
                rotated_images[0].save(gif_path, save_all=True, append_images=rotated_images[1:], duration=100, loop=0)
                progress.update(gif_task, advance=1)
            print(f"GIF动画已成功创建并保存为: {gif_filename}")

            # 保存所有旋转后的图像
            for i, img in enumerate(rotated_images):
                img_filename = f"rot_{i:03d}.png"
                img_path = os.path.join(self.directory, img_filename)
                img.save(img_path)
                print(f"已保存旋转图像: {img_filename}")

        except requests.RequestException as e:
            print(f"下载图像时出错: {e}")
        except IOError as e:
            print(f"处理图像时出错: {e}")

if __name__ == "__main__":
    directory = "images/"
    image_url = "https://i-blog.csdnimg.cn/direct/7556650d2e4c4c4d96b259c2abd77f48.jpeg"
    rotator = ImageRotator(directory)
    rotator.rotate_and_save_gif(image_url)
