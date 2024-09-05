from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

import json
import sys
import os
import math
import copy
import colorsys
import decimal
import traceback

from enum import Enum
from collections import OrderedDict

script_name = os.path.splitext(os.path.basename(__file__))[0]

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

DEFAULT_MAP = "Data\\PB_DT_RoomMaster.json"
DEFAULT_MAP_SURFACE = 1553
DEFAULT_MAP_ROOMS   = 383

TILEWIDTH = 25
TILEHEIGHT = 15
OUTLINE = 3

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
    "m53BRV_005"
]

constant = {}
translation = {}
music_id = []
music_name = []
play_id = []
play_name = []

for file in os.listdir("Data\\Constant"):
    name = os.path.splitext(file)[0]
    with open("Data\\Constant\\" + file, "r", encoding="utf8") as file_reader:
        constant[name] = json.load(file_reader)

for file in os.listdir("Data\\Translation"):
    name = os.path.splitext(file)[0]
    with open("Data\\Translation\\" + file, "r", encoding="utf8") as file_reader:
        translation[name] = json.load(file_reader)

music_id.append(None)
music_name.append("None")
for entry in translation["Music"]:
    music_id.append(entry)
    music_name.append(translation["Music"][entry])

for entry in translation["Play"]:
    play_id.append(entry)
    play_name.append(translation["Play"][entry])
    
def modify_color(color, hsv_mod):
    hue = (color.hueF() + hsv_mod[0]) % 1
    sat = color.saturationF() * hsv_mod[1] if hsv_mod[1] < 1 else color.saturationF() + (1 - color.saturationF())*(hsv_mod[1] - 1)
    val = color.valueF() * hsv_mod[2]      if hsv_mod[2] < 1 else color.valueF() + (1 - color.valueF())*(hsv_mod[2] - 1)
    return QColor.fromHsvF(hue, sat, val)
    
def is_room_adjacent(room_1, room_2, consider_hard_one_ways = False):
    if room_1.out_of_map != room_2.out_of_map:
        return False
    if left_room_check(room_1, room_2):
        return door_vertical_check(room_1, room_2, Direction.LEFT, Direction.LEFT_BOTTOM, Direction.LEFT_TOP)
    if bottom_room_check(room_1, room_2):
        return door_horizontal_check(room_1, room_2, Direction.BOTTOM, Direction.BOTTOM_RIGHT, Direction.BOTTOM_LEFT)
    if right_room_check(room_1, room_2):
        if consider_hard_one_ways and room_2.name == "m08TWR_019":
            return False
        return door_vertical_check(room_1, room_2, Direction.RIGHT, Direction.RIGHT_BOTTOM, Direction.RIGHT_TOP)
    if top_room_check(room_1, room_2):
        if consider_hard_one_ways and room_1.name == "m07LIB_000":
            return False
        return door_horizontal_check(room_1, room_2, Direction.TOP, Direction.TOP_LEFT, Direction.TOP_RIGHT)
    return False

def left_room_check(room_1, room_2):
    return bool(room_2.offset_x == room_1.offset_x - 1 * room_2.width and room_1.offset_z - 1 * (room_2.height - 1) <= room_2.offset_z <= room_1.offset_z + 1 * (room_1.height - 1))

def bottom_room_check(room_1, room_2):
    return bool(room_1.offset_x - 1 * (room_2.width - 1) <= room_2.offset_x <= room_1.offset_x + 1 * (room_1.width - 1) and room_2.offset_z == room_1.offset_z - 1 * room_2.height)

def right_room_check(room_1, room_2):
    return bool(room_2.offset_x == room_1.offset_x + 1 * room_1.width and room_1.offset_z - 1 * (room_2.height - 1) <= room_2.offset_z <= room_1.offset_z + 1 * (room_1.height - 1))

def top_room_check(room_1, room_2):
    return bool(room_1.offset_x - 1 * (room_2.width - 1) <= room_2.offset_x <= room_1.offset_x + 1 * (room_1.width - 1) and room_2.offset_z == room_1.offset_z + 1 * room_1.height)

def door_vertical_check(room_1, room_2, direction_1, direction_2, direction_3):
    for door_1 in room_1.door_flag:
        if door_1.direction_part == direction_1:
            for door_2 in room_2.door_flag:
                if door_2.direction_part == OppositeDirection[direction_1] and door_1.z_block == (door_2.z_block + (room_2.offset_z - room_1.offset_z)):
                    return True
        if door_1.direction_part == direction_2:
            for door_2 in room_2.door_flag:
                if door_2.direction_part == OppositeDirection[direction_2] and door_1.z_block == (door_2.z_block + (room_2.offset_z - room_1.offset_z)):
                    return True
        if door_1.direction_part == direction_3:
            for door_2 in room_2.door_flag:
                if door_2.direction_part == OppositeDirection[direction_3] and door_1.z_block == (door_2.z_block + (room_2.offset_z - room_1.offset_z)):
                    return True
    return False

def door_horizontal_check(room_1, room_2, direction_1, direction_2, direction_3):
    for door_1 in room_1.door_flag:
        if door_1.direction_part == direction_1:
            for door_2 in room_2.door_flag:
                if door_2.direction_part == OppositeDirection[direction_1] and door_1.x_block == (door_2.x_block + (room_2.offset_x - room_1.offset_x)):
                    return True
        if door_1.direction_part == direction_2:
            for door_2 in room_2.door_flag:
                if door_2.direction_part == OppositeDirection[direction_2] and door_1.x_block == (door_2.x_block + (room_2.offset_x - room_1.offset_x)):
                    return True
        if door_1.direction_part == direction_3:
            for door_2 in room_2.door_flag:
                if door_2.direction_part == OppositeDirection[direction_3] and door_1.x_block == (door_2.x_block + (room_2.offset_x - room_1.offset_x)):
                    return True
    return False

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

OppositeDirection = {
    Direction.LEFT:         Direction.RIGHT,
    Direction.BOTTOM:       Direction.TOP,
    Direction.RIGHT:        Direction.LEFT,
    Direction.TOP:          Direction.BOTTOM,
    Direction.LEFT_BOTTOM:  Direction.RIGHT_BOTTOM,
    Direction.RIGHT_BOTTOM: Direction.LEFT_BOTTOM,
    Direction.LEFT_TOP:     Direction.RIGHT_TOP,
    Direction.RIGHT_TOP:    Direction.LEFT_TOP,
    Direction.TOP_LEFT:     Direction.BOTTOM_LEFT,
    Direction.TOP_RIGHT:    Direction.BOTTOM_RIGHT,
    Direction.BOTTOM_RIGHT: Direction.TOP_RIGHT,
    Direction.BOTTOM_LEFT:  Direction.TOP_LEFT,
}

#Classes

class RoomTheme(Enum):
    Default = 1
    Light   = 2
    Dark    = 0

theme_to_mod = {
    RoomTheme.Default: (0,   1,    1),
    RoomTheme.Light:   (0, 1/3, 1.75),
    RoomTheme.Dark:    (0,   1, 0.25)
}

class Room:
    def __init__(self, name, area, out_of_map, room_type, room_path, width, height, offset_x, offset_z, door_flag, no_traverse, music, play):
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

class Door:
    def __init__(self, x_block, z_block, direction_part, breakable):
        self.x_block = x_block
        self.z_block = z_block
        self.direction_part = direction_part
        self.breakable = breakable

