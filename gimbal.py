from time import sleep

class Gimbal:
    @property
    def position(self):
        if not hasattr(self, '_position'):
            return None
        return self._position

    @position.setter
    def position(self, position):
        self._position = position

    def wait_for_position(self):
        sleep(0.5)
