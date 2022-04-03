from setuptools import find_packages, setup

setup(
    name='tag-space-tools',
    version='0.2',
    python_requires='>=3.9',
    description='Tool to fix tags for TagSpaces.',

    package_dir={'': 'lib'},
    packages=find_packages(exclude=("*test*",)),
    entry_points={'console_scripts': [
        'tag-space-tools = tag_space_tools.gui.__main__:main']},

    install_requires=['more_itertools', 'progressbar2', 'PyQt5'],
)
