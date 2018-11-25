from setuptools import setup

setup(
    name='worker_images',
    packages=['worker_images'],
    include_package_data=True,
    install_requires=[
        'flask',
        'nats'
    ],
)