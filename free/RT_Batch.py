# -*- coding: utf-8 -*-
#MenuTitle: RT_批处理【V1.01】
#By_RealType

#定制插脚脚本+V：real_type
#依赖dvanilla类库

import sys
import vanilla
import copy
class RTBatch():
	
	def __init__(self):
		
		self.font = Glyphs.font
		self.currentLayer = self.font.selectedLayers[0]
		self.currentGlyph = self.currentLayer.parent
		self.masterId = self.currentLayer.master.id
		self.glyphs = []
		self.layers = []
		if self.font.currentTab == None:
			self.glyphs = self.font.selection
			for glyph in self.glyphs:
				for layer in glyph.layers:
					self.layers.append(layer)
		else:
			self.glyphs.append(self.currentGlyph)
			self.layers = self.font.selectedLayers

		self.doit = 0
		titles = [
			u"清空所选字符的前景",
			u"清空所选字符的背景",
			u"所选字符前景移动到背景",
			u"所选字符前景复制到背景",
			u"所选字符背景移动到前景",
			u"所选字符背景复制到前景",
			u"清空所选字符所有参考线",
			u"清空所选字符所有注释",
			u"清空所选字符所有定位点",
			u"释放所选字符前景部件",
			u"释放所选字符背景部件",
			u"左右居中",
			u"上下居中",
			u"上下左右居中",
		]
		self.width = 300
		self.h = 30
		self.y = 10
		self.w = vanilla.Window((self.width, self.h * len(titles)+100), u"RT_批处理【V1.01】")

		self.w.label1 = vanilla.TextBox((50, self.y, 200, self.h), u"选择你的操作")
		self.y += self.h

		self.w.radioGroup = vanilla.RadioGroup(
			(50, self.y, 300, self.h * len(titles)),
			titles,
			callback=self.radioSelect,
			isVertical=True,
		)
		self.y += self.h * len(titles) + 20
		self.w.btn = vanilla.Button((self.width / 2 - 20, self.y, 40, 10),u"执行",callback=self.dodo)
		
		self.w.radioGroup.set(0)
		self.selectedNum = 0
		self.w.center()
		self.w.open()
		self.w.makeKey()

	def radioSelect(self, sender):
		self.selectedNum = sender.get()

	def dodo(self,sender):
		try:
		   
			self.font.disableUpdateInterface()
			selectedNum = self.selectedNum
			#print self.glyphs
			if len(self.layers)>0:

				for layer in self.layers:
					#print(layer)
					if selectedNum==0:
						layer.clear()
					elif selectedNum==1:
						layer.background.clear()
					elif selectedNum==2 or selectedNum==3:
						try:
							if layer.components:
								layer.background.components = copy.copy(layer.components)
							if layer.paths:
								layer.background.paths = copy.copy(layer.paths)
						except:
							if layer.shapes:
								layer.background.shapes = copy.copy(layer.shapes)
						if selectedNum==2:
							layer.clear()
					elif selectedNum==4 or selectedNum==5:
						try:
							if layer.background.components:
								layer.components = copy.copy(layer.background.components)
							if layer.background.paths:
								layer.paths = copy.copy(layer.background.paths)
						except:
							if layer.background:
								layer.shapes = copy.copy(layer.background.shapes)
						if selectedNum==4:
							layer.background.clear()
					elif selectedNum==6:
						layer.guides=None
					elif selectedNum==7:
						layer.annotations=None
					elif selectedNum==8:
						layer.anchors=None
					elif selectedNum==9:
						layer.decomposeComponents()
					elif selectedNum==10:
						layer.background.decomposeComponents()
					elif selectedNum==11:
						width = layer.width
						w = (width-layer.bounds.size.width)/2
						layer.LSB=w
						layer.width=width
					elif selectedNum==12:
						
						height  = layer.associatedFontMaster().ascender - layer.associatedFontMaster().descender 
						h = layer.associatedFontMaster().ascender-height/2
						offsetY = h - (layer.bounds.origin.y + layer.bounds.size.height/2) 
						for path in layer.paths:
							path.applyTransform((1,0,0,1,0,offsetY))
					elif selectedNum==13:
						width = layer.width
						w = (width-layer.bounds.size.width)/2
						layer.LSB=w
						layer.width=width
						height  = layer.associatedFontMaster().ascender - layer.associatedFontMaster().descender 
						h = layer.associatedFontMaster().ascender-height/2
						offsetY = h - (layer.bounds.origin.y + layer.bounds.size.height/2) 
						for path in layer.paths:
							path.applyTransform((1,0,0,1,0,offsetY))

			self.w.close()
		except:
			print("Unexpected error:", sys.exc_info())
		finally:
			self.font.enableUpdateInterface()
				
		
RTBatch()
		
		