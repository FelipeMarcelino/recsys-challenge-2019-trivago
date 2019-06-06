from setuptools import find_packages, setup

setup(
    name='src',
    packages=find_packages(),
    version='0.1.0',
    description='This projects aims to solution recsys challenge 2019 Trivago. The model is based in actor-critic(Reinforcemente Learning). Usage of LSTM to capture users sessions and CNN to solve localation list in such way that relevants items stay in top of the list!',
    author='Felipe Marcelino',
    license='MIT',
)
