"""
    Dynaconf 初始配置
"""

from pathlib import Path

from dynaconf import Dynaconf

root_path = Path(__file__).parent.parent.absolute()
settings = Dynaconf(
    root_path=str(root_path),  # 解决 PyCharm OSError: Starting path not found
    envvar_prefix="DYNACONF",
    settings_files=["./conf/settings.yaml", "./conf/.secrets.yaml"],
    environments=True,
    load_dotenv=True,
    env="boe",
)

if __name__ == "__main__":
    print(root_path)
    print(settings.DB)
    # for k,v in settings.items():
    #     print(k, v)
