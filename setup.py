from setuptools import find_packages, setup

setup(
    name='tag-space-move',
    version=0.1,
    python_requires='>=3.9',
    description='Tool to fix tags for TagSpaces.',
    packages=find_packages(exclude=("*test*",)),
    entry_points={'console_scripts': [
        'fix-tag-space = tagspace_move.__main__:main',
    ]},
    package_dir={"": "lib"},
)
