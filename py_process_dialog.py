from PySide2.QtWidgets import QProgressDialog


class ProcessDialog(QProgressDialog):
    def __init__(self):
        super(ProcessDialog, self).__init__()
