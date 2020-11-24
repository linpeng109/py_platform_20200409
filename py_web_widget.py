import datetime
import os

from PySide2.QtWebEngineWidgets import QWebEngineSettings, QWebEngineView


class WebEngineView(QWebEngineView):

    def __init__(self, tabWidget, config, logger):
        super(WebEngineView, self).__init__()
        self.config = config
        self.logger = logger
        self.tabWidget = tabWidget
        self.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)  # 支持视频播放
        # self.settings().setAttribute(QWebEngineSettings.SpatialNavigationEnabled, True)  # 支持视频播放
        self.page().windowCloseRequested.connect(self.on_windowCloseRequested)  # 页面关闭请求
        self.page().profile().downloadRequested.connect(self.on_downloadRequested)  # 页面下载请求

    #  支持页面关闭请求
    def on_windowCloseRequested(self):
        the_index = self.mainwindow.tabWidget.currentIndex()
        self.mainwindow.tabWidget.removeTab(the_index)

    #  支持页面下载按钮
    def on_downloadRequested(self, downloadItem):
        if downloadItem.isFinished() == False and downloadItem.state() == 0:
            # 生成文件存储地址
            the_filename = downloadItem.url().fileName()
            if len(the_filename) == 0 or "." not in the_filename:
                cur_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                the_filename = "下载文件" + cur_time + ".xls"
            the_sourceFile = os.path.join(os.getcwd(), the_filename)

            # 下载文件
            # downloadItem.setSavePageFormat(QWebEngineDownloadItem.CompleteHtmlSaveFormat)
            downloadItem.setPath(the_sourceFile)
            downloadItem.accept()
            downloadItem.finished.connect(self.on_downloadfinished)

    #  下载结束触发函数
    def on_downloadfinished(self):
        js_string = '''
        alert("下载成功，请到软件同目录下，查找下载文件！"); 
        '''
        self.page().runJavaScript(js_string)

    # 重载QWebEnginView的createwindow()函数
    def createWindow(self, QWebEnginePage_WebWindowType):
        new_webview = WebEngineView(self.tabWidget, config=self.config, logger=self.logger)
        self.tabWidget.addTabItem(new_webview, '新页面')
        return new_webview
