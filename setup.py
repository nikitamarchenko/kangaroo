import uuid
from setuptools import setup, find_packages
from pip.req import parse_requirements


install_requires_pip = [str(ir.req) for ir in parse_requirements('requirements.txt', session=uuid.uuid1())]


setup(
    name='kangaroo',
    version='0.0.1',
    packages=find_packages(),
    url='',
    license='',
    author='nmarchenko',
    author_email='',
    description='',
    setup_requires=[
        'setuptools_git >= 0.3'],
    entry_points={
        'console_scripts': [
            'kangaroo-manager-api = kangaroo.manager:main',
            'kangaroo-vm-worker = kangaroo.vm.server:serve',
            'kangaroo-network-worker = kangaroo.network.server:serve',
            'kangaroo = kangaroo.cli:entry_point',
        ]
    },
    install_requires=install_requires_pip,
    include_package_data=True
)
