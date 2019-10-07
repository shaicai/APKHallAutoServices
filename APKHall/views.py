from django.shortcuts import render
from django.http import HttpResponse
import os
import re
import ruamel.yaml
# Create your views here.


def apkhall(request):
    return render(request, 'apkhall.html')


def change_yaml(thing,Modular,sort,name):
    fb = open("F:\\APKHallAutoTestProject\\data\\Login.yaml", "r", encoding="utf-8")
    alldata = ruamel.yaml.safe_load(fb)
    alldata[Modular][sort][name] = thing
    fr = open("F:\\APKHallAutoTestProject\\data\\Login.yaml", "w", encoding="utf-8")
    ruamel.yaml.dump(alldata, fr)
    fb.close()


def getFiles(dir, suffix):  # 查找根目录，文件后缀
    res = []
    for root, directory, files in os.walk(dir):  # =>当前根,根下目录,目录下的文件
        for filename in files:
            name, suf = os.path.splitext(filename)  # =>文件名,文件后缀
            if suf == suffix:
                res.append(os.path.join(root, filename))  # =>吧一串字符串组合成路径
    return res

def package_name():
    ccc = getFiles("F:\\APKHallAutoTestProject\public\\app",'.apk')
    package = ''
    if 'JJMahjong' in ccc[0]:
        package = 'cn.jj.mahjong'
    elif 'JJLord' in ccc[0]:
        package = 'cn.jj'
    elif 'JJLordSingleXHCG' in ccc[0]:
        package = 'com.philzhu.www.ddz'
    elif 'JJHLLord' in ccc[0]:
        package = 'cn.jj.lordhl'
    elif 'JJHall' in ccc[0]:
        package = 'cn.jj.hall'
    elif 'JJFish' in ccc[0]:
        package = 'cn.jj.fish'
    elif 'Chinachess' in ccc[0]:
        package = 'cn.jj.chess'
    else:
        print("APK的包名存在问题，请检查后重新上传")
        quit()
    return package

def upload_file(request):
    if request.method == "POST":    # 请求方法为POST时，进行处理
        for file in getFiles("F:\\APKHallAutoTestProject\public\\app", '.apk'):  # =>查找以.py结尾的文件
            os.remove(file)
        myFile = request.FILES.get("myfile", None)    # 获取上传的文件，如果没有文件，则默认为None
        ctx = {}
        if not myFile:
            ctx['rlt'] = "未上传任何文件"
            return render(request, "apkhall.html", ctx)
        destination = open(os.path.join("F:\\APKHallAutoTestProject\public\\app", myFile.name), 'wb+')
        # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():      # 分块写入文件
            destination.write(chunk)
        destination.close()
        ctx['rlt'] = "文件上传成功"
        return render(request, "apkhall.html", ctx)


def getresult(request):
    check_box_list = request.POST.getlist('check_box_list')
    name = request.POST.get('firstname')
    list = []
    for i in check_box_list:
        if int(i) == 3:
            list.append("testcase/Halllocal")
        elif int(i) == 1:
            list.append("testcase/enterAPK")
        elif int(i) == 4:
            list.append("testcase/ThirdPartyLogin")
        elif int(i) == 2:
            list.append("testcase/XiaoHaiTun")
        elif int(i) == 5:
            list.append("testcase/ALLGame")
        else:
            pass
    file = open('F:\APKHallAutoTestProject\caselist.txt', 'w')
    for i in list:
        file.write(i + '\n')
    file.close()

    change_yaml([name], 'Setting', 'sendemail', 'receivers')  # 修改接收者的邮箱
    packagename = package_name()  # 获取长尾包的类型
    change_yaml(packagename, 'Setting', 'apk_package', 'packagename')  # 修改配置中的包名

    os.system(r'F:\\APKHallAutoTestProject\\APKHallAutoTestProject.bat')
    return render(request, "apkhall.html")


def adb_devices(request):
    list = []
    ctv = {}
    out = os.popen("adb devices")
    for i in out.readlines():
        if 'List of devices' in i or "adb" in i or 'daemon' in i or 'offline' in i or "unauthorized" in i or len(
                i) < 5:
            pass
        else:
            serial = re.findall('(.*?)\\tdevice', i)
            s1 = ','.join(serial)
            list.append(s1)
    if len(list)> 1:
        ctv['rlc'] = "连接的设备超过一个，请检查服务器设备连接状况"
    elif len(list) == 1:
        ctv['rlc'] = "连接了一个设备，服务可正常使用"
    else:
        ctv['rlc'] = "服务器未连接任何设备，请连接设备后使用"

    return render(request, "apkhall.html", ctv)