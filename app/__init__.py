from flask import Flask, request
from werkzeug.datastructures import ImmutableMultiDict, FileStorage
from app.kenzie import FILES_DIRECTORY, image
from os import getenv

MAX_CONTENT_LENGTH = int(getenv('MAX_CONTENT_LENGTH'))

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH*1024*1024

@app.post("/upload")
def upload():
    files: ImmutableMultiDict[str, FileStorage] = request.files


    for file in files.values():
        try:
            image.upload_image(file)
        except FileExistsError:
            return {"msg":"Arquivo já existe."}, 409
        except FileNotFoundError:
            return {'msg':'Extensão não suportada.'}, 415

    return {'msg':"Upload realizado com sucesso."}, 201


@app.get("/download-zip")
def download_dir_as_zip():
    file_type = request.args.get('file_extension')
    compression_ratio = request.args.get('compression_ratio', 6)

    if not file_type:
        return {"msg":'Query param `file_extension` é obrigatório.'}, 400
    
    return image.download_zip(file_type, compression_ratio)

@app.get("/download/<file_name>")
def download(file_name):
    
    return image.download_file(file_name)

@app.get("/files/<extension>")
@app.get("/files")
def files(extension = None):
    return image.get_files(extension)


@app.errorhandler(413)
def too_big(error):
    return {'msg':f'O arquivo ultrapassa o limite permitido de {MAX_CONTENT_LENGTH}MB.'}, 413