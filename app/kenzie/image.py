from werkzeug.datastructures import FileStorage
from flask import send_file, send_from_directory, jsonify
import os
from app.kenzie import ALLOWED_EXTENSIONS, FILES_DIRECTORY


def file_already_exists(filename: str, extension: str) -> bool:
    #  f"./files/{extension}"
    extension_path = os.path.join(FILES_DIRECTORY, extension)

    # return True
    return filename in os.listdir(extension_path)


def upload_image(file: FileStorage) -> None:
    filename: str = file.filename

    # kenzie.jpg
    _, extension = os.path.splitext(filename)
    extension = extension.replace(".", "")

    if file_already_exists(filename, extension):
        raise FileExistsError
    
    saving_path = os.path.join(FILES_DIRECTORY, extension, filename)
    file.save(saving_path)


def download_zip(file_type: str, compression_ratio: str):
    output_file = f'{file_type}.zip'
    #  ./files/{file_type}
    input_path = os.path.join(FILES_DIRECTORY, file_type)
    # /tmp/file_fype.zip
    output_path_file = os.path.join('/tmp',output_file)

    # /tmp/file_type.zip
    if file_type in ALLOWED_EXTENSIONS.split(","):
        if os.path.isfile(output_path_file):
                os.remove(output_path_file)
        if os.listdir(input_path) == []:
            return {"msg":'O repositório está vazio.'}, 404

        command = f"zip -r -j -{compression_ratio} {output_path_file} {input_path}"

        os.system(command)
        return send_file(output_path_file, as_attachment=True)
    return {"msg":'Tipo de extensão não suportada.'}, 404

def download_file(file_name):
    file_type = file_name.split('.')[1]
    input_path = os.path.join(FILES_DIRECTORY, file_type)
    if file_type in ALLOWED_EXTENSIONS.split(","):
        if os.listdir(input_path) == []:
                return {"msg":'Arquivo não encontrado.'}, 404

        if not os.path.isfile(f"{FILES_DIRECTORY}/{file_type}/{file_name}"):
                return {"msg": "Arquivo não encontrado."}, 404

        return send_from_directory(
            os.path.realpath(f'{FILES_DIRECTORY}/{file_type}'),
            file_name,
            as_attachment=True
        ), 200
    return {"msg": 'Tipo de extensão não suportado para download.'}, 415

def get_files(extension):
    all_files = []
    if extension:
        for current_extension in ALLOWED_EXTENSIONS.split(","):
            if extension == current_extension:
                for file_name in os.listdir(f"{FILES_DIRECTORY}/{extension}"):
                    input_path = os.path.join(f"{FILES_DIRECTORY}/{extension}", file_name)
                    if(os.path.isfile(input_path)):
                        all_files.append(file_name)
                return jsonify(all_files)
        return {"msg": 'Tipo de extensão não suportada.'}, 404

    else:
        for current_extension in ALLOWED_EXTENSIONS.split(","):
            for file_name in os.listdir(f"{FILES_DIRECTORY}/{current_extension}"):
                input_path = os.path.join(f"{FILES_DIRECTORY}/{current_extension}", file_name)
                if(os.path.isfile(input_path)):
                    all_files.append(file_name)
        return jsonify(all_files)