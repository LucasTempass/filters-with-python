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
    [gui.Button('Sticker 1'), gui.Button('Sticker 2')],
    [gui.Text('Nenhum filtro aplicado', key='filtro_aplicado', visible=False)],
    [gui.Graph((CANVAS_SIZE, CANVAS_SIZE), (0, 0), (CANVAS_SIZE, CANVAS_SIZE), enable_events=True, key='image')],
    [gui.Button('Take Photo')],
    [gui.Button('Save', disabled=True)],
]

window = gui.Window('Instagram Filters App', layout, finalize=True)

image_path = None
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
        if image_path:
            # Armazena a imagem original
            original_image = cv2.imread(image_path)
            stickers_image = original_image.copy()
            update_canvas(original_image)
            window['Save'].update(disabled=False)

    if event == 'Take Photo':
        cap = cv2.VideoCapture(1)
        ret, frame = cap.read()
        if ret:
            # Aplica stickers e filtros ao frame
            x, y = values['image']  # Use a chave correta para obter as coordenadas do canvas
            sticker = Sticker('sticker1.png')  # Substitua pelo seu sticker real
            image_with_sticker = sticker.apply(frame, x, y)

            if filtro_aplicado:
                image_with_filter = filtro_aplicado.apply(image_with_sticker)
            else:
                image_with_filter = image_with_sticker

            # Exibe a imagem no canvas
            update_canvas(image_with_filter)

            # Salva a imagem modificada
            filename = gui.popup_get_file('Save as', save_as=True, file_types=(('PNG Files', '*.png'),))
            if filename:
                cv2.imwrite(filename, image_with_filter)
            window['Save'].update(disabled=False)

        cv2.destroyAllWindows()

    if event == 'image':
        x, y = values['image']

        if not selected_sticker:
            continue

        stickers_image = selected_sticker.apply(stickers_image, x, y)

        if filtro_aplicado:
            update_canvas(filtro_aplicado.apply(stickers_image))
        else:
            update_canvas(stickers_image)

    if image_path:
        if event in nome_filtros:
            for filtro in filtros:
                if event != filtro.nome:
                    continue

                filtro_aplicado = filtro
                window['filtro_aplicado'].update('Filtro aplicado: ' + filtro_aplicado.nome)
                window['filtro_aplicado'].update(visible=True)

                # Para evitar de aplicar o filtro várias vezes, aplica apenas sobre a imagem original com os stickers
                update_canvas(filtro.apply(stickers_image))

        if event == 'Save':
            filename = gui.popup_get_file('Save as', save_as=True, file_types=(('PNG Files', '*.png'),))
            if filename:
                cv2.imwrite(filename, final_image)

        if event.startswith('Sticker'):
            if event == 'Sticker 1':
                selected_sticker = sticker1
            elif event == 'Sticker 2':
                selected_sticker = sticker2

window.close()
