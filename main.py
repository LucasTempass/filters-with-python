import PySimpleGUI as gui
import cv2

from filtros import filtros
from sticker import Sticker

CANVAS_SIZE = 600

nome_filtros = [filtro.nome for filtro in filtros]

sticker1 = Sticker('sticker1.png')
sticker2 = Sticker('sticker2.png')

layout = [
    [gui.Input(key='file', enable_events=True), gui.FileBrowse()],
    [gui.Text('Filtros')],
    [gui.Button(filtro.nome) for filtro in filtros],
    [gui.Text('Stickers')],
    [gui.Button('Rainbow'), gui.Button('Pizza')],
    [gui.Graph((CANVAS_SIZE, CANVAS_SIZE), (0, 0), (CANVAS_SIZE, CANVAS_SIZE), enable_events=True, key='image')],
    [gui.Button('Tirar foto')],
    [gui.Button('Salvar', disabled=True)],
]

window = gui.Window('Instagram Filters App', layout, finalize=True, resizable=True)

selected_sticker = None
filtro_aplicado = None
canvas_width = CANVAS_SIZE
canvas_height = CANVAS_SIZE
final_image = None
stickers_image = None
original_image = None


def update_canvas(image):
    global final_image
    global canvas_width
    global canvas_height

    graph_element = window['image']

    # Calcule a proporção da altura da imagem para a sua largura
    ratio = image.shape[0] / image.shape[1]

    canvas_width = int(CANVAS_SIZE / ratio)
    canvas_height = CANVAS_SIZE

    # Configure a largura e a altura do widget para corresponder às dimensões do canvas
    graph_element.Widget.config(width=canvas_width, height=canvas_height)

    # Redimensione a imagem para se ajustar às dimensões do canvas
    final_image = cv2.resize(image, (canvas_width, canvas_height))

    # Converta a imagem para bytes para exibição na GUI
    bytes = cv2.imencode('.png', final_image)[1].tobytes()

    graph_element.draw_image(data=bytes, location=(0, CANVAS_SIZE))


while True:
    event, values = window.read()

    if event == gui.WIN_CLOSED:
        break

    if event == 'file':
        image_path = values['file']

        if not image_path:
            continue

        # Armazena a imagem original
        original_image = cv2.imread(image_path)
        stickers_image = original_image.copy()

        update_canvas(original_image)

        window['Salvar'].update(disabled=False)

    if event == 'Tirar foto':
        cap = cv2.VideoCapture(0)
        result, frame = cap.read()
        if result:
            # Armazena a imagem original
            original_image = frame
            stickers_image = frame.copy()

            update_canvas(original_image)

            window['Salvar'].update(disabled=False)
        cap.release()

    if event == 'image':
        x, y = values['image']
        # Inverte a coordenada y para que a origem seja no canto superior esquerdo
        y = canvas_height - y

        if not selected_sticker:
            continue

        stickers_image = selected_sticker.apply(stickers_image, x, y)

        if filtro_aplicado:
            update_canvas(filtro_aplicado.apply(stickers_image))
        else:
            update_canvas(stickers_image)

    if original_image is not None:
        if event in nome_filtros:
            for filtro in filtros:
                if event != filtro.nome:
                    continue

                filtro_aplicado = filtro

                # Para evitar de aplicar o filtro várias vezes, aplica apenas sobre a imagem original com os stickers
                update_canvas(filtro.apply(stickers_image))

        if event == 'Salvar':
            filename = gui.popup_get_file('Save as', save_as=True, file_types=(('PNG Files', '*.png'),))
            if filename:
                cv2.imwrite(filename, final_image)

        if event == 'Rainbow':
            selected_sticker = sticker1
        if event == 'Pizza':
            selected_sticker = sticker2

window.close()
