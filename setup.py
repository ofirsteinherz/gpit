from setuptools import setup, find_packages

# Read the content of README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='gpit',
    version='0.0.4',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'gpit=gpit.main:main',
        ],
    },
    # Additional metadata
    author='Ofir Steinherz',
    author_email='ofir.steinherz@gmail.com',
    description='GPT-Powered Commit Assistance',
    long_description=long_description,
    long_description_content_type='text/markdown',
)