import setuptools

with open('README.md') as f:
    long_description = f.read()

setuptools.setup(
    name="st-combobox",
    version="1.1.1",
    author="hoggatt",
    description="Streamlit AutoComplete ComboBox",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/hoggatt/st-combobox",
    packages=setuptools.find_packages(),
    include_package_data=True,
    license='MIT',
    classifiers=[],
    project_urls={
        'Source Code': 'https://github.com/hoggatt/st-combobox',
    },
    python_requires=">=3.7",
    install_requires=[
        "streamlit >= 1.0",
    ],
    extras_require={
        "tests": ["wikipedia"],
        "dev": ["black", "isort", "ruff"],
    },
)
