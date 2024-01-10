import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="nonebot-adapter-minecraft",  # 项目名称，保证它的唯一性，不要跟已存在的包名冲突即可
    version="1.0.5",  # 程序版本
    author="17TheWord",  # 项目作者
    author_email="17theword@gmail.com",  # 作者邮件
    description="NoneBot2与MineCraft Server互通的适配器",  # 项目的一句话描述
    long_description=long_description,  # 加长版描述？
    long_description_content_type="text/markdown",  # 描述使用Markdown
    url="https://github.com/17TheWord/nonebot-adapter-minecraft",  # 项目地址
    packages=setuptools.find_namespace_packages(),  # 无需修改
    package_data={
        'nonebot.adapters.minecraft': ['bot.pyi'],
    },
    classifiers=[
        "Programming Language :: Python :: 3.9",  # 使用Python3.10
        "License :: OSI Approved :: GNU Affero General Public License v3",  # 开源协议
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
