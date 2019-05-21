#	MIT License
#
#	Copyright (c) 2019 J M Evans (g4 <at> novadsp <dot> com)
#
#	Permission is hereby granted, free of charge, to any person obtaining a copy
#	of this software and associated documentation files (the "Software"), to deal
#	in the Software without restriction, including without limitation the rights
#	to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#	copies of the Software, and to permit persons to whom the Software is
#	furnished to do so, subject to the following conditions:
#
#	The above copyright notice and this permission notice shall be included in all
#	copies or substantial portions of the Software.
#
#	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#	SOFTWARE.
#

from browser import alert, document, window, websocket
import json

#----------------------------------------------------------
# get global
def getGlobal():
	return __BRYTHON__

#----------------------------------------------------------
# convert a generic JS object into a Python string
def toString(jsObj):
	#window.js_dump(jsObj)
	if jsObj is None:
		return "null"
	props = {}
	for k,v in enumerate(jsObj):
		if jsObj[v] is not None:
			props[v] = jsObj[v]
	return str(props)

#----------------------------------------------------------
# check a JS object to see if it has valid key
def exists(jsObj,key):
	for k,v in enumerate(jsObj):
		if v == key:
			return True
	return False

#----------------------------------------------------------
# track the actual states. websocket close can be delayed.
eDisconnected = 1
eConnecting = 2
eConnected = 3
eDisconnecting = 4

#----------------------------------------------------------
#
class Application:

	#
	def __init__(self,url,ui,grid,tree):
		print("__init__ => " + url)
		self.url = url
		self.ui = ui
		self.state = eDisconnected
		self.webSocket = None
		self.grid = grid
		self.tree = tree
		#
		# attach some event handlers for the toolbar buttons
		btn = self.ui['layout_top_toolbar'].get('btnConnect')
		btn.onClick = self.onClickConnect
		btn = self.ui['layout_top_toolbar'].get('btnDisconnect')
		self.ui['layout_top_toolbar'].disable('btnDisconnect')
		btn.onClick = self.onClickDisconnect
		btn = self.ui['layout_top_toolbar'].get('btnClear')
		self.ui['layout_top_toolbar'].disable('btnClear')
		btn.onClick = self.onClickClear
		# for grid and tree
		self.tree.on('changed.jstree',self.onClickTree)
		self.grid.on('click',self.onClickGrid)

	# web socket handlers				
	def on_open(self,evt):
		self.state = eConnected
		self.ui['layout_top_toolbar'].disable('btnConnect')
		self.ui['layout_top_toolbar'].enable('btnDisconnect')

	def on_message(self,evt):
		print(evt.data)
		self.grid.add({ 'recid': self.grid.total, 'directory' : evt.data })
		if self.grid.total > 0:
			self.ui['layout_top_toolbar'].enable('btnClear')

	def on_close(self,evt):
		self.state = eDisconnected
		self.ui['layout_top_toolbar'].enable('btnConnect')
		self.ui['layout_top_toolbar'].disable('btnDisconnect')

	def on_wsError(self,evt):
		pass

	# handle opening and binding of the socket
	def openSocket(self):
		print("openSocket")
		if not websocket.supported:
			alert("WebSocket is not supported by your browser")
			return
		if self.state == eDisconnected:
			self.state = eConnecting
			# open a web socket
			self.webSocket = websocket.WebSocket(self.url)
			# bind functions to web socket events
			self.webSocket.bind('open',self.on_open)
			self.webSocket.bind('close',self.on_close)
			self.webSocket.bind('message',self.on_message)
			self.webSocket.bind('error',self.on_wsError)

	# set socket to close
	def closeSocket(self):
		print("closeSocket")
		if self.state == eConnected or self.state == eConnecting:
			# console.log("closing {0}".format(self.state))
			self.webSocket.close()
			# self.state = eDisconnected

	# event handlers
	def onClickConnect(self,evt):
		self.openSocket()

	def onClickDisconnect(self,evt):
		self.closeSocket()

	def onClickGrid(self,evt):
		pass
		# sel = self.grid.getSelection()
		
	def onClickClear(self,evt):
		self.grid.clear()

	def onClickTree(self,evt,data):
		# print(data.node.text)
		if self.state == eConnected:
			self.webSocket.send(data.node.text)
		
#----------------------------------------------------------
# the main w2ui layout
w2layoutDefinition = {
		'name': 'layout',
		'padding': 8,
		'panels': [
			# { type: 'left', size: '16px', style: "background-color: rgb(255,255,255);" },
			{ 'type': 'top', 'size': 24, 'style': 'background-color: rgb(255,255,255);',
				'toolbar': 
				{
					'name': 'toolbar',
					# hook up button event handler
					# 'onClick': window.app.onClickToolbar,
					'items': 
					[
						{ 'type': 'button',  'id': 'btnConnect',  'caption': 'Connect', 'icon': 'w2ui-icon-check' },
						{ 'type': 'button',  'id': 'btnDisconnect',  'caption': 'Disconnect', 'icon': 'w2ui-icon-cross', 'disabled': False },
						{ 'type': 'button',  'id': 'btnClear',  'caption': 'Clear', 'icon': 'w2ui-icon-cross' },
						{ 'type': 'spacer' },
					],
				},
			},
			{ 
				'type': 'left', 'resizable': True, 'size': '25%', 'content': '<div style="background-color: rgb(255,255,255); border:8px;"; id="jstree_container"></div>', 'style': "background-color: rgb(255,255,255);",
			},
			{ 
				'type': 'main', 'minSize': 100, 'content': 'content'	
				},
			# { 'type': 'preview',  'size': '50%', 'resizable': True, 'content': '<div style="height: 100%; width: 100%, background-color: rgb(255,255,255);" id="canvas-holder"><canvas id="bar-chart"></canvas></div>',  style: "background-color: rgb(255,255,255);" },
			{ 'type': 'right', 'size': '16px', 'style': "background-color: rgb(255,255,255);"  },
		]
	}

# the tree
treeDefinition = { 'core' : 
	{
		'themes' : { 'multiple': False, 'dots': False },
		'data' : 
		[ 
			{ 'text': 'Root node', 'state': { 'opened' : True },
				'children': [
					{ 'text' : 'Child node 1', 'children': [ 
							{ 'text' : "1.1" } 
						] 
					},
					{ 'text' : 'Child node 2' } 
				]
			}
		]
	}
}

# the grid layout
gridDefinition = { 
	'name': 'grid', 
	# 'header': 'Brython',
	'show': {
		'header': False,
		'footer': True,
		'toolbar': False,
		'toolbarDelete': False
	},
	'columns': [
			# { field: 'recid', caption: 'ID', size: '50px', sortable: false, attr: 'align=left' },
			{ 'field': 'directory', 'caption': 'Directory', 'size': '30%', 'sortable': True, 'resizable': True },
	],
	'records': [
			# it's possible to add literals as shown below
			# { 'recid': 1, 'directory': 'alpha', },
		]
	}

# attach the lay0out to the HTML div
window.jQuery('#main').w2layout(w2layoutDefinition)
# jstree_container is defined in the style tag of the left-hand panel
tree = window.jQuery('#jstree_container').jstree(treeDefinition)
# create the grid
grid = window.jQuery().w2grid(gridDefinition)
# and insert the grid into the w2ui layout
window.w2ui.layout.content('main', grid)
# set up the global application instance
document.pyapp = Application("wss://echo.websocket.org",window.w2ui,grid,tree)
# ensure grid and friends are refreshed
# grid.refresh()

