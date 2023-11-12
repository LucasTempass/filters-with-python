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
