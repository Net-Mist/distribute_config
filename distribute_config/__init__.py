import os
import sys
import argparse
import yaml
from typing import Dict

from .variable import Variable


class Config:
    class __Config:
        def __init__(self):
            # variables maps the "path" of a variable to an instance of class Variable
            self.variables = {}
            self.namespace = ""
            self.parser = argparse.ArgumentParser(description='Arguments')
            self.parser.add_argument("-c", type=str, default="config.yml", help="relative path to config file")

        def define_var(self, name, default, description, type):
            if self.namespace:
                name = self.namespace + "." + name
                variable = Variable(name, default, description, type)
            else:
                variable = Variable(name, default, description, type)
            self.__add_variables(variable)

            self.parser.add_argument("--" + variable.name, type=type, help=variable.description)

        def __add_variables(self, variable: Variable):
            """add variable to variables dict and create path corresponding with the variable name. 

            Args:
                variable (Variable): variable to add
            """
            splited_path = variable.name.split(".")
            variables_sub_group = self.variables
            for sub_path in splited_path[:-1]:
                if not sub_path in variables_sub_group:
                    variables_sub_group[sub_path] = {}
                variables_sub_group = variables_sub_group[sub_path]
            if splited_path[-1] not in variables_sub_group:
                variables_sub_group[splited_path[-1]] = variable
            else:
                raise KeyError("variable already defined")

        def convert_to_dict(self):
            return self._convert_to_dict(self.variables)

        @classmethod
        def _convert_to_dict(cls, variables):
            out_dict = {}
            for key in variables:
                if type(variables[key]) == Variable:
                    out_dict[key] = variables[key].get_value()
                else:
                    out_dict[key] = cls._convert_to_dict(variables[key])
            return out_dict

    __instance = None

    def __init__(self):
        if not Config.__instance:
            Config.__instance = Config.__Config()

    def _ConfigNamespace__set_namespace(self, name):
        self.__instance.namespace = name

    @classmethod
    def define_int(cls, var_name, default, description):
        cls.__instance.define_var(var_name, default, description, int)

    def __str__(self):
        str = "Config\n"
        str += Config.__print_sub_variables(self.__instance.variables, 0)
        return str

    @staticmethod
    def __print_sub_variables(variables, sub_level: int):
        output_str = ""
        for key in variables:
            if type(variables[key]) == dict:
                output_str += key + ":\n"
                output_str += Config.__print_sub_variables(
                    variables[key], sub_level + 1)
            else:
                output_str += "  " * sub_level + \
                    key + ": " + \
                    str(variables[key].value) + "\n"
        return output_str

    @classmethod
    def get_var(cls, name):
        path = name.split(".")
        variables = cls.__instance.variables
        for sub_path in path:
            variables = variables[sub_path]

        if type(variables) == Variable:
            return variables.value
        else:
            return variables

    @classmethod
    def set_val(cls, name, val):
        path = name.split(".")
        variables = cls.__instance.variables
        for sub_path in path:
            variables = variables[sub_path]

        assert type(variables) == Variable
        variables.value = val

    @classmethod
    def get_dict(cls):
        return cls.__instance.convert_to_dict()

    @classmethod
    def write_conf(cls, file_path):
        with open(file_path, "w") as f:
            yaml.dump(cls.get_dict(), f, default_flow_style=False)

    @classmethod
    def load_conf(cls):
        """This method load the conf in 3 steps:
        1. Load the config.yml file if exist, or load a file specified by -c option when starting the program
        2. Load the env variables 
        3. parse the python commande line
        """
        args = cls.__instance.parser.parse_args()

        config_file_name = args.c
        if not os.path.exists(config_file_name):
            print("Create config file", config_file_name, "with default value")
            cls.write_conf(config_file_name)
            print("Please update config file and restart")
            print("You can find information on all parameters by running with --help")

        # 1
        with open(config_file_name, 'r') as stream:
            yml_content = yaml.safe_load(stream)
        cls.load_dict(yml_content, cls.__instance.variables)

        # 2
        for var in os.environ:
            path = ".".join(var.lower().split("__"))
            try:
                cls.set_val(path, os.environ[var])
                print("Load env variable", var)
            except KeyError:
                pass

    @staticmethod
    def load_dict(loading_dict, variables):
        for key in loading_dict:
            if type(loading_dict[key]) == dict:
                Config.load_dict(loading_dict[key], variables[key])
            else:
                variables[key].value = loading_dict[key]





class ConfigNamespace:
    def __init__(self, name):
        config = Config()
        config.__set_namespace(name)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        config = Config()
        config.__set_namespace("")


Config()
