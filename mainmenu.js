const {Menu} = require('electron')
const electron = require('electron')
const app = electron.app

const template = [
  {
    label: ('File'),
    submenu: [
      { role: 'Exit', label: ('Exit'), click: () => { app.quit(); } },
    ]
  },
  {
    label: ('Edit'),
    submenu: [
      {
        role: 'undo', label: ('Undo')
      },
      {
        role: 'redo', label: ('Redo')
      },
      {
        type: 'separator'
      },
      {
        role: 'cut', label: ('Cut')
      },
      {
        role: 'copy', label: ('Copy')
      },
      {
        role: 'paste', label: ('Paste')
      },
      {
        role: 'delete', label: ('Delete')
      },
      {
        role: 'selectall', label: ('Select all')
      }
    ]
  },
  {
    label: ('View'),
    submenu: [
      {
        role: 'resetzoom', label: ('Actual size')
      },
      {
        role: 'zoomin', label: ('Zoom in')
      },
      {
        role: 'zoomout', label: ('Zoom out')
      },
      { type: 'separator' },
      {
        role: 'togglefullscreen', label: ('Toggle fullscreen')
      },
      { type: 'separator' },
	  { role: 'Reload', label: ('Reload'), click: () => { app.getCurrentWindow.reload(); } },
      { type: 'separator' },
      { role: 'toggleDeveloperTools', label: ('Toggle Developer Tools'), click: () => 
		{ 	app.mainWindow.webContents.isDevToolsOpened() ? app.mainWindow.webContents.closeDevTools() : app.mainWindow.webContents.openDevTools(); } 
		},
    ]
  },
  {
    role: 'window', label: ('Window'),
    submenu: [
      {
        role: 'minimize', label: ('Minimize')
      },
      {
        role: 'close', label: ('Close')
      }
    ]
  },
  {
    role: 'help', label: ('Help'),
    submenu: [
      {
        label: ('Learn more'),
        click () { require('electron').shell.openExternal('https://github.com/crilleengvall/electron-tutorial-app') }
      }
    ]
  }
]

if (process.platform === 'darwin') {
  const name = app.getName()
  template.unshift({
    label: name,
    submenu: [
      {
        role: 'about', label: ('About') + " " + app.getName()
      },
      {
        type: 'separator'
      },
      {
        role: 'services', label: ('Services'),
        submenu: []
      },
      {
        type: 'separator'
      },
      {
        role: 'hide', label: ('Hide') + " " + app.getName()
      },
      {
        role: 'hideothers', label: ('Hide others')
      },
      {
        role: 'unhide', label: ('Unhide')
      },
      {
        type: 'separator'
      },
      {
        role: 'quit', label: ('Quit') + " " + app.getName()
      }
    ]
  })
  template[1].submenu.push(
    {
      type: 'separator'
    },
    {
      label: ('Speech'),
      submenu: [
        {
          role: 'startspeaking', label: ('Start speaking')
        },
        {
          role: 'stopspeaking', label: ('Stop speaking')
        }
      ]
    }
  )
  template[3].submenu = [
    {
      label: ('Close'),
      accelerator: 'CmdOrCtrl+W',
      role: 'close'
    },
    {
      label: ('Minimize'),
      accelerator: 'CmdOrCtrl+M',
      role: 'minimize'
    },
    {
      label: ('Zoom'),
      role: 'zoom'
    },
    {
      type: 'separator'
    },
    {
      label: ('Bring all to front'),
      role: 'front'
    }
  ]
}

const menu = Menu.buildFromTemplate(template);
Menu.setApplicationMenu(menu);

