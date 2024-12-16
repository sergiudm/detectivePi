from setuptools import setup, find_packages

setup(
    name="detective_pi",
    version="0.1.5",  
    author="Sergiu Han",  
    author_email="sergiudm@outlook.com",  
    description="A versatile tool for daily use",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sergiudm/detective", 
    packages=find_packages(include=["detective", "detective.*"]),
    install_requires=[
        "opencv-python",
        "opencv-python-headless",
        "mediapipe",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",  
    entry_points={  
    },
)
