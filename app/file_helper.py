import os


def remove_file(path):
    if os.path.exists(path):
        os.remove(path)


def save_file(files, fileKey, path):
    file = files[fileKey]
    ext = file.filename.split(".")[-1]
    file_path = os.path.join(
        path, file.filename)
    file_path = file_path + f".{ext}"
    file.save(file_path)
    
    return file_path
