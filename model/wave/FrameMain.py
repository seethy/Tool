# -*- coding:utf-8 -*-
import WaveGrid, FileHandler
import re
import model.math.NewtonMethod as nm
import wx

#set the file filter
wildcard1 = "All excel files (*.xls;*.xlsx)|*.xls;*.xlsx"

class MyFrame(wx.Frame):
    def __init__(self, parent, ID, title):
        wx.Frame.__init__(self, parent, -1, title, wx.DefaultPosition, wx.Size(600,400))
        ## set menu
        menubar = wx.MenuBar()
        file = wx.Menu()
        model = wx.Menu()
        quit = wx.MenuItem(file, 105, '&退出\tCtrl+Q', '退出程序')
        file.AppendItem(quit)
        wavelength = wx.MenuItem(file, 200, '&波长模型', '使用牛顿迭代法计算波长')
        wavelength_txt = wx.MenuItem(file, 201, '&波长模型(文本)', '使用牛顿迭代法计算波长')
        wavelength_xls = wx.MenuItem(file, 202, '&波长模型(Excel)', '使用牛顿迭代法计算波长')
        lowwaveheight = wx.MenuItem(file, 203, '&低波长模型(文本)', '使用牛顿迭代法计算波长')
        model.AppendItem(wavelength)
        model.AppendItem(wavelength_txt)
        model.AppendItem(wavelength_xls)
        model.AppendItem(lowwaveheight)

        menubar.Append(file, '&文件')
        menubar.Append(model, '&模型')

        wx.EVT_MENU(self, 105, self.OnQuit)
        wx.EVT_MENU(self, 200, self.OnWaveLength)
        wx.EVT_MENU(self, 201, self.OnWaveLengthTxt)
        wx.EVT_MENU(self, 202, self.OnWaveLengthExcel)
        self.SetMenuBar(menubar)
        self.Centre()

    def OnQuit(self, event):
        self.Close()

    def OnWaveLength(self, event):
        self.DestroyChildren()

        vbox = wx.BoxSizer(wx.HORIZONTAL)

        srclabel = wx.StaticText(self, pos=(10, 10), label='统一周期：')
        vbox.Add(srclabel, proportion=0, flag=wx.RIGHT, border=10)
        self.periodTxtCtrl = wx.TextCtrl(self, pos=(80,5),size=(80,25))
        vbox.Add(self.periodTxtCtrl, proportion=1)
        setPeriodbtn = wx.Button(self, label="设置", pos=(180,5), size=(90, 25))
        vbox.Add(setPeriodbtn, proportion=0)
        setPeriodbtn.Bind(wx.EVT_BUTTON, self.OnSetPeriod)
        calbtn = wx.Button(self, label="执行计算", pos=(300,5), size=(90, 25))
        vbox.Add(calbtn, proportion=0)
        calbtn.Bind(wx.EVT_BUTTON, self.OnCal)
        clearbtn = wx.Button(self, label="清空", pos=(350, 5), size=(90, 25))
        vbox.Add(clearbtn, proportion=0)
        clearbtn.Bind(wx.EVT_BUTTON, self.OnClear)

        self.wavegrid = WaveGrid.WaveGrid(self, id=-1, pos=(10, 35),size=(400,300))
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(vbox)
        mainSizer.Add(self.wavegrid, 1, wx.EXPAND)
        self.SetSizerAndFit(mainSizer)

    def OnClear(self, event):
        self.wavegrid.data.clear()
        self.wavegrid.Refresh()

    def OnSetPeriod(self, event):
        periodvalue = self.periodTxtCtrl.GetValue()
        pattern = re.compile(r'^[-+]?[0-9]*\.?[0-9]+$')
        match = pattern.match(periodvalue)
        if match:
            for r in range(0, self.wavegrid.data.GetNumberRows()):
                self.wavegrid.data.SetValue(r, 1, periodvalue)
            self.wavegrid.Refresh()
        else:
            dlg = wx.MessageDialog(self, message='周期格式不合法，请重新输入', caption='Message', style=wx.OK)
            dlg.ShowModal()
            dlg.Destroy()

    def OnCal(self, event):
        pattern = re.compile(r'^[-+]?[0-9]*\.?[0-9]+$')
        newtonmethod = nm.NewtonMethod()
        for r in range(0, self.wavegrid.data.GetNumberRows()):
            deep = self.wavegrid.data.GetValue(r,0).strip()
            period = self.wavegrid.data.GetValue(r, 1).strip()
            if pattern.match(deep) and pattern.match(period):
                deepf = float(deep)
                periodf = float(period)
                if deepf > 0 and periodf > 0:
                    wavelength = newtonmethod.GetWaveLenth(period=periodf, depth=deepf)
                    self.wavegrid.data.SetValue(r,2,'%-.2f' % wavelength)
        self.wavegrid.Refresh()

    def OnWaveLengthTxt(self, event):
        self.DestroyChildren()
        panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(600,400))
        vbox = wx.BoxSizer(wx.HORIZONTAL)

        srclabel = wx.StaticText(panel, pos=(10,10), label='源文件夹：')
        vbox.Add(srclabel, proportion=0, flag=wx.RIGHT, border=10)
        self.sourceDirTxtCtrl = wx.TextCtrl(panel, pos=(80,5), size=(290,25))
        vbox.Add(self.sourceDirTxtCtrl, proportion=1)
        srcbtn = wx.Button(panel, label="选择文件夹...",pos=(380,5), size=(90,25))
        vbox.Add(srcbtn, proportion=0)
        srcbtn.Bind(wx.EVT_BUTTON, self.OnOpenSrcDir)

        destlabel = wx.StaticText(panel, pos=(10, 50), label='结果文件夹：')
        vbox.Add(destlabel, proportion=0, flag=wx.RIGHT, border=10)
        self.destDirTextCtrl = wx.TextCtrl(panel, pos=(80, 50), size=(290, 25))
        vbox.Add(self.destDirTextCtrl, proportion=1)
        destbtn = wx.Button(panel, label="选择文件夹...", pos=(380, 50), size=(90, 25))
        vbox.Add(destbtn, proportion=0)
        destbtn.Bind(wx.EVT_BUTTON, self.OnOpenDestDir)

        exebtn = wx.Button(panel, label="执行计算", pos=(200,100),size=(90,25))
        vbox.Add(exebtn, proportion=0)
        exebtn.Bind(wx.EVT_BUTTON,self.OnExecal)

        statusBar = self.CreateStatusBar()
        statusBar.SetFieldsCount(1)
        statusBar.SetStatusText("源文件中第一列为水深，第二列为周期，二者中间以空格或制表符分隔", 0)
        panel.SetSizer(vbox)

    def OnWaveLengthExcel(self, event):
        self.DestroyChildren()
        panel2 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(600,400))
        vbox2 = wx.BoxSizer(wx.HORIZONTAL)

        srclabel = wx.StaticText(panel2, pos=(10,10), label='Excel文件路径：')
        vbox2.Add(srclabel, proportion=0, flag=wx.RIGHT, border=10)
        self.excelFileTextCtrl = wx.TextCtrl(panel2, pos=(100, 5), size=(290, 25))
        vbox2.Add(self.excelFileTextCtrl, proportion=1)
        filechoosebtn = wx.Button(panel2, label="选择文件...", pos=(400, 5), size=(90, 25))
        vbox2.Add(filechoosebtn, proportion=0)
        filechoosebtn.Bind(wx.EVT_BUTTON, self.OnChooseExcelFile)

        wavedeeplabel = wx.StaticText(panel2, pos=(10,50), label='水深所在的列：')
        vbox2.Add(wavedeeplabel, proportion=0, flag=wx.RIGHT, border=10)
        self.waveDeepTxtCtrl = wx.TextCtrl(panel2, pos=(100,50), size=(100,25))
        vbox2.Add(self.waveDeepTxtCtrl,proportion=1)

        waveperiodlabel = wx.StaticText(panel2, pos=(10, 100), label='周期所在的列：')
        vbox2.Add(waveperiodlabel, proportion=0, flag=wx.RIGHT, border=10)
        self.wavePeriodTxtCtrl = wx.TextCtrl(panel2, pos=(100, 100), size=(100, 25))
        vbox2.Add(self.wavePeriodTxtCtrl, proportion=1)

        wavelengthlabel = wx.StaticText(panel2, pos=(10, 150), label='波长所在的列：')
        vbox2.Add(wavelengthlabel, proportion=0, flag=wx.RIGHT, border=10)
        self.waveLengthTxtCtrl = wx.TextCtrl(panel2, pos=(100, 150), size=(100, 25))
        vbox2.Add(self.waveLengthTxtCtrl, proportion=1)

        exebtn2 = wx.Button(panel2, label="执行计算", pos=(200,200), size=(90,25))
        vbox2.Add(exebtn2, proportion=0)
        exebtn2.Bind(wx.EVT_BUTTON, self.OnExcelExecal)

        statusBar = self.CreateStatusBar()
        statusBar.SetFieldsCount(1)
        statusBar.SetStatusText("Excel文件可以支持多个sheet页，但水深，周期所在的列必须一致：水深，周期，波长所在的列请填字母", 0)
        panel2.SetSizer(vbox2)


    def OnOpenSrcDir(self, event):
        dlg = wx.DirDialog(
            self, message="选择源文件所在目录",
            defaultPath="",
            style=wx.DD_DEFAULT_STYLE
        )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.sourceDirTextCtrl.SetValue(path)
        dlg.Destroy()

    def OnOpenDestDir(self, event):
        dlg = wx.DirDialog(
            self, message="选择结果数据保存目录",
            defaultPath="",
            style=wx.DD_DEFAULT_STYLE
        )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.destDirTextCtrl.SetValue(path)
        dlg.Destroy()

    def OnExecal(self, event):
        sourcedir = self.sourceDirTextCtrl.GetValue()
        destdir = self.destDirTextCtrl.GetValue()
        filehandler = FileHandler.FileHandler()
        filehandler.BatchTxtCal(srcDir=sourcedir, destdir=destdir)
        dlg = wx.MessageDialog(self, message="计算成功", caption="Message",style=wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnChooseExcelFile(self, event):
        dlg = wx.FileDialog(
            self, message="选择水深周期Excel文件",
            defaultFile="",
            wildcard=wildcard1,
            style= wx.OPEN | wx.CHANGE_DIR
        )

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.excelFileTextCtrl.SetValue(path)
        dlg.Destroy()


    def OnExcelExecal(self, event):
        excelfile = self.excelFileTxtCtrl.GetValue()
        deepcolno = self.waveDeepTxtCtrl.GetValue()
        periodcolno = self.wavePeriodTxtCtrl.GetValue()
        lengthcolno = self.waveLengthTxtCtrl.GetValue()
        filehandler = FileHandler.FileHandler()
        filehandler.BatchExcelCal(fileName=excelfile, deepCol = deepcolno, periodCol=periodcolno, lengthCol=lengthcolno)
        dlg = wx.MessageDialog(self, message='计算成功', caption='Message', style=wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, '模型计算')
        frame.Show(True)
        return True

def main():
    app = MyApp(0)
    app.MainLoop()

if __name__ == '__main__':
    main()
