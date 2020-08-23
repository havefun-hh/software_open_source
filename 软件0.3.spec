# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

SETUP_DIR = 'E:\\pycharm_files\\software0.3\\'

a = Analysis(['软件0.3.py', 'Prediction.py', 'MyProblem_2.py', 'Stack_rigidity.py'],
             pathex=['E:\\pycharm_files\\software0.3'],
             binaries=[('C:\\Program Files (x86)\\Microsoft SDKs\\NuGetPackages\\Microsoft.NETCore.Windows.ApiSets-x64\\1.0.0\\runtimes\\win7-x64\\native\\api-ms-win-core-winrt-string-l1-1-0.dll','.'),
             ('C:\\Program Files (x86)\\Microsoft SDKs\\NuGetPackages\\Microsoft.NETCore.Windows.ApiSets-x64\\1.0.0\\runtimes\\win7-x64\\native\\api-ms-win-core-winrt-l1-1-0.dll','.'),
             ('F:\\Program Files\\MySQL\\mysql-8.0.20-winx64\\lib\\libmysql.dll','.'),
             ('F:\\Program Files\\Altair\\2020\\hwdesktop\\hm\\bin\\win64\\libpq.dll','.'),
             ('F:\\Anaconda3\\pkgs\\qt-5.9.7-vc14h73c81de_0\\Library\\bin\\Qt5MultimediaQuick_p.dll','.')
             ],
             datas=[(SETUP_DIR+'images','images'),(SETUP_DIR+'data','data')],
             hiddenimports=['pkg_resources.py2_warn', 'geatpy', 'geatpy.core'],
             hookspath=['C:\\Users\\Lenovo\\.virtualenvs\\Scripts-1Yk4PGcZ\\Lib\\site-packages\\geatpy',
             'C:\\Users\\Lenovo\\.virtualenvs\\Scripts-1Yk4PGcZ\\Lib\\site-packages\\geatpy\\core'
             'C:\\Users\\Lenovo\\.virtualenvs\\Scripts-1Yk4PGcZ\\Lib\\site-packages\\pyqtgraph'],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='软件0.3',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='软件0.3')
