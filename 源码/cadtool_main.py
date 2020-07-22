import sys
import cadtool
from pyautocad import Autocad,APoint,aDouble
from re import findall
from json import loads
from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
                             QAction, QFileDialog, QApplication)
from PyQt5.QtGui import QIcon
class cad:
    def __init__(self,ui):
        self.acad = Autocad(create_if_not_exists=True)
        self.ui = ui
    def info(self,str_):
        #信息提示
        self.acad.prompt(str_)
        self.ui.label.setText(str_+"\n"+'\n'.join(self.ui.label.toPlainText().split('\n')[:20]))
    def new_layer(self,name,attr=''):
                #设置图层
        #输入要改变的图元，目标图层名字,传attr新建图层样式，attr为字典
        #attr ={'color':1,
                # 'linetype'：'ACAD_ISO08W100',
                # 'lineweight':0.13
                # }
        
        layer = self.acad.ActiveDocument.Layers.Add(name)
        
        
        #如果有参数，就改，会覆盖
        pro = [i for i in attr]
        
        if 'color' in pro and attr['color']:

            try:
                layer.color = attr['color']
                 # ClrNum为颜色索引号，其取值范围为[0,256]；
                 # 标准颜色的颜色索引号指定如下：：1 红、2 黄、3 绿、4 青、5 蓝、6 洋红、7 白/黑；
                 # 0 ByBlock、256 ByLayer；
                 # 其他颜色索引号见 https://wenku.baidu.com/view/9d458b70195f312b3069a505.html。
            except:
                 self.info('error！！！！！！！！！颜色设置失败，请自行设置')
        if 'linetype' in pro and attr['linetype']:
            try:#设置线型
                self.acad.ActiveDocument.Linetypes.Load(attr['Linetype'],"acadiso.lin")
                # 加载线型，"ACAD_ISO05W100"为线型名称，详细信息见CAD帮助文档；
                # "acadiso.lin"为用于公制单位的线型定义文件，详细信息见CAD帮助文档；
                # 为图层指定线型前，需先加载相关线型；
                # 注意：不能重复加载，否则报错——'记录名重复'
                layer.Linetype = attr['Linetype']
            except:
                layer.Linetype = attr['Linetype']
        if 'lineweight' in pro and attr['lineweight']:
            try:#设置线型宽
                layer.Lineweight = attr['Lineweight']*100
                # 13表示线宽为0.01mm的13倍，即0.13mm；
                # 线宽值∈{0,5,9,13,15,18,20,25,30,35,40,50,53,60,70,80,90,100,106,120,140,158,200,211}；
                # 线宽值在上述集合中选取，含义为0.01mm的整数倍；其他数值非系统默认；
                # 可以修改现有线宽，但不能添加或删除线宽，修改在CAD程序中进行。
            except:
                self.info('error！！！！！！！！！线宽设置错误，检查cad是否有次线宽，或自行设置')
        return layer
    def set_layer(self,from_object,target,attr={}):
        layers_names = [self.acad.ActiveDocument.Layers.Item(i).Name for i in range(self.acad.ActiveDocument.Layers.count)]
        # 当前文件模型空间中所包含的所有图层名称
        
        if(target not in layers_names):
            #没有这个图层，新建一个
            self.new_layer(target,attr)  
        from_object.layer = target
        


    def cad_o(self,h_offset,v_offset,space=50,start=[0,0],config=''):
        #cad o命令
        #输入偏移数组，输出偏移线
        #['1','2','3'] or ['0']
        #水平偏移数组，垂直偏移
        #min_left #记录图形最下角位置y，防止重叠
        p2 = APoint(0,0)
        if ['0'] != h_offset: #画水平偏移线
            offset_data_arrary = []
            for i in range(len(h_offset)):
                offset_data_arrary.append(float(h_offset[i]))
            offset_length = max(offset_data_arrary)*3 #线的长度
            p1 = APoint(start[0],start[1]+self.min_left)#起始点
            p2 = APoint(0, self.min_left+start[1]-offset_length)#终点
            self.min_left =p2.y - space #间隔50，便于下次画 
         ###################min_left = p2.y -50 #间隔50，便于下次画 
            #向下画线
            obj = self.acad.model.AddLine(p1, p2)
            if config:
                target_layer = config['layer']
                self.set_layer(obj,target_layer['name'],target_layer)
            for offset in offset_data_arrary:#右侧偏移
                p1.x += offset
                p2.x += offset
                self.acad.model.AddLine(p1, p2)
            self.acad.model.AddLine(APoint(0,p2.y), p2) #下边连接
            if config:
                target_layer = config['layer']
                self.set_layer(obj,target_layer['name'],target_layer)
            self.info('水平偏移'+str(offset_data_arrary))

        if ['0'] != v_offset: #画竖直偏移线
            offset_data_arrary = []
            for i in range(len(v_offset)):
                offset_data_arrary.append(float(v_offset[i]))
            if p2.y:
                offset_length =p2.y #线的长度
                p1 = APoint(0, p2.y)#起始点
            else:
                self.min_left -= space #间隔50，便于下次画 
                offset_length = max(offset_data_arrary)*3
                p1 =APoint(0,min_left)
                p2 = APoint(offset_length,min_left)
            #向右画线
            self.acad.model.AddLine(p1, p2)
            if config:
                target_layer = config['layer']
                self.set_layer(obj,target_layer['name'],target_layer)
            for offset in offset_data_arrary:#上侧偏移
                p1.y += offset
                p2.y += offset
                self.acad.model.AddLine(p1, p2)
            if config:
                target_layer = config['layer']
                self.set_layer(obj,target_layer['name'],target_layer)
            self.info('垂直偏移'+str(offset_data_arrary))
    def cad_pl(self,arr):
       
    #输入坐标数组 [(1,2),(2,3)] or [apoint(1,2),apoint(1,3)] or[1,2,0,1,3,0]
    #画线，返回pl对象
        try:
            if len(arr[0]) == 2:
                #[(1,2),(2,3)]
                tmp = []
                for item in arr:
                    tmp.append((item[0],item[1],0))
                pnts = [j for i in tmp for j in i]  # 将各点坐标顺序变换为1行多列的1维数组。
                
            elif len(arr[0]) ==3:
                #[apoint(1,2),apoint(1,3)]
                pnts = [j for i in arr for j in i] 
            else:
                self.info('cad_pl error!!')
                return  
        except:
            #[1,2,0,1,3,0]
            pnts = arr
        pnts = aDouble(pnts)
        return self.acad.model.AddPolyLine(pnts)
        



    def offset(self,config=''):
        #可以批量偏移的偏移命令
        ###数据获取
        if(config):
            target_layer = config['layer']
            datas = config['data']
            space = config['space']
            start = config['start']
            datas=config['data']
        else:
            space = 800
            start = [0,0]#窗户起始右下标
            target_layer = ''
            datas= self.ui.text.toPlainText().replace('，',',').split('\n')
        if not datas:
            self.info('需要先输入数据')
            return
        self.min_left = 0 #左下角位置
        #数据处理成固定格式，123 123
        #self.info('读取数据 '+str(datas))
        
        for i in range(len(datas)):
            #'2,3,4 4,3,2' or '1,2,3,4'
            if '#' in datas[i]:
                offset = datas[i].split('#')
            elif '\t' in datas[i]:
                offset = datas[i].split('\t')
            elif ' ' in datas[i]:
                offset = datas[i].split(' ')
            else:
                offset = [datas[i],'0']
            ##['1,2,3','3,2,1'] or ['1,2,3','0']
            h_offset = findall(r'\d+[\.]?\d*',offset[0])#取出所有数字
            v_offset = findall(r'\d+[\.]?\d*',offset[1])#取出所有数字
            #画偏移
            obj = self.cad_o(h_offset,v_offset,space=space,start=start,config=config)
    def window(self,config=''): 
        #窗户向左画
        if(config):
            space = config['space']
            start = config['start']#窗户起始右下标
            target_layer = config['layer']
            datas = config['data']
        else:
            space = 800
            start = [0,0]#窗户起始右下标
            target_layer = ''
            datas= self.ui.text.toPlainText().replace('，',',')
        if datas:
            hvs = findall(r'\d+[\.]?\d*',datas)#取出所有数字
        else:
            self.info('请输入数据')
            return

        #self.info(list(range(len(hvs))[::2]))
        for i in range(len(hvs))[::2]:
            h = float(hvs[i])
            v = float(hvs[i+1])
            self.acad.model.AddText('{}x{}'.format(hvs[i],hvs[i+1]), APoint(start[0]-h,start[1]-700), 300)
            self.info('窗口绘制： {},{}'.format(hvs[i],hvs[i+1]))
            x,y = start[0],start[1]
            pnts = [(x,y),(x-h,y),(x-h,y+v),(x,y+v),(x,y),(x,y+v/2),(x-h,y+v/2),(x-h/2,y+v/2),(x-h/2,y+v),(x-h/2,y)]
            obj = self.cad_pl(pnts)
            if target_layer:
                self.set_layer(obj,target_layer['name'],target_layer)
            start =(start[0]-space-h,start[1])
            #pnts.append(-h,min_right 0,min_right 0,-v+min_right -h,-v+min_right -h,min_right -h/2,min_right -h/2,-v+min_right -h/2,-v/2+min_right, -h,-v/2+min_right 0,-v/2+min_right)
    def balcony(self,config=''):
        if(config):
            space = config['space']
            start = config['start']#窗户起始右下标
            target_layer = config['layer']
            datas = config['data']
        else:
            space = 800
            start = [0,0]#窗户起始右下标
            target_layer = ''
            datas= self.ui.text.toPlainText().replace('，',',')
        if datas:
            hvs = findall(r'\d+[\.]?\d*',datas)#取出所有数字
        else:
            self.info('请输入数据')
            return

        #self.info(list(range(len(hvs))[::2]))
        for i in range(len(hvs))[::2]:
            h = float(hvs[i])
            v = float(hvs[i+1])
            self.acad.model.AddText('{}x{}'.format(hvs[i],hvs[i+1]), APoint(start[0],start[1]-700), 300)
            self.info('阳台绘制： {},{}'.format(hvs[i],hvs[i+1]))
            num = 0
            x,y = start#起点元祖
            while h/(2**num)>2000:
                num+=1
            min_h = h/(2**num)
            pnts = []
            for i in range(2**num):
                #一组
                temp_pnts = [(x,y),(x+min_h,y),(x+min_h,y+v),(x,y+v),(x,y),(x,y+v*2/3),(x+min_h,y+v*2/3),(x+min_h/2,y+v*2/3),(x+min_h/2,y),(x+min_h,y)]
                pnts+= temp_pnts
                x+=min_h#下一个
            obj = self.cad_pl(pnts)
            if target_layer:
                self.set_layer(obj,target_layer['name'],target_layer)
            start =(start[0]+h+space,start[1])

    def door(self,config=''):
        #door 向左下画
        if(config):
            space = config['space']
            start = config['start']#窗户起始右下标
            target_layer = config['layer']
            datas = config['data']
        else:
            space = 800
            start = [0,0]#窗户起始右下标
            target_layer = ''
            datas = self.ui.text.toPlainText().replace('，',',')
        if datas:
            hvs = findall(r'\d+[\.]?\d*',datas)#取出所有数字
        else:
            self.info('请输入数据')
            return
        #self.info(list(range(len(hvs))[::2]))
        for i in range(len(hvs))[::2]:
            h = float(hvs[i])
            v = float(hvs[i+1])
            self.acad.model.AddText('{}x{}'.format(hvs[i],hvs[i+1]), APoint(start[0]-h,start[1]-v-700), 300)
            self.info('门绘制： {},{}'.format(hvs[i],hvs[i+1]))
            x,y = start#起点元祖
            pnts = [(x,y),(x-h,y),(x-h,y-v),(x,y-v),(x,y)]
            outer = self.cad_pl(pnts)#框
            if config:

                self.set_layer(outer,target_layer['name'],target_layer)
            pnts = [(x,y),(x-0.82*h,y-0.1*v),(x-h,y-v)]
            inner = self.cad_pl(pnts)#里面黄线
            inner.color = 2
            # 标准颜色的颜色索引号指定如下：：1 红、2 黄、3 绿、4 青、5 蓝、6 洋红、7 白/黑；
            start =(start[0]-space-h,start[1])

    def draw_from_config(self,path='config.json'):
       #self.info(path)
        #self.info(data)
        data =  self.ui.text.toPlainText()
        if data:
            try:
                data = loads(data)
                self.info('正在读取 '+data['name'])
            except:
                self.info('配置解析失败，请检查是否为json格式')
                return        
        else:
            self.info('请先输入数据')
            return
        for key in ['offset','window','balcony','door']:
            if tmp := data.get(key):
                if tmp.get('name'):
                    self.info('\n\n*****开始绘制： '+tmp['name'])
                eval("self.%s(tmp)"%key)
        self.info('\n\n================================')

