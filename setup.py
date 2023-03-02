from setuptools import setup, find_packages

setup(
    name='streamlit-router',
    version='0.1.0',
    author='mapix',
    author_email='mapix.me@gmail.com',
    packages=find_packages(),
    install_requires=['streamlit', 'werkzeug'],
    url='https://github.com/mapix/streamlit-router',
    description='werkzeug router for streamlit',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved",
        "Topic :: Scientific/Engineering",
    ]
)