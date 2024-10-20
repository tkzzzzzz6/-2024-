from PIL import Image
import os
import requests
from io import BytesIO
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn

class ImageRotator:
    def __init__(self, directory):
        self.directory = directory
        os.makedirs(self.directory, exist_ok=True)

    def rotate_and_save_gif(self, image_url):
        try:
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
                rotate_task = progress.add_task("旋转图片", total=24)
                for i in range(24):
                    angle = i * 30
                    rotated_im = im.rotate(angle)
                    rotated_images.append(rotated_im)
                    progress.update(rotate_task, advance=1)

            # 创建GIF
            gif_filename = f"{base_name}_rotation.gif"
            gif_path = os.path.join(self.directory, gif_filename)
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeElapsedColumn()
            ) as progress:
                gif_task = progress.add_task("创建GIF", total=1)
                rotated_images[0].save(gif_path, save_all=True, append_images=rotated_images[1:], duration=100, loop=0)
                progress.update(gif_task, advance=1)
            print(f"GIF动画已成功创建并保存为: {gif_filename}")

            # 显示所有旋转后的图片
            fig, axes = plt.subplots(4, 6, figsize=(20, 15))
            for i, ax in enumerate(axes.flat):
                if i < 24:
                    ax.imshow(rotated_images[i])
                    ax.set_title(f"旋转 {i*30}°", fontproperties='SimHei')
                ax.axis('off')
            plt.tight_layout()
            plt.show()

            # 显示GIF动画
            fig, ax = plt.subplots()
            ax.axis('off')

            def animate(i):
                ax.clear()
                ax.imshow(rotated_images[i])
                ax.axis('off')
                ax.set_title(f"旋转 {i*30}°", fontproperties='SimHei')

            anim = FuncAnimation(fig, animate, frames=24, interval=100, repeat=True)
            plt.show()

        except requests.RequestException as e:
            print(f"下载图片时出错: {e}")
        except IOError as e:
            print(f"处理图片时出错: {e}")

if __name__ == "__main__":
    directory = "images/"
    image_url = "https://i-blog.csdnimg.cn/direct/7556650d2e4c4c4d96b259c2abd77f48.jpeg"
    rotator = ImageRotator(directory)
    rotator.rotate_and_save_gif(image_url)