class RoomItem(QGraphicsRectItem):
    def __init__(self, index, room_data, can_move, group_list, main_window):
        super().__init__(0, 0, room_data.width * TILEWIDTH, room_data.height * TILEHEIGHT)
        self.setCursor(Qt.PointingHandCursor)
        
        self.index = index
        self.room_data = room_data
        self.can_move = can_move
        self.group_list = group_list
        self.main_window = main_window
        
        self.outline = QPen()
        self.outline.setWidth(OUTLINE)
        self.outline.setJoinStyle(Qt.MiterJoin)
        
        self.setToolTip(room_data.name)
        
        self.reset_pos()
        self.reset_flags()
        
        self.set_theme(RoomTheme.Default)
    
    def set_theme(self, theme):
        self.current_theme = theme
        self.reset_layer(theme.value)
        self.reset_brush()
    
    def reset_brush(self):
        #Fill
        area_index = 18 if self.room_data.out_of_map else int(self.room_data.area.split("::")[-1][1:3]) - 1
        current_fill = QColor(area_color[area_index])
        current_door_fill = modify_color(current_fill, theme_to_mod[self.current_theme])
        current_room_fill = modify_color(current_fill, theme_to_mod[self.current_theme])
        if self.room_data.room_type == "ERoomType::Load" or self.room_data.name == "m02VIL_000":
            current_room_fill.setAlphaF(0.5)
        self.setBrush(current_room_fill)
        #Outline
        current_outline = modify_color(QColor("#ffffff"), theme_to_mod[self.current_theme])
        self.outline.setColor(current_outline)
        self.setPen(self.outline)
        #Child items
        for item in self.childItems():
            if type(item) == QGraphicsRectItem:
                item.setBrush(current_door_fill)
            if type(item) == QGraphicsTextItem:
                item.setDefaultTextColor(current_outline)
    
    def reset_flags(self):
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)
        self.setFlag(QGraphicsItem.ItemIsMovable, self.can_move or not self.main_window.restrictions)
    
    def set_static(self):
        self.setFlags(QGraphicsItem.ItemSendsGeometryChanges)
    
    def reset_layer(self, priority):
        self.setZValue(priority*100 - self.room_data.width*self.room_data.height)
    
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSelectedChange:
            self.set_theme(RoomTheme.Light if value else RoomTheme.Default)
            if value and not self.can_move and self.main_window.restrictions:
                self.reset_layer(RoomTheme.Default.value)
        return super().itemChange(change, value)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.LeftButton and self.main_window.restrictions:
            for room in self.scene().selectedItems():
                for e in room.group_list:
                    self.main_window.room_list[e].setSelected(True)
        if event.button() == Qt.RightButton and not self.isSelected():
            for room in self.scene().selectedItems():
                room.setSelected(False)
            self.setSelected(True)
    
    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.main_window.view.setDragMode(QGraphicsView.NoDrag)
    
    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        #Place room
        for room_1 in self.scene().selectedItems():
            room_1.snap_to_grid()
        #Change a backer room's area id based on what it is connected to
        if len(self.scene().selectedItems()) < 2:
            room_1 = self.scene().selectedItems()[0]
            if "m88BKR" in room_1.room_data.name:
                for room_2 in self.main_window.room_list:
                    if "m88BKR" in room_2.room_data.name:
                        continue
                    if is_room_adjacent(room_1.room_data, room_2.room_data):
                        room_1.room_data.area = room_2.room_data.area
                        room_1.reset_brush()
                        self.main_window.music_drop_down.setCurrentIndex(music_id.index(room_2.room_data.music))
                        self.main_window.play_drop_down.setCurrentIndex(play_id.index(room_2.room_data.play))
                        break
        if event.button() == Qt.LeftButton:
            self.main_window.set_unsaved()
    
    def mouseDoubleClickEvent(self, event):
        if not event.button() == Qt.LeftButton:
            return
        super().mouseDoubleClickEvent(event)
        #Select all rooms belonging to the same area
        if self.room_data.area != "EAreaID::None":
            for room in self.main_window.room_list:
                if room.room_data.area == self.room_data.area:
                    room.setSelected(True)

    def snap_to_grid(self):
        x_round_mode = decimal.ROUND_HALF_UP if self.pos().x() < 0 else decimal.ROUND_HALF_DOWN
        y_round_mode = decimal.ROUND_HALF_UP if self.pos().y() < 0 else decimal.ROUND_HALF_DOWN
        self.room_data.offset_x = float(decimal.Decimal(self.pos().x() /  TILEWIDTH).quantize(0, x_round_mode))
        self.room_data.offset_z = float(decimal.Decimal(self.pos().y() / TILEHEIGHT).quantize(0, y_round_mode))
        #The train room's z offset must always be positive
        if self.room_data.name == "m09TRN_002" and self.room_data.offset_z < 0 and self.main_window.restrictions:
            self.room_data.offset_z = 0
        self.reset_pos()
    
    def paint(self, painter, option, widget):
        option.state &= ~QStyle.State_Selected
        super().paint(painter, option, widget)
    
    def reset_pos(self):
        self.setPos(self.room_data.offset_x * TILEWIDTH, self.room_data.offset_z * TILEHEIGHT)

