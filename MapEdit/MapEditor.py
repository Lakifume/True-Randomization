import json
import sys
from enum import Enum
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

TILEWIDTH = 25
TILEHEIGHT = 15
OUTLINE = 3

KEY_METADATA = 1

area_color = [
    "#000080",
    "#9a6324",
    "#999999",
    "#a4cc3b",
    "#c6c087",
    "#f58231",
    "#911eb4",
    "#469990",
    "#1717e5",
    "#800000",
    "#4363d8",
    "#e5cb17",
    "#808000",
    "#3cb44b",
    "#f032e6",
    "#000000",
    "#e6194b",
    "#3ec7e6",
    "#666666"
]

music_id = []
music_name = []
play_id = []
play_name = []
restrictions = False

with open("Data\\BossRooms.json", "r") as file_reader:
    boss_room = json.load(file_reader)
    
with open("Data\\ConnectedRooms.json", "r") as file_reader:
    connected_room = json.load(file_reader)

with open("Data\\MusicTranslation.json", "r") as file_reader:
    music_translate = json.load(file_reader)

with open("Data\\PlayTranslation.json", "r") as file_reader:
    play_translate = json.load(file_reader)

for i in music_translate:
    music_id.append(i["Value"]["MusicId"])
    music_name.append(i["Value"]["MusicName"])

for i in play_translate:
    play_id.append(i["Value"]["PlayId"])
    play_name.append(i["Value"]["PlayName"])

class Direction(Enum):
    LEFT         = 0x0001
    BOTTOM       = 0x0002
    RIGHT        = 0x0004
    TOP          = 0x0008
    LEFT_BOTTOM  = 0x0010
    RIGHT_BOTTOM = 0x0020
    LEFT_TOP     = 0x0040
    RIGHT_TOP    = 0x0080
    TOP_LEFT     = 0x0100
    TOP_RIGHT    = 0x0200
    BOTTOM_RIGHT = 0x0400
    BOTTOM_LEFT  = 0x0800

class Room:
    def __init__(self, name, area, same_room, out_of_map, room_type, room_path, consider_left, consider_right, consider_top, consider_bottom, width, height, offset_x, offset_z, door_flag, no_traverse, music, play):
        self.name = name
        self.area = area
        self.same_room = same_room
        self.out_of_map = out_of_map
        self.room_type = room_type
        self.room_path = room_path
        self.consider_left = consider_left
        self.consider_right = consider_right
        self.consider_top = consider_top
        self.consider_bottom = consider_bottom
        self.width = width
        self.height = height
        self.offset_x = offset_x
        self.offset_z = offset_z
        self.door_flag = door_flag
        self.no_traverse = no_traverse
        self.music = music
        self.play = play
        
class Door:
    def __init__(self, x_block, z_block, direction_part):
        self.x_block = x_block
        self.z_block = z_block
        self.direction_part = direction_part
        
class Void:
    def __init__(self, x_block, z_block):
        self.x_block = x_block
        self.z_block = z_block
        
