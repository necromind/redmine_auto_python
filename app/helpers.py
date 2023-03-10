from importlib import import_module
from typing import Union


def class_factory(
        module_class_string, super_cls: Union[type, None] = None, **kwargs):
    """
    :param module_class_string: full name of the class to create an object of
    :param super_cls: expected super class for validity, None if bypass
    :param kwargs: parameters to pass
    :return:
    """
    module_name, class_name = module_class_string.rsplit(".", 1)
    module = import_module(module_name)
    assert hasattr(module, class_name), "class {} is not in {}" \
        .format(class_name, module_name)
    # print('reading class {} from module {}'.format(class_name, module_name))
    cls = getattr(module, class_name)
    if super_cls is not None:
        assert issubclass(cls, super_cls), "class {} should inherit from {}" \
            .format(class_name, super_cls.__name__)
    # print('initialising {} with params {}'.format(class_name, kwargs))
    obj = cls(**kwargs)
    return obj
