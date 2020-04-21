import pickle
import os


def load_all_binary_objects(file_path):
    with open(file_path, "rb") as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break


def save_object_in_binary(obj, file_path):
    # file_path is PosixPath (from Pathlib) and its raise an exception when you try open by him,
    # so convert the variable to string and open regular.
    with open(str(file_path), "ab+") as f:
            pickle.dump(obj, f)


def get_iterator_all_files_name(path):
    for (dir_path, dir_names, file_names) in os.walk(str(path)):
        for f in file_names:
            yield os.path.join(dir_path, f)
