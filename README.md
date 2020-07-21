##启动##
打开cadtool_main.exe和cad，如果没有打开cad会自动打开
##功能##
1. ***批量偏移：*** 输入x方向或y方向或两个方向的数据的偏移距离，生成偏移线。支持输入多组数据
2. ***生成窗户：***  给定xy方向尺寸，绘制窗户
3. ***生成阳台：***  给定xy方向尺寸，按最大2m一组绘制阳台，
4. ***生成单元门：***给定xy方向尺寸，绘制单元门
5. ***读取配置：***读取json文件绘图

##输入数据##
- 在输入框中输入数据，
- ctrl+o打开文件，程序自动读取文件内容（utf-8）

##json配置文件示例##


    {
    "name": "xx小区x#楼_立面图配置",//当前配置的名字，便于管理
    "offset": {  //偏移线实体
        "name": "偏移线",//偏移实体的名字，便于管理
        "data": ["123,1232，123,123,123# 123,345,345",
                "456,34,5,34,34 345,345,345,56",
                 "2343,234,234,34   345,234,234"],
        //任意组的偏移线。每组偏移线里前面是x方向的偏移，没有则写0；后面是y方向的偏移数组，没有则写0或不写；中间为分隔符，可以是#、空格、tab
        "space": 800,//不同组之间的间隔
        "start": [0, 0],//左上角坐标
        "layer": {//所属图层信息，没有会新建，可设置图层的color，linetype，lineweight即颜色、线型、线宽
            "name": "建筑物"
        }
    },
    "window": {//窗户实体
        "name": "窗口",
        "data": "1920.56,1320分割102，123",//x,y方向尺寸，以任意非数字字符分开
        "space": 800,//窗户与窗户间的间隔
        "start": [0, 1000],//起始位置
        "layer": {//所属图层
            "name": "窗口",
            "color": 4
        }
    },
    "balcony": {
        "name": "阳台",
        "data": "1500,1232  1543，2342,1234,1234",
        "space": 800,
        "start": [0, 800],
        "layer": {
            "name": "阳台",
            "color": 3
        }
    },
    "door": {
        "name": "单元门",
        "data": "1200,1900 1350,3030",
        "space": 800,
        "start": [0, 0],
        "layer": {
            "name": "单元门",
            "color": 6
        }
    }
    }

