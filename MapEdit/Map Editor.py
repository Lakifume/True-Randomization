import json
import sys
import os
import copy
from enum import Enum
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

script_name, script_extension = os.path.splitext(os.path.basename(__file__))

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
area_black = [
    "#00001f",
    "#271604",
    "#272727",
    "#2a3709",
    "#353321",
    "#441f06",
    "#24032f",
    "#0c2724",
    "#02023f",
    "#1f0000",
    "#0c163a",
    "#3f3602",
    "#1f1f00",
    "#092f0e",
    "#42073f",
    "#000000",
    "#3f020e",
    "#0a353f",
    "#171717"
]
area_white = [
    "#ffffff",
    "#ffffff",
    "#ffffff",
    "#ffffff",
    "#ffffff",
    "#ffffff",
    "#ffffff",
    "#ffffff",
    "#ffffff",
    "#ffffff",
    "#ffffff",
    "#ffffff",
    "#ffffff",
    "#ffffff",
    "#ffffff",
    "#ffffff",
    "#ffffff",
    "#ffffff",
    "#ffffff"
]
boss_room = [
    "m01SIP_022",
    "m03ENT_013",
    "m05SAN_012",
    "m05SAN_023",
    "m06KNG_020",
    "m07LIB_011",
    "m07LIB_038",
    "m08TWR_019",
    "m10BIG_011",
    "m12SND_027",
    "m13ARC_005",
    "m14TAR_004",
    "m15JPN_016",
    "m17RVA_008",
    "m18ICE_004",
    "m18ICE_018",
    "m18ICE_019",
    "m20JRN_003",
    "m50BRM_001",
    "m50BRM_003",
    "m50BRM_005",
    "m50BRM_007",
    "m50BRM_009",
    "m50BRM_051",
    "m50BRM_053",
    "m50BRM_055",
    "m50BRM_057",
    "m50BRM_059",
    "m53BRV_001",
    "m53BRV_003",
    "m53BRV_005",
    "m77LBP_000"
]

music_id = []
music_name = []
play_id = []
play_name = []

assign_list = []

restrictions = False
search_mode = False
logic_mode = False
area_mode = False
assign_mode = False
key_mode = False

right_held = False
mid_held   = False
x1_held    = False
x2_held    = False
    
with open("Data\\Constant\\ConnectedRooms.json", "r", encoding="utf8") as file_reader:
    connected_room = json.load(file_reader)

with open("Data\\Translation\\MusicTranslation.json", "r", encoding="utf8") as file_reader:
    music_translate = json.load(file_reader)

with open("Data\\Translation\\PlayTranslation.json", "r", encoding="utf8") as file_reader:
    play_translate = json.load(file_reader)

music_id.append(None)
music_name.append("None")
for i in music_translate:
    music_id.append(i)
    music_name.append(music_translate[i])

for i in play_translate:
    play_id.append(i)
    play_name.append(play_translate[i])

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
    def __init__(self, name, area, out_of_map, room_type, room_path, width, height, offset_x, offset_z, door_flag, no_traverse, music, play, unused):
        self.name = name
        self.area = area
        self.out_of_map = out_of_map
        self.room_type = room_type
        self.room_path = room_path
        self.width = width
        self.height = height
        self.offset_x = offset_x
        self.offset_z = offset_z
        self.door_flag = door_flag
        self.no_traverse = no_traverse
        self.music = music
        self.play = play
        self.unused = unused

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
    def __init__(self, x_block, z_block, direction_part, breakable):
        self.x_block = x_block
        self.z_block = z_block
        self.direction_part = direction_part
        self.breakable = breakable

class Void:
    def __init__(self, x_block, z_block):
        self.x_block = x_block
        self.z_block = z_block

