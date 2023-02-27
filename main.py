import argparse 
from traffic_counter import TrafficCounter

def CLI():
    # Определяю здесь значения по умолчанию, чтобы сделать документацию самообновляющейся
    minArea_default       = 200
    direction_default     = ['H','0.5']
    numCount_default      = 10
    videoWidth_default    = 640
    videoParams_default   = ['mjpg','avi']
    startingFrame_default = 10

    parser = argparse.ArgumentParser(description='Находит контуры на видеофайле')          # Создал объект синтаксического анализатора
    parser.add_argument('-p', '--path', type=str, help="""Название видео или путь до него.
    Работает лучше с .avi файлами.
    Если путь или имя не указаны, вместо них будет использована камера.""")        # Вместо использования меты='--path', просто ввожу '--path'. По какой-то причине аргумент меты вызывал проблемы.
    parser.add_argument('-a', '--minArea', type=int, help=f'Минимальная площадь (в пикселях) для рисования ограничительной рамки (обычно это: {minArea_default})',
                        default=minArea_default)
    parser.add_argument('-d', '--direction', type=str, default=direction_default, nargs=2, help=f"""Символ: H или V
    обозначающий ориентацию счетной линии. H - горизонтальная, V - вертикальная.
    Если не указано, то по умолчанию {direction_default[0]}, {direction_default[1]}. Второй параметр
    является плавающим числом от 0 до 1, указывающим место, в котором
    должна быть проведена линия.""")
    parser.add_argument('-n', '--numCount', type=int, default=numCount_default,help=f"""Количество контуров, которые должны быть обнаружены программой (обычно это: {numCount_default}).""")
    parser.add_argument('-w', '--webcam', type=int, nargs='+',help="""Позволяет пользователю указать, что использовать в качестве источника видеосигнала""")
    parser.add_argument('--rgb', action='store_true', help="Булевский флаг для использования цветов rbg.")
    parser.add_argument('-vo', '--video_out', type=str, default="",help="Укажите имя видеофайла для вывода")
    parser.add_argument('-vw', '--video_width', type=int, default=videoWidth_default,help=f"Размер видео будет изменен до этой ширины (обычно это: {videoWidth_default}). Высота будет вычисляться автоматически, чтобы сохранить соотношение сторон")
    parser.add_argument('-vp', '--video_params', type=str, default=videoParams_default,nargs=2,help=f"Предоставьте видеокодек и расширение (в таком порядке) для выходного видео. Например: `--video_params mjpg avi`. Обычные значения это: {videoParams_default[0]} {videoParams_default[1]}")
    parser.add_argument('-sf', '--starting_frame', type=int, default=startingFrame_default,help=f"Выберите начальный кадр для анализа видео (обычно это: {startingFrame_default}). Все кадры до этого будут по-прежнему использоваться для среднего фона")
    args = parser.parse_args()
    return args

def make_video_params_dict(video_params):
    codec     = video_params[0]
    extension = video_params[1]
    
    params_dict = {
        'codec'    : codec,
        'extension': extension,
    }
    return params_dict

def main(args):
    video_source   = args.path
    line_direction = args.direction[0]
    line_position  = float(args.direction[1])
    video_width    = args.video_width
    min_area       = int(args.minArea)
    video_out      = args.video_out
    numCnts        = int(args.numCount)
    video_params   = make_video_params_dict(args.video_params)
    starting_frame = args.starting_frame
    tc = TrafficCounter(video_source,
                        line_direction,
                        line_position,
                        video_width,
                        min_area,
                        video_out,
                        numCnts,
                        video_params,
                        starting_frame,)

    tc.main_loop()

if __name__ == '__main__':
    args = CLI()
    main(args)
