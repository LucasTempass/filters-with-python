import cv2
import numpy as np


class Sticker:
    def __init__(self, sticker_path):
        self.sticker = cv2.imread(sticker_path, -1)
        self.selected = False

    def apply(self, image, x, y):
        if image is None:
            print("Erro: A imagem é None.")
            return image

        image_with_sticker = image.copy()

        sticker_height, sticker_width, _ = self.sticker.shape

        for sticker_y in range(sticker_height):
            for sticker_x in range(sticker_width):
                alpha = self.sticker[sticker_y, sticker_x][3] / 255.0

                if alpha <= 0:
                    continue

                for c in range(3):
                    # Mapeia as coordenadas do sticker para as coordenadas da imagem
                    image_y = y + sticker_y
                    image_x = x + sticker_x

                    # Verifica se as coordenadas estão dentro dos limites da imagem
                    if image_y >= image.shape[0] or image_x >= image.shape[1]:
                        continue

                    # Aplica a transparência
                    sticker_channel = self.sticker[sticker_y, sticker_x, c] * alpha
                    image_channel = (1 - alpha) * image[image_y, image_x, c]

                    # Combina os canais da imagem e do sticker
                    image_with_sticker[image_y, image_x, c] = image_channel + sticker_channel

        return image_with_sticker
