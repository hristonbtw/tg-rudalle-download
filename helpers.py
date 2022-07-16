import os

def get_sessions():
    result = []
    dirname = './ss'
    sessions = os.listdir(dirname)
    for file in sessions:
        if file.endswith('.session'):
            session = "".join(file.split('.')[:-1])
            result.append(f"{session}")
    return result
