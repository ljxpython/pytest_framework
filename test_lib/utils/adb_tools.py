"""
使用Python调用ADB命令
引用第三方库：https://github.com/JeffLIrion/adb_shell

安装：pip install adb-shell

"""

import os
from typing import Optional, Union

from adb_shell.adb_device import AdbDeviceTcp, AdbDeviceUsb
from adb_shell.auth.keygen import keygen
from adb_shell.auth.sign_pythonrsa import PythonRSASigner
from adb_shell.constants import DEFAULT_PUSH_MODE, DEFAULT_READ_TIMEOUT_S

from conf.constants import data_dir

"""
功能
    1. 实例化
        初始化实例需要传入 adbkey，默认可以不传，不传则指定为默认key
        如果传的话，需指定key的存放目录

    2. pull 文件
    3. push 文件
    4. 生成adbkey

"""

DEFAULT_ADBKEY = os.path.join(data_dir, "key", ".android_default_key")


class AdbTools(object):
    def __init__(
        self,
        adbkey=None,
        host=None,
        port: Union[int, str] = 5555,
        default_transport_timeout_s=9.0,
        auth_timeout_s=5.0,
        banner=None,
    ):
        if adbkey is None:
            adbkey = DEFAULT_ADBKEY
        with open(adbkey + "/adbkey") as f:
            priv = f.read()
        with open(adbkey + "/adbkey.pub") as f:
            pub = f.read()
        signer = PythonRSASigner(pub, priv)
        self.devices = AdbDeviceTcp(
            host,
            port,
            default_transport_timeout_s=default_transport_timeout_s,
            banner=banner,
        )
        ## 连接，如果连接不成功则报错
        self.devices.connect(rsa_keys=[signer], auth_timeout_s=auth_timeout_s)

    def shell(
        self,
        cmd=None,
        transport_timeout_s=None,
        read_timeout_s=DEFAULT_READ_TIMEOUT_S,
        timeout_s=None,
        decode=True,
    ):
        resp = self.devices.shell(
            cmd,
            transport_timeout_s=transport_timeout_s,
            read_timeout_s=read_timeout_s,
            decode=decode,
            timeout_s=timeout_s,
        )
        return resp

    def pull(
        self,
        device_path,
        local_path,
        progress_callback=None,
        transport_timeout_s=None,
        read_timeout_s=DEFAULT_READ_TIMEOUT_S,
    ):
        resp = self.devices.pull(
            device_path,
            local_path,
            progress_callback=progress_callback,
            transport_timeout_s=transport_timeout_s,
            read_timeout_s=read_timeout_s,
        )
        return resp

    def push(
        self,
        local_path,
        device_path,
        st_mode=DEFAULT_PUSH_MODE,
        mtime=0,
        progress_callback=None,
        transport_timeout_s=None,
        read_timeout_s=DEFAULT_READ_TIMEOUT_S,
    ):
        resp = self.devices.push(
            local_path,
            device_path,
            st_mode=st_mode,
            mtime=mtime,
            progress_callback=progress_callback,
            transport_timeout_s=transport_timeout_s,
            read_timeout_s=read_timeout_s,
        )
        return resp

    def root(
        self,
        transport_timeout_s=None,
        read_timeout_s=DEFAULT_READ_TIMEOUT_S,
        timeout_s=None,
    ):
        resp = self.devices.root(
            transport_timeout_s=transport_timeout_s,
            read_timeout_s=read_timeout_s,
            timeout_s=timeout_s,
        )
        return resp

    def reboot(
        self,
        fastboot=False,
        transport_timeout_s=None,
        read_timeout_s=DEFAULT_READ_TIMEOUT_S,
        timeout_s=None,
    ):
        resp = self.devices.reboot(
            fastboot=fastboot,
            transport_timeout_s=transport_timeout_s,
            read_timeout_s=DEFAULT_READ_TIMEOUT_S,
            timeout_s=timeout_s,
        )
        return resp

    def disconnect(self):
        """adb disconnect"""
        resp = self.devices.close()
        return resp

    # 生成adbkey
    def keygen(self, path):
        keygen(path)

    def adb_stream(
        self,
        command,
        transport_timeout_s=None,
        read_timeout_s=DEFAULT_READ_TIMEOUT_S,
        decode=True,
    ):
        """增加流式的adb命令执行"""
        return self.devices.streaming_shell(
            command,
            transport_timeout_s=transport_timeout_s,
            read_timeout_s=read_timeout_s,
            decode=decode,
        )


if __name__ == "__main__":
    devices = AdbTools(host="host", port="port")
    resp = devices.shell(cmd="echo test")
    print(resp)
