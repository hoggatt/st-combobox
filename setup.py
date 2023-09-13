import setuptools

setuptools.setup(
    name="st-combobox",
    version="0.1.0",
    author="hoggatt",
    description="Autocomplete Combobox",
    long_description="Streamlit combobox that dynamically updates "
    + "and provides a list of suggestions based on a provided function",
    long_description_content_type="text/plain",
    url="https://github.com/hoggatt/st-combobox",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.7, !=3.9.7",
    install_requires=[
        "streamlit >= 1.0",
    ],
    extras_require={
        "tests": ["wikipedia"],
        "dev": ["black", "isort", "ruff"],
    },
)
