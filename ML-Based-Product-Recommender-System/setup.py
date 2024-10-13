from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

## edit below variables as per your requirements -
REPO_NAME = "ML Based Products Recommender System"
AUTHOR_USER_NAME = "Koshi"
SRC_REPO = "products_recommender"
LIST_OF_REQUIREMENTS = []


setup(
    name=SRC_REPO,
    version="0.0.1",
    author="Kosh",
    description="A small local packages for ML based products recommendations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    author_email="koshi.gg23@gmail.com",
    packages=find_packages(),
    license="MIT",
    python_requires=">=3.8",
    install_requires=LIST_OF_REQUIREMENTS
)
