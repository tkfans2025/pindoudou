import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# 定义24种基础颜色（RGB格式）
BASE_COLORS = [
    (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
    (0, 255, 255), (255, 0, 255), (128, 0, 0), (0, 128, 0),
    (0, 0, 128), (128, 128, 0), (128, 0, 128), (0, 128, 128),
    (255, 192, 203), (173, 216, 230), (144, 238, 144), (255, 218, 185),
    (255, 239, 213), (221, 160, 221), (255, 165, 0), (128, 128, 128),
    (192, 192, 192), (255, 255, 255), (0, 0, 0), (165, 42, 42)
]

# 将颜色映射到最接近的基础颜色
def quantize_color(color):
    return min(BASE_COLORS, key=lambda c: sum((c[i] - color[i]) ** 2 for i in range(3)))

# 将图片转换为拼豆豆布局图
def image_to_bead_layout(image, output_size):
    image = image.resize(output_size)
    image = image.convert("RGB")
    pixels = np.array(image)
    bead_layout = np.zeros_like(pixels)
    for i in range(pixels.shape[0]):
        for j in range(pixels.shape[1]):
            bead_layout[i, j] = quantize_color(pixels[i, j])
    bead_image = Image.fromarray(bead_layout.astype('uint8'), 'RGB')
    return bead_image

# 描边并标注序号
def add_grid_and_numbers(image, grid_size, cell_size=25):
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    width, height = image.size
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            left = j * cell_size
            top = i * cell_size
            right = left + cell_size
            bottom = top + cell_size
            draw.rectangle([left, top, right, bottom], outline="black")
            number = i * grid_size[1] + j + 1
            draw.text((left + 2, top + 2), str(number), fill="black", font=font)
    return image

# Streamlit 应用
def main():
    st.title("拼豆豆生成器")
    st.write("上传图片并生成拼豆豆布局图")

    # 上传图片
    uploaded_file = st.file_uploader("上传图片", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="上传的图片", use_column_width=True)

        # 输入行数和列数
        cols1, cols2 = st.columns(2)
        with cols1:
            rows = st.number_input("行数（例如 35）", min_value=1, value=35)
        with cols2:
            cols = st.number_input("列数（例如 35）", min_value=1, value=35)

        # 生成拼豆豆布局图
        if st.button("生成拼豆豆布局图"):
            cell_size = 25
            bead_layout = image_to_bead_layout(image, output_size=(rows, cols))
            bead_layout = bead_layout.resize((cols * cell_size, rows * cell_size), Image.NEAREST)
            bead_layout_with_grid = add_grid_and_numbers(bead_layout, grid_size=(rows, cols), cell_size=cell_size)

            # 显示结果
            st.image(bead_layout_with_grid, caption="拼豆豆布局图", use_column_width=True)

            # 提供下载链接
            bead_layout_with_grid.save("bead_layout.png")
            with open("bead_layout.png", "rb") as file:
                btn = st.download_button(
                    label="下载拼豆豆布局图",
                    data=file,
                    file_name="bead_layout.png",
                    mime="image/png"
                )

if __name__ == "__main__":
    main()