# -*- mode: python ; coding: utf-8 -*-
from build_support import bibliotecas_tk

a = Analysis(['main.py'], pathex=[], binaries=[], datas=bibliotecas_tk(), hiddenimports=[],
             hookspath=[], hooksconfig={}, runtime_hooks=[], excludes=[], noarchive=False)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, a.binaries, a.datas, [], name='TaskManager',
          debug=False, bootloader_ignore_signals=False, strip=False, upx=False,
          console=False, disable_windowed_traceback=False)
