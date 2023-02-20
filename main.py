import os
import pandas as pd
import time
dataframe1 = pd.read_excel('listadoPredicas.xlsx')

#  IMPORTANTE
#  Cambiar el valor de indiceInicio y indiceFin
#  para que se descarguen las predicas que se deseen
#  indiceInicio  significa desde que fila se va a empezar a descargar
#  indiceFin  significa hasta que fila se va a descargar
#  Ejemplo:  indiceInicio = 100  y  indiceFin = 200  descargara las predicas de la fila 100 a la fila 200

indiceInicio = 1

indiceFin = 3

#  RECOMIENDO que se descarguen por bloques y no todas las predicas de una vez, porque aun falta cortarlas para que solo quede la predica
#  y no el video completo

#NO CAMBIAR EL NOMBRE DEL ARCHIVO xlsx A NINGUN OTRO NOMBRE NI MOVERLO DE LUGAR

sub = dataframe1.iloc[indiceInicio-1:indiceFin]

urls = []
for index, row in sub.iterrows():
    url = row[2]
    urls.append(url)
    print(url)

import yt_dlp

URLS = urls


for url in URLS:

    # get INFO to create folder
    ydl_opts1 = {
        'format': 'mp3/bestaudio/best',
        'postprocessors': [{ 
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts1) as ydl1:
        info_dict = ydl1.extract_info(url, download=False)
        # error_code = ydl.download(URLS)
        utcDate = info_dict['release_date']

        # convert utcDate to local date
        utcDate = time.strptime(utcDate, "%Y%m%d")
        localDate = time.strftime("%d-%m-%Y", utcDate)


        # create folder with localDate
        folderName = localDate
        if not os.path.exists(folderName):
            os.makedirs(folderName)
        
        # download audio
        ydl_opts = {
            'format': 'mp3/bestaudio/best',
            'outtmpl': folderName + '/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download(url)

    