class RoomItem(QGraphicsRectItem):
    def __init__(self, index, room_data, logic_data, outline, fill, fill_black, fill_white, opacity, icon_color, can_move, group_list, room_list, music_drop_down, metadata=None, parent=None):
        super().__init__(0, 0, room_data.width, room_data.height, parent)
        self.setPos(room_data.offset_x, room_data.offset_z)
        self.setData(KEY_METADATA, metadata)
        self.setCursor(Qt.PointingHandCursor)
        
        self.index = index
        self.room_data = room_data
        self.logic_data = logic_data
        self.outline = QPen(outline)
        self.outline.setWidth(OUTLINE)
        self.outline.setJoinStyle(Qt.MiterJoin)
        self.fill = fill
        self.fill_black = fill_black
        self.fill_white = fill_white
        self.opacity = opacity
        self.icon_color = icon_color
        self.can_move = can_move
        self.group_list = group_list
        self.room_list = room_list
        self.music_drop_down = music_drop_down
        
        self.setPen(self.outline)
        self.setBrush(QColor(fill[:1] + opacity + fill[1:]))
        self.setToolTip(room_data.name)

    def mousePressEvent(self, event):
        if right_held or mid_held or x1_held or x2_held:
            return
        super().mousePressEvent(event)
        #Normal mode selection
        for i in self.scene().selectedItems():
            if restrictions and not search_mode and not logic_mode and not area_mode and not key_mode:
                for e in i.group_list:
                    self.room_list[e].setSelected(True)
        #Assign mode selection
        if assign_mode:
            if self.logic_data.is_gate and self not in assign_list:
                #Checking if one of the rooms is already assigned to gate
                check = False
                for i in assign_list:
                    if self.index in i.logic_data.gate_list:
                        check = True
                    if i.index in self.logic_data.gate_list:
                        return
                #Changing gate fill
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
    
    def mouseMoveEvent(self, event):
        #Ignore mouse move if another button than left mouse is held
        if right_held or mid_held or x1_held or x2_held:
            return
        super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        if event.button() != Qt.LeftButton:
            return
        super().mouseReleaseEvent(event)
        #Place room
        for i in self.scene().selectedItems():
            self.apply_round(i)
            #Change a backer room's area id based on what it is connected to
            if "m88BKR" in i.room_data.name:
                for e in self.room_list:
                    if "m88BKR" in e.room_data.name:
                        continue
                    if e.room_data.out_of_map:
                        continue
                    if i.room_data.room_path == "ERoomPath::Left":
                        if e.room_data.offset_x == round(i.room_data.offset_x - e.room_data.width) and round(i.room_data.offset_z - e.room_data.height - TILEHEIGHT, 1) <= e.room_data.offset_z <= round(i.room_data.offset_z + i.room_data.height - TILEHEIGHT):
                            for o in e.room_data.door_flag:
                                if o.direction_part == Direction.RIGHT and 0 == (o.z_block + round((e.room_data.offset_z - i.room_data.offset_z)/TILEHEIGHT)):
                                    if e.room_data.area != i.room_data.area:
                                        i.room_data.area = e.room_data.area
                                        self.music_drop_down.setCurrentIndex(music_id.index(e.room_data.music))
                    if i.room_data.room_path == "ERoomPath::Right":
                        if e.room_data.offset_x == round(i.room_data.offset_x + i.room_data.width) and round(i.room_data.offset_z - e.room_data.height - TILEHEIGHT, 1) <= e.room_data.offset_z <= round(i.room_data.offset_z + i.room_data.height - TILEHEIGHT):
                            for o in e.room_data.door_flag:
                                if o.direction_part == Direction.LEFT and 0 == (o.z_block + round((e.room_data.offset_z - i.room_data.offset_z)/TILEHEIGHT)):
                                    if e.room_data.area != i.room_data.area:
                                        i.room_data.area = e.room_data.area
                                        self.music_drop_down.setCurrentIndex(music_id.index(e.room_data.music))
                if i.room_data.area == "EAreaID::None":
                    i.fill       = area_color[18]
                    i.fill_black = area_black[18]
                    i.fill_white = area_white[18]
                else:
                    i.fill       = area_color[int(i.room_data.area.split("::")[-1][1:3]) - 1]
                    i.fill_black = area_black[int(i.room_data.area.split("::")[-1][1:3]) - 1]
                    i.fill_white = area_white[int(i.room_data.area.split("::")[-1][1:3]) - 1]
                i.setBrush(QColor(i.fill[:1] + i.opacity + i.fill[1:]))
                for e in i.childItems():
                    if type(e) == QGraphicsRectItem:
                        e.setBrush(QColor(i.fill))
    
    def mouseDoubleClickEvent(self, event):
        if right_held or mid_held or x1_held or x2_held:
            return
        super().mouseDoubleClickEvent(event)
        #Select all rooms belonging to the same area
        if self.room_data.area != "EAreaID::None" and not assign_mode:
            for i in self.room_list:
                if i.room_data.area == self.room_data.area:
                    i.setSelected(True)

    def apply_round(self, item):
        #Snap room to grid
        x = round(item.pos().x() / TILEWIDTH) * TILEWIDTH
        y = round(item.pos().y() / TILEHEIGHT) * TILEHEIGHT
        #The train room's z offset must always be positive
        if item.room_data.name == "m09TRN_002" and y < 0 and restrictions:
            item.setPos(x, 0)
        else:
            item.setPos(x, y)
        item.room_data.offset_x = item.pos().x()
        item.room_data.offset_z = item.pos().y()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.unsaved = False
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
        self.view.setDragMode(QGraphicsView.RubberBandDrag)
        self.scene.installEventFilter(self)
        
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.scale(1, -1)
        self.current_zoom = 1
        self.setCentralWidget(self.view)
        
        #Menu
        
        bar = self.menuBar()
        file_bar = bar.addMenu("File")
        edit_bar = bar.addMenu("Edit")
        select_bar = bar.addMenu("Select")
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
        self.use_restr.setShortcut(QKeySequence(Qt.Key_F1))
        self.use_restr.triggered.connect(self.use_restr_action)
        self.use_restr.setChecked(True)
        edit_bar.addAction(self.use_restr)
        
        self.select_all = QAction("Select all", self)
        self.select_all.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_A))
        self.select_all.triggered.connect(self.select_all_action)
        select_bar.addAction(self.select_all)
        
        self.select_none = QAction("Deselect all", self)
        self.select_none.setShortcut(QKeySequence(Qt.SHIFT + Qt.CTRL + Qt.Key_A))
        self.select_none.triggered.connect(self.select_none_action)
        select_bar.addAction(self.select_none)
        
        self.select_invert = QAction("Invert selection", self)
        self.select_invert.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_I))
        self.select_invert.triggered.connect(self.select_invert_action)
        select_bar.addAction(self.select_invert)
        
        self.show_out = QAction("Show out-of-map rooms", self, checkable = True)
        self.show_out.setShortcut(QKeySequence(Qt.Key_F2))
        self.show_out.triggered.connect(self.show_out_action)
        view_bar.addAction(self.show_out)
        
        self.show_name = QAction("Show room names", self, checkable = True)
        self.show_name.setShortcut(QKeySequence(Qt.Key_F3))
        self.show_name.triggered.connect(self.show_name_action)
        view_bar.addAction(self.show_name)
        
        self.room_search = QAction("Room Search", self, checkable = True)
        self.room_search.setShortcut(QKeySequence(Qt.Key_S))
        self.room_search.triggered.connect(self.room_search_action)
        tool_bar.addAction(self.room_search)
        
        self.logic_editor = QAction("Logic Editor", self, checkable = True)
        self.logic_editor.setShortcut(QKeySequence(Qt.Key_L))
        self.logic_editor.triggered.connect(self.logic_editor_action)
        tool_bar.addAction(self.logic_editor)
        
        self.area_order = QAction("Area Order", self, checkable = True)
        self.area_order.setShortcut(QKeySequence(Qt.Key_O))
        self.area_order.triggered.connect(self.area_order_action)
        tool_bar.addAction(self.area_order)
        
        self.key_location = QAction("Key Locations", self, checkable = True)
        self.key_location.setShortcut(QKeySequence(Qt.Key_K))
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
        self.reverse.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_E))
        self.reverse.setIcon(QIcon("Data\\reverse_icon.png"))
        self.reverse.setToolTip("Toggle save/warp entrances\nShortcut: Ctrl + E")
        self.reverse.clicked.connect(self.reverse_action)
        self.reverse.setFixedSize(50, 30)
        
        self.swap = QPushButton()
        self.swap.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_T))
        self.swap.setIcon(QIcon("Data\\swap_icon.png"))
        self.swap.setToolTip("Toggle save/warp room type\nShortcut: Ctrl + T")
        self.swap.clicked.connect(self.swap_action)
        self.swap.setFixedSize(50, 30)
        
        self.duplicate = QPushButton()
        self.duplicate.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_D))
        self.duplicate.setIcon(QIcon("Data\\duplicate_icon.png"))
        self.duplicate.setToolTip("Duplicate a save/warp/transition room\nShortcut: Ctrl + D")
        self.duplicate.clicked.connect(self.duplicate_action)
        self.duplicate.setFixedSize(50, 30)
        
        self.delete = QPushButton()
        self.delete.setShortcut(QKeySequence(Qt.Key_Delete))
        self.delete.setIcon(QIcon("Data\\delete_icon.png"))
        self.delete.setToolTip("Delete/tag room as unused\nShortcut: Del")
        self.delete.clicked.connect(self.delete_action)
        self.delete.setFixedSize(50, 30)
        
        self.zoom_in = QPushButton()
        self.zoom_in.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_Plus))
        self.zoom_in.setIcon(QIcon("Data\\in_icon.png"))
        self.zoom_in.setToolTip("Zoom in\nShortcut: Ctrl + Plus")
        self.zoom_in.clicked.connect(self.zoom_in_action)
        self.zoom_in.setFixedSize(50, 30)
        
        self.zoom_out = QPushButton()
        self.zoom_out.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_Minus))
        self.zoom_out.setIcon(QIcon("Data\\out_icon.png"))
        self.zoom_out.setToolTip("Zoom out\nShortcut: Ctrl + Minus")
        self.zoom_out.clicked.connect(self.zoom_out_action)
        self.zoom_out.setFixedSize(50, 30)
        self.zoom_out.setEnabled(False)
        
        #Labels
        
        self.lock_label = QLabel()
        self.lock_label.setPixmap(QPixmap("Data\\lock_icon.png"))
        
        self.seed_label = QLabel()
        self.seed_label.setVisible(False)
        retain = self.seed_label.sizePolicy()
        retain.setRetainSizeWhenHidden(True)
        self.seed_label.setSizePolicy(retain)
        
        #Drop down lists
        
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
        
        #List widgets
        
        list_layout = QVBoxLayout()
        
        self.room_search_list = QListWidget()
        self.room_search_list.currentItemChanged.connect(self.room_search_list_change)
        self.room_search_list.setVisible(False)
        retain = self.room_search_list.sizePolicy()
        retain.setRetainSizeWhenHidden(True)
        self.room_search_list.setSizePolicy(retain)
        list_layout.addWidget(self.room_search_list)
        
        self.area_order_list = QListWidget()
        self.area_order_list.currentItemChanged.connect(self.area_order_list_change)
        self.area_order_list.setDragDropMode(QAbstractItemView.InternalMove)
        self.area_order_list.setVisible(False)
        retain = self.area_order_list.sizePolicy()
        retain.setRetainSizeWhenHidden(True)
        self.area_order_list.setSizePolicy(retain)
        list_layout.addWidget(self.area_order_list)
        
        #Boxes
        
        gate_box_layout = QVBoxLayout()
        self.gate_box = QGroupBox()
        self.gate_box.setLayout(gate_box_layout)
        self.gate_box.setVisible(False)
        retain = self.gate_box.sizePolicy()
        retain.setRetainSizeWhenHidden(True)
        self.gate_box.setSizePolicy(retain)
        
        #Box content
        
        self.gate_toggle = QPushButton("Gate Toggle")
        self.gate_toggle.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_G))
        self.gate_toggle.setToolTip("Toggle whether selected room is a gate or not.\nShortcut: Ctrl + G")
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
        self.assign_mode.setShortcut(QKeySequence(Qt.CTRL + Qt.Key_B))
        self.assign_mode.setToolTip("Select gates to assign to selected room in this mode.\nShortcut: Ctrl + B")
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
        hbox_top.addWidget(self.seed_label)
        hbox_top.addStretch(1)
        hbox_top.addWidget(self.music_drop_down)
        hbox_top.addWidget(self.play_drop_down)
        
        hbox_center = QHBoxLayout()
        hbox_center.addWidget(self.gate_box)
        hbox_center.addStretch(1)
        hbox_center.addLayout(list_layout)
        
        hbox_bottom = QHBoxLayout()
        hbox_bottom.addWidget(self.reverse)
        hbox_bottom.addWidget(self.swap)
        hbox_bottom.addWidget(self.duplicate)
        hbox_bottom.addWidget(self.delete)
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
    
    def eventFilter(self, obj, event):
        #Try to prevent holding several mouse buttons at once as that can cause major glitches
        global right_held
        global mid_held
        global x1_held
        global x2_held
        if event.type() in [QEvent.GraphicsSceneMousePress, QEvent.GraphicsSceneMouseDoubleClick]:
            if event.button() == Qt.LeftButton and not right_held and not mid_held and not x1_held and not x2_held:
                self.view.setDragMode(QGraphicsView.RubberBandDrag)
            if event.button() == Qt.RightButton:
                self.view.setDragMode(QGraphicsView.NoDrag)
                right_held = True
            if event.button() == Qt.MiddleButton:
                self.view.setDragMode(QGraphicsView.NoDrag)
                mid_held = True
            if event.button() == Qt.XButton1:
                self.view.setDragMode(QGraphicsView.NoDrag)
                x1_held = True
            if event.button() == Qt.XButton2:
                self.view.setDragMode(QGraphicsView.NoDrag)
                x2_held = True
        elif event.type() == QEvent.GraphicsSceneMouseRelease:
            if event.button() == Qt.LeftButton and not right_held and not mid_held and not x1_held and not x2_held:
                self.view.setDragMode(QGraphicsView.NoDrag)
            if event.button() == Qt.RightButton:
                right_held = False
            if event.button() == Qt.MiddleButton:
                mid_held = False
            if event.button() == Qt.XButton1:
                x1_held = False
            if event.button() == Qt.XButton2:
                x2_held = False
        return super().eventFilter(obj, event)
    
    def closeEvent(self, event):
        if self.safety_save():
            event.accept()
        else:
            event.ignore()
    
    def safety_save(self):
        #Before closing the current map prompt a safety save message
        if self.unsaved:
            choice = QMessageBox.question(self, "Save", "Save current map ?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if choice == QMessageBox.Yes:
                if not self.save_file():
                    return False
            if choice == QMessageBox.Cancel:
                return False
        return True
    
    def open_file(self):
        if not self.safety_save():
            return
        self.path = (QFileDialog.getOpenFileName(parent=self, caption="Open", dir="Custom", filter="*.json"))[0]
        if self.path:
            self.string = self.path
            self.title_string = " (" + self.string + ")"
            self.load_from_json(self.string)
            self.direct_save = True

    def save_file(self):
        if self.direct_save:
            self.save_to_json(self.string)
            return True
        else:
            return self.save_file_as()

    def save_file_as(self):
        self.path = (QFileDialog.getSaveFileName(parent=self, caption="Save as", dir="Custom", filter="*.json"))[0]
        if self.path:
            self.string = self.path
            self.title_string = " (" + self.string + ")"
            self.save_to_json(self.string)
            self.direct_save = True
            return True
        return False

    def reset(self):
        if not self.safety_save():
            return
        self.string = "Data/RoomMaster/PB_DT_RoomMaster.json"
        self.title_string = ""
        self.load_from_json(self.string)
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
    
    def select_all_action(self):
        for i in self.room_list:
            i.setSelected(True)
    
    def select_none_action(self):
        for i in self.room_list:
            i.setSelected(False)
    
    def select_invert_action(self):
        for i in self.room_list:
            if i.isSelected():
                i.setSelected(False)
            else:
                i.setSelected(True)
    
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
        global search_mode
        if self.room_search.isChecked():
            search_mode = True
            #Disable other tools
            self.logic_editor.setChecked(False)
            self.logic_editor_action()
            self.area_order.setChecked(False)
            self.area_order_action()
            self.key_location.setChecked(False)
            self.key_location_action()
            #Disable menu options
            self.use_restr.setEnabled(False)
            self.select_all.setEnabled(False)
            self.select_none.setEnabled(False)
            self.select_invert.setEnabled(False)
            #Initiate
            self.disable_buttons()
            for i in self.room_list:
                i.setSelected(False)
                i.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)
            self.room_search_list.setCurrentItem(self.room_search_list.item(0))
            self.room_search_list_change(self.room_search_list.item(0))
            self.room_search_list.setVisible(True)
        else:
            search_mode = False
            self.enable_buttons()
            self.use_restr.setEnabled(True)
            self.select_all.setEnabled(True)
            self.select_none.setEnabled(True)
            self.select_invert.setEnabled(True)
            self.room_search_list.setVisible(False)
            self.reset_room()
    
    def logic_editor_action(self):
        global logic_mode
        if self.logic_editor.isChecked():
            #Disable other tools
            self.room_search.setChecked(False)
            self.room_search_action()
            self.area_order.setChecked(False)
            self.area_order_action()
            self.key_location.setChecked(False)
            self.key_location_action()
            #Disable menu options
            self.use_restr.setEnabled(False)
            self.select_all.setEnabled(False)
            self.select_none.setEnabled(False)
            self.select_invert.setEnabled(False)
            self.show_out.setChecked(False)
            self.show_out.setEnabled(False)
            #Initiate
            self.disable_buttons()
            for i in self.room_list:
                i.setSelected(False)
                i.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)
                if i.logic_data == None:
                    i.setVisible(False)
            logic_mode = True
            self.selection_event()
            self.gate_box.setVisible(True)
        else:
            logic_mode = False
            self.enable_buttons()
            self.use_restr.setEnabled(True)
            self.select_all.setEnabled(True)
            self.select_none.setEnabled(True)
            self.select_invert.setEnabled(True)
            self.show_out.setEnabled(True)
            self.assign_mode.setChecked(False)
            self.assign_mode_action()
            self.gate_box.setVisible(False)
            self.reset_room()
    
    def area_order_action(self):
        global area_mode
        if self.area_order.isChecked():
            area_mode = True
            #Disable other tools
            self.room_search.setChecked(False)
            self.room_search_action()
            self.logic_editor.setChecked(False)
            self.logic_editor_action()
            self.key_location.setChecked(False)
            self.key_location_action()
            #Disable menu options
            self.use_restr.setEnabled(False)
            self.select_all.setEnabled(False)
            self.select_none.setEnabled(False)
            self.select_invert.setEnabled(False)
            #Initiate
            self.disable_buttons()
            for i in self.room_list:
                i.setSelected(False)
                i.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)
            self.area_order_list.setCurrentItem(self.area_order_list.item(0))
            self.area_order_list_change(self.area_order_list.item(0))
            self.area_order_list.setVisible(True)
        else:
            area_mode = False
            self.enable_buttons()
            self.use_restr.setEnabled(True)
            self.select_all.setEnabled(True)
            self.select_none.setEnabled(True)
            self.select_invert.setEnabled(True)
            self.area_order_list.setVisible(False)
            self.reset_room()
    
    def key_location_action(self):
        global key_mode
        if self.key_location.isChecked():
            #Disable other tools
            self.room_search.setChecked(False)
            self.room_search_action()
            self.logic_editor.setChecked(False)
            self.logic_editor_action()
            self.area_order.setChecked(False)
            self.area_order_action()
            #CheckLog
            name, extension = os.path.splitext(self.string)
            box = QMessageBox(self)
            box.setWindowTitle("Error")
            box.setIcon(QMessageBox.Critical)
            try:
                log_path = os.path.abspath(os.path.join("", os.pardir)) + "\\SpoilerLog\\KeyLocation.json"
                with open(log_path, "r", encoding="utf8") as file_reader:
                    self.log = json.load(file_reader)
                if not self.log["Map"] and name.split("/")[-1] != "PB_DT_RoomMaster":
                    box.setText("Current key location is meant for the default map.")
                    box.exec()
                    self.key_location.setChecked(False)
                    self.key_location_action()
                    return
                elif self.log["Map"] and name.split("/")[-1] != self.log["Map"]:
                    box.setText("Current key location is meant for map " + self.log["Map"] + ".")
                    box.exec()
                    self.key_location.setChecked(False)
                    self.key_location_action()
                    return
                self.seed_label.setText(str(self.log["Seed"]))
            except FileNotFoundError:
                box.setText("No key log found.")
                box.exec()
                self.key_location.setChecked(False)
                self.key_location_action()
                return
            key_mode = True
            #Disable menu options
            self.use_restr.setEnabled(False)
            self.select_all.setEnabled(False)
            self.select_none.setEnabled(False)
            self.select_invert.setEnabled(False)
            self.show_out.setChecked(True)
            self.show_out_action()
            self.show_out.setEnabled(False)
            #Fill information
            self.key_drop_down.clear()
            for i in self.log["Key"]:
                self.key_drop_down.addItem(i)
            #Initiate
            self.disable_buttons()
            for i in self.room_list:
                i.setSelected(False)
                i.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)
            self.key_drop_down.setCurrentIndex(0)
            self.key_drop_down_change(0)
            self.key_drop_down.setVisible(True)
            self.seed_label.setVisible(True)
        else:
            key_mode = False
            self.enable_buttons()
            self.use_restr.setEnabled(True)
            self.select_all.setEnabled(True)
            self.select_none.setEnabled(True)
            self.select_invert.setEnabled(True)
            self.show_out.setEnabled(True)
            self.key_drop_down.setVisible(False)
            self.seed_label.setVisible(False)
            self.reset_room()
    
    def how_to(self):
        box = QMessageBox(self)
        box.setWindowTitle("How to use")
        box.setText("Map Editor:\n\nThis editor allows you to fully customize the layout of the game's map. You can click and drag each room to change its location on the grid and you can select entire areas by double-clicking one of its rooms.\nSave your creations to the Custom folder for them to be picked by the randomizer.\n\nLogic Editor:\n\nOnce you've finished laying out a map you can use the logic editor tool to guide the randomizer in its key item placement to prevent unbeatable seeds on your map.\nEach gate represents a room that is an obstacle to the player's progression which must be connected to other previous gates and linked to the rooms that it leads to.\nThe randomizer will look for the first set of gates at the start of the game then move onto the next and so on until every key item is placed based on this consecution of requirements.\nBy default the list of requirements checks for x OR y items, to create a check for x AND y items simply chain several gates back to back.\nThe graphical cues of this mode are:\n\n-Dark fill: standard non-gate rooms\n-White fill: Gate rooms that selected room is connected to\n-Blue outline: rooms that have no requirement to get to\n-Green outline: rooms that are connected to selected gate\n-Red outline: rooms that are being assigned a gate in assign mode\n\nArea Order:\n\nA simple tool that lets you reorder the difficulty scaling of each area. Try to arrange these in the order that the player will most likely traverse them.\n\nYou can submit your own layout creations to me on Discord (Lakifume#4066) if you want them to be added as presets in the main download of the randomizer.")
        box.exec()
    
    def guidelines(self):
        box = QMessageBox(self)
        box.setWindowTitle("Map guidelines")
        box.setText("Here are some tips that will help you build maps that are fun to play on:\n\n-making use of as many rooms as possible\n-connecting as many entrances as possible\n-keeping each area separated using transition rooms\n-ensuring that boss rooms are placed relatively close to a save/warp point\n-having the \"Use restrictions\" option enabled while building your map\n-not overlapping any rooms except for the semi-transparent ones\n\nAdditionally here are some useful things to know when building maps:\n\n-backer rooms can be connected to any area and will be automatically updated\n-transition rooms that are connected directly into a submerged room can only be entered if the player has Deep Sinker\n-a few bosses can softlock if their rooms are placed in undesirable spots, refer to the Boss restrictions page for more info\n-room m03ENT_1200 has a transition that does not work properly when connected to a different room, so the randomizer script will ignore this room when connecting the map")
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
            if i.room_data.room_type in ["ERoomType::Save", "ERoomType::Warp"]:
                if i.room_data.room_path == "ERoomPath::Left":
                    i.room_data.room_path = "ERoomPath::Right"
                    i.room_data.door_flag = self.convert_flag_to_door([1, 4], i.room_data.width)
                    i.childItems()[1].setVisible(False)
                    i.childItems()[2].setVisible(True)
                elif i.room_data.room_path == "ERoomPath::Right":
                    i.room_data.room_path = "ERoomPath::Both"
                    i.room_data.door_flag = self.convert_flag_to_door([1, 5], i.room_data.width)
                    i.childItems()[1].setVisible(True)
                    i.childItems()[2].setVisible(True)
                elif i.room_data.room_path == "ERoomPath::Both":
                    i.room_data.room_path = "ERoomPath::Left"
                    i.room_data.door_flag = self.convert_flag_to_door([1, 1], i.room_data.width)
                    i.childItems()[1].setVisible(True)
                    i.childItems()[2].setVisible(False)
    
    def swap_action(self):
        for i in self.scene.selectedItems():
            if i.room_data.room_type == "ERoomType::Save":
                i.room_data.room_type = "ERoomType::Warp"
                i.childItems()[0].setPixmap(QPixmap("Data\\warp.png"))
            elif i.room_data.room_type == "ERoomType::Warp":
                i.room_data.room_type = "ERoomType::Save"
                i.childItems()[0].setPixmap(QPixmap("Data\\save.png"))
    
    def duplicate_action(self):
        for i in self.scene.selectedItems():
            i.setSelected(False)
            if i.room_data.room_type in ["ERoomType::Save", "ERoomType::Warp", "ERoomType::Load"]:
                #Determine the new room name with an inst number that isn't taken
                taken_inst = []
                for e in self.room_list:
                    current_inst = int(e.room_data.name.split("_")[-1])
                    if e.room_data.area == i.room_data.area and current_inst//100 == 13:
                        taken_inst.append(current_inst)
                taken_inst.sort()
                if taken_inst:
                    max_inst = taken_inst[-1]
                else:
                    max_inst = 1300
                for e in range(1300, max_inst + 2):
                    if not e in taken_inst:
                        new_inst = e
                        break
                if new_inst >= 1400:
                    return
                room_data = copy.deepcopy(i.room_data)
                room_data.name = room_data.area.split("::")[-1] + "_" + str(new_inst)
                room_data.offset_x = i.room_data.offset_x + TILEWIDTH
                room_data.offset_z = i.room_data.offset_z - TILEHEIGHT
                room = RoomItem(len(self.room_list), room_data, None, i.outline, i.fill, i.fill_black, i.fill_white, i.opacity, i.icon_color, True, [], self.room_list, self.music_drop_down)
                self.scene.addItem(room)
                self.room_list.append(room)
                self.add_room_items(room)
                self.room_search_list.addItem(room_data.name)
                self.json_file["MapData"][room.room_data.name] = copy.deepcopy(self.json_file["MapData"][i.room_data.name])
                self.use_restr_action()
                self.show_out_action()
                self.show_name_action()
                room.setSelected(True)
    
    def delete_action(self):
        #Only truly delete rooms that were previously added by the user
        #For vanilla rooms just tag them as unused
        for i in self.scene.selectedItems():   
            current_inst = int(i.room_data.name.split("_")[-1])
            if current_inst//100 == 13:
                self.scene.removeItem(i)
                self.room_list.remove(i)
                self.room_search_list.takeItem(self.room_search_list.row(self.room_search_list.findItems(i.room_data.name, Qt.MatchExactly)[0]))
                del self.json_file["MapData"][i.room_data.name]
            elif i.room_data.room_type == "ERoomType::Normal" and not i.room_data.out_of_map:
                if i.room_data.unused:
                    i.room_data.unused = False
                    i.outline.setColor("#ffffff")
                    i.setPen(i.outline)
                else:
                    i.room_data.unused = True
                    i.outline.setColor("#000000")
                    i.setPen(i.outline)
        self.show_out_action()
    
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
    
    def room_search_list_change(self, item):
        for i in self.room_list:
            self.fill_room(i, "#000000")
        i = self.room_list[self.room_search_list.currentRow()]
        self.reveal_room(i)
    
    def area_order_list_change(self, item):
        #Unsaved tag
        if not self.unsaved:
            self.change_title("*")
            self.unsaved = True
        #Color rooms
        for i in self.room_list:
            if i.room_data.area == "EAreaID::" + item.text():
                self.reveal_room(i)
            else:
                self.fill_room(i, "#000000")
        i.setSelected(True)
    
    def key_drop_down_change(self, index):
        for i in self.room_list:
            if i.room_data.name in self.log["Key"][self.key_drop_down.itemText(index)]:
                self.reveal_room(i)
            else:
                self.fill_room(i, "#000000")
    
    def music_drop_down_change(self, index):
        for i in self.scene.selectedItems():
            i.room_data.music = music_id[index]
    
    def play_drop_down_change(self, index):
        for i in self.scene.selectedItems():
            i.room_data.play = play_id[index]
    
    def fill_room(self, i, color):
        if color == "#000000":
            i.setBrush(QColor(i.fill_black[:1] + i.opacity + i.fill_black[1:]))
            for e in i.childItems():
                if type(e) == QGraphicsRectItem:
                    e.setBrush(QColor(i.fill_black))
        elif color == "#ffffff":
            i.setBrush(QColor(i.fill_white[:1] + i.opacity + i.fill_white[1:]))
            for e in i.childItems():
                if type(e) == QGraphicsRectItem:
                    e.setBrush(QColor(i.fill_white))
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
        if color == "#ffffff" and i.room_data.unused:
            i.outline.setColor("#000000")
        else:
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
        if not i.can_move and restrictions:
            i.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)
        else:
            i.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable | QGraphicsItem.ItemIsMovable)
    
    def change_title(self, suffix):
        self.setWindowTitle(script_name + self.title_string + suffix)
    
    def selection_event(self):
        #Assign mode selection
        if assign_mode:
            self.assign_selection_event()
        #Logic editor selection
        elif logic_mode:
            self.logic_selection_event()
        #Normal editor selection
        else:
            self.normal_selection_event()

    def normal_selection_event(self):
        #Unsaved tag
        if not self.unsaved:
            self.change_title("*")
            self.unsaved = True
        #Layer change
        for i in self.room_list:
            if i.isSelected():
                i.setZValue(74 - (i.room_data.width/TILEWIDTH)*(i.room_data.height/TILEHEIGHT))
            else:
                i.setZValue(0 - (i.room_data.width/TILEWIDTH)*(i.room_data.height/TILEHEIGHT))
        #Display music drop down
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
        #Unsaved tag
        if not self.unsaved:
            self.change_title("*")
            self.unsaved = True
        #Update gates
        for i in self.room_list:
            if i.logic_data == None:
                continue
            self.fill_room(i, "#000000")
            self.outline_room(i, "#ffffff")
            if i.logic_data.is_gate:
                self.reveal_room(i)
        #Layer change
        for i in self.room_list:
            if i.isSelected():
                i.setZValue(74 - (i.room_data.width/TILEWIDTH)*(i.room_data.height/TILEHEIGHT))
            else:
                i.setZValue(0 - (i.room_data.width/TILEWIDTH)*(i.room_data.height/TILEHEIGHT))
        #Outline gated rooms
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
        #Nothing selected
        if not self.scene.selectedItems():
            self.gate_toggle.setEnabled(False)
            self.disable_checkboxes()
            self.uncheck_checkboxes()
            self.assign_mode.setEnabled(False)
        #One selected
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
        #Multiple selected
        else:
            self.gate_toggle.setEnabled(False)
            self.disable_checkboxes()
            self.uncheck_checkboxes()
            self.assign_mode.setEnabled(True)
            for i in self.scene.selectedItems():
                if i.index == 0:
                    self.assign_mode.setEnabled(False)
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
        self.selection_event()
    
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
            assign_list.clear()
            self.selection_event()
    
    def unassign_all_action(self):
        for i in self.room_list:
            if i.logic_data == None:
                continue
            i.logic_data.gate_list.clear()
        self.room_list[0].setSelected(True)
        self.selection_event()
    
    def enable_buttons(self):
        self.reverse.setEnabled(True)
        self.swap.setEnabled(True)
        self.duplicate.setEnabled(True)
        self.delete.setEnabled(True)
        self.music_drop_down.setEnabled(True)
        self.play_drop_down.setEnabled(True)
    
    def disable_buttons(self):
        self.reverse.setEnabled(False)
        self.swap.setEnabled(False)
        self.duplicate.setEnabled(False)
        self.delete.setEnabled(False)
        self.music_drop_down.setEnabled(False)
        self.play_drop_down.setEnabled(False)
    
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
        self.area_order_list.clear()
        self.room_list = []
        self.change_title("")
        #Open main
        with open(filename, "r", encoding="utf8") as file_reader:
            self.json_file = json.load(file_reader)
        #Process
        self.draw_map()
        self.fill_area()
        self.use_restr_action()
        self.show_out_action()
        self.show_name_action()
        if self.room_search.isChecked():
            self.room_search_action()
        if self.logic_editor.isChecked():
            self.logic_editor_action()
        if self.area_order.isChecked():
            self.area_order_action()
        if self.key_location.isChecked():
            self.key_location_action()
        self.selection_event()
        #Finalize
        self.unsaved = False
    
    def save_to_json(self, filename):
        self.update_offsets()
        self.update_logic()
        self.update_order()
        with open(filename, "w", encoding="utf8") as file_writer:
            file_writer.write(json.dumps(self.json_file, indent=2))
        self.change_title("")
        self.unsaved = False
    
    def convert_json_to_room(self, name, json):
        area = json["AreaID"]
        out_of_map = json["OutOfMap"]
        room_type = json["RoomType"]
        room_path = json["RoomPath"]
        width = json["AreaWidthSize"] * TILEWIDTH
        height = json["AreaHeightSize"] * TILEHEIGHT
        offset_x = round(json["OffsetX"]/12.6) * TILEWIDTH
        offset_z = round(json["OffsetZ"]/7.2) * TILEHEIGHT 
        door_flag = self.convert_flag_to_door(json["DoorFlag"], round(width/TILEWIDTH))
        no_traverse = self.convert_no_traverse_to_block(json["NoTraverse"], round(width/TILEWIDTH))
        music = json["BgmID"]
        play = json["BgmType"]
        unused = json["Unused"]
        
        room = Room(name, area, out_of_map, room_type, room_path, width, height, offset_x, offset_z, door_flag, no_traverse, music, play, unused)
        return room
    
    def convert_json_to_logic(self, json):
        is_gate = json["GateRoom"]
        gate_list = self.convert_gate_to_index(json["NearestGate"])
        double_jump = json["Doublejump"]
        high_jump = json["HighJump"]
        invert = json["Invert"]
        deepsinker = json["Deepsinker"]
        dimension_shift = json["Dimensionshift"]
        reflector_ray = json["Reflectionray"]
        aqua_stream = json["Aquastream"]
        blood_steal = json["Bloodsteel"]
        zangetsuto = json["Swordsman"]
        silver_bromide = json["Silverbromide"]
        aegis_plate = json["BreastplateofAguilar"]
        carpenter = json["Keyofbacker1"]
        warhorse = json["Keyofbacker2"]
        millionaire = json["Keyofbacker3"]
        celeste = json["Keyofbacker4"]
        
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
                    breakable = (direction & (direction_part.value << 16)) != 0
                    door = Door(x_block, z_block, direction_part, breakable)
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
        index = 0
        for i in self.json_file["MapData"]:
            if i in group_list:
                new_group_list.append(index)
            index += 1
        return new_group_list
    
    def convert_gate_to_index(self, gate_list):
        new_gate_list = []
        index = 0
        for i in self.json_file["MapData"]:
            if i in gate_list:
                new_gate_list.append(index)
            index += 1
        return new_gate_list
    
    def convert_index_to_gate(self, gate_list):
        new_gate_list = []
        for i in self.room_list:
            if i.index in gate_list:
                new_gate_list.append(i.room_data.name)
        return new_gate_list
    
    def draw_map(self):
        outline = QPen("#ffffff")
        outline.setWidth(OUTLINE)
        outline.setJoinStyle(Qt.MiterJoin)
        
        #Map origin
        
        origin_horizontal = self.scene.addLine(-(TILEHEIGHT/2 - 1.5), 0.0, TILEHEIGHT/2 - 1.5, 0.0)
        origin_horizontal.setPen(outline)
        origin_vertical = self.scene.addLine(0.0, TILEHEIGHT/2 - 1.5, 0.0, -(TILEHEIGHT/2 - 1.5))
        origin_vertical.setPen(outline)
        
        #Map boundary
        
        bound_1_horizontal = self.scene.addLine(-256*TILEWIDTH, -32*TILEHEIGHT, -256*TILEWIDTH + (TILEHEIGHT/2 - 1.5), -32*TILEHEIGHT)
        bound_1_horizontal.setPen(outline)
        bound_1_vertical = self.scene.addLine(-256*TILEWIDTH, -32*TILEHEIGHT + (TILEHEIGHT/2 - 1.5), -256*TILEWIDTH, -32*TILEHEIGHT)
        bound_1_vertical.setPen(outline)
        
        bound_2_horizontal = self.scene.addLine(256*TILEWIDTH - (TILEHEIGHT/2 - 1.5), 128*TILEHEIGHT, 256*TILEWIDTH, 128*TILEHEIGHT)
        bound_2_horizontal.setPen(outline)
        bound_2_vertical = self.scene.addLine(256*TILEWIDTH, 128*TILEHEIGHT, 256*TILEWIDTH, 128*TILEHEIGHT - (TILEHEIGHT/2 - 1.5))
        bound_2_vertical.setPen(outline)
        
        index = 0
        for i in self.json_file["MapData"]:
            
            #Converting data
            
            room_data = self.convert_json_to_room(i, self.json_file["MapData"][i])
            try:
                logic_data = self.convert_json_to_logic(self.json_file["KeyLogic"][i])
            except KeyError:
                logic_data = None
            self.room_search_list.addItem(room_data.name)
            group_list = []
            can_move = True
            
            #No width rooms
            
            if room_data.width == 0:
                room_data.width = TILEWIDTH/2
            if room_data.height == 0:
                room_data.height = TILEHEIGHT/2
            
            #Area color
            
            if room_data.out_of_map:
                fill = area_color[18]
                fill_black = area_black[18]
                fill_white = area_white[18]
            else:
                fill = area_color[int(room_data.area.split("::")[-1][1:3]) - 1]
                fill_black = area_black[int(room_data.area.split("::")[-1][1:3]) - 1]
                fill_white = area_white[int(room_data.area.split("::")[-1][1:3]) - 1]
            
            #Room outline
            
            if room_data.unused:
                outline = "#000000"
            else:
                outline = "#ffffff"
            
            #Room group
            
            for e in connected_room:
                if room_data.name in e["Room"]:
                    group_list = e["Room"]
                    can_move = e["CanMove"]
                    break
            
            #Room opacity
            
            if room_data.room_type == "ERoomType::Load"or room_data.name == "m02VIL_000":
                opacity = "80"
            else:
                opacity = "ff"
            
            icon_color = 0
            
            #Creating room
            
            room = RoomItem(index, room_data, logic_data, outline, fill, fill_black, fill_white, opacity, icon_color, can_move, self.convert_group_to_index(group_list), self.room_list, self.music_drop_down)
            self.scene.addItem(room)
            self.room_list.append(room)
            self.add_room_items(room)
            
            index += 1
            
    def add_room_items(self, room):
        outline = QPen("#00000000")
        outline.setWidth(OUTLINE)
        outline.setJoinStyle(Qt.MiterJoin)
        
        #Icons
        
        if room.room_data.room_type == "ERoomType::Save":
            icon = self.scene.addPixmap(QPixmap("Data\\save.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width/2 - 6, room.room_data.height/2 + TILEHEIGHT/2 - 1.5)
            icon.setParentItem(room)
        if room.room_data.room_type == "ERoomType::Warp":
            icon = self.scene.addPixmap(QPixmap("Data\\warp.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width/2 - 6, room.room_data.height/2 + TILEHEIGHT/2 - 1.5)
            icon.setParentItem(room)
        if room.room_data.name in boss_room:
            icon = self.scene.addPixmap(QPixmap("Data\\boss.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width/2 - 6, room.room_data.height/2 + TILEHEIGHT/2 - 1.5)
            icon.setParentItem(room)
        if int(room.room_data.name[1:3]) == 88:
            icon = self.scene.addPixmap(QPixmap("Data\\key.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width/2 - 6, room.room_data.height/2 + TILEHEIGHT/2 - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m01SIP_000":
            icon = self.scene.addPixmap(QPixmap("Data\\start.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width/2 - 6, room.room_data.height/2 + TILEHEIGHT/2 - 1.5)
            icon.setParentItem(room)
        if room.room_data.name in ["m04GDN_001", "m10BIG_000"]:
            icon = self.scene.addPixmap(QPixmap("Data\\portal.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width/2 - 6, room.room_data.height/2 + TILEHEIGHT/2 - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m05SAN_006":
            icon = self.scene.addPixmap(QPixmap("Data\\barber.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width/2 - 6, room.room_data.height/2 + TILEHEIGHT/2 - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m06KNG_021":
            icon = self.scene.addPixmap(QPixmap("Data\\flame.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width/2 - 6, room.room_data.height/2 + TILEHEIGHT/2 - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m07LIB_009":
            icon = self.scene.addPixmap(QPixmap("Data\\book.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width/2 - 6, room.room_data.height/2 + TILEHEIGHT/2 - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m19K2C_000":
            icon = self.scene.addPixmap(QPixmap("Data\\crown.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width/2 - 6, room.room_data.height/2 + TILEHEIGHT/2 - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m51EBT_000":
            icon = self.scene.addPixmap(QPixmap("Data\\8bit.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width/2 - 6, room.room_data.height/2 + TILEHEIGHT/2 - 1.5)
            icon.setParentItem(room)
        if room.room_data.name in ["m09TRN_001", "m09TRN_004"]:
            icon = self.scene.addPixmap(QPixmap("Data\\gate.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width/2 - 6, room.room_data.height/2 + TILEHEIGHT/2 - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m03ENT_1200":
            icon = self.scene.addPixmap(QPixmap("Data\\cross.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width/2 - 6, room.room_data.height/2 + TILEHEIGHT/2 - 1.5)
            icon.setParentItem(room)
        
        #Wall
        
        if room.room_data.name == "m03ENT_000":
            icon = self.scene.addPixmap(QPixmap("Data\\spike_opening.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width/2 - 6, TILEHEIGHT*13 - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m03ENT_007":
            icon = self.scene.addPixmap(QPixmap("Data\\one_way_left.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width - 13.5, TILEHEIGHT - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m05SAN_003":
            icon = self.scene.addPixmap(QPixmap("Data\\wall_horizontal.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width/2 - 6, TILEHEIGHT*8 + 6)
            icon.setParentItem(room)
        if room.room_data.name == "m05SAN_009":
            icon = self.scene.addPixmap(QPixmap("Data\\one_way_down.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width/2 - 6, TILEHEIGHT*4 + 11)
            icon.setParentItem(room)
        if room.room_data.name == "m05SAN_017":
            icon = self.scene.addPixmap(QPixmap("Data\\one_way_left.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width/2 - 1, TILEHEIGHT - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m05SAN_019":
            icon = self.scene.addPixmap(QPixmap("Data\\one_way_left.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(TILEWIDTH - 23.5, TILEHEIGHT - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m05SAN_021":
            icon = self.scene.addPixmap(QPixmap("Data\\one_way_right.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width - 13.5, room.room_data.height - TILEHEIGHT*2 - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m06KNG_013":
            icon = self.scene.addPixmap(QPixmap("Data\\one_way_right.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width - 13.5, TILEHEIGHT - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m07LIB_005":
            icon = self.scene.addPixmap(QPixmap("Data\\one_way_down.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width -18.5, TILEHEIGHT - 1.5)
            icon.setParentItem(room)
        if room.room_data.name in ["m07LIB_006", "m11UGD_045"]:
            icon = self.scene.addPixmap(QPixmap("Data\\hole.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width/2 - 6, TILEHEIGHT - 1.5)
            icon.setParentItem(room)
        if room.room_data.name in ["m07LIB_008", "m07LIB_014", "m11UGD_016", "m18ICE_016"]:
            icon = self.scene.addPixmap(QPixmap("Data\\hole.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width - 8.5, room.room_data.height - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m07LIB_021":
            icon = self.scene.addPixmap(QPixmap("Data\\one_way_down.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width/2 - 6, room.room_data.height - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m07LIB_023":
            icon = self.scene.addPixmap(QPixmap("Data\\one_way_left.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width - 11.5, TILEHEIGHT*3 - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m07LIB_035" or room.room_data.name == "m11UGD_056":
            icon = self.scene.addPixmap(QPixmap("Data\\opening.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width/2 - 6, TILEHEIGHT*3 - 9)
            icon.setParentItem(room)
        if room.room_data.name == "m09TRN_003":
            icon = self.scene.addPixmap(QPixmap("Data\\one_way_right.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width - 13.5, TILEHEIGHT - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m08TWR_009":
            icon = self.scene.addPixmap(QPixmap("Data\\one_way_left.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width - 11.5, TILEHEIGHT*11 - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m11UGD_015":
            icon = self.scene.addPixmap(QPixmap("Data\\one_way_right.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width/2 - 11, TILEHEIGHT - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m11UGD_046":
            icon = self.scene.addPixmap(QPixmap("Data\\hole_left.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(1.5, room.room_data.height - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m11UGD_056":
            icon = self.scene.addPixmap(QPixmap("Data\\wall_vertical.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width - 8.5, room.room_data.height - 1.5)
            icon.setParentItem(room)
        if room.room_data.name in ["m15JPN_010", "m17RVA_005"]:
            icon = self.scene.addPixmap(QPixmap("Data\\ceiling_hole.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width - 13.5, room.room_data.height - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m17RVA_003":
            icon = self.scene.addPixmap(QPixmap("Data\\ceiling_hole_right.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width - 13.5, room.room_data.height - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m18ICE_015":
            icon = self.scene.addPixmap(QPixmap("Data\\wall_vertical.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width/2 - 6, TILEHEIGHT - 1.5)
            icon.setParentItem(room)
        
        #Water
        
        if room.room_data.name in ["m11UGD_021", "m11UGD_022", "m11UGD_023", "m11UGD_024", "m11UGD_025", "m11UGD_026", "m11UGD_044", "m11UGD_045"]:
            for e in range(round(room.room_data.width/TILEWIDTH)):
                for o in range(round(room.room_data.height/TILEHEIGHT)):
                    icon = self.scene.addPixmap(QPixmap("Data\\bubble.png"))
                    icon.setTransform(QTransform.fromScale(1, -1))
                    icon.setPos(e*TILEWIDTH + 6, o*TILEHEIGHT + 13.5)
                    icon.setParentItem(room)
        if room.room_data.name in ["m11UGD_005", "m11UGD_036"]:
            for e in range(round(room.room_data.width/TILEWIDTH)):
                icon = self.scene.addPixmap(QPixmap("Data\\wave.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(e*TILEWIDTH + 6, 20.5)
                icon.setParentItem(room)
        if room.room_data.name in ["m11UGD_019", "m11UGD_040"]:
            for e in range(round(room.room_data.width/TILEWIDTH)):
                icon = self.scene.addPixmap(QPixmap("Data\\wave.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(e*TILEWIDTH + 6, 28.5)
                icon.setParentItem(room)
        if room.room_data.name in ["m11UGD_042", "m11UGD_046"]:
            for e in range(round(room.room_data.width/TILEWIDTH)):
                icon = self.scene.addPixmap(QPixmap("Data\\wave.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(e*TILEWIDTH + 6, 43.5)
                icon.setParentItem(room)
        if room.room_data.name in ["m11UGD_043"]:
            for e in range(round(room.room_data.width/TILEWIDTH)-1):
                icon = self.scene.addPixmap(QPixmap("Data\\wave.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(e*TILEWIDTH + 6, 13.5)
                icon.setParentItem(room)
        
        #No traverse
        
        for e in room.room_data.no_traverse:
            if room.room_data.name == "m11UGD_013":
                icon = self.scene.addPixmap(QPixmap("Data\\void.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(e.x_block*TILEWIDTH + 0.5, (e.z_block + 3)*TILEHEIGHT + 4.5)
            elif room.room_data.name == "m11UGD_031":
                icon = self.scene.addPixmap(QPixmap("Data\\void.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(e.x_block*TILEWIDTH + 0.5, (e.z_block + 4)*TILEHEIGHT + 4.5)
            else:
                icon = self.scene.addPixmap(QPixmap("Data\\void.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(e.x_block*TILEWIDTH + 0.5, (e.z_block + 1)*TILEHEIGHT + 4.5)
            icon.setParentItem(room)
        
        #Doors
        
        for e in room.room_data.door_flag:
            if e.direction_part == Direction.LEFT or (room.room_data.room_type == "ERoomType::Save" or room.room_data.room_type == "ERoomType::Warp") and len(room.room_data.door_flag) == 1:
                door = self.scene.addRect(0, 0, OUTLINE, 6, outline, QColor(room.fill))
                door.setPos(e.x_block*TILEWIDTH - 1.5, e.z_block*TILEHEIGHT + 4.5)
                door.setParentItem(room)
                if e.direction_part != Direction.LEFT:
                    door.setVisible(False)
            if e.direction_part == Direction.BOTTOM:
                door = self.scene.addRect(0, 0, 6, OUTLINE, outline, QColor(room.fill))
                door.setPos(e.x_block*TILEWIDTH + 9.5, e.z_block*TILEHEIGHT - 1.5)
                door.setParentItem(room)
            if e.direction_part == Direction.RIGHT or (room.room_data.room_type == "ERoomType::Save" or room.room_data.room_type == "ERoomType::Warp") and len(room.room_data.door_flag) == 1:
                door = self.scene.addRect(0, 0, OUTLINE, 6, outline, QColor(room.fill))
                door.setPos(e.x_block*TILEWIDTH + TILEWIDTH - 1.5, e.z_block*TILEHEIGHT + 4.5)
                door.setParentItem(room)
                if e.direction_part != Direction.RIGHT:
                    door.setVisible(False)
            if e.direction_part == Direction.TOP:
                door = self.scene.addRect(0, 0, 6, OUTLINE, outline, QColor(room.fill))
                door.setPos(e.x_block*TILEWIDTH + 9.5, e.z_block*TILEHEIGHT + TILEHEIGHT - 1.5)
                door.setParentItem(room)
            if e.direction_part == Direction.LEFT_BOTTOM:
                if room.room_data.area == "EAreaID::m10BIG":
                    door = self.scene.addRect(0, 0, OUTLINE, 8, outline, QColor(room.fill))
                    door.setPos(e.x_block*TILEWIDTH - 1.5, e.z_block*TILEHEIGHT - 0.5)
                else:
                    door = self.scene.addRect(0, 0, OUTLINE, 6, outline, QColor(room.fill))
                    door.setPos(e.x_block*TILEWIDTH - 1.5, e.z_block*TILEHEIGHT + 1.5)
                door.setParentItem(room)
            if e.direction_part == Direction.RIGHT_BOTTOM:
                if room.room_data.area == "EAreaID::m10BIG":
                    door = self.scene.addRect(0, 0, OUTLINE, 8, outline, QColor(room.fill))
                    door.setPos(e.x_block*TILEWIDTH + TILEWIDTH - 1.5, e.z_block*TILEHEIGHT - 0.5)
                else:
                    door = self.scene.addRect(0, 0, OUTLINE, 6, outline, QColor(room.fill))
                    door.setPos(e.x_block*TILEWIDTH + TILEWIDTH - 1.5, e.z_block*TILEHEIGHT + 1.5)
                door.setParentItem(room)
            if e.direction_part == Direction.LEFT_TOP:
                if room.room_data.area == "EAreaID::m10BIG":
                    door = self.scene.addRect(0, 0, OUTLINE, 8, outline, QColor(room.fill))
                    door.setPos(e.x_block*TILEWIDTH - 1.5, e.z_block*TILEHEIGHT + 7.5)
                else:
                    door = self.scene.addRect(0, 0, OUTLINE, 6, outline, QColor(room.fill))
                    door.setPos(e.x_block*TILEWIDTH - 1.5, e.z_block*TILEHEIGHT + 7.5)
                door.setParentItem(room)
            if e.direction_part == Direction.RIGHT_TOP:
                if room.room_data.area == "EAreaID::m10BIG":
                    door = self.scene.addRect(0, 0, OUTLINE, 8, outline, QColor(room.fill))
                    door.setPos(e.x_block*TILEWIDTH + TILEWIDTH - 1.5, e.z_block*TILEHEIGHT + 7.5)
                else:
                    door = self.scene.addRect(0, 0, OUTLINE, 6, outline, QColor(room.fill))
                    door.setPos(e.x_block*TILEWIDTH + TILEWIDTH - 1.5, e.z_block*TILEHEIGHT + 7.5)
                door.setParentItem(room)
            if e.direction_part == Direction.TOP_LEFT:
                if room.room_data.area == "EAreaID::m10BIG":
                    door = self.scene.addRect(0, 0, 8, OUTLINE, outline, QColor(room.fill))
                    door.setPos(e.x_block*TILEWIDTH - 0.5, e.z_block*TILEHEIGHT + TILEHEIGHT - 1.5)
                else:
                    door = self.scene.addRect(0, 0, 6, OUTLINE, outline, QColor(room.fill))
                    door.setPos(e.x_block*TILEWIDTH + 1.5, e.z_block*TILEHEIGHT + TILEHEIGHT - 1.5)
                door.setParentItem(room)
            if e.direction_part == Direction.TOP_RIGHT:
                if room.room_data.area == "EAreaID::m10BIG":
                    door = self.scene.addRect(0, 0, 8, OUTLINE, outline, QColor(room.fill))
                    door.setPos(e.x_block*TILEWIDTH + 17.5, e.z_block*TILEHEIGHT + TILEHEIGHT - 1.5)
                else:
                    door = self.scene.addRect(0, 0, 6, OUTLINE, outline, QColor(QColor(room.fill)))
                    door.setPos(e.x_block*TILEWIDTH + 17.5, e.z_block*TILEHEIGHT + TILEHEIGHT - 1.5)
                door.setParentItem(room)
            if e.direction_part == Direction.BOTTOM_RIGHT:
                if room.room_data.area == "EAreaID::m10BIG":
                    door = self.scene.addRect(0, 0, 8, OUTLINE, outline, QColor(room.fill))
                    door.setPos(e.x_block*TILEWIDTH + 17.5, e.z_block*TILEHEIGHT - 1.5)
                else:
                    door = self.scene.addRect(0, 0, 6, OUTLINE, outline, QColor(room.fill))
                    door.setPos(e.x_block*TILEWIDTH + 17.5, e.z_block*TILEHEIGHT - 1.5)
                door.setParentItem(room)
            if e.direction_part == Direction.BOTTOM_LEFT:
                if room.room_data.area == "EAreaID::m10BIG":
                    door = self.scene.addRect(0, 0, 8, OUTLINE, outline, QColor(room.fill))
                    door.setPos(e.x_block*TILEWIDTH - 0.5, e.z_block*TILEHEIGHT - 1.5)
                else:
                    door = self.scene.addRect(0, 0, 6, OUTLINE, outline, QColor(room.fill))
                    door.setPos(e.x_block*TILEWIDTH + 1.5, e.z_block*TILEHEIGHT - 1.5)
                door.setParentItem(room)
        
        #Text
        
        text = self.scene.addText(room.room_data.name.replace("_", ""), "Impact")
        text.setDefaultTextColor(QColor("#ffffff"))
        text.setTransform(QTransform.fromScale(0.25, -0.5))
        text.setPos(room.room_data.width/2 - text.document().size().width()/8, room.room_data.height/2 + TILEHEIGHT/2 - 0.5)
        text.setParentItem(room)
    
    def fill_area(self):
        for i in self.json_file["AreaOrder"]:
            self.area_order_list.addItem(i)

    def update_offsets(self):
        for i in self.room_list:
            self.json_file["MapData"][i.room_data.name]["AreaID"]   = i.room_data.area
            self.json_file["MapData"][i.room_data.name]["RoomType"] = i.room_data.room_type
            self.json_file["MapData"][i.room_data.name]["RoomPath"] = i.room_data.room_path
            self.json_file["MapData"][i.room_data.name]["OffsetX"]  = i.room_data.offset_x * 12.6 / TILEWIDTH
            self.json_file["MapData"][i.room_data.name]["OffsetZ"]  = i.room_data.offset_z * 7.2 / TILEHEIGHT
            if self.json_file["MapData"][i.room_data.name]["RoomType"] in ["ERoomType::Save", "ERoomType::Warp", "ERoomType::Load"]:
                if self.json_file["MapData"][i.room_data.name]["RoomPath"] == "ERoomPath::Left":
                    self.json_file["MapData"][i.room_data.name]["DoorFlag"] = [1, 1]
                elif self.json_file["MapData"][i.room_data.name]["RoomPath"] == "ERoomPath::Right":
                    self.json_file["MapData"][i.room_data.name]["DoorFlag"] = [1, 4]
                elif self.json_file["MapData"][i.room_data.name]["RoomPath"] == "ERoomPath::Both":
                    self.json_file["MapData"][i.room_data.name]["DoorFlag"] = [1, 5]
            self.json_file["MapData"][i.room_data.name]["BgmID"]   = i.room_data.music
            self.json_file["MapData"][i.room_data.name]["BgmType"] = i.room_data.play
            self.json_file["MapData"][i.room_data.name]["Unused"]  = i.room_data.unused
        #Village fix
        self.json_file["MapData"]["m02VIL_099"]["OffsetX"] = self.json_file["MapData"]["m02VIL_002"]["OffsetX"]
        self.json_file["MapData"]["m02VIL_099"]["OffsetZ"] = self.json_file["MapData"]["m02VIL_002"]["OffsetZ"]
        self.json_file["MapData"]["m02VIL_100"]["OffsetX"] = self.json_file["MapData"]["m02VIL_002"]["OffsetX"]
        self.json_file["MapData"]["m02VIL_100"]["OffsetZ"] = self.json_file["MapData"]["m02VIL_002"]["OffsetZ"]
        #Ice fix
        self.json_file["MapData"]["m18ICE_020"]["OffsetX"] = self.json_file["MapData"]["m18ICE_019"]["OffsetX"]
        self.json_file["MapData"]["m18ICE_020"]["OffsetZ"] = self.json_file["MapData"]["m18ICE_019"]["OffsetZ"]
    
    def update_logic(self):
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
            self.json_file["KeyLogic"][i.room_data.name]["GateRoom"]             = i.logic_data.is_gate
            self.json_file["KeyLogic"][i.room_data.name]["NearestGate"]          = self.convert_index_to_gate(i.logic_data.gate_list)
            self.json_file["KeyLogic"][i.room_data.name]["Doublejump"]           = i.logic_data.double_jump
            self.json_file["KeyLogic"][i.room_data.name]["HighJump"]             = i.logic_data.high_jump
            self.json_file["KeyLogic"][i.room_data.name]["Invert"]               = i.logic_data.invert
            self.json_file["KeyLogic"][i.room_data.name]["Deepsinker"]           = i.logic_data.deepsinker
            self.json_file["KeyLogic"][i.room_data.name]["Dimensionshift"]       = i.logic_data.dimension_shift
            self.json_file["KeyLogic"][i.room_data.name]["Reflectionray"]        = i.logic_data.reflector_ray
            self.json_file["KeyLogic"][i.room_data.name]["Aquastream"]           = i.logic_data.aqua_stream
            self.json_file["KeyLogic"][i.room_data.name]["Bloodsteel"]           = i.logic_data.blood_steal
            self.json_file["KeyLogic"][i.room_data.name]["Swordsman"]            = i.logic_data.zangetsuto
            self.json_file["KeyLogic"][i.room_data.name]["Silverbromide"]        = i.logic_data.silver_bromide
            self.json_file["KeyLogic"][i.room_data.name]["BreastplateofAguilar"] = i.logic_data.aegis_plate
            self.json_file["KeyLogic"][i.room_data.name]["Keyofbacker1"]         = i.logic_data.carpenter
            self.json_file["KeyLogic"][i.room_data.name]["Keyofbacker2"]         = i.logic_data.warhorse
            self.json_file["KeyLogic"][i.room_data.name]["Keyofbacker3"]         = i.logic_data.millionaire
            self.json_file["KeyLogic"][i.room_data.name]["Keyofbacker4"]         = i.logic_data.celeste
    
    def update_order(self):
        self.json_file["AreaOrder"].clear()
        for i in range(self.area_order_list.count()):
            self.json_file["AreaOrder"].append(self.area_order_list.item(i).text())

def main():
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()