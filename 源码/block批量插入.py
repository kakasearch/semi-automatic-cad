#连接到AutoCAD软件
from pyautocad import Autocad, APoint


acad = Autocad(create_if_not_exists=True)


def insert_block(in_path,name,x,y,z,xscale=1, yscale=1, zscale=1, rotation=0):
	#插入一个块
	insertionPnt = APoint(10, 0)
	insertionPnt = APoint(x,y,z)
	acad.model.InsertBlock(insertionPnt, in_path.replace('/','\\'), xscale, yscale, zscale, rotation)
	insertionPnt.x+=50
	insertionPnt.y+=50
	text = acad.model.AddText(name, insertionPnt, 15)



in_path = input('输入要插入的块文件位置：')#"d:/desktop/井盖.dwg"#
if in_path:
	if path :=input('输入坐标dat格式(点名,,x,y,z)文件位置：'):
		acad.prompt("准备批量插入块。。。\n")
		print('已连接',acad.doc.Name,'开始插入块')
		with open(path,encoding='utf-8')as f:
			points = f.readlines()
		for point in points:
			temp = point.replace('\n','').split(',')
			name = temp[0]
			x =float(temp[2])
			y = float(temp[3])
			z = float(temp[4])
			print(x,y,z)
			insert_block(in_path,name,x,y,z)
		acad.prompt("插入完毕")

          # 外部文件名尽量与当前文件中的各块名称不同；
          # 插入后外部文件名将作为其在当前文件中的块名；
          # 外部文件的坐标原点为其作为块的定位夹点。
           # acad.model.InsertBlock(InsertionPoint, Name, Xscale, Yscale, ZScale, Rotation)