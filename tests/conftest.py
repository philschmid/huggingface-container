from pytest import fixture, skip
# https://github.com/huggingface/infinity/blob/trial/test/integ/conftest.py
def pytest_addoption(parser):
    parser.addoption("--tag", action="store")
    

@fixture()
def tag(request):
    return request.config.getoption("--tag")