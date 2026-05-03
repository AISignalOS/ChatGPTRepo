from setuptools import setup, find_packages

setup(
    name="research-agent-cli",
    version="1.0.0",
    packages=find_packages(),
    install_requires=["click>=8.1.0", "httpx>=0.27.0", "rich>=13.0.0", "beautifulsoup4>=4.12.0"],
    entry_points={
        "console_scripts": [
            "research-agent=research_agent.cli:main"
        ]
    },
    python_requires=">=3.10",
)
