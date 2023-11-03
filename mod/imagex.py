# 此模块用于图片格式转换为JPEG
# process_image(image_path) 或者Image.Image图片对象
# 返回转换后的图片
from io import BytesIO
import requests
from PIL import Image
import os


def process_image(image_in):
    # 判断传入参数是图片对象还是路径字符串
    if isinstance(image_in, str):
        # 传入的是路径字符串，判断路径是否存在
        if not os.path.exists(image_in):
            try:
                response = requests.get(image_in)
                # 检查响应状态码
                if response.status_code == 200:
                    # 从响应中获取图片数据
                    image_data = response.content
                    image_stream = BytesIO(image_data)
                    # 打开图片并返回图片对象
                    image = Image.open(image_stream)

                    return image
                else:
                    raise ValueError("Invalid image path: {}".format(image_in))
            except Exception as e:
                raise ValueError(e)

        # 打开图片
        image = Image.open(image_in)
    elif isinstance(image_in, Image.Image):
        # 传入的是图片对象
        image = image_in
    else:
        raise ValueError("Invalid input type. Must be a path string or an image object.")

    # 获取图片的编码格式
    image_format = image.format.lower()

    # 如果图片不是JPEG格式，则进行转换
    if image_format != 'jpeg':
        # 创建一个新的空白图片对象
        new_image = Image.new("RGB", image.size)

        # 将原始图片的内容复制到新图片对象中
        new_image.paste(image)

        # 将图片对象转为JPEG格式
        image = new_image.convert("RGB")

    return image


# 示例
if __name__ == "__main__":
    # 传入路径字符串
    image_path = "path/to/image.jpg"
    processed_image = process_image(image_path)
    processed_image.show()

    # 传入图片对象
    image_obj = Image.open("path/to/image.png")
    processed_image = process_image(image_obj)
    processed_image.show()
