from setuptools import setup, find_packages
from typing import List 

def get_requirements() -> List[str]:
    requirement_list: List[str] = []
    
    try:
        with open("requirements.txt", "r") as f:    
            lines = f.readlines()
            
            for line in lines:
                requirement = line.strip()
                
                if requirement and requirement != "-e .":
                    requirement_list.append(requirement)
            
    except FileNotFoundError:
        print("requirements.txt not found")
    
    return requirement_list

setup(
    name='network security',
    version='0.0.1',
    author='MKhai Truong',
    author_email='minhkhai0402@gmail.com',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=get_requirements()
)