# py_platform_new

#### 介绍

建模大师(V1.2)

#### 软件架构

软件架构说明 使用Python及PySide2框架开发，为了方便后期维护修改和功能扩展，在第一版基础上重新做了结构构建

#### 安装教程

1. 安装Python，并检测安装版本 py -V
2. 安装python虚拟运行环境并依赖包 py -m venv venv cd venv/script active.bat cd .. cd .. pip install -r requirements.txt

3. 编译并生成执行文件 pyinstaller -F Master.spec

#### 使用说明

1. 程序包包括： Master.exe；   
   py_platform.ini；   
   pythoncom39.dll；   
   pywintypes39.dll； 其他文件非必须
2. readme.txt(包含sha验证码，运行环境要求及各个版本修改内容提要)
3. 修改记录id为对应git版本控制，版本控制服务器目前开发分支：huangkun_20201124

#### 修改记录

1. modified_20210114_01：如果将ini文件中web、threejs、master、minesched、whittle各配置段注销（以分号开始），程序将不启动相对应的应用
