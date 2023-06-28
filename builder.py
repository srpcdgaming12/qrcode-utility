import os
import shutil
import requests
import subprocess
from zipfile import ZipFile


class MakeEnv:
    def __init__(self):
        self.build_dir = os.path.join(os.getcwd(), 'build')
        self.dist_dir = os.path.join(os.getcwd(), 'dist')
        self.work_dir = os.path.join(os.getcwd(), 'build', 'work')
        self.spec_dir = os.path.join(os.getcwd(), 'build', 'spec')

    def check_directory(self):
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)
        if os.path.exists(self.dist_dir):
            shutil.rmtree(self.dist_dir)
        os.mkdir(self.build_dir)
        os.mkdir(self.dist_dir)
        os.mkdir(self.work_dir)
        os.mkdir(self.spec_dir)


class Build(MakeEnv):
    pyinstaller_version = subprocess.run(["pyinstaller", "--version"], capture_output=True, text=True).stdout.strip()

    def __init__(self):
        super().__init__()
        self.pyzbar_location = os.path.join(os.getenv("LOCALAPPDATA"), "Programs", "Python",
                                            "Python311", "Lib", "site-packages", "pyzbar")
        self.check_directory()

    def get_pyzbar(self):
        if not os.path.exists(self.pyzbar_location):
            raise FileNotFoundError("Pyzbar with Python 3.11 must be installed in order to continue with installation.")
        shutil.copytree(self.pyzbar_location, self.build_dir+"\\pyzbar")

    def get_pyinstaller(self):
        pyinstaller_version = "v5.12.0"

        if self.pyinstaller_version == pyinstaller_version[1:]:
            return

        pyinstaller_url = f"https://github.com/pyinstaller/pyinstaller/archive/refs/tags/{pyinstaller_version}.zip"
        pyinstaller_dir = os.path.join(self.build_dir, 'pyinstaller')
        os.makedirs(pyinstaller_dir, exist_ok=True)
        zip_path = os.path.join(self.build_dir, f"PyInstaller-{pyinstaller_version}.zip")
        pyinstaller = os.path.join(pyinstaller_dir, f"pyinstaller-{pyinstaller_version[1:]}")

        with requests.get(pyinstaller_url, stream=True) as pyinstaller_get:
            pyinstaller_get.raise_for_status()
            with open(os.path.join(self.build_dir, f"PyInstaller-{pyinstaller_version}.zip"), 'wb') as pyinstaller_dest:
                shutil.copyfileobj(pyinstaller_get.raw, pyinstaller_dest)
        with ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(pyinstaller_dir)

        files = os.listdir(pyinstaller)
        for file in files:
            source_path = os.path.join(pyinstaller, file)
            destination_path = os.path.join(pyinstaller_dir, file)
            shutil.move(source_path, destination_path)

        subprocess.run(['pip', 'uninstall', 'pyinstaller', '-y'])
        subprocess.run(['pip', 'install', pyinstaller_dir], cwd=self.build_dir)

    def get_src(self):
        github_qrcode_utility = "https://github.com/srpcdgaming12/qrcode-utility.git"
        subprocess.run(['git', 'clone', github_qrcode_utility], cwd=self.build_dir)
        shutil.copytree(f"{self.build_dir}\\qrcode-utility\\src", os.path.join(self.build_dir, 'src'))

    def get_upx(self):
        upx_path = "https://github.com/upx/upx/releases/download/v4.0.2/upx-4.0.2-win64.zip"

        with requests.get(upx_path, stream=True) as upx_get:
            upx_get.raise_for_status()
            with open(os.path.join(self.build_dir, 'upx.zip'), 'wb') as upx_dest:
                shutil.copyfileobj(upx_get.raw, upx_dest)

        shutil.unpack_archive(os.path.join(self.build_dir, 'upx.zip'), self.build_dir)
        os.rename(os.path.join(self.build_dir, 'upx-4.0.2-win64'), os.path.join(self.build_dir, 'upx'))

    def compile(self):
        self.get_pyzbar()
        self.get_src()
        self.get_pyinstaller()
        self.get_upx()
        command = ['pyinstaller', '--onefile', '--windowed', '--icon', '..\\src\\icons\\qrcode_gen_icon.ico',
                   '--workpath', f'"{self.work_dir}"', '--distpath', f'"{self.dist_dir}"', '--specpath', 
                   f'"{self.spec_dir}"', '--upx-dir', 'build\\upx', '--add-data', '..\\src\\icons;icons',  
                   '--add-data', '..\\pyzbar;pyzbar', '--disable-windowed-traceback', '--clean', 
                   'build\\src\\main.py']
        subprocess.run(' '.join(command))

        return self


if __name__ == '__main__':
    build = Build().compile()
