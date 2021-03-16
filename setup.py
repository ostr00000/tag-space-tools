from setuptools import find_packages, setup

setup(
    name='tag-space-tools',
    version=0.1,
    python_requires='>=3.9',
    description='Tool to fix tags for TagSpaces.',
    packages=find_packages(exclude=("*test*",)),
    install_requires=['more_itertools'],
    entry_points={'console_scripts': [
        'fix-tag-space = tag_space_tools.__main__:main',
        'tag-space-tools = tag_space_tools.gui.__main__:main',
    ]},
    package_dir={"": "lib"},
    extras_require={'gui': ['PyQt5']},
)
