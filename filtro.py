import numpy as np
import cv2


class Filtro:
    def __init__(self, nome, filtro):
        # função aplicada na imagem
        self.filtroFn = filtro
        # nome exibido em tela
        self.nome = nome
        self.window_size = (800, 600)

    def apply(self, image):
        
        image = cv2.resize(image, (self.window_size[0] - 20, self.window_size[1] - 100))
        return self.filtroFn(image)


def apply_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def apply_sepia(image):
    kernel = np.array([[0.272, 0.534, 0.131],
                       [0.349, 0.686, 0.168],
                       [0.393, 0.769, 0.189]])
    return cv2.filter2D(image, -1, kernel)


filtroGrayscale = Filtro('Grayscale', apply_grayscale)
filtroSepia = Filtro('Sepia', apply_sepia)

# TODO adicionar filtros
# lista de filtros disponíveis
filtros = [filtroSepia, filtroGrayscale]
