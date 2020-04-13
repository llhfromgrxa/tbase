# -*- coding: UTF-8 -*-

import os
import sys
import yaml
import traceback




class Config(object):

    def __new__(cls):
        """
        单例模式初始化
        """
        if not hasattr(cls, "instance"):
            cls.instance = super(Config, cls).__new__(cls)
            cls.instance._init()
        return cls.instance

    def _init(self):
        """
        初始化
        """
        self._config_path_candidate = [
            "/td01/config.yaml",
            "/etc/td01/config.yaml",
            "./config.yaml"
        ]
        self.config_dict = None
        self.load_config()


    def load_config(self, path=None):
        """
        读取配置文件, 若已经读取不再重复读取

        Parameters:
            path - 读取的目标文件路径, 为None时读取默认文件
        """
        if self.config_dict is not None:
            return
        if path is None:
            for cp in self._config_path_candidate:
                if os.path.isfile(cp):
                    self._config_path = cp
                    break
        else:
            self._config_path = path
        if self._config_path is None or not os.path.isfile(self._config_path):
            sys.exit(1)

        self._config_path = os.path.realpath(
            os.path.abspath(self._config_path))

        try:
            with open(self._config_path, "r") as f:
                self.config_dict = yaml.load(f, Loader=yaml.FullLoader)

        except Exception as e:
            print(
                "[!]load config error! Please check config file: {}! \n".format(self._config_path))
            traceback.print_exc()
            sys.exit(1)

    def get_config(self, name):
        """
        获取配置

        Parameters:
            name - str, 获取的配置名称

        Returns:
            获取到的值
        """
        return self.config_dict[name]

if __name__ == "__main__":
    print Config().get_config("elasticsearch.hosts")
    print type(Config().get_config("elasticsearch.hosts"))
    print ""