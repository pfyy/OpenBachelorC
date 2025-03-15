callback_func_dict = {}


def register_callback_func(callback_func_name, callback_func):
    callback_func_dict[callback_func_name] = callback_func


def invoke_callback_func(callback_func_name):
    if callback_func_name in callback_func_dict:
        callback_func = callback_func_dict[callback_func_name]
        callback_func()