class GraphicsView(QGraphicsView):
    def __init__(self, scene, window):
        super().__init__(scene, window)
        self.middle_button_held = False
        self.start_pos = None

    def mousePressEvent(self, event):
        if event.button() in [Qt.LeftButton, Qt.RightButton]:
            super().mousePressEvent(event)
        if event.button() == Qt.MiddleButton:
            self.middle_button_held = True
            self.start_pos = event.position()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.middle_button_held:
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - (event.position().x() - self.start_pos.x()))
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - (event.position().y() - self.start_pos.y()))
            self.start_pos = event.position()

    def mouseReleaseEvent(self, event):
        if event.button() in [Qt.LeftButton, Qt.RightButton]:
            super().mouseReleaseEvent(event)
        if event.button() == Qt.MiddleButton:
            self.middle_button_held = False
    
    def wheelEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            current_scale = abs(self.transform().m11())
            current_scale_exp = math.log(current_scale, 2)
            if event.angleDelta().y() > 0 and current_scale_exp < 3:
                self.scale(2.0, 2.0)
            if event.angleDelta().y() < 0 and current_scale_exp > 0:
                self.scale(0.5, 0.5)
        else:
            super().wheelEvent(event)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        sys.excepthook = self.exception_hook
        self.initUI()
        self.unsaved      = False
        self.restrictions = False
        self.reset()
        
    def initUI(self):
        self.setStyleSheet("QWidget{background:transparent; color: #ffffff; font-family: Cambria; font-size: 18px}"
        + "QMainWindow{border-image: url(Data/background.png)}"
        + "QGraphicsView{border: 0px; selection-background-color: #320288ff}"
        + "QGraphicsView::item:selected{background-color: #320288ff}"
        + "QMenuBar{background-color: #21222e}"
        + "QMenuBar::item:selected{background: #320288ff}"
        + "QMenuBar::item:pressed{border: 1px solid #640288ff}"
        + "QMenu{background-color: #21222e; margin: 4px}"
        + "QMenu::item{padding: 2px 4px 2px 4px}"
        + "QMenu::item:selected{background: #320288ff}"
        + "QMenu::item:pressed{border: 1px solid #640288ff}" 
        + "QComboBox{background-color: #21222e; selection-background-color: #320288ff}"
        + "QComboBox QAbstractItemView{border: 1px solid #21222e}"
        + "QMessageBox{background-color: #21222e}"
        + "QDialog{background-color: #21222e}"
        + "QGroupBox{background-color: #21222e; border: 2px solid white}"
        + "QPushButton{background-color: #21222e}"
        + "QListWidget{background-color: #21222e; border: 1px solid #21222e}"
        + "QScrollBar::add-page{background-color: #1b1c26}"
        + "QScrollBar::sub-page{background-color: #1b1c26}"
        + "QToolTip{border: 0px; background-color: #21222e; color: #ffffff; font-family: Cambria; font-size: 18px}")
        
        #Graphics
        
        self.scene = QGraphicsScene(self)
        self.view = GraphicsView(self.scene, self) 
        self.scene.selectionChanged.connect(self.selection_event)
        self.view.setDragMode(QGraphicsView.RubberBandDrag)
        self.scene.installEventFilter(self)
        
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setAlignment(Qt.AlignLeft)
        self.view.scale(1, -1)
        self.setCentralWidget(self.view)
        
        #Menu
        
        self.bar   = self.menuBar()
        file_bar   = self.bar.addMenu("File")
        edit_bar   = self.bar.addMenu("Edit")
        select_bar = self.bar.addMenu("Select")
        view_bar   = self.bar.addMenu("View")
        tool_bar   = self.bar.addMenu("Tools")
        help_bar   = self.bar.addMenu("Help")

        open = QAction("Open", self)
        open.setShortcut(QKeySequence(Qt.CTRL | Qt.Key_O))
        open.triggered.connect(self.open_file)
        file_bar.addAction(open)

        self.save = QAction("Save", self)
        self.save.setShortcut(QKeySequence(Qt.CTRL | Qt.Key_S))
        self.save.triggered.connect(self.save_file)
        file_bar.addAction(self.save)

        save_as = QAction("Save as", self)
        save_as.setShortcut(QKeySequence(Qt.SHIFT | Qt.CTRL | Qt.Key_S))
        save_as.triggered.connect(self.save_file_as)
        file_bar.addAction(save_as)

        reset = QAction("Reset", self)
        reset.setShortcut(QKeySequence(Qt.CTRL | Qt.Key_R))
        reset.triggered.connect(self.reset)
        file_bar.addAction(reset)
        
        self.use_restr = QAction("Use restrictions", self, checkable = True)
        self.use_restr.setShortcut(QKeySequence(Qt.Key_F1))
        self.use_restr.triggered.connect(self.use_restr_action)
        self.use_restr.setChecked(True)
        edit_bar.addAction(self.use_restr)
        
        self.restore_music = QAction("Restore Music", self)
        self.restore_music.setShortcut(QKeySequence(Qt.Key_F2))
        self.restore_music.triggered.connect(self.restore_music_action)
        edit_bar.addAction(self.restore_music)
        
        self.select_all = QAction("Select all", self)
        self.select_all.setShortcut(QKeySequence(Qt.CTRL | Qt.Key_A))
        self.select_all.triggered.connect(self.select_all_action)
        select_bar.addAction(self.select_all)
        
        self.select_none = QAction("Deselect all", self)
        self.select_none.setShortcut(QKeySequence(Qt.SHIFT | Qt.CTRL | Qt.Key_A))
        self.select_none.triggered.connect(self.select_none_action)
        select_bar.addAction(self.select_none)
        
        self.select_invert = QAction("Invert selection", self)
        self.select_invert.setShortcut(QKeySequence(Qt.CTRL | Qt.Key_I))
        self.select_invert.triggered.connect(self.select_invert_action)
        select_bar.addAction(self.select_invert)
        
        self.show_out = QAction("Show out-of-map rooms", self, checkable = True)
        self.show_out.setShortcut(QKeySequence(Qt.Key_F3))
        self.show_out.triggered.connect(self.show_out_action)
        view_bar.addAction(self.show_out)
        
        self.show_name = QAction("Show room names", self, checkable = True)
        self.show_name.setShortcut(QKeySequence(Qt.Key_F4))
        self.show_name.triggered.connect(self.show_name_action)
        view_bar.addAction(self.show_name)
        
        self.room_search = QAction("Room Search", self, checkable = True)
        self.room_search.setShortcut(QKeySequence(Qt.Key_S))
        self.room_search.triggered.connect(self.room_search_action)
        tool_bar.addAction(self.room_search)
        
        self.area_order = QAction("Area Order", self, checkable = True)
        self.area_order.setShortcut(QKeySequence(Qt.Key_O))
        self.area_order.triggered.connect(self.area_order_action)
        tool_bar.addAction(self.area_order)
        
        self.comp_check = QAction("Completion Check", self, checkable = True)
        self.comp_check.setShortcut(QKeySequence(Qt.Key_C))
        self.comp_check.triggered.connect(self.comp_check_action)
        tool_bar.addAction(self.comp_check)
        
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
        
        self.context_menu = QMenu(self)
        
        context_action_1 = self.context_menu.addAction(QIcon("Data\\Icon\\reverse_icon.png")  , "Entrances")
        context_action_2 = self.context_menu.addAction(QIcon("Data\\Icon\\swap_icon.png")     , "Room type")
        context_action_3 = self.context_menu.addAction(QIcon("Data\\Icon\\duplicate_icon.png"), "Duplicate")
        context_action_4 = self.context_menu.addAction(QIcon("Data\\Icon\\delete_icon.png")   , "Delete")
        
        context_action_1.triggered.connect(self.reverse_action)
        context_action_2.triggered.connect(self.swap_action)
        context_action_3.triggered.connect(self.duplicate_action)
        context_action_4.triggered.connect(self.delete_action)
        
        #Buttons
        
        self.reverse = QPushButton()
        self.reverse.setShortcut(QKeySequence(Qt.CTRL | Qt.Key_E))
        self.reverse.setIcon(QIcon("Data\\Icon\\reverse_icon.png"))
        self.reverse.setToolTip("Toggle save/warp entrances\nShortcut: Ctrl + E")
        self.reverse.clicked.connect(self.reverse_action)
        self.reverse.setFixedSize(50, 30)
        
        self.swap = QPushButton()
        self.swap.setShortcut(QKeySequence(Qt.CTRL | Qt.Key_T))
        self.swap.setIcon(QIcon("Data\\Icon\\swap_icon.png"))
        self.swap.setToolTip("Toggle save/warp room type\nShortcut: Ctrl + T")
        self.swap.clicked.connect(self.swap_action)
        self.swap.setFixedSize(50, 30)
        
        self.duplicate = QPushButton()
        self.duplicate.setShortcut(QKeySequence(Qt.CTRL | Qt.Key_D))
        self.duplicate.setIcon(QIcon("Data\\Icon\\duplicate_icon.png"))
        self.duplicate.setToolTip("Duplicate a save/warp/transition room\nShortcut: Ctrl + D")
        self.duplicate.clicked.connect(self.duplicate_action)
        self.duplicate.setFixedSize(50, 30)
        
        self.delete = QPushButton()
        self.delete.setShortcut(QKeySequence(Qt.Key_Delete))
        self.delete.setIcon(QIcon("Data\\Icon\\delete_icon.png"))
        self.delete.setToolTip("Delete a duplicated room\nShortcut: Del")
        self.delete.clicked.connect(self.delete_action)
        self.delete.setFixedSize(50, 30)
        
        self.zoom_in = QPushButton()
        self.zoom_in.setShortcut(QKeySequence(Qt.CTRL | Qt.Key_Plus))
        self.zoom_in.setIcon(QIcon("Data\\Icon\\in_icon.png"))
        self.zoom_in.setToolTip("Zoom in\nShortcut: Ctrl + Scroll Up")
        self.zoom_in.clicked.connect(self.zoom_in_action)
        self.zoom_in.setFixedSize(50, 30)
        
        self.zoom_out = QPushButton()
        self.zoom_out.setShortcut(QKeySequence(Qt.CTRL | Qt.Key_Minus))
        self.zoom_out.setIcon(QIcon("Data\\Icon\\out_icon.png"))
        self.zoom_out.setToolTip("Zoom out\nShortcut: Ctrl + Scroll Down")
        self.zoom_out.clicked.connect(self.zoom_out_action)
        self.zoom_out.setFixedSize(50, 30)
        
        #Labels
        
        self.lock_label = QLabel()
        self.lock_label.setPixmap(QPixmap("Data\\Icon\\lock_icon.png"))
        
        self.seed_label = QLabel()
        self.seed_label.setVisible(False)
        retain = self.seed_label.sizePolicy()
        retain.setRetainSizeWhenHidden(True)
        self.seed_label.setSizePolicy(retain)
        
        #Groupboxes
        
        comp_box_layout = QVBoxLayout()
        self.comp_box = QGroupBox()
        self.comp_box.setLayout(comp_box_layout)
        self.comp_box.setVisible(False)
        self.comp_box.setFixedSize(200, 70)
        retain = self.comp_box.sizePolicy()
        retain.setRetainSizeWhenHidden(True)
        self.comp_box.setSizePolicy(retain)
        
        comp_name_label_1 = QLabel()
        comp_name_label_1.setText("Rooms used:")
        comp_name_label_2 = QLabel()
        comp_name_label_2.setText("Surface used:")
        self.comp_value_label_1 = QLabel()
        self.comp_value_label_2 = QLabel()
        
        comp_hbox_top = QHBoxLayout()
        comp_hbox_bot = QHBoxLayout()
        
        comp_hbox_top.addWidget(comp_name_label_1)
        comp_hbox_top.addStretch(1)
        comp_hbox_top.addWidget(self.comp_value_label_1)
        comp_hbox_bot.addWidget(comp_name_label_2)
        comp_hbox_bot.addStretch(1)
        comp_hbox_bot.addWidget(self.comp_value_label_2)
        
        comp_box_layout.addLayout(comp_hbox_top)
        comp_box_layout.addLayout(comp_hbox_bot)
        
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
        
        #Layouts
        
        hbox_top = QHBoxLayout()
        hbox_top.addWidget(self.lock_label)
        hbox_top.addWidget(self.key_drop_down)
        hbox_top.addWidget(self.seed_label)
        hbox_top.addStretch(1)
        hbox_top.addWidget(self.music_drop_down)
        hbox_top.addWidget(self.play_drop_down)
        
        hbox_center = QHBoxLayout()
        hbox_center.addWidget(self.comp_box)
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
        self.setWindowIcon(QIcon(resource_path("Map.ico")))
        self.showMaximized()
    
    def eventFilter(self, object, event):
        if event.type() in [QEvent.GraphicsSceneMousePress, QEvent.GraphicsSceneMouseDoubleClick]:
            if event.button() in [Qt.LeftButton, Qt.RightButton]:
                self.view.setDragMode(QGraphicsView.RubberBandDrag)
        return super().eventFilter(object, event)
    
    def contextMenuEvent(self, event):
        if self.scene.selectedItems():
            self.context_menu.exec(event.globalPos())
    
    def closeEvent(self, event):
        event.accept() if self.safety_save() else event.ignore()
    
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
            self.string = self.path.replace("/", "\\")
            self.title_string = f" ({self.string})"
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
            self.string = self.path.replace("/", "\\")
            self.title_string = f" ({self.string})"
            self.save_to_json(self.string)
            self.direct_save = True
            return True
        return False

    def reset(self):
        if not self.safety_save():
            return
        self.string = DEFAULT_MAP
        self.title_string = ""
        self.load_from_json(self.string)
        self.direct_save = False
    
    def use_restr_action(self):
        if self.use_restr.isChecked():
            self.restrictions = True
            self.lock_label.setPixmap(QPixmap("Data\\Icon\\lock_icon.png"))
        else:
            self.restrictions = False
            self.lock_label.setPixmap(QPixmap("Data\\Icon\\unlock_icon.png"))
        for room in self.room_list:
            room.reset_flags()
            room.setSelected(False)
    
    def select_all_action(self):
        for room in self.room_list:
            room.setSelected(True)
    
    def select_none_action(self):
        for room in self.room_list:
            room.setSelected(False)
    
    def select_invert_action(self):
        for room in self.room_list:
            room.setSelected(not room.isSelected())
    
    def show_out_action(self):
        for room in self.room_list:
            if room.room_data.out_of_map:
                room.setVisible(self.show_out.isChecked())
    
    def show_name_action(self):
        for room in self.room_list:
            for item in room.childItems():
                if type(item) == QGraphicsTextItem:
                    item.setVisible(self.show_name.isChecked())
                if type(item) == QGraphicsPixmapItem:
                    item.setVisible(not self.show_name.isChecked())
    
    def room_search_action(self):
        if self.room_search.isChecked():
            #Disable other tools
            self.area_order.setChecked(False)
            self.area_order_action()
            self.key_location.setChecked(False)
            self.key_location_action()
            self.comp_check.setChecked(False)
            self.comp_check_action()
            #Initiate
            self.disable_menus()
            self.disable_buttons()
            for room in self.room_list:
                room.setSelected(False)
                room.set_static()
            self.room_search_list.setCurrentItem(self.room_search_list.item(0))
            self.room_search_list_change(self.room_search_list.item(0))
            self.room_search_list.setVisible(True)
        else:
            self.room_search_list.setCurrentItem(self.room_search_list.item(0))
            self.room_search_list.setVisible(False)
            self.enable_menus()
            self.enable_buttons()
            self.reset_rooms()
    
    def area_order_action(self):
        if self.area_order.isChecked():
            #Disable other tools
            self.room_search.setChecked(False)
            self.room_search_action()
            self.key_location.setChecked(False)
            self.key_location_action()
            self.comp_check.setChecked(False)
            self.comp_check_action()
            #Initiate
            self.disable_menus()
            self.disable_buttons()
            for room in self.room_list:
                room.setSelected(False)
                room.set_static()
            self.area_order_list.setCurrentItem(self.area_order_list.item(0))
            self.area_order_list_change(self.area_order_list.item(0))
            self.area_order_list.setVisible(True)
        else:
            self.area_order_list.setVisible(False)
            self.enable_menus()
            self.enable_buttons()
            self.reset_rooms()
    
    def comp_check_action(self):
        if self.comp_check.isChecked():
            #Disable other tools
            self.room_search.setChecked(False)
            self.room_search_action()
            self.area_order.setChecked(False)
            self.area_order_action()
            self.key_location.setChecked(False)
            self.key_location_action()
            #Initiate
            self.disable_menus()
            self.disable_buttons()
            for room in self.room_list:
                room.setSelected(False)
                room.set_static()
                room.set_theme(RoomTheme.Dark)
            self.comp_box.setVisible(True)
            #Move through rooms
            current_rooms = [self.room_list[0]]
            self.completion_1 = 0
            self.completion_2 = 0
            self.completion_list = []
            while current_rooms:
                for room in current_rooms:
                    self.add_room_to_completion(room)
                current_rooms_copy = [elem for elem in current_rooms]
                for room_1 in current_rooms_copy:
                    for room_2 in self.room_list:
                        if room_1.room_data.name in constant["ConnectedRoom"] and room_2.current_theme == RoomTheme.Dark:
                            if room_2.room_data.name in constant["ConnectedRoom"][room_1.room_data.name]:
                                current_rooms.append(room_2)
                        if is_room_adjacent(room_1.room_data, room_2.room_data, True) and room_2.current_theme == RoomTheme.Dark:
                            current_rooms.append(room_2)
                    current_rooms.remove(room_1)
                current_rooms = list(dict.fromkeys(current_rooms))
                self.comp_value_label_1.setText(str("{:.2f}".format(round((self.completion_1/DEFAULT_MAP_ROOMS)  *100, 2))) + "%")
                self.comp_value_label_2.setText(str("{:.2f}".format(round((self.completion_2/DEFAULT_MAP_SURFACE)*100, 2))) + "%")
                QApplication.processEvents()
        else:
            self.comp_box.setVisible(False)
            self.enable_menus()
            self.enable_buttons()
            self.reset_rooms()
    
    def key_location_action(self):
        if self.key_location.isChecked():
            #Disable other tools
            self.room_search.setChecked(False)
            self.room_search_action()
            self.area_order.setChecked(False)
            self.area_order_action()
            self.comp_check.setChecked(False)
            self.comp_check_action()
            #CheckLog
            name = os.path.splitext(self.string)[0]
            box = QMessageBox(self)
            box.setWindowTitle("Error")
            box.setIcon(QMessageBox.Critical)
            try:
                log_path = os.path.abspath(os.path.join("", os.pardir)) + "\\Spoiler\\KeyLocation.json"
                with open(log_path, "r", encoding="utf8") as file_reader:
                    self.log = json.load(file_reader)
                if not self.log["Map"] and name.split("\\")[-1] != "PB_DT_RoomMaster":
                    box.setText("Current key location is meant for the default map.")
                    box.exec()
                    self.key_location.setChecked(False)
                    self.key_location_action()
                    return
                elif self.log["Map"] and name.split("\\")[-1] != self.log["Map"]:
                    box.setText("Current key location is meant for map " + self.log["Map"] + ".")
                    box.exec()
                    self.key_location.setChecked(False)
                    self.key_location_action()
                    return
                seed_text = str(self.log["Seed"])
                if not self.log["Beatable"]:
                    seed_text += " (not beatable)"
                self.seed_label.setText(seed_text)
            except FileNotFoundError:
                box.setText("No key log found.")
                box.exec()
                self.key_location.setChecked(False)
                self.key_location_action()
                return
            #Keep show out enabled
            self.show_out.setChecked(True)
            self.show_out_action()
            self.show_out.setEnabled(False)
            #Fill information
            self.key_drop_down.clear()
            for entry in self.log["Key"]:
                self.key_drop_down.addItem(entry)
            #Initiate
            self.disable_menus()
            self.disable_buttons()
            for room in self.room_list:
                room.setSelected(False)
                room.set_static()
            self.key_drop_down.setCurrentIndex(0)
            self.key_drop_down_change(0)
            self.key_drop_down.setVisible(True)
            self.seed_label.setVisible(True)
        else:
            self.key_drop_down.setVisible(False)
            self.seed_label.setVisible(False)
            self.show_out.setEnabled(True)
            self.enable_menus()
            self.enable_buttons()
            self.reset_rooms()
    
    def how_to(self):
        box = QMessageBox(self)
        box.setWindowTitle("How to use")
        box.setText("Map Editor:"
        + "\n\n"
        + "This editor allows you to fully customize the layout of the game's map."
        + "\n"
        + "You can click and drag each room to change its location on the grid and you can select entire areas by double-clicking one of its rooms."
        + "\n"
        + "You can navigate the viewport with the mouse wheel to scroll vertically and with Alt held to scroll horizontally."
        + "\n\n"
        + "Save your creations to the Custom folder for them to be picked by the randomizer."
        + "\n\n"
        + "Area Order:"
        + "\n\n"
        + "A simple tool that lets you reorder the difficulty scaling of each area. "
        + "Try to arrange these in the order that the player will most likely traverse them."
        + "\n\n"
        + "You can submit your own layout creations on the Discord server if you want them to be added as presets in the main download of the randomizer.")
        box.exec()
    
    def guidelines(self):
        box = QMessageBox(self)
        box.setWindowTitle("Map guidelines")
        box.setText("Here are some tips that will help you build maps that are fun to play on:"
        + "\n\n"
        + "• making use of as many rooms as possible"
        + "\n"
        + "• connecting as many entrances as possible"
        + "\n"
        + "• keeping each area separated using transition rooms"
        + "\n"
        + "• ensuring that boss rooms are placed relatively close to a save/warp point"
        + "\n"
        + "• having the \"Use restrictions\" option enabled while building your map"
        + "\n"
        + "• not overlapping any rooms except for the semi-transparent ones"
        + "\n"
        + "• keeping the layout of the map within the area visible with Space Bar"
        + "\n\n"
        + "Additionally here are some useful things to know when building maps:"
        + "\n\n"
        + "• backer rooms can be connected to any area and will be automatically updated"
        + "\n"
        + "• a few bosses can softlock if their rooms are placed in undesirable spots, refer to the Boss restrictions page for more info"
        + "\n"
        + "• room m03ENT_1200 has a transition that does not work properly when connected to a different room, so the randomizer script will ignore this room when connecting the map"
        + "\n"
        + "• the in-game minimap has a limitation as to how far it can display rooms, you can preview this limitation by pressing the space bar")
        box.exec()
    
    def reverse_action(self):
        for room in self.scene.selectedItems():
            if room.room_data.room_type in ["ERoomType::Save", "ERoomType::Warp"]:
                if room.room_data.room_path == "ERoomPath::Left":
                    room.room_data.room_path = "ERoomPath::Right"
                    room.room_data.door_flag = self.convert_flag_to_door([1, 4], room.room_data.width)
                    room.childItems()[1].setVisible(False)
                    room.childItems()[2].setVisible(True)
                elif room.room_data.room_path == "ERoomPath::Right":
                    room.room_data.room_path = "ERoomPath::Both"
                    room.room_data.door_flag = self.convert_flag_to_door([1, 5], room.room_data.width)
                    room.childItems()[1].setVisible(True)
                    room.childItems()[2].setVisible(True)
                elif room.room_data.room_path == "ERoomPath::Both":
                    room.room_data.room_path = "ERoomPath::Left"
                    room.room_data.door_flag = self.convert_flag_to_door([1, 1], room.room_data.width)
                    room.childItems()[1].setVisible(True)
                    room.childItems()[2].setVisible(False)
                self.set_unsaved()
    
    def swap_action(self):
        for room in self.scene.selectedItems():
            if room.room_data.room_type == "ERoomType::Save":
                room.room_data.room_type = "ERoomType::Warp"
                room.childItems()[0].setPixmap(QPixmap("Data\\Icon\\warp.png"))
                self.set_unsaved()
            elif room.room_data.room_type == "ERoomType::Warp":
                room.room_data.room_type = "ERoomType::Save"
                room.childItems()[0].setPixmap(QPixmap("Data\\Icon\\save.png"))
                self.set_unsaved()
    
    def duplicate_action(self):
        for room_1 in self.scene.selectedItems():
            room_1.setSelected(False)
            if room_1.room_data.room_type in ["ERoomType::Save", "ERoomType::Warp", "ERoomType::Load"]:
                #Determine the new room name with an inst number that isn't taken
                taken_inst = []
                for room_2 in self.room_list:
                    current_inst = int(room_2.room_data.name.split("_")[-1])
                    if room_2.room_data.area == room_1.room_data.area and current_inst//100 == 13:
                        taken_inst.append(current_inst)
                taken_inst.sort()
                max_inst = 1300
                if taken_inst:
                    max_inst = taken_inst[-1]
                for num in range(1300, max_inst + 2):
                    if not num in taken_inst:
                        new_inst = num
                        break
                if new_inst >= 1400:
                    return
                #Add the new room
                room_data = copy.deepcopy(room_1.room_data)
                room_data.name = room_data.area.split("::")[-1] + "_" + str(new_inst)
                room_data.offset_x = room_1.room_data.offset_x + 1
                room_data.offset_z = room_1.room_data.offset_z - 1
                new_room = RoomItem(len(self.room_list), room_data, True, [], self)
                self.scene.addItem(new_room)
                self.room_list.append(new_room)
                self.add_room_items(new_room)
                self.room_search_list.addItem(room_data.name)
                self.use_restr_action()
                self.show_out_action()
                self.show_name_action()
                new_room.setSelected(True)
    
    def delete_action(self):
        #Only delete rooms that were previously added by the user
        for room in self.scene.selectedItems():   
            current_inst = int(room.room_data.name.split("_")[-1])
            if current_inst//100 == 13:
                self.scene.removeItem(room)
                self.room_list.remove(room)
                self.room_search_list.takeItem(self.room_search_list.row(self.room_search_list.findItems(room.room_data.name, Qt.MatchExactly)[0]))
        self.show_out_action()
    
    def zoom_in_action(self):
        current_scale = abs(self.view.transform().m11())
        current_scale_exp = math.log(current_scale, 2)
        new_scale_exp = min(round(current_scale_exp) + 1, 3)
        new_scale = 2**new_scale_exp
        new_transform = self.view.transform().fromScale(new_scale, -new_scale)
        self.view.setTransform(new_transform)
    
    def zoom_out_action(self):
        current_scale = abs(self.view.transform().m11())
        current_scale_exp = math.log(current_scale, 2)
        new_scale_exp = max(round(current_scale_exp) - 1, 0)
        new_scale = 2**new_scale_exp
        new_transform = self.view.transform().fromScale(new_scale, -new_scale)
        self.view.setTransform(new_transform)
    
    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Space:
            self.map_limit.setVisible(True)
    
    def keyReleaseEvent(self, event):
        super().keyReleaseEvent(event)
        if event.key() == Qt.Key_Space:
            self.map_limit.setVisible(False)
    
    def room_search_list_change(self, item):
        if item is None:
            return
        for room in self.room_list:
            room.set_theme(RoomTheme.Dark)
        self.room_list[self.room_search_list.currentRow()].set_theme(RoomTheme.Default)
    
    def area_order_list_change(self, item):
        if item is None:
            return
        for room in self.room_list:
            if room.room_data.area == f"EAreaID::{item.text()}":
                room.set_theme(RoomTheme.Default)
            else:
                room.set_theme(RoomTheme.Dark)
        if self.area_order_list.isVisible():
            self.set_unsaved()
    
    def add_room_to_completion(self, room):
        room.set_theme(RoomTheme.Default)
        if not room.room_data.out_of_map and room.room_data.room_type == "ERoomType::Normal":
            self.completion_1 += 1
        for tile in range(room.room_data.width*room.room_data.height):
            tile_relative_coord = (tile % room.room_data.width, tile // room.room_data.width)
            if tile_relative_coord in room.room_data.no_traverse:
                continue
            tile_absolute_coord = (room.room_data.offset_x + tile_relative_coord[0], room.room_data.offset_z + tile_relative_coord[1])
            if tile_absolute_coord in self.completion_list:
                continue
            self.completion_list.append(tile_absolute_coord)
            self.completion_2 += 1
    
    def key_drop_down_change(self, index):
        if index < 0:
            return
        for room in self.room_list:
            if room.room_data.name in self.log["Key"][self.key_drop_down.itemText(index)]:
                room.set_theme(RoomTheme.Default)
            else:
                room.set_theme(RoomTheme.Dark)
    
    def music_drop_down_change(self, index):
        for room in self.scene.selectedItems():
            room.room_data.music = music_id[index]
        if self.music_drop_down.isVisible():
            self.set_unsaved()
    
    def play_drop_down_change(self, index):
        for room in self.scene.selectedItems():
            room.room_data.play = play_id[index]
        if self.play_drop_down.isVisible():
            self.set_unsaved()
    
    def restore_music_action(self):
        #Confirm
        choice = QMessageBox.question(self, "Confirm", "This will set all music settings back to default.\nProceed ?", QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.No:
            return
        #Copy music from the vanilla map
        with open(DEFAULT_MAP, "r") as file_reader:
            copy_from = json.load(file_reader)
        for room in self.room_list:
            if "m88BKR" in room.room_data.name:
                continue
            if room.room_data.name in copy_from["MapData"]:
                room.room_data.music = copy_from["MapData"][room.room_data.name]["BgmID"]
                room.room_data.play  = copy_from["MapData"][room.room_data.name]["BgmType"]
            else:
                area_save = room.room_data.name.split("_")[0] + "_1000"
                room.room_data.music = copy_from["MapData"][area_save]["BgmID"]
                room.room_data.play  = copy_from["MapData"][area_save]["BgmType"]
            room.setSelected(False)
        self.set_unsaved()
    
    def reset_rooms(self):
        for room in self.room_list:
            if not room.room_data.out_of_map:
                room.setVisible(True)
            room.setSelected(False)
            room.set_theme(RoomTheme.Default)
            room.reset_flags()
    
    def change_title(self, suffix):
        self.setWindowTitle(script_name + self.title_string + suffix)
    
    def set_unsaved(self):
        if not self.unsaved:
            self.change_title("*")
            self.unsaved = True

    def selection_event(self):
        #Display music drop down
        if self.scene.selectedItems():
            if len(self.scene.selectedItems()) == 1:
                self.music_drop_down.setCurrentIndex(music_id.index(self.scene.selectedItems()[0].room_data.music))
                self.play_drop_down.setCurrentIndex(play_id.index(self.scene.selectedItems()[0].room_data.play))
            self.music_drop_down.setVisible(True)
            self.play_drop_down.setVisible(True)
        else:
            self.music_drop_down.setVisible(False)
            self.play_drop_down.setVisible(False)
    
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
    
    def enable_menus(self):
        self.use_restr.setEnabled(True)
        self.restore_music.setEnabled(True)
        self.select_all.setEnabled(True)
        self.select_none.setEnabled(True)
        self.select_invert.setEnabled(True)
    
    def disable_menus(self):
        self.use_restr.setEnabled(False)
        self.restore_music.setEnabled(False)
        self.select_all.setEnabled(False)
        self.select_none.setEnabled(False)
        self.select_invert.setEnabled(False)

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
        self.update_json()
        #Process
        self.draw_map()
        self.fill_area()
        self.use_restr_action()
        self.show_out_action()
        self.show_name_action()
        if self.room_search.isChecked():
            self.room_search_action()
        if self.area_order.isChecked():
            self.area_order_action()
        if self.key_location.isChecked():
            self.key_location_action()
        if self.comp_check.isChecked():
            self.comp_check_action()
        self.unsaved = False
    
    def save_to_json(self, filename):
        self.update_map()
        self.update_order()
        with open(filename, "w", encoding="utf8") as file_writer:
            file_writer.write(json.dumps(self.json_file, indent=2))
        self.change_title("")
        self.unsaved = False
    
    def convert_json_to_room(self, name, json):
        area        = json["AreaID"]
        out_of_map  = json["OutOfMap"]
        room_type   = json["RoomType"]
        room_path   = json["RoomPath"]
        width       = json["AreaWidthSize"]
        height      = json["AreaHeightSize"]
        offset_x    = round(json["OffsetX"]/12.6)
        offset_z    = round(json["OffsetZ"]/7.2)
        door_flag   = self.convert_flag_to_door(json["DoorFlag"], width)
        no_traverse = self.convert_no_traverse_to_void(json["NoTraverse"], width)
        music       = json["BgmID"]
        play        = json["BgmType"]
        
        room = Room(name, area, out_of_map, room_type, room_path, width, height, offset_x, offset_z, door_flag, no_traverse, music, play)
        return room
    
    def convert_flag_to_door(self, door_flag, width):
        door_list = []
        for num in range(0, len(door_flag), 2):
            tile_index = door_flag[num]
            direction = door_flag[num+1]
            tile_index -= 1
            x_block = tile_index % width
            z_block = tile_index // width
            for direction_part in Direction:
                if (direction & direction_part.value) != 0:
                    breakable = (direction & (direction_part.value << 16)) != 0
                    door = Door(x_block, z_block, direction_part, breakable)
                    door_list.append(door)
        return door_list
    
    def convert_door_to_flag(self, door_list, width):
        door_flags_by_coords = OrderedDict()
        for door in door_list:
            coords = (door.x_block, door.z_block)
            if coords not in door_flags_by_coords:
                door_flags_by_coords[coords] = 0
            door_flags_by_coords[coords] |= door.direction_part.value
            if door.breakable:
                door_flags_by_coords[coords] |= (door.direction_part.value << 16)
        door_flag = []
        for (x, z), dir_flags in door_flags_by_coords.items():
            tile_index_in_room = z*width + x
            tile_index_in_room += 1
            door_flag.extend([tile_index_in_room, dir_flags])
        return door_flag
    
    def convert_no_traverse_to_void(self, no_traverse, width):
        void_list = []
        for void in no_traverse:
            tile_index = void - 1
            x_block = tile_index % width
            z_block = tile_index // width
            void_list.append((x_block, z_block))
        return void_list
    
    def convert_void_to_no_traverse(self, void_list, width):
        no_traverse = []
        for void in void_list:
            no_traverse.append(void[0] + void[1]*width + 1)
        return no_traverse
    
    def convert_group_to_index(self, group_list):
        new_group_list = []
        index = 0
        for room in self.json_file["MapData"]:
            if room in group_list:
                new_group_list.append(index)
            index += 1
        return new_group_list
    
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
        
        bound_1_horizontal = self.scene.addLine(-32*TILEWIDTH, -32*TILEHEIGHT, -32*TILEWIDTH + (TILEHEIGHT/2 - 1.5), -32*TILEHEIGHT)
        bound_1_horizontal.setPen(outline)
        bound_1_vertical = self.scene.addLine(-32*TILEWIDTH, -32*TILEHEIGHT + (TILEHEIGHT/2 - 1.5), -32*TILEWIDTH, -32*TILEHEIGHT)
        bound_1_vertical.setPen(outline)
        
        bound_2_horizontal = self.scene.addLine(256*TILEWIDTH - (TILEHEIGHT/2 - 1.5), 128*TILEHEIGHT, 256*TILEWIDTH, 128*TILEHEIGHT)
        bound_2_horizontal.setPen(outline)
        bound_2_vertical = self.scene.addLine(256*TILEWIDTH, 128*TILEHEIGHT, 256*TILEWIDTH, 128*TILEHEIGHT - (TILEHEIGHT/2 - 1.5))
        bound_2_vertical.setPen(outline)
        
        self.map_limit = self.scene.addRect(0, -24*TILEHEIGHT, 136*TILEWIDTH, 72*TILEHEIGHT, QPen("#00000000"), QColor("#320288ff"))
        self.map_limit.setVisible(False)
        
        index = 0
        for room in self.json_file["MapData"]:
            
            #Converting data
            
            room_data = self.convert_json_to_room(room, self.json_file["MapData"][room])
            self.room_search_list.addItem(room_data.name)
            group_list = []
            can_move = True
            
            #Room group
            
            for entry in constant["RestrictedRoom"]:
                if room_data.name in entry["Room"]:
                    group_list = entry["Room"]
                    can_move = entry["CanMove"]
                    break
            
            #Creating room
            
            new_room = RoomItem(index, room_data, can_move, self.convert_group_to_index(group_list), self)
            self.scene.addItem(new_room)
            self.room_list.append(new_room)
            self.add_room_items(new_room)
            
            index += 1
            
    def add_room_items(self, room):
        
        #Icons
        
        if room.room_data.room_type == "ERoomType::Save":
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\save.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width*TILEWIDTH/2 - 6, room.room_data.height*TILEHEIGHT/2 + TILEHEIGHT/2 - 1.5)
            icon.setParentItem(room)
        if room.room_data.room_type == "ERoomType::Warp":
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\warp.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width*TILEWIDTH/2 - 6, room.room_data.height*TILEHEIGHT/2 + TILEHEIGHT/2 - 1.5)
            icon.setParentItem(room)
        if room.room_data.name in boss_room:
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\boss.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width*TILEWIDTH/2 - 6, room.room_data.height*TILEHEIGHT/2 + TILEHEIGHT/2 - 1.5)
            icon.setParentItem(room)
        if int(room.room_data.name[1:3]) == 88:
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\key.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width*TILEWIDTH/2 - 6, room.room_data.height*TILEHEIGHT/2 + TILEHEIGHT/2 - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m01SIP_000":
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\start.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width*TILEWIDTH/2 - 6, room.room_data.height*TILEHEIGHT/2 + TILEHEIGHT/2 - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m03ENT_004":
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\blood.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width*TILEWIDTH/2 - 6, TILEHEIGHT - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m03ENT_1200":
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\cross.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width*TILEWIDTH/2 - 6, room.room_data.height*TILEHEIGHT/2 + TILEHEIGHT/2 - 1.5)
            icon.setParentItem(room)
        if room.room_data.name in ["m04GDN_001", "m10BIG_000"]:
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\portal.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width*TILEWIDTH/2 - 6, room.room_data.height*TILEHEIGHT/2 + TILEHEIGHT/2 - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m05SAN_006":
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\barber.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width*TILEWIDTH/2 - 6, room.room_data.height*TILEHEIGHT/2 + TILEHEIGHT/2 - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m06KNG_021":
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\flame.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width*TILEWIDTH/2 - 6, room.room_data.height*TILEHEIGHT/2 + TILEHEIGHT/2 - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m07LIB_009":
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\book.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width*TILEWIDTH/2 - 6, room.room_data.height*TILEHEIGHT/2 + TILEHEIGHT/2 - 1.5)
            icon.setParentItem(room)
        if room.room_data.name in ["m09TRN_001", "m09TRN_004"]:
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\gate.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width*TILEWIDTH/2 - 6, room.room_data.height*TILEHEIGHT/2 + TILEHEIGHT/2 - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m19K2C_000":
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\crown.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width*TILEWIDTH/2 - 6, room.room_data.height*TILEHEIGHT/2 + TILEHEIGHT/2 - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m51EBT_000":
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\8bit.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width*TILEWIDTH/2 - 6, room.room_data.height*TILEHEIGHT/2 + TILEHEIGHT/2 - 1.5)
            icon.setParentItem(room)
        if room.room_data.name in ["m18ICE_019", "m77LBP_000"]:
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\end.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width*TILEWIDTH/2 - 6, room.room_data.height*TILEHEIGHT/2 + TILEHEIGHT/2 - 1.5)
            icon.setParentItem(room)
        
        #Wall
        
        if room.room_data.name == "m03ENT_000":
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\spike_opening.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width*TILEWIDTH/2 - 6, TILEHEIGHT*13 - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m03ENT_007":
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\one_way_left.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width*TILEWIDTH - 13.5, TILEHEIGHT - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m05SAN_003":
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\wall_horizontal.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width*TILEWIDTH/2 - 6, TILEHEIGHT*8 + 6)
            icon.setParentItem(room)
        if room.room_data.name == "m05SAN_009":
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\one_way_down.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width*TILEWIDTH/2 - 6, TILEHEIGHT*4 + 11)
            icon.setParentItem(room)
        if room.room_data.name == "m05SAN_017":
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\one_way_left.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width*TILEWIDTH/2 - 1, TILEHEIGHT - 1.5)
            icon.setParentItem(room)
        if room.room_data.name in ["m05SAN_019", "m08TWR_019"]:
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\one_way_left.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(TILEWIDTH - 23.5, TILEHEIGHT - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m05SAN_021":
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\one_way_right.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width*TILEWIDTH - 13.5, room.room_data.height*TILEHEIGHT - TILEHEIGHT*2 - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m06KNG_013":
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\one_way_right.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width*TILEWIDTH - 13.5, TILEHEIGHT - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m07LIB_005":
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\one_way_down.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width*TILEWIDTH -18.5, TILEHEIGHT - 1.5)
            icon.setParentItem(room)
        if room.room_data.name in ["m07LIB_006", "m11UGD_045"]:
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\hole.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width*TILEWIDTH/2 - 6, TILEHEIGHT - 1.5)
            icon.setParentItem(room)
        if room.room_data.name in ["m07LIB_008", "m07LIB_014", "m11UGD_016", "m18ICE_016"]:
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\hole.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width*TILEWIDTH - 8.5, room.room_data.height*TILEHEIGHT - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m07LIB_021":
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\one_way_down.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width*TILEWIDTH/2 - 6, room.room_data.height*TILEHEIGHT - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m07LIB_023":
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\one_way_left.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width*TILEWIDTH - 11.5, TILEHEIGHT*3 - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m07LIB_035" or room.room_data.name == "m11UGD_056":
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\opening.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width*TILEWIDTH/2 - 6, TILEHEIGHT*3 - 9)
            icon.setParentItem(room)
        if room.room_data.name == "m09TRN_003":
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\one_way_right.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width*TILEWIDTH - 13.5, TILEHEIGHT - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m08TWR_009":
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\one_way_left.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width*TILEWIDTH - 11.5, TILEHEIGHT*11 - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m11UGD_015":
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\one_way_right.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width*TILEWIDTH/2 - 11, TILEHEIGHT - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m11UGD_046":
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\hole_left.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(1.5, room.room_data.height*TILEHEIGHT - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m11UGD_056":
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\wall_vertical.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width*TILEWIDTH - 8.5, room.room_data.height*TILEHEIGHT - 1.5)
            icon.setParentItem(room)
        if room.room_data.name in ["m15JPN_010", "m17RVA_005"]:
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\ceiling_hole.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width*TILEWIDTH - 13.5, room.room_data.height*TILEHEIGHT - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m17RVA_003":
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\ceiling_hole_right.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width*TILEWIDTH - 13.5, room.room_data.height*TILEHEIGHT - 1.5)
            icon.setParentItem(room)
        if room.room_data.name == "m18ICE_015":
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\wall_vertical.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(room.room_data.width*TILEWIDTH/2 - 6, TILEHEIGHT - 1.5)
            icon.setParentItem(room)
        
        #Water
        
        if room.room_data.name in ["m11UGD_021", "m11UGD_022", "m11UGD_023", "m11UGD_024", "m11UGD_025", "m11UGD_044", "m11UGD_045"]:
            for num_1 in range(room.room_data.width):
                for num_2 in range(room.room_data.height):
                    icon = self.scene.addPixmap(QPixmap("Data\\Icon\\bubble.png"))
                    icon.setTransform(QTransform.fromScale(1, -1))
                    icon.setPos(num_1*TILEWIDTH + 6, num_2*TILEHEIGHT + 13.5)
                    icon.setParentItem(room)
        if room.room_data.name == "m11UGD_026":
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\bubble.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(6, 13.5)
            icon.setParentItem(room)
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\wave.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(TILEWIDTH + 6, 13.5)
            icon.setParentItem(room)
        if room.room_data.name in ["m11UGD_005", "m11UGD_036"]:
            for num in range(room.room_data.width):
                icon = self.scene.addPixmap(QPixmap("Data\\Icon\\wave.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(num*TILEWIDTH + 6, 20.5)
                icon.setParentItem(room)
        if room.room_data.name in ["m11UGD_019", "m11UGD_040"]:
            for num in range(room.room_data.width):
                icon = self.scene.addPixmap(QPixmap("Data\\Icon\\wave.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(num*TILEWIDTH + 6, 28.5)
                icon.setParentItem(room)
        if room.room_data.name in ["m11UGD_042", "m11UGD_046"]:
            for num in range(room.room_data.width):
                icon = self.scene.addPixmap(QPixmap("Data\\Icon\\wave.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(num*TILEWIDTH + 6, 43.5)
                icon.setParentItem(room)
        if room.room_data.name == "m11UGD_043":
            for num in range(room.room_data.width - 1):
                icon = self.scene.addPixmap(QPixmap("Data\\Icon\\wave.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(num*TILEWIDTH + 6, 13.5)
                icon.setParentItem(room)
        
        #No traverse
        
        for void in room.room_data.no_traverse:
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\void.png"))
            icon.setTransform(QTransform.fromScale(1, -1))
            icon.setPos(void[0]*TILEWIDTH + 0.5, (void[1] + 1)*TILEHEIGHT + 4.5)
            icon.setParentItem(room)
        
        #Doors
        
        outline = QPen("#00000000")
        
        if room.room_data.area == "EAreaID::m10BIG":
            door_offset = -0.5
            door_height =  8
        else:
            door_offset =  1.5
            door_height =  6
        
        for door in room.room_data.door_flag:
            if door.direction_part == Direction.LEFT or (room.room_data.room_type in ["ERoomType::Save", "ERoomType::Warp"]) and len(room.room_data.door_flag) == 1:
                new_door = self.scene.addRect(0, 0, OUTLINE, 6, outline)
                new_door.setPos(door.x_block*TILEWIDTH - 1.5, door.z_block*TILEHEIGHT + 4.5)
                new_door.setParentItem(room)
                if door.direction_part != Direction.LEFT:
                    new_door.setVisible(False)
            if door.direction_part == Direction.RIGHT or (room.room_data.room_type in ["ERoomType::Save", "ERoomType::Warp"]) and len(room.room_data.door_flag) == 1:
                new_door = self.scene.addRect(0, 0, OUTLINE, 6, outline)
                new_door.setPos(door.x_block*TILEWIDTH + TILEWIDTH - 1.5, door.z_block*TILEHEIGHT + 4.5)
                new_door.setParentItem(room)
                if door.direction_part != Direction.RIGHT:
                    new_door.setVisible(False)
            if door.direction_part == Direction.BOTTOM:
                new_door = self.scene.addRect(0, 0, 6, OUTLINE, outline)
                new_door.setPos(door.x_block*TILEWIDTH + 9.5, door.z_block*TILEHEIGHT - 1.5)
                new_door.setParentItem(room)
            if door.direction_part == Direction.TOP:
                new_door = self.scene.addRect(0, 0, 6, OUTLINE, outline)
                new_door.setPos(door.x_block*TILEWIDTH + 9.5, door.z_block*TILEHEIGHT + TILEHEIGHT - 1.5)
                new_door.setParentItem(room)
            if door.direction_part == Direction.LEFT_BOTTOM:
                new_door = self.scene.addRect(0, 0, OUTLINE, door_height, outline)
                new_door.setPos(door.x_block*TILEWIDTH - 1.5, door.z_block*TILEHEIGHT + door_offset)
                new_door.setParentItem(room)
            if door.direction_part == Direction.RIGHT_BOTTOM:
                new_door = self.scene.addRect(0, 0, OUTLINE, door_height, outline)
                new_door.setPos(door.x_block*TILEWIDTH + TILEWIDTH - 1.5, door.z_block*TILEHEIGHT + door_offset)
                new_door.setParentItem(room)
            if door.direction_part == Direction.LEFT_TOP:
                new_door = self.scene.addRect(0, 0, OUTLINE, door_height, outline)
                new_door.setPos(door.x_block*TILEWIDTH - 1.5, door.z_block*TILEHEIGHT + 7.5)
                new_door.setParentItem(room)
            if door.direction_part == Direction.RIGHT_TOP:
                new_door = self.scene.addRect(0, 0, OUTLINE, door_height, outline)
                new_door.setPos(door.x_block*TILEWIDTH + TILEWIDTH - 1.5, door.z_block*TILEHEIGHT + 7.5)
                new_door.setParentItem(room)
            if door.direction_part == Direction.TOP_LEFT:
                new_door = self.scene.addRect(0, 0, door_height, OUTLINE, outline)
                new_door.setPos(door.x_block*TILEWIDTH + door_offset, door.z_block*TILEHEIGHT + TILEHEIGHT - 1.5)
                new_door.setParentItem(room)
            if door.direction_part == Direction.TOP_RIGHT:
                new_door = self.scene.addRect(0, 0, door_height, OUTLINE, outline)
                new_door.setPos(door.x_block*TILEWIDTH + 17.5, door.z_block*TILEHEIGHT + TILEHEIGHT - 1.5)
                new_door.setParentItem(room)
            if door.direction_part == Direction.BOTTOM_RIGHT:
                new_door = self.scene.addRect(0, 0, door_height, OUTLINE, outline)
                new_door.setPos(door.x_block*TILEWIDTH + 17.5, door.z_block*TILEHEIGHT - 1.5)
                new_door.setParentItem(room)
            if door.direction_part == Direction.BOTTOM_LEFT:
                new_door = self.scene.addRect(0, 0, door_height, OUTLINE, outline,)
                new_door.setPos(door.x_block*TILEWIDTH + door_offset, door.z_block*TILEHEIGHT - 1.5)
                new_door.setParentItem(room)
        
        #Text
        
        text = self.scene.addText(room.room_data.name.replace("_", ""), "Impact")
        text.setTransform(QTransform.fromScale(0.25, -0.5))
        text.setPos(room.room_data.width*TILEWIDTH/2 - text.document().size().width()/8, room.room_data.height*TILEHEIGHT/2 + TILEHEIGHT/2 - 0.5)
        text.setParentItem(room)
        
        room.reset_brush()
    
    def fill_area(self):
        for i in self.json_file["AreaOrder"]:
            self.area_order_list.addItem(i)

    def update_map(self):
        self.json_file["MapData"].clear()
        for room in self.room_list:
            self.json_file["MapData"][room.room_data.name] = {}
            self.json_file["MapData"][room.room_data.name]["AreaID"]         = room.room_data.area
            self.json_file["MapData"][room.room_data.name]["OutOfMap"]       = room.room_data.out_of_map
            self.json_file["MapData"][room.room_data.name]["RoomType"]       = room.room_data.room_type
            self.json_file["MapData"][room.room_data.name]["RoomPath"]       = room.room_data.room_path
            self.json_file["MapData"][room.room_data.name]["AreaWidthSize"]  = room.room_data.width
            self.json_file["MapData"][room.room_data.name]["AreaHeightSize"] = room.room_data.height
            self.json_file["MapData"][room.room_data.name]["OffsetX"]        = round(room.room_data.offset_x * 12.6, 1)
            self.json_file["MapData"][room.room_data.name]["OffsetZ"]        = round(room.room_data.offset_z *  7.2, 1)
            self.json_file["MapData"][room.room_data.name]["DoorFlag"]       = self.convert_door_to_flag(room.room_data.door_flag, room.room_data.width)
            self.json_file["MapData"][room.room_data.name]["NoTraverse"]     = self.convert_void_to_no_traverse(room.room_data.no_traverse, room.room_data.width)
            self.json_file["MapData"][room.room_data.name]["BgmID"]          = room.room_data.music
            self.json_file["MapData"][room.room_data.name]["BgmType"]        = room.room_data.play
        #Village fix
        self.json_file["MapData"]["m02VIL_099"]["OffsetX"] = self.json_file["MapData"]["m02VIL_002"]["OffsetX"]
        self.json_file["MapData"]["m02VIL_099"]["OffsetZ"] = self.json_file["MapData"]["m02VIL_002"]["OffsetZ"]
        self.json_file["MapData"]["m02VIL_100"]["OffsetX"] = self.json_file["MapData"]["m02VIL_002"]["OffsetX"]
        self.json_file["MapData"]["m02VIL_100"]["OffsetZ"] = self.json_file["MapData"]["m02VIL_002"]["OffsetZ"]
        #Ice fix
        self.json_file["MapData"]["m18ICE_020"]["OffsetX"] = self.json_file["MapData"]["m18ICE_019"]["OffsetX"]
        self.json_file["MapData"]["m18ICE_020"]["OffsetZ"] = self.json_file["MapData"]["m18ICE_019"]["OffsetZ"]
    
    def update_order(self):
        self.json_file["AreaOrder"].clear()
        for index in range(self.area_order_list.count()):
            self.json_file["AreaOrder"].append(self.area_order_list.item(index).text())
    
    def update_json(self):
        #Update 2.9.0
        if "KeyLogic" in self.json_file:
            del self.json_file["KeyLogic"]
        for room in self.json_file["MapData"]:
            if "Unused" in self.json_file["MapData"][room]:
                del self.json_file["MapData"][room]["Unused"]
        #Update 2.9.1
        offset = 2
        for room in ["m11UGD_013", "m11UGD_031"]:
            no_traverse = []
            outdated = False
            for void in self.json_file["MapData"][room]["NoTraverse"]:
                no_traverse.append(void + offset*self.json_file["MapData"][room]["AreaWidthSize"])
                if void < 0:
                    outdated = True
            if outdated:
                self.json_file["MapData"][room]["NoTraverse"] = sorted(no_traverse)
            offset += 1
        #Update 2.9.2
        for file in os.listdir("Data\\ExtraRoom"):
            name = os.path.splitext(file)[0]
            if not name in self.json_file["MapData"]:
                with open("Data\\ExtraRoom\\" + file, "r", encoding="utf8") as file_reader:
                    extra_room = json.load(file_reader)
                self.json_file["MapData"][name] = extra_room
    
    def exception_hook(self, exc_type, exc_value, exc_traceback):
        box = QMessageBox(self)
        box.setWindowTitle("Error")
        box.setIcon(QMessageBox.Critical)
        box.setText("An error has occured")
        traceback_format = traceback.format_exception(exc_type, exc_value, exc_traceback)
        traceback_string = "".join(traceback_format)
        box.setInformativeText(traceback_string)
        box.exec()

def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()