def showDialog(ui):
    ui.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  
    # 弹出文件选择框。第一个字符串参数是getOpenFileName()方法的标题。第二个字符串参数指定了对话框的工作目录。
    # 默认的，文件过滤器设置成All files (*)。
    fname = QFileDialog.getOpenFileName(None, 'Open file', './config.json','*;;*.json;;*.txt')
    # 选中文件后，读出文件的内容，并设置成文本编辑框组件的显示文本
    if fname[0]:
        f = open(fname[0], 'r',encoding='utf-8')

        with f:
            data = f.read()
            ui.text.setPlainText(data)

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        MainWindow = QMainWindow()
        ui = cadtool.Ui_cad_tool()
        ui.setupUi(MainWindow)
        
        MainWindow.show()
        cad = cad(ui)
        ui.window_btn.clicked.connect(lambda :cad.window())
        ui.door_btn.clicked.connect(lambda :cad.door())
        ui.offset_btn.clicked.connect(lambda :cad.offset())
        ui.balcony_btn.clicked.connect(lambda :cad.balcony())
        ui.config_btn.clicked.connect(lambda :cad.draw_from_config())
        ui.actionopen_2.triggered.connect(lambda :showDialog(ui))
        ui.actionexit_2.triggered.connect(lambda :exit())
        #ui.plainTextEdit_5.setPlainText("...")
        sys.exit(app.exec_())
    except Exception as e:
        cad.info(str(e))