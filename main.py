import PySimpleGUI as gui
import cv2

from filtros import filtros
from sticker import Sticker

CANVAS_SIZE = 400

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
    [gui.Graph((CANVAS_SIZE, CANVAS_SIZE), (0, 0), (CANVAS_SIZE, CANVAS_SIZE), enable_events=True, key='image')],
    # ações
    [gui.Button('Save', disabled=True)],
]

window = gui.Window('Instagram Filters App', layout, finalize=True)

image_path = None
selected_sticker = None
filtro_aplicado = None


def set_image(image):
    ratio = image.shape[0] / image.shape[1]
    # keep original image ratio
    width = int(CANVAS_SIZE / ratio)
    height = CANVAS_SIZE
    # alters the size of the Graph element
    window['image'].Widget.config(width=width, height=height)
    image = cv2.resize(image, (width, height))
    img_bytes = cv2.imencode('.png', image)[1].tobytes()
    window['image'].draw_image(data=img_bytes, location=(0, CANVAS_SIZE))


while True:
    event, values = window.read()

    if event == gui.WIN_CLOSED:
        break

    if event == 'file':
        image_path = values['file']
        if image_path:
            set_image(cv2.imread(image_path))
            window['Save'].update(disabled=False)

    if event == 'image':
        x, y = values[event]
        location = (x - 28, y + 28)  # figure size is (56, 56)
        # Using option `filename` if the image source is a file
        sticker = gui.EMOJI_BASE64_HAPPY_BIG_SMILE
        window['image'].draw_image(data=sticker, location=location)

    if image_path:
        if event in nome_filtros:
            for filtro in filtros:
                if event != filtro.nome:
                    continue
                window['filtro_aplicado'].update(visible=True)
                window['filtro_aplicado'].update('Filtro aplicado: ' + filtro.nome)
                set_image(filtro.apply(cv2.imread(image_path)))
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
