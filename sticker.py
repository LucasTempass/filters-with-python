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

        if not isinstance(x, (int, np.int64)) or not isinstance(y, (int, np.int64)):
            print("Erro: As coordenadas x e y devem ser números inteiros.")
            return image

        if 0 <= y < image.shape[0] and 0 <= x < image.shape[1]:
            image_with_sticker = image.copy()
            sticker_height, sticker_width, _ = self.sticker.shape

            for i in range(sticker_height):
                for j in range(sticker_width):
                    alpha = self.sticker[i, j][3] / 255.0
                    if alpha > 0:
                        for c in range(3):
                            image_with_sticker[y + i, x + j, c] = (1 - alpha) * image[y + i, x + j, c] + alpha * self.sticker[i, j, c]

            return image_with_sticker
        else:
            print("Erro: Coordenadas fora dos limites da imagem.")
            return image

    