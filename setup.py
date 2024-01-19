import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="nonebot-adapter-minecraft",
    version="1.0.7",
    author="17TheWord",
    author_email="17theword@gmail.com",
    description="NoneBot2与MineCraft Server互通的适配器",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MineGraphCN/nonebot-adapter-minecraft",
    packages=setuptools.find_namespace_packages(),
    package_data={
        'nonebot.adapters.minecraft': ['bot.pyi'],
    },
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'nonebot2>=2.1.3',
        'nonebot2[fastapi]',
        'nonebot2[websockets]',
        'mcqq-tool>=1.0.5',
        'aio-mc-rcon>=3.2.2',
    ],
)
