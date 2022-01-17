import os

FILES_DIRECTORY = os.getenv('FILES_DIRECTORY')
ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS')


def create_dirs() -> None:
    # ['jpg', 'png', 'gif']
    for ext in ALLOWED_EXTENSIONS.split(","):
        # f"{FILES_DIRECTORY}/{ext}"
        path = os.path.join(FILES_DIRECTORY, ext)

        if not os.path.exists(path):
            os.makedirs(path)



create_dirs()