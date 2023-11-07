import PySimpleGUI as gui
import cv2

from filtro import filtros
from sticker import Sticker

nome_filtros = [filtro.nome for filtro in filtros]

sticker1 = Sticker('sticker1.png')
sticker2 = Sticker('sticker2.png')

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
    # filtros aplicado
    [gui.Text('Nenhum filtro aplicado', key='filtro_aplicado', visible=False)],
    # imagem
    [gui.Image(key='image', size=(400, 400))],
    # ações
    [gui.Button('Save', disabled=True)],
]

window = gui.Window('Instagram Filters App', layout, finalize=True)

image_path = None
selected_sticker = None
filtro_aplicado = None

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
            window['Save'].update(disabled=False)

    if image_path:
        if event in nome_filtros:
            for filtro in filtros:
                if event != filtro.nome:
                    continue
                window['filtro_aplicado'].update(visible=True)
                window['filtro_aplicado'].update('Filtro aplicado: ' + filtro.nome)
                img_bytes = cv2.imencode('.png', filtro.apply(cv2.imread(image_path)))[1].tobytes()
                window['image'].update(data=img_bytes)
                filtro_aplicado = filtro
        if event == 'Save':
            filename = gui.popup_get_file('Save as', save_as=True, file_types=(('PNG Files', '*.png'),))
            if filename:
                cv2.imwrite(filename, filtro_aplicado.apply(cv2.imread(image_path)))
        if event.startswith('Sticker'):
            if event == 'Sticker 1':
                selected_sticker = sticker1
            elif event == 'Sticker 2':
                selected_sticker = sticker2
            x, y = values['Canvas']
            image_with_sticker = selected_sticker.apply(cv2.imread(image_path), x, y)
            bytes_imagem = cv2.imencode('.png', image_with_sticker)[1].tobytes()
            window['image'].update(data=bytes_imagem)

window.close()
