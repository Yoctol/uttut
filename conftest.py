import os
import pytest


@pytest.fixture(scope='session')
def data_folder():
    cur_path = os.path.abspath(__file__)
    cur_dir = os.path.dirname(cur_path)
    return os.path.join(cur_dir, 'test_file')


@pytest.fixture(scope='session')
def get_data_path(data_folder):
    def foo(file_name):
        return os.path.join(data_folder, file_name)
    return foo