class RoomItem(QGraphicsRectItem):
    def __init__(self, data, outline, fill, opacity, can_move, group_list, room_list, metadata=None, parent=None):
        super().__init__(0, 0, data.width, data.height, parent)
        self.setPos(data.offset_x, data.offset_z)
        self.setData(KEY_METADATA, metadata)
        self.setCursor(Qt.PointingHandCursor)
        
        self.data = data
        self.fill = fill
        self.opacity = opacity
        self.can_move = can_move
        self.group_list = group_list
        self.room_list = room_list
        
        self.setPen(outline)
        self.setBrush(QColor(fill[:1] + opacity + fill[1:]))

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        for i in self.scene().selectedItems():
            if restrictions:
                for e in i.group_list:
                    self.room_list[e].setSelected(1)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        for i in self.scene().selectedItems():
            self.apply_round(i)
    
    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        if not self.data.out_of_map:
            for i in self.room_list:
                if i.data.area == self.data.area:
                    i.setSelected(True)

    def apply_round(self, item):
        x = round(item.pos().x() / TILEWIDTH) * TILEWIDTH
        y = round(item.pos().y() / TILEHEIGHT) * TILEHEIGHT
        if item.data.name == "m09TRN_002" and y < 0 and restrictions:
            item.setPos(x, 0)
        else:
            item.setPos(x, y)

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.reset()
        
    def initUI(self):
        self.setStyleSheet("QWidget{background:transparent; color: #ffffff; font-family: Cambria; font-size: 18px}"
        + "QGraphicsView{border: 0px}"
        + "QMenuBar{background-color: #21222e}"
        + "QMenu{background-color: #21222e}" 
        + "QComboBox{background-color: #21222e}"
        + "QMessageBox{background-color: #21222e}"
        + "QDialog{background-color: #21222e}"
        + "QPushButton{background-color: #21222e}"
        + "QListWidget{background-color: #21222e}"
        + "QToolTip{border: 0px; background-color: #21222e; color: #ffffff; font-family: Cambria; font-size: 18px}")
        
        #Graphics
        
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)
        self.scene.selectionChanged.connect(self.selection_event)
        
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff);
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff);
        self.view.setDragMode(QGraphicsView.RubberBandDrag)
        self.view.scale(1, -1)
        self.current_zoom = 1
        self.setCentralWidget(self.view)
        
        #Menu
        
        bar = self.menuBar()
        file_bar = bar.addMenu("File")
        edit_bar = bar.addMenu("Edit")
        view_bar = bar.addMenu("View")
        tool_bar = bar.addMenu("Tools")
        help_bar = bar.addMenu("Help")

        open = QAction("Open", self)
        open.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_O))
        open.triggered.connect(self.open_file)
        file_bar.addAction(open)

        self.save = QAction("Save", self)
        self.save.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_S))
        self.save.triggered.connect(self.save_file)
        file_bar.addAction(self.save)

        save_as = QAction("Save as", self)
        save_as.setShortcut(QKeySequence(Qt.SHIFT + Qt.CTRL + Qt.Key_S))
        save_as.triggered.connect(self.save_file_as)
        file_bar.addAction(save_as)

        reset = QAction("Reset", self)
        reset.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_R))
        reset.triggered.connect(self.reset)
        file_bar.addAction(reset)
        
        self.use_restr = QAction("Use restrictions", self, checkable = True)
        self.use_restr.setShortcut(QKeySequence(Qt.Key_1))
        self.use_restr.triggered.connect(self.use_restr_action)
        self.use_restr.setChecked(True)
        edit_bar.addAction(self.use_restr)
        
        self.show_out = QAction("Show hidden rooms", self, checkable = True)
        self.show_out.setShortcut(QKeySequence(Qt.Key_2))
        self.show_out.triggered.connect(self.show_out_action)
        view_bar.addAction(self.show_out)
        
        self.show_name = QAction("Show room names", self, checkable = True)
        self.show_name.setShortcut(QKeySequence(Qt.Key_3))
        self.show_name.triggered.connect(self.show_name_action)
        view_bar.addAction(self.show_name)
        
        self.room_search = QAction("Room Search", self, checkable = True)
        self.room_search.setShortcut(QKeySequence(Qt.Key_4))
        self.room_search.triggered.connect(self.room_search_action)
        tool_bar.addAction(self.room_search)
        
        self.key_location = QAction("Key Locations", self, checkable = True)
        self.key_location.setShortcut(QKeySequence(Qt.Key_5))
        self.key_location.triggered.connect(self.key_location_action)
        tool_bar.addAction(self.key_location)
        
        how_to = QAction("How to use", self)
        how_to.triggered.connect(self.how_to)
        help_bar.addAction(how_to)
        
        guidelines = QAction("Map guidelines", self)
        guidelines.triggered.connect(self.guidelines)
        help_bar.addAction(guidelines)
        
        restrictions = QAction("Boss restrictions", self)
        restrictions.triggered.connect(self.restrictions)
        help_bar.addAction(restrictions)
        
        #Buttons
        
        reverse = QPushButton()
        reverse.setShortcut(QKeySequence(Qt.Key_D))
        reverse.setIcon(QIcon("Data\\reverse_icon.png"))
        reverse.setToolTip("Toggle save/warp entrance direction\nShortcut: D")
        reverse.clicked.connect(self.reverse)
        reverse.setFixedSize(50, 30)
        
        swap = QPushButton()
        swap.setShortcut(QKeySequence(Qt.Key_T))
        swap.setIcon(QIcon("Data\\swap_icon.png"))
        swap.setToolTip("Toggle save/warp room type\nShortcut: T")
        swap.clicked.connect(self.swap)
        swap.setFixedSize(50, 30)
        
        ignore_left = QPushButton()
        ignore_left.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_Left))
        ignore_left.setIcon(QIcon("Data\\ignore_left_icon.png"))
        ignore_left.setToolTip("Ignore left transitions\nShortcut: Ctrl + Left")
        ignore_left.clicked.connect(self.ignore_left)
        ignore_left.setFixedSize(50, 30)
        
        ignore_right = QPushButton()
        ignore_right.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_Right))
        ignore_right.setIcon(QIcon("Data\\ignore_right_icon.png"))
        ignore_right.setToolTip("Ignore right transitions\nShortcut: Ctrl + Right")
        ignore_right.clicked.connect(self.ignore_right)
        ignore_right.setFixedSize(50, 30)
        
        ignore_top = QPushButton()
        ignore_top.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_Up))
        ignore_top.setIcon(QIcon("Data\\ignore_top_icon.png"))
        ignore_top.setToolTip("Ignore top transitions\nShortcut: Ctrl + Up")
        ignore_top.clicked.connect(self.ignore_top)
        ignore_top.setFixedSize(50, 30)
        
        ignore_bottom = QPushButton()
        ignore_bottom.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_Down))
        ignore_bottom.setIcon(QIcon("Data\\ignore_bottom_icon.png"))
        ignore_bottom.setToolTip("Ignore bottom transitions\nShortcut: Ctrl + Down")
        ignore_bottom.clicked.connect(self.ignore_bottom)
        ignore_bottom.setFixedSize(50, 30)
        
        self.zoom_in = QPushButton()
        self.zoom_in.setShortcut(QKeySequence(Qt.ALT + Qt.Key_Up))
        self.zoom_in.setIcon(QIcon("Data\\in_icon.png"))
        self.zoom_in.setToolTip("Zoom in\nShortcut: Alt + Up")
        self.zoom_in.clicked.connect(self.zoom_in_action)
        self.zoom_in.setFixedSize(50, 30)
        
        self.zoom_out = QPushButton()
        self.zoom_out.setShortcut(QKeySequence(Qt.ALT + Qt.Key_Down))
        self.zoom_out.setIcon(QIcon("Data\\out_icon.png"))
        self.zoom_out.setToolTip("Zoom out\nShortcut: Alt + Down")
        self.zoom_out.clicked.connect(self.zoom_out_action)
        self.zoom_out.setFixedSize(50, 30)
        self.zoom_out.setEnabled(False)
        
        #Labels
        
        self.lock_label = QLabel()
        self.lock_label.setPixmap(QPixmap("Data\\lock_icon.png"))
        
        #DropDownLists
        
        self.key_drop_down = QComboBox()
        self.key_drop_down.currentIndexChanged.connect(self.key_drop_down_change)
        self.key_drop_down.setVisible(False)
        retain = self.key_drop_down.sizePolicy()
        retain.setRetainSizeWhenHidden(True)
        self.key_drop_down.setSizePolicy(retain)
        
        self.music_drop_down = QComboBox()
        self.music_drop_down.addItems(music_name)
        self.music_drop_down.currentIndexChanged.connect(self.music_drop_down_change)
        self.music_drop_down.setVisible(False)
        retain = self.music_drop_down.sizePolicy()
        retain.setRetainSizeWhenHidden(True)
        self.music_drop_down.setSizePolicy(retain)
        
        self.play_drop_down = QComboBox()
        self.play_drop_down.addItems(play_name)
        self.play_drop_down.currentIndexChanged.connect(self.play_drop_down_change)
        self.play_drop_down.setVisible(False)
        retain = self.play_drop_down.sizePolicy()
        retain.setRetainSizeWhenHidden(True)
        self.play_drop_down.setSizePolicy(retain)
        
        #ListWidgets
        
        self.room_search_list = QListWidget()
        self.room_search_list.itemClicked.connect(self.room_search_list_change)
        self.room_search_list.setVisible(False)
        retain = self.room_search_list.sizePolicy()
        retain.setRetainSizeWhenHidden(True)
        self.room_search_list.setSizePolicy(retain)
        
        #Layouts
        
        hbox_top = QHBoxLayout()
        hbox_top.addWidget(self.lock_label)
        hbox_top.addWidget(self.key_drop_down)
        hbox_top.addStretch(1)
        hbox_top.addWidget(self.music_drop_down)
        hbox_top.addWidget(self.play_drop_down)
        
        hbox_center = QHBoxLayout()
        hbox_center.addStretch(1)
        hbox_center.addWidget(self.room_search_list)
        
        hbox_bottom = QHBoxLayout()
        hbox_bottom.addWidget(reverse)
        hbox_bottom.addWidget(swap)
        hbox_bottom.addStretch(1)
        hbox_bottom.addWidget(ignore_left)
        hbox_bottom.addWidget(ignore_right)
        hbox_bottom.addWidget(ignore_top)
        hbox_bottom.addWidget(ignore_bottom)
        hbox_bottom.addStretch(1)
        hbox_bottom.addWidget(self.zoom_in)
        hbox_bottom.addWidget(self.zoom_out)
        
        vbox = QVBoxLayout()
        vbox.addLayout(hbox_top)
        vbox.addLayout(hbox_center)
        vbox.addLayout(hbox_bottom)
        
        #Window
        
        self.view.setLayout(vbox)
        self.setMinimumSize(1200, 700)
        self.showMaximized()
        self.setWindowIcon(QIcon("Data\\icon.png"))
        
        #Background
        
        background = QPixmap("Data\\background.png")
        palette = QPalette()
        palette.setBrush(QPalette.Window, background)
        self.show()
        self.setPalette(palette)
    
    def open_file(self):
        self.path = (QFileDialog.getOpenFileName(parent=self, caption="Open", dir="Custom", filter="*.json"))[0]
        if self.path:
            self.string = self.path
            self.title_string = " (" + self.string + ")"
            self.load_from_json(self.string)
            self.direct_save = True

    def save_file(self):
        if self.direct_save:
            self.save_to_json(self.string)
        else:
            self.save_file_as()

    def save_file_as(self):
        self.path = (QFileDialog.getSaveFileName(parent=self, caption="Save as", dir="Custom", filter="*.json"))[0]
        if self.path:
            self.string = self.path
            self.title_string = " (" + self.string + ")"
            self.save_to_json(self.string)
            self.direct_save = True

    def reset(self):
        self.title_string = ""
        self.load_from_json("Data\\Content\\PB_DT_RoomMaster.json")
        self.direct_save = False
    
    def use_restr_action(self):
        global restrictions
        if self.use_restr.isChecked():
            restrictions = True
            self.lock_label.setPixmap(QPixmap("Data\\lock_icon.png"))
        else:
            restrictions = False
            self.lock_label.setPixmap(QPixmap("Data\\unlock_icon.png"))
        for i in self.room_list:
            if not i.can_move:
                if restrictions:
                    i.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)
                else:
                    i.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable | QGraphicsItem.ItemIsMovable)
            else:
                i.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable | QGraphicsItem.ItemIsMovable)
    
    def show_out_action(self):
        for i in self.room_list:
            if i.data.out_of_map:
                item = self.room_search_list.findItems(i.data.name, Qt.MatchExactly)[0]
                if self.show_out.isChecked():
                    i.setVisible(True)
                    item.setFlags(item.flags() | Qt.ItemIsSelectable)
                else:
                    i.setVisible(False)
                    item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
    
    def show_name_action(self):
        for i in self.room_list:
            if self.show_name.isChecked():
                for e in i.childItems():
                    if type(e) == QGraphicsTextItem:
                        e.setVisible(True)
                    if type(e) == QGraphicsPixmapItem:
                        e.setVisible(False)
            else:
                for e in i.childItems():
                    if type(e) == QGraphicsTextItem:
                        e.setVisible(False)
                    if type(e) == QGraphicsPixmapItem:
                        e.setVisible(True)
    
    def key_location_action(self):
        if self.key_location.isChecked():
            try:
                with open("Key\\Key.json", "r") as file_reader:
                    self.key_log = json.load(file_reader)
            except FileNotFoundError:
                box = QMessageBox(self)
                box.setWindowTitle("Error")
                box.setIcon(QMessageBox.Critical)
                box.setText("No key log found.")
                box.exec()
                self.key_location.setChecked(False)
                return
            self.room_search.setChecked(False)
            self.room_search_action()
            self.key_drop_down.clear()
            for i in self.key_log:
                self.key_drop_down.addItem(i["Key"])
            self.key_drop_down.setCurrentIndex(0)
            self.key_drop_down_change(0)
            self.key_drop_down.setVisible(True)
        else:
            self.key_drop_down_change(0)
            self.key_drop_down.setVisible(False)
    
    def room_search_action(self):
        if self.room_search.isChecked():
            self.key_location.setChecked(False)
            self.key_location_action()
            self.room_search_list.setCurrentItem(self.room_search_list.item(0))
            self.room_search_list_change(self.room_search_list.item(0))
            self.room_search_list.setVisible(True)
        else:
            self.room_search_list_change(self.room_search_list.item(0))
            self.room_search_list.setVisible(False)
    
    def how_to(self):
        box = QMessageBox(self)
        box.setWindowTitle("How to use")
        box.setText("This editor allows you to fully customize the layout of the game's map. You can click and drag each room to change its location on the grid.\nSave your creations to the Custom folder for them to be picked by the randomizer.\n\nTo give the player a specific key shard at the start of a randomizer for your map simply append a suffix to its filename:\n\n_J for Double Jump\n_I for Invert\n_S for Deep Sinker\n_H for High Jump\n_R for Reflector Ray\n_D for Dimension Shift\n\nYou can submit your own layout creations to me on Discord (Lakifume#4066) if you want them to be added as presets in the main download of the randomizer.")
        box.exec()
    
    def guidelines(self):
        box = QMessageBox(self)
        box.setWindowTitle("Map guidelines")
        box.setText("Here are some tips that will help you build maps that are fun to play on:\n\nAcceptable:\n\n-having a non-downward entrance lead to an empty space\n-connecting a standard room to a transition room directly (except for m03ENT1201)\n-leaving the galleon untouched due to its complexity (note the 2 different heights of sideways entrances)\n\nPreferable:\n\n-making use of as many rooms as possible\n-connecting as many entrances as possible\n-roughly keeping the whole map within the canvas size\n-keeping each area separated using transition rooms\n-ensuring that boss rooms are placed relatively close to a save/warp point\n\nNecessary:\n\n-having the \"Use restrictions\" option enabled while building your map\n-not having any downward entrance lead to an empty space\n-not overlapping any rooms except for the semi-transparent ones\n-not putting any empty entrance that does not ignore transitions right against the side of another room")
        box.exec()
    
    def restrictions(self):
        label = QLabel()
        label.setPixmap(QPixmap("Data\\boss_req.png"))
        layout = QVBoxLayout()
        layout.addWidget(label)
        box = QDialog(self)
        box.setLayout(layout)
        box.setWindowTitle("Boss restrictions")
        box.exec()
    
    def reverse(self):
        for i in self.scene.selectedItems():
            if i.data.room_type == "ERoomType::Save" or i.data.room_type == "ERoomType::Warp":
                if i.data.room_path == "ERoomPath::Left":
                    i.data.room_path = "ERoomPath::Right"
                    i.childItems()[5].setVisible(False)
                    i.childItems()[6].setVisible(True)
                elif i.data.room_path == "ERoomPath::Right":
                    i.data.room_path = "ERoomPath::Both"
                    i.childItems()[5].setVisible(True)
                    i.childItems()[6].setVisible(True)
                elif i.data.room_path == "ERoomPath::Both":
                    i.data.room_path = "ERoomPath::Left"
                    i.childItems()[5].setVisible(True)
                    i.childItems()[6].setVisible(False)
    
    def swap(self):
        for i in self.scene.selectedItems():
            if i.data.room_type == "ERoomType::Save":
                i.data.room_type = "ERoomType::Warp"
                i.childItems()[4].setPixmap("Data\\warp.png")
            elif i.data.room_type == "ERoomType::Warp":
                i.data.room_type = "ERoomType::Save"
                i.childItems()[4].setPixmap("Data\\save.png")
    
    def ignore_left(self):
        for i in self.scene.selectedItems():
            if i.data.consider_left:
                i.data.consider_left = False
                i.childItems()[0].setVisible(True)
            else:
                i.data.consider_left = True
                i.childItems()[0].setVisible(False)
    
    def ignore_right(self):
        for i in self.scene.selectedItems():
            if i.data.consider_right:
                i.data.consider_right = False
                i.childItems()[1].setVisible(True)
            else:
                i.data.consider_right = True
                i.childItems()[1].setVisible(False)
    
    def ignore_top(self):
        for i in self.scene.selectedItems():
            if i.data.consider_top:
                i.data.consider_top = False
                i.childItems()[2].setVisible(True)
            else:
                i.data.consider_top = True
                i.childItems()[2].setVisible(False)
    
    def ignore_bottom(self):
        for i in self.scene.selectedItems():
            if i.data.consider_bottom:
                i.data.consider_bottom = False
                i.childItems()[3].setVisible(True)
            else:
                i.data.consider_bottom = True
                i.childItems()[3].setVisible(False)
    
    def zoom_in_action(self):
        self.view.scale(2, 2)
        self.current_zoom += 1
        self.zoom_out.setEnabled(True)
        if self.current_zoom >= 4:
            self.zoom_in.setEnabled(False)
        else:
            self.zoom_in.setEnabled(True)
    
    def zoom_out_action(self):
        self.view.scale(0.5, 0.5)
        self.current_zoom -= 1
        self.zoom_in.setEnabled(True)
        if self.current_zoom <= 1:
            self.zoom_out.setEnabled(False)
        else:
            self.zoom_out.setEnabled(True)
    
    def key_drop_down_change(self, index):
        for i in self.room_list:
            if not self.key_location.isChecked() or i.data.name in self.key_log[index]["Value"]["RoomList"]:
                i.setBrush(QColor(i.fill[:1] + i.opacity + i.fill[1:]))
                for e in i.childItems():
                    if type(e) == QGraphicsRectItem:
                        e.setBrush(QColor(i.fill))
            else:
                i.setBrush(QColor("#000000"))
                for e in i.childItems():
                    if type(e) == QGraphicsRectItem:
                        e.setBrush(QColor("#000000"))
    
    def music_drop_down_change(self, index):
        for i in self.scene.selectedItems():
            i.data.music = music_id[index]
    
    def play_drop_down_change(self, index):
        for i in self.scene.selectedItems():
            i.data.play = play_id[index]
    
    def room_search_list_change(self, item):
        for i in self.room_list:
            if not self.room_search.isChecked() or i.data.name == item.text():
                i.setBrush(QColor(i.fill[:1] + i.opacity + i.fill[1:]))
                for e in i.childItems():
                    if type(e) == QGraphicsRectItem:
                        e.setBrush(QColor(i.fill))
            else:
                i.setBrush(QColor("#000000"))
                for e in i.childItems():
                    if type(e) == QGraphicsRectItem:
                        e.setBrush(QColor("#000000"))
    
    def change_title(self, suffix):
        self.setWindowTitle("Map Editor" + self.title_string + suffix)
    
    def selection_event(self):
        if not self.unsaved:
            self.change_title("*")
            self.unsaved = True
        for i in self.scene.selectedItems():
            i.setZValue(73 - (i.data.width/TILEWIDTH)*(i.data.height/TILEHEIGHT))
        for i in self.room_list:
            if not i.isSelected():
                i.setZValue(0 - (i.data.width/TILEWIDTH)*(i.data.height/TILEHEIGHT))
        if self.scene.selectedItems():
            self.music_drop_down.setVisible(True)
            self.play_drop_down.setVisible(True)
            if len(self.scene.selectedItems()) == 1:
                self.music_drop_down.setCurrentIndex(music_id.index(self.scene.selectedItems()[0].data.music))
                self.play_drop_down.setCurrentIndex(play_id.index(self.scene.selectedItems()[0].data.play))
        else:
            self.music_drop_down.setVisible(False)
            self.play_drop_down.setVisible(False)
    
    def load_from_json(self, filename):
        self.unsaved = True
        
        self.scene.clear()
        QApplication.processEvents()
        
        self.room_search_list.clear()
        self.room_list = []
        self.change_title("")
        
        with open(filename, "r") as file_reader:
            self.content = json.load(file_reader)
        self.draw_map()
        self.use_restr_action()
        self.show_name_action()
        if self.key_location.isChecked():
            self.key_location_action()
        if self.room_search.isChecked():
            self.room_search_action()
        self.selection_event()
        
        self.unsaved = False
        QApplication.processEvents()
        
        self.show_out_action()
    
    def save_to_json(self, filename):
        self.update_offsets()
        self.same_check()
        self.adj_check()
        with open(filename, "w") as file_writer:
            file_writer.write(json.dumps(self.content, indent=2))
        self.change_title("")
        self.unsaved = False
    
    def convert_json_to_room(self, json):
        name = json["Key"]
        area = json["Value"]["AreaID"]
        same_room = json["Value"]["SameRoom"]
        out_of_map = json["Value"]["OutOfMap"]
        room_type = json["Value"]["RoomType"]
        room_path = json["Value"]["RoomPath"]
        consider_left = json["Value"]["ConsiderLeft"]
        consider_right = json["Value"]["ConsiderRight"]
        consider_top = json["Value"]["ConsiderTop"]
        consider_bottom = json["Value"]["ConsiderBottom"]
        width = json["Value"]["AreaWidthSize"] * TILEWIDTH
        height = json["Value"]["AreaHeightSize"] * TILEHEIGHT
        offset_x = round(json["Value"]["OffsetX"]/12.6) * TILEWIDTH
        offset_z = round(json["Value"]["OffsetZ"]/7.2) * TILEHEIGHT 
        door_flag = self.convert_flag_to_door(json["Value"]["DoorFlag"], round(width/TILEWIDTH))
        no_traverse = self.convert_no_traverse_to_block(json["Value"]["NoTraverse"], round(width/TILEWIDTH))
        music = json["Value"]["BgmID"]
        play = json["Value"]["BgmType"]
        
        room = Room(name, area, same_room, out_of_map, room_type, room_path, consider_left, consider_right, consider_top, consider_bottom, width, height, offset_x, offset_z, door_flag, no_traverse, music, play)
        return room
    
    def convert_flag_to_door(self, door_flag, width):
        door_list = []
        for i in range(0, len(door_flag), 2):
            tile_index = door_flag[i]
            direction = door_flag[i+1]
            tile_index -= 1
            if width == 0:
                x_block = tile_index
                z_block = 0
            else:
                x_block = tile_index % width
                z_block = tile_index // width
            for direction_part in Direction:
                if (direction & direction_part.value) != 0:
                    door = Door(x_block, z_block, direction_part)
                    door_list.append(door)
        return door_list
    
    def convert_no_traverse_to_block(self, no_traverse, width):
        void_list = []
        for i in range(len(no_traverse)):
            tile_index = no_traverse[i]
            tile_index -= 1
            if width == 0:
                x_block = tile_index
                z_block = 0
            else:
                x_block = tile_index % width
                z_block = tile_index // width
                void = Void(x_block, z_block)
                void_list.append(void)
        return void_list
    
    def convert_group_to_index(self, group_list):
        new_group_list = []
        for i in range(615):
            for e in group_list:
                if self.content[i]["Key"] == e:
                    new_group_list.append(i)
        return new_group_list
    
    def draw_map(self):
        for i in self.content:
            data = self.convert_json_to_room(i)
            group_list = []
            can_move = True
            self.room_search_list.addItem(data.name)
            
            if data.width == 0:
                data.width = TILEWIDTH/2
            if data.height == 0:
                data.height = TILEHEIGHT/2
            
            if data.area == "EAreaID::None":
                fill = area_color[18]
            else:
                fill = area_color[int(data.area[10:12]) - 1]
            
            outline = QPen("#ffffff")
            outline.setWidth(OUTLINE)
            outline.setJoinStyle(Qt.MiterJoin)
            
            origin_horizontal = self.scene.addLine(-6.0, 0.0, 6.0, 0.0)
            origin_horizontal.setPen(outline)
            origin_vertical = self.scene.addLine(0.0, TILEHEIGHT/2 - 1.5, 0.0, 0 - (TILEHEIGHT/2 - 1.5))
            origin_vertical.setPen(outline)
            
            for e in connected_room:
                for o in e["Value"]["RoomId"]:
                    if data.name == o:
                        group_list = e["Value"]["RoomId"]
                        can_move = e["Value"]["CanMove"]
                        break
            
            if data.room_type == "ERoomType::Load" or data.name == "m01SIP_022" or data.name == "m02VIL_000" or data.name == "m02VIL_099" or data.name == "m02VIL(101)" or data.name == "m18ICE_020":
                opacity = "80"
            else:
                opacity = "ff"
            
            room = RoomItem(data, outline, fill, opacity, can_move, self.convert_group_to_index(group_list), self.room_list)
            self.scene.addItem(room)
            self.room_list.append(room)
            
            outline.setColor("#00000000")
            
            #IgnoreDirection
            
            if not data.out_of_map:
                pen = QPen("#555555")
                pen.setWidth(2)
                line = self.scene.addLine(2.5, 2.5, 2.5, data.height - 2.5)
                line.setPen(pen)
                line.setParentItem(room)
                if data.consider_left:
                    line.setVisible(False)
                line = self.scene.addLine(data.width - 2.5, 2.5, data.width - 2.5, data.height - 2.5)
                line.setPen(pen)
                line.setParentItem(room)
                if data.consider_right:
                    line.setVisible(False)
                line = self.scene.addLine(2.5, data.height - 2.5, data.width - 2.5, data.height - 2.5)
                line.setPen(pen)
                line.setParentItem(room)
                if data.consider_top:
                    line.setVisible(False)
                line = self.scene.addLine(2.5, 2.5, data.width - 2.5, 2.5)
                line.setPen(pen)
                line.setParentItem(room)
                if data.consider_bottom:
                    line.setVisible(False)
            
            #Icons
            
            if data.room_type == "ERoomType::Save":
                icon = self.scene.addPixmap(QPixmap("Data\\save.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(data.width/2 - 6, data.height/2 + TILEHEIGHT/2 - 1.5)
                icon.setParentItem(room)
            if data.room_type == "ERoomType::Warp":
                icon = self.scene.addPixmap(QPixmap("Data\\warp.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(data.width/2 - 6, data.height/2 + TILEHEIGHT/2 - 1.5)
                icon.setParentItem(room)
            if data.name in boss_room["Value"]["RoomId"]:
                icon = self.scene.addPixmap(QPixmap("Data\\boss.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                if data.name == data.name == "m07LIB_011":
                    icon.setPos(data.width/2 - 6, data.height - 1.5)
                else:
                    icon.setPos(data.width/2 - 6, data.height/2 + TILEHEIGHT/2 - 1.5)
                icon.setParentItem(room)
            if int(data.name[1:3]) == 88:
                icon = self.scene.addPixmap(QPixmap("Data\\key.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(data.width/2 - 6, data.height/2 + TILEHEIGHT/2 - 1.5)
                icon.setParentItem(room)
            if data.name == "m01SIP_000":
                icon = self.scene.addPixmap(QPixmap("Data\\start.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(data.width/2 - 6, data.height/2 + TILEHEIGHT/2 - 1.5)
                icon.setParentItem(room)
            if data.name == "m04GDN_001" or data.name == "m10BIG_000":
                icon = self.scene.addPixmap(QPixmap("Data\\portal.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(data.width/2 - 6, data.height/2 + TILEHEIGHT/2 - 1.5)
                icon.setParentItem(room)
            if data.name == "m05SAN_006":
                icon = self.scene.addPixmap(QPixmap("Data\\barber.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(data.width/2 - 6, data.height/2 + TILEHEIGHT/2 - 1.5)
                icon.setParentItem(room)
            if data.name == "m06KNG_021":
                icon = self.scene.addPixmap(QPixmap("Data\\8bit.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(data.width/2 - 6, data.height/2 + TILEHEIGHT/2 - 1.5)
                icon.setParentItem(room)
            if data.name == "m07LIB_009":
                icon = self.scene.addPixmap(QPixmap("Data\\book.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(data.width/2 - 6, data.height/2 + TILEHEIGHT/2 - 1.5)
                icon.setParentItem(room)
            
            #Key
            
            if data.name == "m03ENT_020" or data.name == "m05SAN_021" or data.name == "m08TWR_019" or data.name == "m15JPN_016" or data.name == "m18ICE_013":
                icon = self.scene.addPixmap(QPixmap("Data\\chest.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(TILEWIDTH/2 - 6, data.height - 1.5)
                icon.setParentItem(room)
            if data.name == "m06KNG_017":
                icon = self.scene.addPixmap(QPixmap("Data\\chest.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(data.width/2 - 6, data.height/2 + TILEHEIGHT/2 - 1.5)
                icon.setParentItem(room)
            if data.name == "m08TWR_019":
                icon = self.scene.addPixmap(QPixmap("Data\\chest.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(data.width/2 - 6, TILEHEIGHT*2 - 1.5)
                icon.setParentItem(room)
            if data.name == "m10BIG_006":
                icon = self.scene.addPixmap(QPixmap("Data\\chest.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(TILEWIDTH*3 + 6, data.height - 1.5)
                icon.setParentItem(room)
            
            #Shard
            
            if data.name == "m02VIL_005" or data.name == "m03ENT_021" or data.name == "m05SAN_000" or data.name == "m11UGD_047" or data.name == "m12SND_026" or data.name == "m13ARC_004":
                icon = self.scene.addPixmap(QPixmap("Data\\shard.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(data.width/2 - 6, data.height/2 + TILEHEIGHT/2 - 1.5)
                icon.setParentItem(room)
            if data.name == "m17RVA_008":
                icon = self.scene.addPixmap(QPixmap("Data\\shard.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(TILEWIDTH/2 - 6, data.height/2 + TILEHEIGHT/2 - 1.5)
                icon.setParentItem(room)
            if data.name == "m07LIB_011":
                icon = self.scene.addPixmap(QPixmap("Data\\shard.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(data.width/2 - 6, TILEHEIGHT - 1.5)
                icon.setParentItem(room)
            
            #Wall
            
            if data.name == "m01SIP_017":
                icon = self.scene.addPixmap(QPixmap("Data\\one_way_left.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(1.5, TILEHEIGHT - 1.5)
                icon.setParentItem(room)
            if data.name == "m03ENT_000":
                icon = self.scene.addPixmap(QPixmap("Data\\spike_opening.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(data.width/2 - 6, TILEHEIGHT*13 - 1.5)
                icon.setParentItem(room)
            if data.name == "m03ENT_007":
                icon = self.scene.addPixmap(QPixmap("Data\\one_way_left.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(data.width - 13.5, TILEHEIGHT - 1.5)
                icon.setParentItem(room)
            if data.name == "m05SAN_003":
                icon = self.scene.addPixmap(QPixmap("Data\\wall_horizontal.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(data.width/2 - 6, TILEHEIGHT*8 + 6)
                icon.setParentItem(room)
            if data.name == "m05SAN_017":
                icon = self.scene.addPixmap(QPixmap("Data\\one_way_left.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(data.width/2 - 1, TILEHEIGHT - 1.5)
                icon.setParentItem(room)
            if data.name == "m05SAN_019" or data.name == "m07LIB_005":
                icon = self.scene.addPixmap(QPixmap("Data\\one_way_down.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(data.width -18.5, TILEHEIGHT - 1.5)
                icon.setParentItem(room)
                if data.name == "m05SAN_019":
                    icon = self.scene.addPixmap(QPixmap("Data\\one_way_left.png"))
                    icon.setTransform(QTransform.fromScale(1, -1))
                    icon.setPos(TILEWIDTH - 23.5, TILEHEIGHT - 1.5)
                    icon.setParentItem(room)
            if data.name == "m05SAN_021" or data.name == "m07LIB_023":
                icon = self.scene.addPixmap(QPixmap("Data\\one_way_right.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(data.width - 13.5, data.height - TILEHEIGHT*2 - 1.5)
                icon.setParentItem(room)
            if data.name == "m06KNG_013":
                icon = self.scene.addPixmap(QPixmap("Data\\one_way_right.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(data.width - 13.5, TILEHEIGHT - 1.5)
                icon.setParentItem(room)
            if data.name == "m06KNG_015" or data.name == "m07LIB_029":
                icon = self.scene.addPixmap(QPixmap("Data\\one_way_up.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(data.width/2 - 6, data.height - 1.5)
                icon.setParentItem(room)
            if data.name == "m07LIB_006" or data.name == "m11UGD_045":
                icon = self.scene.addPixmap(QPixmap("Data\\hole.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(data.width/2 - 6, TILEHEIGHT - 1.5)
                icon.setParentItem(room)
            if data.name == "m07LIB_008" or data.name == "m07LIB_014" or data.name == "m11UGD_016" or data.name == "m18ICE_016":
                icon = self.scene.addPixmap(QPixmap("Data\\hole.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(data.width - 8.5, data.height - 1.5)
                icon.setParentItem(room)
            if data.name == "m07LIB_021":
                icon = self.scene.addPixmap(QPixmap("Data\\one_way_down.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(data.width/2 - 6, data.height - 1.5)
                icon.setParentItem(room)
            if data.name == "m07LIB_035" or data.name == "m11UGD_056":
                icon = self.scene.addPixmap(QPixmap("Data\\opening.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(data.width/2 - 6, TILEHEIGHT*3 - 9)
                icon.setParentItem(room)
            if data.name == "m08TWR_009":
                icon = self.scene.addPixmap(QPixmap("Data\\one_way_left.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(data.width - 11.5, TILEHEIGHT*11 - 1.5)
                icon.setParentItem(room)
            if data.name == "m11UGD_015":
                icon = self.scene.addPixmap(QPixmap("Data\\one_way_right.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(data.width/2 - 11, TILEHEIGHT - 1.5)
                icon.setParentItem(room)
            if data.name == "m11UGD_046":
                icon = self.scene.addPixmap(QPixmap("Data\\hole_left.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(1.5, data.height - 1.5)
                icon.setParentItem(room)
            if data.name == "m11UGD_056":
                icon = self.scene.addPixmap(QPixmap("Data\\wall_vertical.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(data.width - 8.5, data.height - 1.5)
                icon.setParentItem(room)
            if data.name == "m15JPN_010" or data.name == "m17RVA_005":
                icon = self.scene.addPixmap(QPixmap("Data\\ceiling_hole.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(data.width - 13.5, data.height - 1.5)
                icon.setParentItem(room)
            if data.name == "m17RVA_003":
                icon = self.scene.addPixmap(QPixmap("Data\\ceiling_hole_right.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(data.width - 13.5, data.height - 1.5)
                icon.setParentItem(room)
            if data.name == "m18ICE_015":
                icon = self.scene.addPixmap(QPixmap("Data\\wall_vertical.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(data.width/2 - 6, TILEHEIGHT - 1.5)
                icon.setParentItem(room)
            
            #Water
            
            if data.name == "m11UGD_021" or data.name == "m11UGD_022" or data.name == "m11UGD_023" or data.name == "m11UGD_024" or data.name == "m11UGD_025" or data.name == "m11UGD_026" or data.name == "m11UGD_044" or data.name == "m11UGD_045":
                for e in range(round(data.width/TILEWIDTH)):
                    for o in range(round(data.height/TILEHEIGHT)):
                        icon = self.scene.addPixmap(QPixmap("Data\\bubble.png"))
                        icon.setTransform(QTransform.fromScale(1, -1))
                        icon.setPos(e*TILEWIDTH + 6, o*TILEHEIGHT + 13.5)
                        icon.setParentItem(room)
            if data.name == "m11UGD_005" or data.name == "m11UGD_036":
                for e in range(round(data.width/TILEWIDTH)):
                    icon = self.scene.addPixmap(QPixmap("Data\\wave.png"))
                    icon.setTransform(QTransform.fromScale(1, -1))
                    icon.setPos(e*TILEWIDTH + 6, 20.5)
                    icon.setParentItem(room)
            if data.name == "m11UGD_019" or data.name == "m11UGD_040":
                for e in range(round(data.width/TILEWIDTH)):
                    icon = self.scene.addPixmap(QPixmap("Data\\wave.png"))
                    icon.setTransform(QTransform.fromScale(1, -1))
                    icon.setPos(e*TILEWIDTH + 6, 28.5)
                    icon.setParentItem(room)
            if data.name == "m11UGD_042" or data.name == "m11UGD_046":
                for e in range(round(data.width/TILEWIDTH)):
                    icon = self.scene.addPixmap(QPixmap("Data\\wave.png"))
                    icon.setTransform(QTransform.fromScale(1, -1))
                    icon.setPos(e*TILEWIDTH + 6, 43.5)
                    icon.setParentItem(room)
            if data.name == "m11UGD_043":
                for e in range(round(data.width/TILEWIDTH)-1):
                    icon = self.scene.addPixmap(QPixmap("Data\\wave.png"))
                    icon.setTransform(QTransform.fromScale(1, -1))
                    icon.setPos(e*TILEWIDTH + 6, 13.5)
                    icon.setParentItem(room)
            
            #NoTraverse
            
            for e in data.no_traverse:
                if data.name == "m11UGD_013":
                    icon = self.scene.addPixmap(QPixmap("Data\\void.png"))
                    icon.setTransform(QTransform.fromScale(1, -1))
                    icon.setPos(e.x_block*TILEWIDTH + 0.5, (e.z_block + 3)*TILEHEIGHT + 4.5)
                elif data.name == "m11UGD_031":
                    icon = self.scene.addPixmap(QPixmap("Data\\void.png"))
                    icon.setTransform(QTransform.fromScale(1, -1))
                    icon.setPos(e.x_block*TILEWIDTH + 0.5, (e.z_block + 4)*TILEHEIGHT + 4.5)
                else:
                    icon = self.scene.addPixmap(QPixmap("Data\\void.png"))
                    icon.setTransform(QTransform.fromScale(1, -1))
                    icon.setPos(e.x_block*TILEWIDTH + 0.5, (e.z_block + 1)*TILEHEIGHT + 4.5)
                icon.setParentItem(room)
            
            #Doors
            
            if not data.out_of_map:
                for e in data.door_flag:
                    if e.direction_part == Direction.LEFT or (data.room_type == "ERoomType::Save" or data.room_type == "ERoomType::Warp") and len(data.door_flag) == 1:
                        door = self.scene.addRect(0, 0, OUTLINE, 6, outline, QColor(fill))
                        door.setPos(e.x_block*TILEWIDTH - 1.5, e.z_block*TILEHEIGHT + 4.5)
                        door.setParentItem(room)
                        if e.direction_part != Direction.LEFT:
                            door.setVisible(False)
                    if e.direction_part == Direction.BOTTOM:
                        door = self.scene.addRect(0, 0, 6, OUTLINE, outline, QColor(fill))
                        door.setPos(e.x_block*TILEWIDTH + 9.5, e.z_block*TILEHEIGHT - 1.5)
                        door.setParentItem(room)
                    if e.direction_part == Direction.RIGHT or (data.room_type == "ERoomType::Save" or data.room_type == "ERoomType::Warp") and len(data.door_flag) == 1:
                        door = self.scene.addRect(0, 0, OUTLINE, 6, outline, QColor(fill))
                        door.setPos(e.x_block*TILEWIDTH + TILEWIDTH - 1.5, e.z_block*TILEHEIGHT + 4.5)
                        door.setParentItem(room)
                        if e.direction_part != Direction.RIGHT:
                            door.setVisible(False)
                    if e.direction_part == Direction.TOP:
                        door = self.scene.addRect(0, 0, 6, OUTLINE, outline, QColor(fill))
                        door.setPos(e.x_block*TILEWIDTH + 9.5, e.z_block*TILEHEIGHT + TILEHEIGHT - 1.5)
                        door.setParentItem(room)
                    if e.direction_part == Direction.LEFT_BOTTOM:
                        if data.area == "EAreaID::m10BIG":
                            door = self.scene.addRect(0, 0, OUTLINE, 8, outline, QColor(fill))
                            door.setPos(e.x_block*TILEWIDTH - 1.5, e.z_block*TILEHEIGHT - 0.5)
                        else:
                            door = self.scene.addRect(0, 0, OUTLINE, 6, outline, QColor(fill))
                            door.setPos(e.x_block*TILEWIDTH - 1.5, e.z_block*TILEHEIGHT + 1.5)
                        door.setParentItem(room)
                    if e.direction_part == Direction.RIGHT_BOTTOM:
                        if data.area == "EAreaID::m10BIG":
                            door = self.scene.addRect(0, 0, OUTLINE, 8, outline, QColor(fill))
                            door.setPos(e.x_block*TILEWIDTH + TILEWIDTH - 1.5, e.z_block*TILEHEIGHT - 0.5)
                        else:
                            door = self.scene.addRect(0, 0, OUTLINE, 6, outline, QColor(fill))
                            door.setPos(e.x_block*TILEWIDTH + TILEWIDTH - 1.5, e.z_block*TILEHEIGHT + 1.5)
                        door.setParentItem(room)
                    if e.direction_part == Direction.LEFT_TOP:
                        if data.area == "EAreaID::m10BIG":
                            door = self.scene.addRect(0, 0, OUTLINE, 8, outline, QColor(fill))
                            door.setPos(e.x_block*TILEWIDTH - 1.5, e.z_block*TILEHEIGHT + 7.5)
                        else:
                            door = self.scene.addRect(0, 0, OUTLINE, 6, outline, QColor(fill))
                            door.setPos(e.x_block*TILEWIDTH - 1.5, e.z_block*TILEHEIGHT + 7.5)
                        door.setParentItem(room)
                    if e.direction_part == Direction.RIGHT_TOP:
                        if data.area == "EAreaID::m10BIG":
                            door = self.scene.addRect(0, 0, OUTLINE, 8, outline, QColor(fill))
                            door.setPos(e.x_block*TILEWIDTH + TILEWIDTH - 1.5, e.z_block*TILEHEIGHT + 7.5)
                        else:
                            door = self.scene.addRect(0, 0, OUTLINE, 6, outline, QColor(fill))
                            door.setPos(e.x_block*TILEWIDTH + TILEWIDTH - 1.5, e.z_block*TILEHEIGHT + 7.5)
                        door.setParentItem(room)
                    if e.direction_part == Direction.TOP_LEFT:
                        if data.area == "EAreaID::m10BIG":
                            door = self.scene.addRect(0, 0, 8, OUTLINE, outline, QColor(fill))
                            door.setPos(e.x_block*TILEWIDTH - 0.5, e.z_block*TILEHEIGHT + TILEHEIGHT - 1.5)
                        else:
                            door = self.scene.addRect(0, 0, 6, OUTLINE, outline, QColor(fill))
                            door.setPos(e.x_block*TILEWIDTH + 1.5, e.z_block*TILEHEIGHT + TILEHEIGHT - 1.5)
                        door.setParentItem(room)
                    if e.direction_part == Direction.TOP_RIGHT:
                        if data.area == "EAreaID::m10BIG":
                            door = self.scene.addRect(0, 0, 8, OUTLINE, outline, QColor(fill))
                            door.setPos(e.x_block*TILEWIDTH + 17.5, e.z_block*TILEHEIGHT + TILEHEIGHT - 1.5)
                        else:
                            door = self.scene.addRect(0, 0, 6, OUTLINE, outline, QColor(QColor(fill)))
                            door.setPos(e.x_block*TILEWIDTH + 17.5, e.z_block*TILEHEIGHT + TILEHEIGHT - 1.5)
                        door.setParentItem(room)
                    if e.direction_part == Direction.BOTTOM_RIGHT:
                        if data.area == "EAreaID::m10BIG":
                            door = self.scene.addRect(0, 0, 8, OUTLINE, outline, QColor(fill))
                            door.setPos(e.x_block*TILEWIDTH + 17.5, e.z_block*TILEHEIGHT - 1.5)
                        else:
                            door = self.scene.addRect(0, 0, 6, OUTLINE, outline, QColor(fill))
                            door.setPos(e.x_block*TILEWIDTH + 17.5, e.z_block*TILEHEIGHT - 1.5)
                        door.setParentItem(room)
                    if e.direction_part == Direction.BOTTOM_LEFT:
                        if data.area == "EAreaID::m10BIG":
                            door = self.scene.addRect(0, 0, 8, OUTLINE, outline, QColor(fill))
                            door.setPos(e.x_block*TILEWIDTH - 0.5, e.z_block*TILEHEIGHT - 1.5)
                        else:
                            door = self.scene.addRect(0, 0, 6, OUTLINE, outline, QColor(fill))
                            door.setPos(e.x_block*TILEWIDTH + 1.5, e.z_block*TILEHEIGHT - 1.5)
                        door.setParentItem(room)
                
            #Text
            
            text = self.scene.addText(data.name.replace('_', '').replace('(', '').replace(')', ''), "Impact")
            text.setDefaultTextColor(QColor("#ffffff"))
            text.setTransform(QTransform.fromScale(0.25, -0.5))
            text.setPos(data.width/2 - text.document().size().width()/8, data.height/2 + TILEHEIGHT/2 - 0.5)
            text.setParentItem(room)

    def update_offsets(self):
        for i in range(615):
            self.content[i]["Value"]["RoomType"] = self.room_list[i].data.room_type
            self.content[i]["Value"]["RoomPath"] = self.room_list[i].data.room_path
            self.content[i]["Value"]["ConsiderLeft"] = self.room_list[i].data.consider_left
            self.content[i]["Value"]["ConsiderRight"] = self.room_list[i].data.consider_right
            self.content[i]["Value"]["ConsiderTop"] = self.room_list[i].data.consider_top
            self.content[i]["Value"]["ConsiderBottom"] = self.room_list[i].data.consider_bottom
            self.content[i]["Value"]["OffsetX"] = self.room_list[i].pos().x() * 12.6 / TILEWIDTH
            self.content[i]["Value"]["OffsetZ"] = self.room_list[i].pos().y() * 7.2 / TILEHEIGHT
            self.content[i]["Value"]["BgmID"] = self.room_list[i].data.music
            self.content[i]["Value"]["BgmType"] = self.room_list[i].data.play
            if self.content[i]["Value"]["RoomType"] == "ERoomType::Save" or self.content[i]["Value"]["RoomType"] == "ERoomType::Warp":
                if self.content[i]["Value"]["RoomPath"] == "ERoomPath::Left":
                    self.content[i]["Value"]["DoorFlag"] = [1, 1]
                elif self.content[i]["Value"]["RoomPath"] == "ERoomPath::Right":
                    self.content[i]["Value"]["DoorFlag"] = [1, 4]
                elif self.content[i]["Value"]["RoomPath"] == "ERoomPath::Both":
                    self.content[i]["Value"]["DoorFlag"] = [1, 5]

    def same_check(self):
        for i in self.content:
            if i["Value"]["OutOfMap"]:
                continue
            offsetX_1 = i["Value"]["OffsetX"]
            offsetZ_1 = i["Value"]["OffsetZ"]
            for e in self.content:
                if e["Value"]["OutOfMap"]:
                    continue
                offsetX_2 = e["Value"]["OffsetX"]
                offsetZ_2 = e["Value"]["OffsetZ"]
                #SameRoom
                if offsetX_1 == offsetX_2 and offsetZ_1 == offsetZ_2 and i["Key"] != e["Key"]:
                    i["Value"]["SameRoom"] = e["Key"]
                    break;
                else:
                    i["Value"]["SameRoom"] = "None"
    
    def adj_check(self):
        for i in self.content:
            adj_rooms = []
            if i["Value"]["OutOfMap"]:
                continue
            area_1 = i["Value"]["AreaID"]
            width_1 = i["Value"]["AreaWidthSize"]
            height_1 = i["Value"]["AreaHeightSize"]
            offsetX_1 = i["Value"]["OffsetX"]
            offsetZ_1 = i["Value"]["OffsetZ"]
            for e in self.content:
                if e["Value"]["OutOfMap"]:
                    continue
                area_2 = e["Value"]["AreaID"]
                type_2 = e["Value"]["RoomType"]
                width_2 = e["Value"]["AreaWidthSize"]
                height_2 = e["Value"]["AreaHeightSize"]
                offsetX_2 = e["Value"]["OffsetX"]
                offsetZ_2 = e["Value"]["OffsetZ"]
                #Adjacent
                if self.left_check(i, e) or self.bottom_check(i, e) or self.right_check(i, e) or self.top_check(i, e):
                    #TransitionFix
                    if not (type_2 == "ERoomType::Load" and area_2 != area_1 and e["Value"]["SameRoom"] != "None" and e["Key"] != "m02VIL(1201)" and e["Value"]["SameRoom"] != "m03ENT(1201)"):
                        #VillageTransitionFix
                        if e["Value"]["SameRoom"] != "m02VIL(1201)" and e["Key"] != "m03ENT(1201)":
                            adj_rooms.append(e["Key"])
            i["Value"]["AdjacentRoomName"].clear()
            for e in adj_rooms:
                i["Value"]["AdjacentRoomName"].append(e)
        #VeparFix
        if "m02VIL_001" in self.content[22]["Value"]["AdjacentRoomName"]:
            self.content[22]["Value"]["AdjacentRoomName"].remove("m02VIL_001")
        if "m01SIP_022" in self.content[32]["Value"]["AdjacentRoomName"]:
            self.content[32]["Value"]["AdjacentRoomName"].remove("m01SIP_022")
        if not "m02VIL_000" in self.content[22]["Value"]["AdjacentRoomName"]:
            self.content[22]["Value"]["AdjacentRoomName"].append("m02VIL_000")
        #TowerFix
        if "m08TWR_017" in self.content[228]["Value"]["AdjacentRoomName"]:
            self.content[228]["Value"]["AdjacentRoomName"].remove("m08TWR_017")
        if "m08TWR_018" in self.content[228]["Value"]["AdjacentRoomName"]:
            self.content[228]["Value"]["AdjacentRoomName"].remove("m08TWR_018")
        if "m08TWR_018" in self.content[234]["Value"]["AdjacentRoomName"]:
            self.content[234]["Value"]["AdjacentRoomName"].remove("m08TWR_018")
        if "m08TWR_019" in self.content[241]["Value"]["AdjacentRoomName"]:
            self.content[241]["Value"]["AdjacentRoomName"].remove("m08TWR_019")
    
    def left_check(self, i, e):
        return bool(i["Value"]["OffsetX"] > e["Value"]["OffsetX"] >= round(i["Value"]["OffsetX"] - 12.6 * e["Value"]["AreaWidthSize"], 1) and round(i["Value"]["OffsetZ"] - 7.2 * (e["Value"]["AreaHeightSize"] - 1), 1) <= e["Value"]["OffsetZ"] <= round(i["Value"]["OffsetZ"] + 7.2 * (i["Value"]["AreaHeightSize"] - 1), 1))
    
    def bottom_check(self, i, e):
        return bool(round(i["Value"]["OffsetX"] - 12.6 * (e["Value"]["AreaWidthSize"] - 1), 1) <= e["Value"]["OffsetX"] <= round(i["Value"]["OffsetX"] + 12.6 * (i["Value"]["AreaWidthSize"] - 1), 1) and i["Value"]["OffsetZ"] > e["Value"]["OffsetZ"] >= round(i["Value"]["OffsetZ"] - 7.2 * e["Value"]["AreaHeightSize"], 1))
    
    def right_check(self, i, e):
        return bool(i["Value"]["OffsetX"] < e["Value"]["OffsetX"] <= round(i["Value"]["OffsetX"] + 12.6 * i["Value"]["AreaWidthSize"], 1) and round(i["Value"]["OffsetZ"] - 7.2 * (e["Value"]["AreaHeightSize"] - 1), 1) <= e["Value"]["OffsetZ"] <= round(i["Value"]["OffsetZ"] + 7.2 * (i["Value"]["AreaHeightSize"] - 1), 1))
    
    def top_check(self, i, e):
        return bool(round(i["Value"]["OffsetX"] - 12.6 * (e["Value"]["AreaWidthSize"] - 1), 1) <= e["Value"]["OffsetX"] <= round(i["Value"]["OffsetX"] + 12.6 * (i["Value"]["AreaWidthSize"] - 1), 1) and i["Value"]["OffsetZ"] < e["Value"]["OffsetZ"] <= round(i["Value"]["OffsetZ"] + 7.2 * i["Value"]["AreaHeightSize"], 1))

def main():
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()