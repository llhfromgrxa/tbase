 # -*- coding: UTF-8 -*-


import os
import time
import multiprocessing
import common
import exceptions


class OriQueue(object):

    def __init__(self):
        self.uuid = common.generate_uuid()
        self.read_lock = multiprocessing.Lock()
        self.write_lock = multiprocessing.Lock()
        self.pipe_receiver, self.pip_sender = multiprocessing.Pipe(False)

    def get(self):
        with self.read_lock:
            data = self.pipe_receiver.recv()
            return data

    def get_nowait(self):
        with self.read_lock:
            if self.pipe_receiver.poll():
                data = self.pipe_receiver.recv()
                return data
            else:
                raise exceptions.QueueEmpty

    def put(self, data):
        with self.write_lock:
            try:
                self.pip_sender.send(data)
            except ValueError as e:
                raise exceptions.QueueValueError


class OriSharedObj(object):
    """
    用于进程间传递配置信息
    """

    def __init__(self):
        self.lock = multiprocessing.Lock()
        self.pipe_receiver, self.pip_sender = multiprocessing.Pipe(False)

    def get_obj(self):
        with self.lock:
            if self.pipe_receiver.poll():
                obj = self.pipe_receiver.recv()
                self.pip_sender.send(obj)
                return obj
            else:
                raise exceptions.SharedSettingError

    def set_obj(self, obj):
        with self.lock:
            while self.pipe_receiver.poll():
                self.pipe_receiver.recv()
            self.pip_sender.send(obj)


class SharedMem(object):

    def __init__(self, data_struct):
        self._data_index = data_struct
        data_index = 0
        self._module_locks = {}
        for module in self._data_index:
            self._module_locks[module] = multiprocessing.Lock()
            for key in self._data_index[module]:
                self._data_index[module][key] = data_index
                data_index += 1
        self.shared_array = multiprocessing.Array('l', data_index)

    def get_all_module_name(self):
        return self._data_index.keys()

    def reset_all_value(self, module):
        module = self._data_index[module]
        for key in module:
            self.shared_array[module[key]] = 0

    def get_all_value(self, module):
        result = {}
        for key in self._data_index[module]:
            with self._module_locks[module]:
                result[key] = self.shared_array[self._data_index[module][key]]
        return result

    def add_value(self, module, key, value=1):
        with self._module_locks[module]:
            self.shared_array[self._data_index[module][key]] += value

    def get_value(self, module, key):
        value = self.shared_array[self._data_index[module][key]]
        return value

    def set_value(self, module, key, value):
        with self._module_locks[module]:
            self.shared_array[self._data_index[module][key]] = value
