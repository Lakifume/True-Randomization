import json
import sys
import os
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
logic_mode = False
assign_mode = False
assign_list = []

with open("Data\\RoomMaster\\BossRooms.json", "r") as file_reader:
    boss_room = json.load(file_reader)
    
with open("Data\\RoomMaster\\ConnectedRooms.json", "r") as file_reader:
    connected_room = json.load(file_reader)

with open("Data\\RoomMaster\\MusicTranslation.json", "r") as file_reader:
    music_translate = json.load(file_reader)

with open("Data\\RoomMaster\\PlayTranslation.json", "r") as file_reader:
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

class Logic:
    def __init__(self, is_gate, gate_list, double_jump, high_jump, invert, deepsinker, dimension_shift, reflector_ray, aqua_stream, blood_steal, zangetsuto, silver_bromide, aegis_plate, carpenter, warhorse, millionaire, celeste):
        self.is_gate = is_gate
        self.gate_list = gate_list
        self.double_jump = double_jump
        self.high_jump = high_jump
        self.invert = invert
        self.deepsinker = deepsinker
        self.dimension_shift = dimension_shift
        self.reflector_ray = reflector_ray
        self.aqua_stream = aqua_stream
        self.blood_steal = blood_steal
        self.zangetsuto = zangetsuto
        self.silver_bromide = silver_bromide
        self.aegis_plate = aegis_plate
        self.carpenter = carpenter
        self.warhorse = warhorse
        self.millionaire = millionaire
        self.celeste = celeste

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
    def __init__(self, index, room_data, logic_data, outline, fill, opacity, icon_color, can_move, group_list, room_list, metadata=None, parent=None):
        super().__init__(0, 0, room_data.width, room_data.height, parent)
        self.setPos(room_data.offset_x, room_data.offset_z)
        self.setData(KEY_METADATA, metadata)
        self.setCursor(Qt.PointingHandCursor)
        
        self.index = index
        self.room_data = room_data
        self.logic_data = logic_data
        self.outline = outline
        self.fill = fill
        self.opacity = opacity
        self.icon_color = icon_color
        self.can_move = can_move
        self.group_list = group_list
        self.room_list = room_list
        
        self.setPen(outline)
        self.setBrush(QColor(fill[:1] + opacity + fill[1:]))

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        #NormalModeSelection
        for i in self.scene().selectedItems():
            if restrictions and not logic_mode:
                for e in i.group_list:
                    self.room_list[e].setSelected(True)
        #AssignModeSelection
        if assign_mode:
            if self.logic_data.is_gate and self not in assign_list:
                #CheckingIfOneOfTheRoomsIsAlreadyAssignedToGate
                check = False
                for i in assign_list:
                    if self.index in i.logic_data.gate_list:
                        check = True
                    if i.index in self.logic_data.gate_list:
                        return
                #ChangingGateFill
                if check:
                    for i in assign_list:
                        if self.index in i.logic_data.gate_list:
                            i.logic_data.gate_list.remove(self.index)
                    self.setBrush(QColor(self.fill[:1] + self.opacity + self.fill[1:]))
                    for i in self.childItems():
                        if type(i) == QGraphicsRectItem:
                            i.setBrush(QColor(self.fill))
                else:
                    for i in assign_list:
                        if not self.index in i.logic_data.gate_list:
                            i.logic_data.gate_list.append(self.index)
                    self.setBrush(QColor("#ffffff"))
                    for i in self.childItems():
                        if type(i) == QGraphicsRectItem:
                            i.setBrush(QColor("#ffffff"))

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        for i in self.scene().selectedItems():
            self.apply_round(i)
    
    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        if not self.room_data.out_of_map and not assign_mode:
            for i in self.room_list:
                if i.room_data.area == self.room_data.area:
                    i.setSelected(True)

    def apply_round(self, item):
        x = round(item.pos().x() / TILEWIDTH) * TILEWIDTH
        y = round(item.pos().y() / TILEHEIGHT) * TILEHEIGHT
        if item.room_data.name == "m09TRN_002" and y < 0 and restrictions:
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
        + "QGroupBox{background-color: #21222e}"
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
        
        self.show_out = QAction("Show standalone rooms", self, checkable = True)
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
        
        self.logic_editor = QAction("Logic Editor", self, checkable = True)
        self.logic_editor.setShortcut(QKeySequence(Qt.Key_5))
        self.logic_editor.triggered.connect(self.logic_editor_action)
        tool_bar.addAction(self.logic_editor)
        
        self.key_location = QAction("Key Locations", self, checkable = True)
        self.key_location.setShortcut(QKeySequence(Qt.Key_6))
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
        
        self.reverse = QPushButton()
        self.reverse.setShortcut(QKeySequence(Qt.Key_D))
        self.reverse.setIcon(QIcon("Data\\reverse_icon.png"))
        self.reverse.setToolTip("Toggle save/warp entrance direction\nShortcut: D")
        self.reverse.clicked.connect(self.reverse_action)
        self.reverse.setFixedSize(50, 30)
        
        self.swap = QPushButton()
        self.swap.setShortcut(QKeySequence(Qt.Key_T))
        self.swap.setIcon(QIcon("Data\\swap_icon.png"))
        self.swap.setToolTip("Toggle save/warp room type\nShortcut: T")
        self.swap.clicked.connect(self.swap_action)
        self.swap.setFixedSize(50, 30)
        
        self.ignore_left = QPushButton()
        self.ignore_left.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_Left))
        self.ignore_left.setIcon(QIcon("Data\\ignore_left_icon.png"))
        self.ignore_left.setToolTip("Ignore left transitions\nShortcut: Ctrl + Left")
        self.ignore_left.clicked.connect(self.ignore_left_action)
        self.ignore_left.setFixedSize(50, 30)
        
        self.ignore_right = QPushButton()
        self.ignore_right.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_Right))
        self.ignore_right.setIcon(QIcon("Data\\ignore_right_icon.png"))
        self.ignore_right.setToolTip("Ignore right transitions\nShortcut: Ctrl + Right")
        self.ignore_right.clicked.connect(self.ignore_right_action)
        self.ignore_right.setFixedSize(50, 30)
        
        self.ignore_top = QPushButton()
        self.ignore_top.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_Up))
        self.ignore_top.setIcon(QIcon("Data\\ignore_top_icon.png"))
        self.ignore_top.setToolTip("Ignore top transitions\nShortcut: Ctrl + Up")
        self.ignore_top.clicked.connect(self.ignore_top_action)
        self.ignore_top.setFixedSize(50, 30)
        
        self.ignore_bottom = QPushButton()
        self.ignore_bottom.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_Down))
        self.ignore_bottom.setIcon(QIcon("Data\\ignore_bottom_icon.png"))
        self.ignore_bottom.setToolTip("Ignore bottom transitions\nShortcut: Ctrl + Down")
        self.ignore_bottom.clicked.connect(self.ignore_bottom_action)
        self.ignore_bottom.setFixedSize(50, 30)
        
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
        self.room_search_list.currentItemChanged.connect(self.room_search_list_change)
        self.room_search_list.setVisible(False)
        retain = self.room_search_list.sizePolicy()
        retain.setRetainSizeWhenHidden(True)
        self.room_search_list.setSizePolicy(retain)
        
        #Boxes
        
        gate_box_layout = QVBoxLayout()
        self.gate_box = QGroupBox()
        self.gate_box.setLayout(gate_box_layout)
        self.gate_box.setVisible(False)
        retain = self.gate_box.sizePolicy()
        retain.setRetainSizeWhenHidden(True)
        self.gate_box.setSizePolicy(retain)
        
        #BoxContent
        
        self.gate_toggle = QPushButton("Gate Toggle")
        self.gate_toggle.setToolTip("Toggle whether selected room is a gate or not.")
        self.gate_toggle.clicked.connect(self.gate_toggle_action)
        gate_box_layout.addWidget(self.gate_toggle)
        
        self.check_box_1 = QCheckBox("Double Jump")
        self.check_box_1.stateChanged.connect(self.check_box_1_changed)
        gate_box_layout.addWidget(self.check_box_1)
        
        self.check_box_2 = QCheckBox("High Jump")
        self.check_box_2.stateChanged.connect(self.check_box_2_changed)
        gate_box_layout.addWidget(self.check_box_2)
        
        self.check_box_3 = QCheckBox("Invert")
        self.check_box_3.stateChanged.connect(self.check_box_3_changed)
        gate_box_layout.addWidget(self.check_box_3)
        
        self.check_box_15 = QCheckBox("Deep Sinker")
        self.check_box_15.stateChanged.connect(self.check_box_15_changed)
        gate_box_layout.addWidget(self.check_box_15)
        
        self.check_box_4 = QCheckBox("Dimension Shift")
        self.check_box_4.stateChanged.connect(self.check_box_4_changed)
        gate_box_layout.addWidget(self.check_box_4)
        
        self.check_box_5 = QCheckBox("Reflector Ray")
        self.check_box_5.stateChanged.connect(self.check_box_5_changed)
        gate_box_layout.addWidget(self.check_box_5)
        
        self.check_box_6 = QCheckBox("Aqua Stream")
        self.check_box_6.stateChanged.connect(self.check_box_6_changed)
        gate_box_layout.addWidget(self.check_box_6)
        
        self.check_box_7 = QCheckBox("Blood Steal")
        self.check_box_7.stateChanged.connect(self.check_box_7_changed)
        gate_box_layout.addWidget(self.check_box_7)
        
        self.check_box_8 = QCheckBox("Zangetsuto")
        self.check_box_8.stateChanged.connect(self.check_box_8_changed)
        gate_box_layout.addWidget(self.check_box_8)
        
        self.check_box_9 = QCheckBox("Silver Bromide")
        self.check_box_9.stateChanged.connect(self.check_box_9_changed)
        gate_box_layout.addWidget(self.check_box_9)
        
        self.check_box_10 = QCheckBox("Aegis Plate")
        self.check_box_10.stateChanged.connect(self.check_box_10_changed)
        gate_box_layout.addWidget(self.check_box_10)
        
        self.check_box_11 = QCheckBox("Carpenter Key")
        self.check_box_11.stateChanged.connect(self.check_box_11_changed)
        gate_box_layout.addWidget(self.check_box_11)
        
        self.check_box_12 = QCheckBox("Warhorse Key")
        self.check_box_12.stateChanged.connect(self.check_box_12_changed)
        gate_box_layout.addWidget(self.check_box_12)
        
        self.check_box_13 = QCheckBox("Millionaire Key")
        self.check_box_13.stateChanged.connect(self.check_box_13_changed)
        gate_box_layout.addWidget(self.check_box_13)
        
        self.check_box_14 = QCheckBox("Celeste Key")
        self.check_box_14.stateChanged.connect(self.check_box_14_changed)
        gate_box_layout.addWidget(self.check_box_14)
        
        self.assign_mode = QPushButton("Assign Mode")
        self.assign_mode.setToolTip("Select gates to assign to selected room in this mode.")
        self.assign_mode.setCheckable(True)
        self.assign_mode.clicked.connect(self.assign_mode_action)
        gate_box_layout.addWidget(self.assign_mode)
        
        self.unassign_all = QPushButton("Unassign all")
        self.unassign_all.setToolTip("Empty gate list of all rooms.")
        self.unassign_all.clicked.connect(self.unassign_all_action)
        gate_box_layout.addWidget(self.unassign_all)
        
        #Layouts
        
        hbox_top = QHBoxLayout()
        hbox_top.addWidget(self.lock_label)
        hbox_top.addWidget(self.key_drop_down)
        hbox_top.addStretch(1)
        hbox_top.addWidget(self.music_drop_down)
        hbox_top.addWidget(self.play_drop_down)
        
        hbox_center = QHBoxLayout()
        hbox_center.addWidget(self.gate_box)
        hbox_center.addStretch(1)
        hbox_center.addWidget(self.room_search_list)
        
        hbox_bottom = QHBoxLayout()
        hbox_bottom.addWidget(self.reverse)
        hbox_bottom.addWidget(self.swap)
        hbox_bottom.addStretch(1)
        hbox_bottom.addWidget(self.ignore_left)
        hbox_bottom.addWidget(self.ignore_right)
        hbox_bottom.addWidget(self.ignore_top)
        hbox_bottom.addWidget(self.ignore_bottom)
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
        self.load_from_json("Data\\RoomMaster\\Content\\PB_DT_RoomMaster.json")
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
            self.reset_flags(i)
    
    def show_out_action(self):
        for i in self.room_list:
            if i.room_data.out_of_map:
                if self.show_out.isChecked():
                    i.setVisible(True)
                else:
                    i.setVisible(False)
    
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
    
    def room_search_action(self):
        if self.room_search.isChecked():
            #OtherToolDisable
            self.logic_editor.setChecked(False)
            self.logic_editor_action()
            self.key_location.setChecked(False)
            self.key_location_action()
            #Initiate
            self.disable_buttons()
            for i in self.room_list:
                i.setSelected(False)
                i.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)
            self.room_search_list.setCurrentItem(self.room_search_list.item(0))
            self.room_search_list_change(self.room_search_list.item(0))
            self.room_search_list.setVisible(True)
        else:
            self.enable_buttons()
            self.room_search_list.setVisible(False)
            self.reset_room()
    
    def logic_editor_action(self):
        global logic_mode
        if self.logic_editor.isChecked():
            logic_mode = True
            self.show_out.setChecked(False)
            self.show_out.setEnabled(False)
            #OtherToolDisable
            self.room_search.setChecked(False)
            self.room_search_action()
            self.key_location.setChecked(False)
            self.key_location_action()
            #Initiate
            self.disable_buttons()
            for i in self.room_list:
                i.setSelected(False)
                i.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)
                if i.logic_data == None:
                    i.setVisible(False)
            self.selection_event()
            self.gate_box.setVisible(True)
        else:
            logic_mode = False
            self.show_out.setEnabled(True)
            self.enable_buttons()
            self.assign_mode.setChecked(False)
            self.assign_mode_action()
            self.gate_box.setVisible(False)
            self.reset_room()
    
    def key_location_action(self):
        if self.key_location.isChecked():
            try:
                with open("Key\\KeyLocation.json", "r") as file_reader:
                    self.key_log = json.load(file_reader)
            except FileNotFoundError:
                box = QMessageBox(self)
                box.setWindowTitle("Error")
                box.setIcon(QMessageBox.Critical)
                box.setText("No key log found.")
                box.exec()
                self.key_location.setChecked(False)
                return
            #OtherToolDisable
            self.room_search.setChecked(False)
            self.room_search_action()
            self.logic_editor.setChecked(False)
            self.logic_editor_action()
            #FillDropDown
            self.key_drop_down.clear()
            for i in self.key_log:
                self.key_drop_down.addItem(i["Key"])
            #Initiate
            self.disable_buttons()
            for i in self.room_list:
                i.setSelected(False)
                i.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)
            self.key_drop_down.setCurrentIndex(0)
            self.key_drop_down_change(0)
            self.key_drop_down.setVisible(True)
        else:
            self.enable_buttons()
            self.key_drop_down.setVisible(False)
            self.reset_room()
    
    def how_to(self):
        box = QMessageBox(self)
        box.setWindowTitle("How to use")
        box.setText("Map Editor:\n\nThis editor allows you to fully customize the layout of the game's map. You can click and drag each room to change its location on the grid and you can select entire areas by double-clicking one of its rooms.\nSave your creations to the Custom folder for them to be picked by the randomizer.\n\nLogic Editor:\n\nOnce you've finished laying out a map you can use the logic editor tool to guide the randomizer in its key item placement to prevent unbeatable seeds on your map.\nEach gate represents a room that is an obstacle to the player's progression which must be connected to other previous gates and linked to the rooms that it leads to.\nThe randomizer will look for the first set of gates at the start of the game then move onto the next and so on until every key item is placed based on this consecution of requirements.\nThe graphical cues of this mode are:\n\n-Black fill: standard non-gate rooms\n-White fill: Gate rooms that selected room is connected to\n-Blue outline: rooms that have no requirement to get to\n-Green outline: rooms that are connected to selected gate\n-Red outline: rooms that are being assigned a gate in assign mode\n\nYou can submit your own layout creations to me on Discord (Lakifume#4066) if you want them to be added as presets in the main download of the randomizer.")
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
    
    def reverse_action(self):
        for i in self.scene.selectedItems():
            if i.room_data.room_type == "ERoomType::Save" or i.room_data.room_type == "ERoomType::Warp":
                if i.room_data.room_path == "ERoomPath::Left":
                    i.room_data.room_path = "ERoomPath::Right"
                    i.childItems()[5].setVisible(False)
                    i.childItems()[6].setVisible(True)
                elif i.room_data.room_path == "ERoomPath::Right":
                    i.room_data.room_path = "ERoomPath::Both"
                    i.childItems()[5].setVisible(True)
                    i.childItems()[6].setVisible(True)
                elif i.room_data.room_path == "ERoomPath::Both":
                    i.room_data.room_path = "ERoomPath::Left"
                    i.childItems()[5].setVisible(True)
                    i.childItems()[6].setVisible(False)
    
    def swap_action(self):
        for i in self.scene.selectedItems():
            if i.room_data.room_type == "ERoomType::Save":
                i.room_data.room_type = "ERoomType::Warp"
                i.childItems()[4].setPixmap("Data\\warp.png")
            elif i.room_data.room_type == "ERoomType::Warp":
                i.room_data.room_type = "ERoomType::Save"
                i.childItems()[4].setPixmap("Data\\save.png")
    
    def ignore_left_action(self):
        for i in self.scene.selectedItems():
            if i.room_data.consider_left:
                i.room_data.consider_left = False
                i.childItems()[0].setVisible(True)
            else:
                i.room_data.consider_left = True
                i.childItems()[0].setVisible(False)
    
    def ignore_right_action(self):
        for i in self.scene.selectedItems():
            if i.room_data.consider_right:
                i.room_data.consider_right = False
                i.childItems()[1].setVisible(True)
            else:
                i.room_data.consider_right = True
                i.childItems()[1].setVisible(False)
    
    def ignore_top_action(self):
        for i in self.scene.selectedItems():
            if i.room_data.consider_top:
                i.room_data.consider_top = False
                i.childItems()[2].setVisible(True)
            else:
                i.room_data.consider_top = True
                i.childItems()[2].setVisible(False)
    
    def ignore_bottom_action(self):
        for i in self.scene.selectedItems():
            if i.room_data.consider_bottom:
                i.room_data.consider_bottom = False
                i.childItems()[3].setVisible(True)
            else:
                i.room_data.consider_bottom = True
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
            try:
                if i.room_data.name == self.key_log[index]["Value"]["Room"]:
                    self.reveal_room(i)
                else:
                    self.fill_room(i, "#000000")
            except KeyError:
                if i.room_data.name in self.key_log[index]["Value"]["RoomList"]:
                    self.reveal_room(i)
                else:
                    self.fill_room(i, "#000000")
    
    def room_search_list_change(self, item):
        for i in self.room_list:
            i.setSelected(False)
            self.fill_room(i, "#000000")
        i = self.room_list[self.room_search_list.currentRow()]
        self.reveal_room(i)
        i.setSelected(True)
    
    def music_drop_down_change(self, index):
        for i in self.scene.selectedItems():
            i.room_data.music = music_id[index]
    
    def play_drop_down_change(self, index):
        for i in self.scene.selectedItems():
            i.room_data.play = play_id[index]
    
    def fill_room(self, i, color):
        i.setBrush(QColor(color[:1] + i.opacity + color[1:]))
        for e in i.childItems():
            if type(e) == QGraphicsRectItem:
                e.setBrush(QColor(color))
        if color == "#000000" and i.icon_color == 0:
            self.invert_icon(i)
            i.icon_color = 1
        elif color == "#ffffff" and i.icon_color == 1:
            self.invert_icon(i)
            i.icon_color = 0
    
    def invert_icon(self, i):
        for e in i.childItems():
            if type(e) == QGraphicsPixmapItem:
                image = e.pixmap().toImage()
                image.invertPixels()
                e.setPixmap(QPixmap.fromImage(image))
    
    def outline_room(self, i, color):
        i.outline.setColor(color)
        i.setPen(i.outline)
        if color == "#ffffff":
            i.setZValue(0 - (i.room_data.width/TILEWIDTH)*(i.room_data.height/TILEHEIGHT))
        else:
            i.setZValue(74 - (i.room_data.width/TILEWIDTH)*(i.room_data.height/TILEHEIGHT))
    
    def reveal_room(self, i):
        i.setBrush(QColor(i.fill[:1] + i.opacity + i.fill[1:]))
        for e in i.childItems():
            if type(e) == QGraphicsRectItem:
                e.setBrush(QColor(i.fill))
        if i.icon_color == 1:
            self.invert_icon(i)
            i.icon_color = 0
    
    def reset_room(self):
        for i in self.room_list:
            if not i.room_data.out_of_map:
                i.setVisible(True)
            i.setSelected(False)
            self.reveal_room(i)
            self.outline_room(i, "#ffffff")
            self.reset_flags(i)
    
    def reset_flags(self, i):
        if not i.can_move:
            if restrictions:
                i.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)
            else:
                i.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable | QGraphicsItem.ItemIsMovable)
        else:
            i.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable | QGraphicsItem.ItemIsMovable)
    
    def change_title(self, suffix):
        self.setWindowTitle("Map Editor" + self.title_string + suffix)
    
    def selection_event(self):
        #AssignModeSelection
        if assign_mode:
            self.assign_selection_event()
        #LogicEditorSelection
        elif logic_mode:
            self.logic_selection_event()
        #NormalEditorSelection
        else:
            self.normal_selection_event()

    def normal_selection_event(self):
        #UnsavedTag
        if not self.unsaved:
            self.change_title("*")
            self.unsaved = True
        #LayerChange
        for i in self.room_list:
            if i.isSelected():
                i.setZValue(74 - (i.room_data.width/TILEWIDTH)*(i.room_data.height/TILEHEIGHT))
            else:
                i.setZValue(0 - (i.room_data.width/TILEWIDTH)*(i.room_data.height/TILEHEIGHT))
        #DisplayMusicDropDown
        if self.scene.selectedItems():
            self.music_drop_down.setVisible(True)
            self.play_drop_down.setVisible(True)
            if len(self.scene.selectedItems()) == 1:
                self.music_drop_down.setCurrentIndex(music_id.index(self.scene.selectedItems()[0].room_data.music))
                self.play_drop_down.setCurrentIndex(play_id.index(self.scene.selectedItems()[0].room_data.play))
        else:
            self.music_drop_down.setVisible(False)
            self.play_drop_down.setVisible(False)

    def logic_selection_event(self):
        #UnsavedTag
        if not self.unsaved:
            self.change_title("*")
            self.unsaved = True
        #UpdateGates
        for i in self.room_list:
            if i.logic_data == None:
                continue
            self.fill_room(i, "#000000")
            self.outline_room(i, "#ffffff")
            if i.logic_data.is_gate:
                self.reveal_room(i)
        #LayerChange
        for i in self.room_list:
            if i.isSelected():
                i.setZValue(74 - (i.room_data.width/TILEWIDTH)*(i.room_data.height/TILEHEIGHT))
            else:
                i.setZValue(0 - (i.room_data.width/TILEWIDTH)*(i.room_data.height/TILEHEIGHT))
        #OutlineGatedRooms
        for i in self.scene.selectedItems():
            if i.logic_data.is_gate:
                for e in self.room_list:
                    if e.logic_data == None:
                        continue
                    if i.index in e.logic_data.gate_list:
                        self.outline_room(e, "#00ff00")
            elif i.index == 0:
                for e in self.room_list:
                    if e.logic_data == None:
                        continue
                    if not e.logic_data.gate_list:
                        self.outline_room(e, "#0000ff")
        #NothingSelected
        if not self.scene.selectedItems():
            self.gate_toggle.setEnabled(False)
            self.disable_checkboxes()
            self.uncheck_checkboxes()
            self.assign_mode.setEnabled(False)
        #OneSelected
        elif len(self.scene.selectedItems()) == 1:
            if self.scene.selectedItems()[0].index == 0:
                self.gate_toggle.setEnabled(False)
                self.assign_mode.setEnabled(False)
            else:
                self.gate_toggle.setEnabled(True)
                self.assign_mode.setEnabled(True)
            if self.scene.selectedItems()[0].logic_data.is_gate:
                self.enable_checkboxes()
                self.check_gate(self.scene.selectedItems()[0])
            else:
                self.disable_checkboxes()
                self.uncheck_checkboxes()
            for e in self.scene.selectedItems()[0].logic_data.gate_list:
                self.fill_room(self.room_list[e], "#ffffff")
        #MultipleSelected
        else:
            self.gate_toggle.setEnabled(False)
            self.disable_checkboxes()
            self.uncheck_checkboxes()
            self.assign_mode.setEnabled(True)
            for i in self.scene.selectedItems():
                for e in i.logic_data.gate_list:
                    self.fill_room(self.room_list[e], "#ffffff")
    
    def assign_selection_event(self):
        return
    
    def gate_toggle_action(self):
        if self.scene.selectedItems()[0].logic_data.is_gate:
            self.scene.selectedItems()[0].logic_data.is_gate = False
            for i in self.room_list:
                if i.logic_data == None:
                    continue
                if self.scene.selectedItems()[0].index in i.logic_data.gate_list:
                    i.logic_data.gate_list.remove(self.scene.selectedItems()[0].index)
        else:
            self.scene.selectedItems()[0].logic_data.is_gate = True
        self.logic_selection_event()
    
    def assign_mode_action(self):
        global assign_mode
        if self.assign_mode.isChecked():
            assign_mode = True
            self.gate_toggle.setEnabled(False)
            self.disable_checkboxes()
            self.unassign_all.setEnabled(False)
            self.gate_box.setStyleSheet("QGroupBox{border: 1px solid red}")
            assign_list.clear()
            for i in self.scene.selectedItems():
                assign_list.append(i)
                self.outline_room(i, "#ff0000")
            for i in self.room_list:
                i.setFlags(QGraphicsItem.ItemIsFocusable)
        else:
            assign_mode = False
            self.unassign_all.setEnabled(True)
            self.gate_box.setStyleSheet("QGroupBox{border: 1px solid white}")
            for i in self.room_list:
                i.setSelected(False)
                i.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)
            for i in assign_list:
                i.setSelected(True)
                self.outline_room(i, "#ffffff")
    
    def unassign_all_action(self):
        for i in self.room_list:
            if i.logic_data == None:
                continue
            i.logic_data.gate_list.clear()
        self.room_list[0].setSelected(True)
        self.logic_selection_event()
    
    def enable_buttons(self):
        self.reverse.setEnabled(True)
        self.swap.setEnabled(True)
        self.ignore_left.setEnabled(True)
        self.ignore_right.setEnabled(True)
        self.ignore_top.setEnabled(True)
        self.ignore_bottom.setEnabled(True)
    
    def disable_buttons(self):
        self.reverse.setEnabled(False)
        self.swap.setEnabled(False)
        self.ignore_left.setEnabled(False)
        self.ignore_right.setEnabled(False)
        self.ignore_top.setEnabled(False)
        self.ignore_bottom.setEnabled(False)
    
    def enable_checkboxes(self):
        self.check_box_1.setEnabled(True)
        self.check_box_2.setEnabled(True)
        self.check_box_3.setEnabled(True)
        self.check_box_15.setEnabled(True)
        self.check_box_4.setEnabled(True)
        self.check_box_5.setEnabled(True)
        self.check_box_6.setEnabled(True)
        self.check_box_7.setEnabled(True)
        self.check_box_8.setEnabled(True)
        self.check_box_9.setEnabled(True)
        self.check_box_10.setEnabled(True)
        self.check_box_11.setEnabled(True)
        self.check_box_12.setEnabled(True)
        self.check_box_13.setEnabled(True)
        self.check_box_14.setEnabled(True)
    
    def disable_checkboxes(self):
        self.check_box_1.setEnabled(False)
        self.check_box_2.setEnabled(False)
        self.check_box_3.setEnabled(False)
        self.check_box_15.setEnabled(False)
        self.check_box_4.setEnabled(False)
        self.check_box_5.setEnabled(False)
        self.check_box_6.setEnabled(False)
        self.check_box_7.setEnabled(False)
        self.check_box_8.setEnabled(False)
        self.check_box_9.setEnabled(False)
        self.check_box_10.setEnabled(False)
        self.check_box_11.setEnabled(False)
        self.check_box_12.setEnabled(False)
        self.check_box_13.setEnabled(False)
        self.check_box_14.setEnabled(False)
    
    def uncheck_checkboxes(self):
        self.check_box_1.setChecked(False)
        self.check_box_2.setChecked(False)
        self.check_box_3.setChecked(False)
        self.check_box_15.setChecked(False)
        self.check_box_4.setChecked(False)
        self.check_box_5.setChecked(False)
        self.check_box_6.setChecked(False)
        self.check_box_7.setChecked(False)
        self.check_box_8.setChecked(False)
        self.check_box_9.setChecked(False)
        self.check_box_10.setChecked(False)
        self.check_box_11.setChecked(False)
        self.check_box_12.setChecked(False)
        self.check_box_13.setChecked(False)
        self.check_box_14.setChecked(False)
    
    def check_gate(self, i):
        if i.logic_data.double_jump:
            self.check_box_1.setChecked(True)
            self.check_box_1_changed()
        else:
            self.check_box_1.setChecked(False)
        
        if i.logic_data.high_jump:
            self.check_box_2.setChecked(True)
            self.check_box_2_changed()
        else:
            self.check_box_2.setChecked(False)
        
        if i.logic_data.invert:
            self.check_box_3.setChecked(True)
            self.check_box_3_changed()
        else:
            self.check_box_3.setChecked(False)
        
        if i.logic_data.deepsinker:
            self.check_box_15.setChecked(True)
            self.check_box_15_changed()
        else:
            self.check_box_15.setChecked(False)
        
        if i.logic_data.dimension_shift:
            self.check_box_4.setChecked(True)
            self.check_box_4_changed()
        else:
            self.check_box_4.setChecked(False)
        
        if i.logic_data.reflector_ray:
            self.check_box_5.setChecked(True)
            self.check_box_5_changed()
        else:
            self.check_box_5.setChecked(False)
        
        if i.logic_data.aqua_stream:
            self.check_box_6.setChecked(True)
            self.check_box_6_changed()
        else:
            self.check_box_6.setChecked(False)
        
        if i.logic_data.blood_steal:
            self.check_box_7.setChecked(True)
            self.check_box_7_changed()
        else:
            self.check_box_7.setChecked(False)
        
        if i.logic_data.zangetsuto:
            self.check_box_8.setChecked(True)
            self.check_box_8_changed()
        else:
            self.check_box_8.setChecked(False)
        
        if i.logic_data.silver_bromide:
            self.check_box_9.setChecked(True)
            self.check_box_9_changed()
        else:
            self.check_box_9.setChecked(False)
        
        if i.logic_data.aegis_plate:
            self.check_box_10.setChecked(True)
            self.check_box_10_changed()
        else:
            self.check_box_10.setChecked(False)
        
        if i.logic_data.carpenter:
            self.check_box_11.setChecked(True)
            self.check_box_11_changed()
        else:
            self.check_box_11.setChecked(False)
        
        if i.logic_data.warhorse:
            self.check_box_12.setChecked(True)
            self.check_box_12_changed()
        else:
            self.check_box_12.setChecked(False)
        
        if i.logic_data.millionaire:
            self.check_box_13.setChecked(True)
            self.check_box_13_changed()
        else:
            self.check_box_13.setChecked(False)
        
        if i.logic_data.celeste:
            self.check_box_14.setChecked(True)
            self.check_box_14_changed()
        else:
            self.check_box_14.setChecked(False)
    
    def check_box_1_changed(self):
        if self.check_box_1.isChecked():
            if len(self.scene.selectedItems()) == 1:
                self.scene.selectedItems()[0].logic_data.double_jump = True
                self.check_box_1.setStyleSheet("color: " + self.scene.selectedItems()[0].fill)
        else:
            if len(self.scene.selectedItems()) == 1:
                self.scene.selectedItems()[0].logic_data.double_jump = False
            self.check_box_1.setStyleSheet("color: #ffffff")
    
    def check_box_2_changed(self):
        if self.check_box_2.isChecked():
            if len(self.scene.selectedItems()) == 1:
                self.scene.selectedItems()[0].logic_data.high_jump = True
                self.check_box_2.setStyleSheet("color: " + self.scene.selectedItems()[0].fill)
        else:
            if len(self.scene.selectedItems()) == 1:
                self.scene.selectedItems()[0].logic_data.high_jump = False
            self.check_box_2.setStyleSheet("color: #ffffff")
    
    def check_box_3_changed(self):
        if self.check_box_3.isChecked():
            if len(self.scene.selectedItems()) == 1:
                self.scene.selectedItems()[0].logic_data.invert = True
                self.check_box_3.setStyleSheet("color: " + self.scene.selectedItems()[0].fill)
        else:
            if len(self.scene.selectedItems()) == 1:
                self.scene.selectedItems()[0].logic_data.invert = False
            self.check_box_3.setStyleSheet("color: #ffffff")
    
    def check_box_15_changed(self):
        if self.check_box_15.isChecked():
            if len(self.scene.selectedItems()) == 1:
                self.scene.selectedItems()[0].logic_data.deepsinker = True
                self.check_box_15.setStyleSheet("color: " + self.scene.selectedItems()[0].fill)
        else:
            if len(self.scene.selectedItems()) == 1:
                self.scene.selectedItems()[0].logic_data.deepsinker = False
            self.check_box_15.setStyleSheet("color: #ffffff")
    
    def check_box_4_changed(self):
        if self.check_box_4.isChecked():
            if len(self.scene.selectedItems()) == 1:
                self.scene.selectedItems()[0].logic_data.dimension_shift = True
                self.check_box_4.setStyleSheet("color: " + self.scene.selectedItems()[0].fill)
        else:
            if len(self.scene.selectedItems()) == 1:
                self.scene.selectedItems()[0].logic_data.dimension_shift = False
            self.check_box_4.setStyleSheet("color: #ffffff")
    
    def check_box_5_changed(self):
        if self.check_box_5.isChecked():
            if len(self.scene.selectedItems()) == 1:
                self.scene.selectedItems()[0].logic_data.reflector_ray = True
                self.check_box_5.setStyleSheet("color: " + self.scene.selectedItems()[0].fill)
        else:
            if len(self.scene.selectedItems()) == 1:
                self.scene.selectedItems()[0].logic_data.reflector_ray = False
            self.check_box_5.setStyleSheet("color: #ffffff")
    
    def check_box_6_changed(self):
        if self.check_box_6.isChecked():
            if len(self.scene.selectedItems()) == 1:
                self.scene.selectedItems()[0].logic_data.aqua_stream = True
                self.check_box_6.setStyleSheet("color: " + self.scene.selectedItems()[0].fill)
        else:
            if len(self.scene.selectedItems()) == 1:
                self.scene.selectedItems()[0].logic_data.aqua_stream = False
            self.check_box_6.setStyleSheet("color: #ffffff")
    
    def check_box_7_changed(self):
        if self.check_box_7.isChecked():
            if len(self.scene.selectedItems()) == 1:
                self.scene.selectedItems()[0].logic_data.blood_steal = True
                self.check_box_7.setStyleSheet("color: " + self.scene.selectedItems()[0].fill)
        else:
            if len(self.scene.selectedItems()) == 1:
                self.scene.selectedItems()[0].logic_data.blood_steal = False
            self.check_box_7.setStyleSheet("color: #ffffff")
    
    def check_box_8_changed(self):
        if self.check_box_8.isChecked():
            if len(self.scene.selectedItems()) == 1:
                self.scene.selectedItems()[0].logic_data.zangetsuto = True
                self.check_box_8.setStyleSheet("color: " + self.scene.selectedItems()[0].fill)
        else:
            if len(self.scene.selectedItems()) == 1:
                self.scene.selectedItems()[0].logic_data.zangetsuto = False
            self.check_box_8.setStyleSheet("color: #ffffff")
    
    def check_box_9_changed(self):
        if self.check_box_9.isChecked():
            if len(self.scene.selectedItems()) == 1:
                self.scene.selectedItems()[0].logic_data.silver_bromide = True
                self.check_box_9.setStyleSheet("color: " + self.scene.selectedItems()[0].fill)
        else:
            if len(self.scene.selectedItems()) == 1:
                self.scene.selectedItems()[0].logic_data.silver_bromide = False
            self.check_box_9.setStyleSheet("color: #ffffff")
    
    def check_box_10_changed(self):
        if self.check_box_10.isChecked():
            if len(self.scene.selectedItems()) == 1:
                self.scene.selectedItems()[0].logic_data.aegis_plate = True
                self.check_box_10.setStyleSheet("color: " + self.scene.selectedItems()[0].fill)
        else:
            if len(self.scene.selectedItems()) == 1:
                self.scene.selectedItems()[0].logic_data.aegis_plate = False
            self.check_box_10.setStyleSheet("color: #ffffff")
    
    def check_box_11_changed(self):
        if self.check_box_11.isChecked():
            if len(self.scene.selectedItems()) == 1:
                self.scene.selectedItems()[0].logic_data.carpenter = True
                self.check_box_11.setStyleSheet("color: " + self.scene.selectedItems()[0].fill)
        else:
            if len(self.scene.selectedItems()) == 1:
                self.scene.selectedItems()[0].logic_data.carpenter = False
            self.check_box_11.setStyleSheet("color: #ffffff")
    
    def check_box_12_changed(self):
        if self.check_box_12.isChecked():
            if len(self.scene.selectedItems()) == 1:
                self.scene.selectedItems()[0].logic_data.warhorse = True
                self.check_box_12.setStyleSheet("color: " + self.scene.selectedItems()[0].fill)
        else:
            if len(self.scene.selectedItems()) == 1:
                self.scene.selectedItems()[0].logic_data.warhorse = False
            self.check_box_12.setStyleSheet("color: #ffffff")
    
    def check_box_13_changed(self):
        if self.check_box_13.isChecked():
            if len(self.scene.selectedItems()) == 1:
                self.scene.selectedItems()[0].logic_data.millionaire = True
                self.check_box_13.setStyleSheet("color: " + self.scene.selectedItems()[0].fill)
        else:
            if len(self.scene.selectedItems()) == 1:
                self.scene.selectedItems()[0].logic_data.millionaire = False
            self.check_box_13.setStyleSheet("color: #ffffff")
    
    def check_box_14_changed(self):
        if self.check_box_14.isChecked():
            if len(self.scene.selectedItems()) == 1:
                self.scene.selectedItems()[0].logic_data.celeste = True
                self.check_box_14.setStyleSheet("color: " + self.scene.selectedItems()[0].fill)
        else:
            if len(self.scene.selectedItems()) == 1:
                self.scene.selectedItems()[0].logic_data.celeste = False
            self.check_box_14.setStyleSheet("color: #ffffff")

    def load_from_json(self, filename):
        #Reset
        self.unsaved = True
        self.scene.clear()
        QApplication.processEvents()
        self.room_search_list.clear()
        self.room_list = []
        self.change_title("")
        #Open
        with open(filename, "r") as file_reader:
            self.map_content = json.load(file_reader)
        name, extension = os.path.splitext(filename)
        if os.path.isfile(name + ".logic"):
            with open(name + ".logic", "r") as file_reader:
                self.logic_content = json.load(file_reader)
        else:
            with open("Data\\RoomMaster\\Content\\PB_DT_RoomMaster.logic", "r") as file_reader:
                self.logic_content = json.load(file_reader)
        #Process
        self.draw_map()
        self.use_restr_action()
        self.show_out_action()
        self.show_name_action()
        if self.room_search.isChecked():
            self.room_search_action()
        if self.logic_editor.isChecked():
            self.logic_editor_action()
        if self.key_location.isChecked():
            self.key_location_action()
        self.selection_event()
        #Finalize
        self.unsaved = False
    
    def save_to_json(self, filename):
        self.update_offsets()
        self.update_logic()
        self.same_check()
        self.adj_check()
        with open(filename, "w") as file_writer:
            file_writer.write(json.dumps(self.map_content, indent=2))
        name, extension = os.path.splitext(filename)
        with open(name + ".logic", "w") as file_writer:
            file_writer.write(json.dumps(self.logic_content, indent=2))
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
    
    def convert_json_to_logic(self, json):
        is_gate = json["Value"]["GateRoom"]
        gate_list = self.convert_gate_to_index(json["Value"]["NearestGate"])
        double_jump = json["Value"]["Doublejump"]
        high_jump = json["Value"]["HighJump"]
        invert = json["Value"]["Invert"]
        deepsinker = json["Value"]["Deepsinker"]
        dimension_shift = json["Value"]["Dimensionshift"]
        reflector_ray = json["Value"]["Reflectionray"]
        aqua_stream = json["Value"]["Aquastream"]
        blood_steal = json["Value"]["Bloodsteel"]
        zangetsuto = json["Value"]["Swordsman"]
        silver_bromide = json["Value"]["Silverbromide"]
        aegis_plate = json["Value"]["BreastplateofAguilar"]
        carpenter = json["Value"]["Keyofbacker1"]
        warhorse = json["Value"]["Keyofbacker2"]
        millionaire = json["Value"]["Keyofbacker3"]
        celeste = json["Value"]["Keyofbacker4"]
        
        logic = Logic(is_gate, gate_list, double_jump, high_jump, invert, deepsinker, dimension_shift, reflector_ray, aqua_stream, blood_steal, zangetsuto, silver_bromide, aegis_plate, carpenter, warhorse, millionaire, celeste)
        return logic
    
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
        for i in range(len(self.map_content)):
            if self.map_content[i]["Key"] in group_list:
                new_group_list.append(i)
        return new_group_list
    
    def convert_gate_to_index(self, gate_list):
        new_gate_list = []
        for i in range(len(self.map_content)):
            if self.map_content[i]["Key"] in gate_list:
                new_gate_list.append(i)
        return new_gate_list
    
    def convert_index_to_gate(self, gate_list):
        new_gate_list = []
        for i in self.room_list:
            if i.index in gate_list:
                new_gate_list.append(i.room_data.name)
        return new_gate_list
    
    def draw_map(self):
        logic_index = 0
        for i in range(len(self.map_content)):
            
            #ConvertingData
            
            room_data = self.convert_json_to_room(self.map_content[i])
            if self.map_content[i]["Key"] == self.logic_content[logic_index]["Key"]:
                logic_data = self.convert_json_to_logic(self.logic_content[logic_index])
                if logic_index < len(self.logic_content) - 1:
                    logic_index += 1
            else:
                logic_data = None
            self.room_search_list.addItem(room_data.name)
            group_list = []
            can_move = True
            
            
            #NoWidthRooms
            
            if room_data.width == 0:
                room_data.width = TILEWIDTH/2
            if room_data.height == 0:
                room_data.height = TILEHEIGHT/2
            
            #AreaColor
            
            if room_data.area == "EAreaID::None":
                fill = area_color[18]
            else:
                fill = area_color[int(room_data.area[10:12]) - 1]
            
            #RoomOutline
            
            outline = QPen("#ffffff")
            outline.setWidth(OUTLINE)
            outline.setJoinStyle(Qt.MiterJoin)
            
            #MapOrigin
            
            origin_horizontal = self.scene.addLine(-(TILEHEIGHT/2 - 1.5), 0.0, TILEHEIGHT/2 - 1.5, 0.0)
            origin_horizontal.setPen(outline)
            origin_vertical = self.scene.addLine(0.0, TILEHEIGHT/2 - 1.5, 0.0, -(TILEHEIGHT/2 - 1.5))
            origin_vertical.setPen(outline)
            
            #MapBoundary
            
            bound_1_horizontal = self.scene.addLine(-256*TILEWIDTH, -32*TILEHEIGHT, -256*TILEWIDTH + (TILEHEIGHT/2 - 1.5), -32*TILEHEIGHT)
            bound_1_horizontal.setPen(outline)
            bound_1_vertical = self.scene.addLine(-256*TILEWIDTH, -32*TILEHEIGHT + (TILEHEIGHT/2 - 1.5), -256*TILEWIDTH, -32*TILEHEIGHT)
            bound_1_vertical.setPen(outline)
            
            bound_2_horizontal = self.scene.addLine(256*TILEWIDTH - (TILEHEIGHT/2 - 1.5), 128*TILEHEIGHT, 256*TILEWIDTH, 128*TILEHEIGHT)
            bound_2_horizontal.setPen(outline)
            bound_2_vertical = self.scene.addLine(256*TILEWIDTH, 128*TILEHEIGHT, 256*TILEWIDTH, 128*TILEHEIGHT - (TILEHEIGHT/2 - 1.5))
            bound_2_vertical.setPen(outline)
            
            #RoomGroup
            
            for e in connected_room:
                for o in e["Value"]["RoomId"]:
                    if room_data.name == o:
                        group_list = e["Value"]["RoomId"]
                        can_move = e["Value"]["CanMove"]
                        break
            
            #RoomOpacity
            
            if room_data.room_type == "ERoomType::Load" or room_data.name == "m01SIP_022" or room_data.name == "m02VIL_000" or room_data.name == "m02VIL_099" or room_data.name == "m02VIL(101)" or room_data.name == "m18ICE_020":
                opacity = "80"
            else:
                opacity = "ff"
            
            icon_color = 0
            
            #CreatingRoom
            
            room = RoomItem(i, room_data, logic_data, outline, fill, opacity, icon_color, can_move, self.convert_group_to_index(group_list), self.room_list)
            self.scene.addItem(room)
            self.room_list.append(room)
            
            #NoOutline
            
            outline.setColor("#00000000")
            
            #IgnoreDirection
            
            if not room_data.out_of_map:
                pen = QPen("#555555")
                pen.setWidth(2)
                line = self.scene.addLine(2.5, 2.5, 2.5, room_data.height - 2.5)
                line.setPen(pen)
                line.setParentItem(room)
                if room_data.consider_left:
                    line.setVisible(False)
                line = self.scene.addLine(room_data.width - 2.5, 2.5, room_data.width - 2.5, room_data.height - 2.5)
                line.setPen(pen)
                line.setParentItem(room)
                if room_data.consider_right:
                    line.setVisible(False)
                line = self.scene.addLine(2.5, room_data.height - 2.5, room_data.width - 2.5, room_data.height - 2.5)
                line.setPen(pen)
                line.setParentItem(room)
                if room_data.consider_top:
                    line.setVisible(False)
                line = self.scene.addLine(2.5, 2.5, room_data.width - 2.5, 2.5)
                line.setPen(pen)
                line.setParentItem(room)
                if room_data.consider_bottom:
                    line.setVisible(False)
            
            #Icons
            
            if room_data.room_type == "ERoomType::Save":
                icon = self.scene.addPixmap(QPixmap("Data\\save.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(room_data.width/2 - 6, room_data.height/2 + TILEHEIGHT/2 - 1.5)
                icon.setParentItem(room)
            if room_data.room_type == "ERoomType::Warp":
                icon = self.scene.addPixmap(QPixmap("Data\\warp.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(room_data.width/2 - 6, room_data.height/2 + TILEHEIGHT/2 - 1.5)
                icon.setParentItem(room)
            if room_data.name in boss_room["Value"]["RoomId"]:
                icon = self.scene.addPixmap(QPixmap("Data\\boss.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(room_data.width/2 - 6, room_data.height/2 + TILEHEIGHT/2 - 1.5)
                icon.setParentItem(room)
            if int(room_data.name[1:3]) == 88:
                icon = self.scene.addPixmap(QPixmap("Data\\key.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(room_data.width/2 - 6, room_data.height/2 + TILEHEIGHT/2 - 1.5)
                icon.setParentItem(room)
            if room_data.name == "m01SIP_000":
                icon = self.scene.addPixmap(QPixmap("Data\\start.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(room_data.width/2 - 6, room_data.height/2 + TILEHEIGHT/2 - 1.5)
                icon.setParentItem(room)
            if room_data.name == "m04GDN_001" or room_data.name == "m10BIG_000":
                icon = self.scene.addPixmap(QPixmap("Data\\portal.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(room_data.width/2 - 6, room_data.height/2 + TILEHEIGHT/2 - 1.5)
                icon.setParentItem(room)
            if room_data.name == "m05SAN_006":
                icon = self.scene.addPixmap(QPixmap("Data\\barber.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(room_data.width/2 - 6, room_data.height/2 + TILEHEIGHT/2 - 1.5)
                icon.setParentItem(room)
            if room_data.name == "m06KNG_021":
                icon = self.scene.addPixmap(QPixmap("Data\\8bit.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(room_data.width/2 - 6, room_data.height/2 + TILEHEIGHT/2 - 1.5)
                icon.setParentItem(room)
            if room_data.name == "m07LIB_009":
                icon = self.scene.addPixmap(QPixmap("Data\\book.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(room_data.width/2 - 6, room_data.height/2 + TILEHEIGHT/2 - 1.5)
                icon.setParentItem(room)
            
            #Wall
            
            if room_data.name == "m01SIP_017":
                icon = self.scene.addPixmap(QPixmap("Data\\one_way_left.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(1.5, TILEHEIGHT - 1.5)
                icon.setParentItem(room)
            if room_data.name == "m03ENT_000":
                icon = self.scene.addPixmap(QPixmap("Data\\spike_opening.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(room_data.width/2 - 6, TILEHEIGHT*13 - 1.5)
                icon.setParentItem(room)
            if room_data.name == "m03ENT_007":
                icon = self.scene.addPixmap(QPixmap("Data\\one_way_left.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(room_data.width - 13.5, TILEHEIGHT - 1.5)
                icon.setParentItem(room)
            if room_data.name == "m05SAN_003":
                icon = self.scene.addPixmap(QPixmap("Data\\wall_horizontal.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(room_data.width/2 - 6, TILEHEIGHT*8 + 6)
                icon.setParentItem(room)
            if room_data.name == "m05SAN_017":
                icon = self.scene.addPixmap(QPixmap("Data\\one_way_left.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(room_data.width/2 - 1, TILEHEIGHT - 1.5)
                icon.setParentItem(room)
            if room_data.name == "m05SAN_019" or room_data.name == "m07LIB_005":
                icon = self.scene.addPixmap(QPixmap("Data\\one_way_down.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(room_data.width -18.5, TILEHEIGHT - 1.5)
                icon.setParentItem(room)
                if room_data.name == "m05SAN_019":
                    icon = self.scene.addPixmap(QPixmap("Data\\one_way_left.png"))
                    icon.setTransform(QTransform.fromScale(1, -1))
                    icon.setPos(TILEWIDTH - 23.5, TILEHEIGHT - 1.5)
                    icon.setParentItem(room)
            if room_data.name == "m05SAN_021":
                icon = self.scene.addPixmap(QPixmap("Data\\one_way_right.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(room_data.width - 13.5, room_data.height - TILEHEIGHT*2 - 1.5)
                icon.setParentItem(room)
            if room_data.name == "m06KNG_013":
                icon = self.scene.addPixmap(QPixmap("Data\\one_way_right.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(room_data.width - 13.5, TILEHEIGHT - 1.5)
                icon.setParentItem(room)
            if room_data.name == "m06KNG_015" or room_data.name == "m07LIB_029":
                icon = self.scene.addPixmap(QPixmap("Data\\one_way_up.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(room_data.width/2 - 6, room_data.height - 1.5)
                icon.setParentItem(room)
            if room_data.name == "m07LIB_006" or room_data.name == "m11UGD_045":
                icon = self.scene.addPixmap(QPixmap("Data\\hole.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(room_data.width/2 - 6, TILEHEIGHT - 1.5)
                icon.setParentItem(room)
            if room_data.name == "m07LIB_008" or room_data.name == "m07LIB_014" or room_data.name == "m11UGD_016" or room_data.name == "m18ICE_016":
                icon = self.scene.addPixmap(QPixmap("Data\\hole.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(room_data.width - 8.5, room_data.height - 1.5)
                icon.setParentItem(room)
            if room_data.name == "m07LIB_021":
                icon = self.scene.addPixmap(QPixmap("Data\\one_way_down.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(room_data.width/2 - 6, room_data.height - 1.5)
                icon.setParentItem(room)
            if room_data.name == "m07LIB_023":
                icon = self.scene.addPixmap(QPixmap("Data\\one_way_left.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(room_data.width - 11.5, TILEHEIGHT*3 - 1.5)
                icon.setParentItem(room)
            if room_data.name == "m07LIB_035" or room_data.name == "m11UGD_056":
                icon = self.scene.addPixmap(QPixmap("Data\\opening.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(room_data.width/2 - 6, TILEHEIGHT*3 - 9)
                icon.setParentItem(room)
            if room_data.name == "m08TWR_009":
                icon = self.scene.addPixmap(QPixmap("Data\\one_way_left.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(room_data.width - 11.5, TILEHEIGHT*11 - 1.5)
                icon.setParentItem(room)
            if room_data.name == "m11UGD_015":
                icon = self.scene.addPixmap(QPixmap("Data\\one_way_right.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(room_data.width/2 - 11, TILEHEIGHT - 1.5)
                icon.setParentItem(room)
            if room_data.name == "m11UGD_046":
                icon = self.scene.addPixmap(QPixmap("Data\\hole_left.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(1.5, room_data.height - 1.5)
                icon.setParentItem(room)
            if room_data.name == "m11UGD_056":
                icon = self.scene.addPixmap(QPixmap("Data\\wall_vertical.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(room_data.width - 8.5, room_data.height - 1.5)
                icon.setParentItem(room)
            if room_data.name == "m15JPN_010" or room_data.name == "m17RVA_005":
                icon = self.scene.addPixmap(QPixmap("Data\\ceiling_hole.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(room_data.width - 13.5, room_data.height - 1.5)
                icon.setParentItem(room)
            if room_data.name == "m17RVA_003":
                icon = self.scene.addPixmap(QPixmap("Data\\ceiling_hole_right.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(room_data.width - 13.5, room_data.height - 1.5)
                icon.setParentItem(room)
            if room_data.name == "m18ICE_015":
                icon = self.scene.addPixmap(QPixmap("Data\\wall_vertical.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(room_data.width/2 - 6, TILEHEIGHT - 1.5)
                icon.setParentItem(room)
            
            #Water
            
            if room_data.name == "m11UGD_021" or room_data.name == "m11UGD_022" or room_data.name == "m11UGD_023" or room_data.name == "m11UGD_024" or room_data.name == "m11UGD_025" or room_data.name == "m11UGD_026" or room_data.name == "m11UGD_044" or room_data.name == "m11UGD_045":
                for e in range(round(room_data.width/TILEWIDTH)):
                    for o in range(round(room_data.height/TILEHEIGHT)):
                        icon = self.scene.addPixmap(QPixmap("Data\\bubble.png"))
                        icon.setTransform(QTransform.fromScale(1, -1))
                        icon.setPos(e*TILEWIDTH + 6, o*TILEHEIGHT + 13.5)
                        icon.setParentItem(room)
            if room_data.name == "m11UGD_005" or room_data.name == "m11UGD_036":
                for e in range(round(room_data.width/TILEWIDTH)):
                    icon = self.scene.addPixmap(QPixmap("Data\\wave.png"))
                    icon.setTransform(QTransform.fromScale(1, -1))
                    icon.setPos(e*TILEWIDTH + 6, 20.5)
                    icon.setParentItem(room)
            if room_data.name == "m11UGD_019" or room_data.name == "m11UGD_040":
                for e in range(round(room_data.width/TILEWIDTH)):
                    icon = self.scene.addPixmap(QPixmap("Data\\wave.png"))
                    icon.setTransform(QTransform.fromScale(1, -1))
                    icon.setPos(e*TILEWIDTH + 6, 28.5)
                    icon.setParentItem(room)
            if room_data.name == "m11UGD_042" or room_data.name == "m11UGD_046":
                for e in range(round(room_data.width/TILEWIDTH)):
                    icon = self.scene.addPixmap(QPixmap("Data\\wave.png"))
                    icon.setTransform(QTransform.fromScale(1, -1))
                    icon.setPos(e*TILEWIDTH + 6, 43.5)
                    icon.setParentItem(room)
            if room_data.name == "m11UGD_043":
                for e in range(round(room_data.width/TILEWIDTH)-1):
                    icon = self.scene.addPixmap(QPixmap("Data\\wave.png"))
                    icon.setTransform(QTransform.fromScale(1, -1))
                    icon.setPos(e*TILEWIDTH + 6, 13.5)
                    icon.setParentItem(room)
            
            #NoTraverse
            
            for e in room_data.no_traverse:
                if room_data.name == "m11UGD_013":
                    icon = self.scene.addPixmap(QPixmap("Data\\void.png"))
                    icon.setTransform(QTransform.fromScale(1, -1))
                    icon.setPos(e.x_block*TILEWIDTH + 0.5, (e.z_block + 3)*TILEHEIGHT + 4.5)
                elif room_data.name == "m11UGD_031":
                    icon = self.scene.addPixmap(QPixmap("Data\\void.png"))
                    icon.setTransform(QTransform.fromScale(1, -1))
                    icon.setPos(e.x_block*TILEWIDTH + 0.5, (e.z_block + 4)*TILEHEIGHT + 4.5)
                else:
                    icon = self.scene.addPixmap(QPixmap("Data\\void.png"))
                    icon.setTransform(QTransform.fromScale(1, -1))
                    icon.setPos(e.x_block*TILEWIDTH + 0.5, (e.z_block + 1)*TILEHEIGHT + 4.5)
                icon.setParentItem(room)
            
            #Doors
            
            if not room_data.out_of_map:
                for e in room_data.door_flag:
                    if e.direction_part == Direction.LEFT or (room_data.room_type == "ERoomType::Save" or room_data.room_type == "ERoomType::Warp") and len(room_data.door_flag) == 1:
                        door = self.scene.addRect(0, 0, OUTLINE, 6, outline, QColor(fill))
                        door.setPos(e.x_block*TILEWIDTH - 1.5, e.z_block*TILEHEIGHT + 4.5)
                        door.setParentItem(room)
                        if e.direction_part != Direction.LEFT:
                            door.setVisible(False)
                    if e.direction_part == Direction.BOTTOM:
                        door = self.scene.addRect(0, 0, 6, OUTLINE, outline, QColor(fill))
                        door.setPos(e.x_block*TILEWIDTH + 9.5, e.z_block*TILEHEIGHT - 1.5)
                        door.setParentItem(room)
                    if e.direction_part == Direction.RIGHT or (room_data.room_type == "ERoomType::Save" or room_data.room_type == "ERoomType::Warp") and len(room_data.door_flag) == 1:
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
                        if room_data.area == "EAreaID::m10BIG":
                            door = self.scene.addRect(0, 0, OUTLINE, 8, outline, QColor(fill))
                            door.setPos(e.x_block*TILEWIDTH - 1.5, e.z_block*TILEHEIGHT - 0.5)
                        else:
                            door = self.scene.addRect(0, 0, OUTLINE, 6, outline, QColor(fill))
                            door.setPos(e.x_block*TILEWIDTH - 1.5, e.z_block*TILEHEIGHT + 1.5)
                        door.setParentItem(room)
                    if e.direction_part == Direction.RIGHT_BOTTOM:
                        if room_data.area == "EAreaID::m10BIG":
                            door = self.scene.addRect(0, 0, OUTLINE, 8, outline, QColor(fill))
                            door.setPos(e.x_block*TILEWIDTH + TILEWIDTH - 1.5, e.z_block*TILEHEIGHT - 0.5)
                        else:
                            door = self.scene.addRect(0, 0, OUTLINE, 6, outline, QColor(fill))
                            door.setPos(e.x_block*TILEWIDTH + TILEWIDTH - 1.5, e.z_block*TILEHEIGHT + 1.5)
                        door.setParentItem(room)
                    if e.direction_part == Direction.LEFT_TOP:
                        if room_data.area == "EAreaID::m10BIG":
                            door = self.scene.addRect(0, 0, OUTLINE, 8, outline, QColor(fill))
                            door.setPos(e.x_block*TILEWIDTH - 1.5, e.z_block*TILEHEIGHT + 7.5)
                        else:
                            door = self.scene.addRect(0, 0, OUTLINE, 6, outline, QColor(fill))
                            door.setPos(e.x_block*TILEWIDTH - 1.5, e.z_block*TILEHEIGHT + 7.5)
                        door.setParentItem(room)
                    if e.direction_part == Direction.RIGHT_TOP:
                        if room_data.area == "EAreaID::m10BIG":
                            door = self.scene.addRect(0, 0, OUTLINE, 8, outline, QColor(fill))
                            door.setPos(e.x_block*TILEWIDTH + TILEWIDTH - 1.5, e.z_block*TILEHEIGHT + 7.5)
                        else:
                            door = self.scene.addRect(0, 0, OUTLINE, 6, outline, QColor(fill))
                            door.setPos(e.x_block*TILEWIDTH + TILEWIDTH - 1.5, e.z_block*TILEHEIGHT + 7.5)
                        door.setParentItem(room)
                    if e.direction_part == Direction.TOP_LEFT:
                        if room_data.area == "EAreaID::m10BIG":
                            door = self.scene.addRect(0, 0, 8, OUTLINE, outline, QColor(fill))
                            door.setPos(e.x_block*TILEWIDTH - 0.5, e.z_block*TILEHEIGHT + TILEHEIGHT - 1.5)
                        else:
                            door = self.scene.addRect(0, 0, 6, OUTLINE, outline, QColor(fill))
                            door.setPos(e.x_block*TILEWIDTH + 1.5, e.z_block*TILEHEIGHT + TILEHEIGHT - 1.5)
                        door.setParentItem(room)
                    if e.direction_part == Direction.TOP_RIGHT:
                        if room_data.area == "EAreaID::m10BIG":
                            door = self.scene.addRect(0, 0, 8, OUTLINE, outline, QColor(fill))
                            door.setPos(e.x_block*TILEWIDTH + 17.5, e.z_block*TILEHEIGHT + TILEHEIGHT - 1.5)
                        else:
                            door = self.scene.addRect(0, 0, 6, OUTLINE, outline, QColor(QColor(fill)))
                            door.setPos(e.x_block*TILEWIDTH + 17.5, e.z_block*TILEHEIGHT + TILEHEIGHT - 1.5)
                        door.setParentItem(room)
                    if e.direction_part == Direction.BOTTOM_RIGHT:
                        if room_data.area == "EAreaID::m10BIG":
                            door = self.scene.addRect(0, 0, 8, OUTLINE, outline, QColor(fill))
                            door.setPos(e.x_block*TILEWIDTH + 17.5, e.z_block*TILEHEIGHT - 1.5)
                        else:
                            door = self.scene.addRect(0, 0, 6, OUTLINE, outline, QColor(fill))
                            door.setPos(e.x_block*TILEWIDTH + 17.5, e.z_block*TILEHEIGHT - 1.5)
                        door.setParentItem(room)
                    if e.direction_part == Direction.BOTTOM_LEFT:
                        if room_data.area == "EAreaID::m10BIG":
                            door = self.scene.addRect(0, 0, 8, OUTLINE, outline, QColor(fill))
                            door.setPos(e.x_block*TILEWIDTH - 0.5, e.z_block*TILEHEIGHT - 1.5)
                        else:
                            door = self.scene.addRect(0, 0, 6, OUTLINE, outline, QColor(fill))
                            door.setPos(e.x_block*TILEWIDTH + 1.5, e.z_block*TILEHEIGHT - 1.5)
                        door.setParentItem(room)
            
            #Text
            
            text = self.scene.addText(room_data.name.replace('_', '').replace('(', '').replace(')', ''), "Impact")
            text.setDefaultTextColor(QColor("#ffffff"))
            text.setTransform(QTransform.fromScale(0.25, -0.5))
            text.setPos(room_data.width/2 - text.document().size().width()/8, room_data.height/2 + TILEHEIGHT/2 - 0.5)
            text.setParentItem(room)

    def update_offsets(self):
        for i in self.room_list:
            self.map_content[i.index]["Value"]["RoomType"] = i.room_data.room_type
            self.map_content[i.index]["Value"]["RoomPath"] = i.room_data.room_path
            self.map_content[i.index]["Value"]["ConsiderLeft"] = i.room_data.consider_left
            self.map_content[i.index]["Value"]["ConsiderRight"] = i.room_data.consider_right
            self.map_content[i.index]["Value"]["ConsiderTop"] = i.room_data.consider_top
            self.map_content[i.index]["Value"]["ConsiderBottom"] = i.room_data.consider_bottom
            self.map_content[i.index]["Value"]["OffsetX"] = i.pos().x() * 12.6 / TILEWIDTH
            self.map_content[i.index]["Value"]["OffsetZ"] = i.pos().y() * 7.2 / TILEHEIGHT
            self.map_content[i.index]["Value"]["BgmID"] = i.room_data.music
            self.map_content[i.index]["Value"]["BgmType"] = i.room_data.play
            if self.map_content[i.index]["Value"]["RoomType"] == "ERoomType::Save" or self.map_content[i.index]["Value"]["RoomType"] == "ERoomType::Warp":
                if self.map_content[i.index]["Value"]["RoomPath"] == "ERoomPath::Left":
                    self.map_content[i.index]["Value"]["DoorFlag"] = [1, 1]
                elif self.map_content[i.index]["Value"]["RoomPath"] == "ERoomPath::Right":
                    self.map_content[i.index]["Value"]["DoorFlag"] = [1, 4]
                elif self.map_content[i.index]["Value"]["RoomPath"] == "ERoomPath::Both":
                    self.map_content[i.index]["Value"]["DoorFlag"] = [1, 5]
    
    def update_logic(self):
        logic_index = 0
        for i in self.room_list:
            if i.logic_data == None:
                continue
            if i.logic_data.is_gate and not i.logic_data.double_jump and not i.logic_data.high_jump and not i.logic_data.invert and not i.logic_data.deepsinker and not i.logic_data.dimension_shift and not i.logic_data.reflector_ray and not i.logic_data.aqua_stream and not i.logic_data.blood_steal and not i.logic_data.zangetsuto and not i.logic_data.silver_bromide and not i.logic_data.aegis_plate and not i.logic_data.carpenter and not i.logic_data.warhorse and not i.logic_data.millionaire and not i.logic_data.celeste:
                i.logic_data.is_gate = False
                for e in self.room_list:
                    if e.logic_data == None:
                        continue
                    if i.index in e.logic_data.gate_list:
                        e.logic_data.gate_list.remove(i.index)
            self.logic_content[logic_index]["Value"]["GateRoom"] = i.logic_data.is_gate
            self.logic_content[logic_index]["Value"]["NearestGate"] = self.convert_index_to_gate(i.logic_data.gate_list)
            self.logic_content[logic_index]["Value"]["Doublejump"] = i.logic_data.double_jump
            self.logic_content[logic_index]["Value"]["HighJump"] = i.logic_data.high_jump
            self.logic_content[logic_index]["Value"]["Invert"] = i.logic_data.invert
            self.logic_content[logic_index]["Value"]["Deepsinker"] = i.logic_data.deepsinker
            self.logic_content[logic_index]["Value"]["Dimensionshift"] = i.logic_data.dimension_shift
            self.logic_content[logic_index]["Value"]["Reflectionray"] = i.logic_data.reflector_ray
            self.logic_content[logic_index]["Value"]["Aquastream"] = i.logic_data.aqua_stream
            self.logic_content[logic_index]["Value"]["Bloodsteel"] = i.logic_data.blood_steal
            self.logic_content[logic_index]["Value"]["Swordsman"] = i.logic_data.zangetsuto
            self.logic_content[logic_index]["Value"]["Silverbromide"] = i.logic_data.silver_bromide
            self.logic_content[logic_index]["Value"]["BreastplateofAguilar"] = i.logic_data.aegis_plate
            self.logic_content[logic_index]["Value"]["Keyofbacker1"] = i.logic_data.carpenter
            self.logic_content[logic_index]["Value"]["Keyofbacker2"] = i.logic_data.warhorse
            self.logic_content[logic_index]["Value"]["Keyofbacker3"] = i.logic_data.millionaire
            self.logic_content[logic_index]["Value"]["Keyofbacker4"] = i.logic_data.celeste
            if logic_index < len(self.logic_content) - 1:
                logic_index += 1

    def same_check(self):
        for i in self.map_content:
            if i["Value"]["OutOfMap"]:
                continue
            offsetX_1 = i["Value"]["OffsetX"]
            offsetZ_1 = i["Value"]["OffsetZ"]
            for e in self.map_content:
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
        for i in self.map_content:
            adj_rooms = []
            if i["Value"]["OutOfMap"]:
                continue
            area_1 = i["Value"]["AreaID"]
            width_1 = i["Value"]["AreaWidthSize"]
            height_1 = i["Value"]["AreaHeightSize"]
            offsetX_1 = i["Value"]["OffsetX"]
            offsetZ_1 = i["Value"]["OffsetZ"]
            for e in self.map_content:
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
        if "m02VIL_001" in self.map_content[22]["Value"]["AdjacentRoomName"]:
            self.map_content[22]["Value"]["AdjacentRoomName"].remove("m02VIL_001")
        if "m01SIP_022" in self.map_content[32]["Value"]["AdjacentRoomName"]:
            self.map_content[32]["Value"]["AdjacentRoomName"].remove("m01SIP_022")
        if not "m02VIL_000" in self.map_content[22]["Value"]["AdjacentRoomName"]:
            self.map_content[22]["Value"]["AdjacentRoomName"].append("m02VIL_000")
        #TowerFix
        if "m08TWR_017" in self.map_content[228]["Value"]["AdjacentRoomName"]:
            self.map_content[228]["Value"]["AdjacentRoomName"].remove("m08TWR_017")
        if "m08TWR_018" in self.map_content[228]["Value"]["AdjacentRoomName"]:
            self.map_content[228]["Value"]["AdjacentRoomName"].remove("m08TWR_018")
        if "m08TWR_018" in self.map_content[234]["Value"]["AdjacentRoomName"]:
            self.map_content[234]["Value"]["AdjacentRoomName"].remove("m08TWR_018")
        if "m08TWR_019" in self.map_content[241]["Value"]["AdjacentRoomName"]:
            self.map_content[241]["Value"]["AdjacentRoomName"].remove("m08TWR_019")
        #GebelFix
        if not "m02VIL_099" in self.map_content[166]["Value"]["AdjacentRoomName"]:
            self.map_content[166]["Value"]["AdjacentRoomName"].append("m02VIL_099")
        #BaelFix
        if not "m02VIL_099" in self.map_content[475]["Value"]["AdjacentRoomName"]:
            self.map_content[475]["Value"]["AdjacentRoomName"].append("m02VIL_099")
    
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