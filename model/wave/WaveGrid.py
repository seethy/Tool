# -*- coding:utf-8 -*-
import wx, wx.grid
import pyperclip

class WaveGridData(wx.grid.PyGridTableBase):
    _cols = "水深 周期 波长".split()
    _data = [ ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''],
              ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''],
              ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''],
              ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''],
              ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''],
              ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''],
              ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''],
              ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''],
              ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''],
              ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''], ['', '', ''],
            ]
    _highlighted = set()

    def GetColLabelValue(self, col):
        return self._cols[col]

    def GetNumberRows(self):
        return len(self._data)

    def GetNumberCols(self):
        return len(self._cols)

    def GetValue(self, row, col):
        return self._data[row][col]

    def SetValue(self, row, col, val):
        self._data[row][col] = val

    def GetAttr(self, row, col, kind):
        attr = wx.grid.GridCellAttr()
        attr.SetBackgroundColour(wx.GREEN if row in self._highlighted else wx.WHITE)

    def set_value(self, row, col, val):
        self._highlighted.add(row)
        self.SetValue(row, col, val)

    def clearhightlight(self):
        self._highlighted.clear()

    def clear(self):
        for r in range(0, self.GetNumberRows()):
            for c in range(0, self.GetNumberCols()):
                self._data[r][c] = ''
        self.clearhightlight()

class WaveFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None)
        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.waveGrid = WaveGrid(self, id=-1, pos=(10,35), size=(400,300))
        self.Sizer.Add(self.waveGrid, 1, wx.EXPAND)

class WaveGrid(wx.grid.Grid):
    def __init__(self, parent, id, pos, size):
        wx.grid.Grid.__init__(self, parent, id, pos, size)
        self.data = WaveGridData()
        self.SetTable(self.data)
        self.SetSelectionMode(wx.grid.Grid.wxGridSelectCells)
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.onRightClick)
        self.Bind(wx.grid.EVT_GRID_RANGE_SELECT, self.onRangeSelect)
        self.chosedLeftCol = 0
        self.chosedRightCol = 0
        self.chosedTopRow = 0
        self.chosedBottomRow = 0

    def onRightClick(self, event):
        self.PopupMenu(GridPopupMenu(self), event.GetPosition())

    def onRangeSelect(self, event):
        if event.Selecting():
            self.chosedLeftCol = event.GetLeftCol()
            self.chosedRightCol = event.GetRightCol()
            self.chosedTopRow = event.GetTopRow()
            self.chosedBottomRow = event.GetBottomRow()

class GridPopupMenu(wx.Menu):
    def __init__(self, parent):
        super(GridPopupMenu, self).__init__()
        self.parent = parent

        mmi = wx.MenuItem(self, wx.NewId(), '复制')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnCopy, mmi)

        cmi = wx.MenuItem(self, wx.NewId(), '粘贴')
        self.AppendItem(cmi)
        self.Bind(wx.EVT_MENU, self.OnPaste, cmi)

    def OnCopy(self, e):
        copytext = ""
        for row in range(self.parent.chosedTopRow, self.parent.chosedBottomRow + 1):
            for col in range(self.parent.chosedLeftCol, self.parent.chosedRightCol + 1):
                copytext = copytext + self.parent.data.GetValue(row, col) + "\t"
            copytext = copytext[0:len(copytext)-1]
            copytext = copytext + "\n"
        copytext = copytext[0:len(copytext)-1]
        pyperclip.copy(copytext)

    def OnPaste(self, e):
        self.parent.data.clearhightlight()
        row = self.parent.chosedTopRow
        col = self.parent.chosedLeftCol
        pastext = pyperclip.paste()
        for r in pastext.split("\n"):
            col = self.parent.chosedLeftCol
            for v in r.split("\t"):
                self.parent.data.set_value(row, col, v)
                col = col + 1
                if col > self.parent.chosedRightCol:
                    break
            row = row + 1
            if row > self.parent.chosedBottomRow:
                break
        self.parent.Refresh()

def main():
    app = wx.PySimpleApp()
    app.TopWindow = WaveFrame()
    app.TopWindow.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()


