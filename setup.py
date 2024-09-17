import os
from importlib.machinery import SourceFileLoader

from pkg_resources import parse_requirements
from setuptools import find_packages, setup

module_name = "productmanager"

module = SourceFileLoader(
    module_name, os.path.join(module_name, "__init__.py")
).load_module()


def load_requirements(filepath: str) -> list:
    requirements = []

    with open(filepath, "r") as fp:
        for req in parse_requirements(fp.read()):
            extras = "[{}]".format(",".join(req.extras) if req.extras else "")
            requirements.append("{}{}{}".format(req.name, extras, req.specifier))

    return requirements


setup(
    name=module_name,
    version="1.0",
    author=module.__author__,
    author_email=module.__email__,
    license=module.__license__,
    description=module.__doc__,
    url="https://github.com/temaxuck/Brendwall-Technical-Assessment/",
    python_requires=">=3.10",
    platforms="all",
    packages=find_packages(),
    install_requires=load_requirements("requirements.txt"),
    entry_points={
        "console_scripts": [
            "{0} = {0}.__main__:main".format(module_name),
        ]
    },
    include_package_data=True,
)
