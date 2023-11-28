from abc import ABC


class IApi(ABC):
    def get_response(self, args):
        pass

    def get_result(self, args):
        pass
