import PySimpleGUI as gui
import cv2

from filtros import filtros

nome_filtros = [filtro.nome for filtro in filtros]

layout = [
    # input
    [gui.Input(key='file', enable_events=True), gui.FileBrowse()],
    # filtros
    [gui.Text('Filtros')],
    [gui.Button(filtro.nome) for filtro in filtros],
    # stickers
    [gui.Text('Stickers')],
    # TODO adicionar stickers
    [gui.Button('Sticker 1'), gui.Button('Sticker 2')],
    # imagem
    [gui.Image(key='image', size=(400, 400))],
    # ações
    [gui.Button('Save')],
]

window = gui.Window('Instagram Filters App', layout, finalize=True)

image_path = None

while True:
    event, values = window.read()

    if event == gui.WIN_CLOSED:
        break

    if event == 'file':
        image_path = values['file']
        if image_path:
            image = cv2.imread(image_path)
            imageBytes = cv2.imencode('.png', image)[1].tobytes()
            window['image'].update(data=imageBytes)

    if image_path:
        if event in nome_filtros:
            for filtro in filtros:
                if event == filtro.nome:
                    # aplicar filtro
                    bytes_imagem = cv2.imencode('.png', filtro.apply(cv2.imread(image_path)))[1].tobytes()
                    window['image'].update(data=bytes_imagem)
        if event == 'Save':
            filename = gui.popup_get_file('Save as', save_as=True, file_types=(('PNG Files', '*.png'),))
            if filename:
                if event in nome_filtros:
                    for filtro in filtros:
                        if event == filtro.nome:
                            cv2.imwrite(filename, filtro.apply(cv2.imread(image_path)))
window.close()
