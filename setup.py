from setuptools import setup, find_packages

setup(
    name='todo_app',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'PyQt6',
    ],
    entry_points={
        'gui_scripts': [
            'todo=main:main',
        ],
    },
    include_package_data=True,
    package_data={
        '': ['icon.png', 'warning.png'],
    },
    author='Dmitry',
    description='Простое PyQt-приложение To-Do',
)
