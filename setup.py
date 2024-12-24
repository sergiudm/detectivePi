from setuptools import setup, find_packages

setup(
    name="Thread-Everything",
    version="0.3.0",
    author="Sergiu Han, Jihan Li",
    author_email="sergiudm@outlook.com, 12211820@mail.sustech.edu.cn",
    description="An easy-to-use interface to run threads from different machines",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://sergiudm.github.io/Thread-Everything/",
    packages=find_packages(include=["detective", "detective.*"]),
    install_requires=["opencv-python", "opencv-python-headless", "mediapipe", "pygame"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    entry_points={},
)
