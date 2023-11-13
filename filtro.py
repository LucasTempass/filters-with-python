import cv2


class Filtro:
    def __init__(self, nome, filtro):
        # função aplicada na imagem
        self.filtroFn = filtro
        # nome exibido em tela
        self.nome = nome

    def apply(self, image):
        return self.filtroFn(image)
