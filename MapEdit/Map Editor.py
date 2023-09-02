import json
import sys
import os
import copy
import colorsys
from enum import Enum
from collections import OrderedDict
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

script_name, script_extension = os.path.splitext(os.path.basename(__file__))

DEFAULT_MAP = "Data\\PB_DT_RoomMaster.json"

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

music_id = []
music_name = []
play_id = []
play_name = []

restrictions = False

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

def modify_color_with_hsv(color, hue_mod, sat_mod, val_mod):
    hsv = colorsys.rgb_to_hsv(int(color[-6:-4], 16)/255, int(color[-4:-2], 16)/255, int(color[-2: len(color)], 16)/255)
    hue = (hsv[0] + hue_mod) % 1
    if sat_mod < 1:
        sat = hsv[1] * sat_mod
    else:
        sat = hsv[1] + (1 - hsv[1])*(sat_mod - 1)
    if val_mod < 1:
        val = hsv[2] * val_mod
    else:
        val = hsv[2] + (1 - hsv[2])*(val_mod - 1)
    rgb = colorsys.hsv_to_rgb(hue, sat, val)
    return color[:-6] + "{:02x}".format(round(rgb[0]*255)) + "{:02x}".format(round(rgb[1]*255)) + "{:02x}".format(round(rgb[2]*255))

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

class RoomTheme(Enum):
    Default = 0
    Light   = 1
    Dark    = 2

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

class Void:
    def __init__(self, x_block, z_block):
        self.x_block = x_block
        self.z_block = z_block

class RoomItem(QGraphicsRectItem):
    def __init__(self, index, room_data, outline, fill, opacity, can_move, group_list, main_window, metadata=None, parent=None):
        super().__init__(0, 0, room_data.width * TILEWIDTH, room_data.height * TILEHEIGHT, parent)
        self.setData(KEY_METADATA, metadata)
        self.setCursor(Qt.PointingHandCursor)
        
        self.index = index
        self.room_data = room_data
        self.outline = QPen(outline)
        self.outline.setWidth(OUTLINE)
        self.outline.setJoinStyle(Qt.MiterJoin)
        self.fill = fill
        self.opacity = opacity
        self.can_move = can_move
        self.group_list = group_list
        self.main_window = main_window
        
        self.room_theme = {}
        self.current_theme = RoomTheme.Default
        self.icon_inverted = False
        
        self.setPen(self.outline)
        self.set_fill(self.fill)
        self.set_theme(self.current_theme)
        self.setToolTip(room_data.name)
        self.reset_pos()
        self.reset_flags()
        self.reset_layer(False)
    
    def set_fill(self, color):
        self.room_theme[RoomTheme.Default] = color
        self.room_theme[RoomTheme.Light]   = modify_color_with_hsv(color, 0, 1/3, 1.75)
        self.room_theme[RoomTheme.Dark]    = modify_color_with_hsv(color, 0,   1, 0.25)
        self.reset_brush()
    
    def set_theme(self, theme):
        self.current_theme = theme
        if theme == RoomTheme.Dark:
            if not self.icon_inverted:
                self.invert_icon()
        elif self.icon_inverted:
            self.invert_icon()
        self.reset_brush()
    
    def reset_pos(self):
        self.setPos(self.room_data.offset_x * TILEWIDTH, self.room_data.offset_z * TILEHEIGHT)
    
    def reset_brush(self):
        self.fill = self.room_theme[self.current_theme]
        self.setBrush(QColor(self.fill[:1] + "{:02x}".format(round(self.opacity*255)) + self.fill[1:]))
        for i in self.childItems():
            if type(i) == QGraphicsRectItem:
                i.setBrush(QColor(self.fill))
    
    def reset_flags(self):
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsFocusable)
        if self.can_move or not restrictions:
            self.setFlag(QGraphicsItem.ItemIsMovable, True)
    
    def set_static(self):
        self.setFlags(QGraphicsItem.ItemSendsGeometryChanges)
    
    def invert_icon(self):
        self.icon_inverted = not self.icon_inverted
        for i in self.childItems():
            if type(i) == QGraphicsPixmapItem:
                image = i.pixmap().toImage()
                image.invertPixels()
                i.setPixmap(QPixmap.fromImage(image))
    
    def paint(self, painter, option, widget):
        option.state &= ~QStyle.State_Selected
        super().paint(painter, option, widget)
    
    def reset_layer(self, has_priority):
        if has_priority:
            self.setZValue(74 - self.room_data.width*self.room_data.height)
        else:
            self.setZValue(0 - self.room_data.width*self.room_data.height)
    
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemSelectedChange:
            if value:
                self.set_theme(RoomTheme.Light)
            else:
                self.set_theme(RoomTheme.Default)
            self.reset_layer(value and (self.can_move or not restrictions))
        return super().itemChange(change, value)

    def mousePressEvent(self, event):
        if right_held or mid_held or x1_held or x2_held:
            return
        super().mousePressEvent(event)
        #Normal mode selection
        for i in self.scene().selectedItems():
            if restrictions:
                for e in i.group_list:
                    self.main_window.room_list[e].setSelected(True)
    
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
            i.apply_round()
            #Change a backer room's area id based on what it is connected to
            if "m88BKR" in i.room_data.name:
                for e in self.main_window.room_list:
                    if "m88BKR" in e.room_data.name:
                        continue
                    if e.room_data.out_of_map:
                        continue
                    if i.room_data.room_path == "ERoomPath::Left":
                        if e.room_data.offset_x == round(i.room_data.offset_x - e.room_data.width) and round(i.room_data.offset_z - e.room_data.height - 1, 1) <= e.room_data.offset_z <= round(i.room_data.offset_z + i.room_data.height - 1):
                            for o in e.room_data.door_flag:
                                if o.direction_part == Direction.RIGHT and 0 == (o.z_block + e.room_data.offset_z - i.room_data.offset_z):
                                    if e.room_data.area != i.room_data.area:
                                        i.room_data.area = e.room_data.area
                                        self.main_window.music_drop_down.setCurrentIndex(music_id.index(e.room_data.music))
                    if i.room_data.room_path == "ERoomPath::Right":
                        if e.room_data.offset_x == round(i.room_data.offset_x + i.room_data.width) and round(i.room_data.offset_z - e.room_data.height - 1, 1) <= e.room_data.offset_z <= round(i.room_data.offset_z + i.room_data.height - 1):
                            for o in e.room_data.door_flag:
                                if o.direction_part == Direction.LEFT and 0 == (o.z_block + e.room_data.offset_z - i.room_data.offset_z):
                                    if e.room_data.area != i.room_data.area:
                                        i.room_data.area = e.room_data.area
                                        self.main_window.music_drop_down.setCurrentIndex(music_id.index(e.room_data.music))
                if i.room_data.area == "EAreaID::None":
                    i.set_fill(area_color[18])
                else:
                    i.set_fill(area_color[int(i.room_data.area.split("::")[-1][1:3]) - 1])
    
    def mouseDoubleClickEvent(self, event):
        if right_held or mid_held or x1_held or x2_held:
            return
        super().mouseDoubleClickEvent(event)
        #Select all rooms belonging to the same area
        if self.room_data.area != "EAreaID::None":
            for i in self.main_window.room_list:
                if i.room_data.area == self.room_data.area:
                    i.setSelected(True)

    def apply_round(self):
        #Snap room to grid
        self.room_data.offset_x = round(self.pos().x() / TILEWIDTH)
        self.room_data.offset_z = round(self.pos().y() / TILEHEIGHT)
        #The train room's z offset must always be positive
        if self.room_data.name == "m09TRN_002" and self.room_data.offset_z < 0 and restrictions:
            self.room_data.offset_z = 0
        self.reset_pos()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.unsaved = False
        self.reset()
        
    def initUI(self):
        self.setStyleSheet("QWidget{background:transparent; color: #ffffff; font-family: Cambria; font-size: 18px}"
        + "QMainWindow{background-image: url(Data/background.png); background-position: center}"
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
        + "QPushButton{background-color: #21222e}"
        + "QListWidget{background-color: #21222e; border: 1px solid #21222e}"
        + "QScrollBar::add-page{background-color: #1b1c26}"
        + "QScrollBar::sub-page{background-color: #1b1c26}"
        + "QToolTip{border: 0px; background-color: #21222e; color: #ffffff; font-family: Cambria; font-size: 18px}")
        
        #Graphics
        
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self) 
        self.scene.selectionChanged.connect(self.selection_event)
        self.view.setDragMode(QGraphicsView.RubberBandDrag)
        self.scene.installEventFilter(self)
        
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setAlignment(Qt.AlignLeft)
        self.view.scale(1, -1)
        self.current_zoom = 1
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
        
        boss_res = QAction("Boss restrictions", self)
        boss_res.triggered.connect(self.boss_res)
        help_bar.addAction(boss_res)
        
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
        self.zoom_in.setToolTip("Zoom in\nShortcut: Ctrl + Plus")
        self.zoom_in.clicked.connect(self.zoom_in_action)
        self.zoom_in.setFixedSize(50, 30)
        
        self.zoom_out = QPushButton()
        self.zoom_out.setShortcut(QKeySequence(Qt.CTRL | Qt.Key_Minus))
        self.zoom_out.setIcon(QIcon("Data\\Icon\\out_icon.png"))
        self.zoom_out.setToolTip("Zoom out\nShortcut: Ctrl + Minus")
        self.zoom_out.clicked.connect(self.zoom_out_action)
        self.zoom_out.setFixedSize(50, 30)
        self.zoom_out.setEnabled(False)
        
        #Labels
        
        self.lock_label = QLabel()
        self.lock_label.setPixmap(QPixmap("Data\\Icon\\lock_icon.png"))
        
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
        
        #Layouts
        
        hbox_top = QHBoxLayout()
        hbox_top.addWidget(self.lock_label)
        hbox_top.addWidget(self.key_drop_down)
        hbox_top.addWidget(self.seed_label)
        hbox_top.addStretch(1)
        hbox_top.addWidget(self.music_drop_down)
        hbox_top.addWidget(self.play_drop_down)
        
        hbox_center = QHBoxLayout()
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
        self.show()
    
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
            self.string = self.path.replace("/", "\\")
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
            self.string = self.path.replace("/", "\\")
            self.title_string = " (" + self.string + ")"
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
        global restrictions
        if self.use_restr.isChecked():
            restrictions = True
            self.lock_label.setPixmap(QPixmap("Data\\Icon\\lock_icon.png"))
        else:
            restrictions = False
            self.lock_label.setPixmap(QPixmap("Data\\Icon\\unlock_icon.png"))
        for i in self.room_list:
            i.reset_flags()
            i.setSelected(False)
    
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
        if self.room_search.isChecked():
            #Disable other tools
            self.area_order.setChecked(False)
            self.area_order_action()
            self.key_location.setChecked(False)
            self.key_location_action()
            #Initiate
            self.disable_menus()
            self.disable_buttons()
            for i in self.room_list:
                i.setSelected(False)
                i.set_static()
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
            #Initiate
            self.disable_menus()
            self.disable_buttons()
            for i in self.room_list:
                i.setSelected(False)
                i.set_static()
            self.area_order_list.setCurrentItem(self.area_order_list.item(0))
            self.area_order_list_change(self.area_order_list.item(0))
            self.area_order_list.setVisible(True)
        else:
            self.area_order_list.setVisible(False)
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
            #CheckLog
            name, extension = os.path.splitext(self.string)
            box = QMessageBox(self)
            box.setWindowTitle("Error")
            box.setIcon(QMessageBox.Critical)
            try:
                log_path = os.path.abspath(os.path.join("", os.pardir)) + "\\SpoilerLog\\KeyLocation.json"
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
            for i in self.log["Key"]:
                self.key_drop_down.addItem(i)
            #Initiate
            self.disable_menus()
            self.disable_buttons()
            for i in self.room_list:
                i.setSelected(False)
                i.set_static()
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
        box.setText("Map Editor:\n\nThis editor allows you to fully customize the layout of the game's map. You can click and drag each room to change its location on the grid and you can select entire areas by double-clicking one of its rooms.\nSave your creations to the Custom folder for them to be picked by the randomizer.\n\nArea Order:\n\nA simple tool that lets you reorder the difficulty scaling of each area. Try to arrange these in the order that the player will most likely traverse them.\n\nYou can submit your own layout creations to me on Discord (Lakifume#4066) if you want them to be added as presets in the main download of the randomizer.")
        box.exec()
    
    def guidelines(self):
        box = QMessageBox(self)
        box.setWindowTitle("Map guidelines")
        box.setText("Here are some tips that will help you build maps that are fun to play on:\n\n• making use of as many rooms as possible\n• connecting as many entrances as possible\n• keeping each area separated using transition rooms\n• ensuring that boss rooms are placed relatively close to a save/warp point\n• having the \"Use restrictions\" option enabled while building your map\n• not overlapping any rooms except for the semi-transparent ones\n• keeping the layout of the map within the area visible with Space Bar\n\nAdditionally here are some useful things to know when building maps:\n\n• backer rooms can be connected to any area and will be automatically updated\n• a few bosses can softlock if their rooms are placed in undesirable spots, refer to the Boss restrictions page for more info\n• room m03ENT_1200 has a transition that does not work properly when connected to a different room, so the randomizer script will ignore this room when connecting the map\n• the in-game minimap has a limitation as to how far it can display rooms, you can preview this limitation by pressing the space bar")
        box.exec()
    
    def boss_res(self):
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
                self.set_unsaved()
    
    def swap_action(self):
        for i in self.scene.selectedItems():
            if i.room_data.room_type == "ERoomType::Save":
                i.room_data.room_type = "ERoomType::Warp"
                i.childItems()[0].setPixmap(QPixmap("Data\\Icon\\warp.png"))
            elif i.room_data.room_type == "ERoomType::Warp":
                i.room_data.room_type = "ERoomType::Save"
                i.childItems()[0].setPixmap(QPixmap("Data\\Icon\\save.png"))
            self.set_unsaved()
    
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
                room_data.offset_x = i.room_data.offset_x + 1
                room_data.offset_z = i.room_data.offset_z - 1
                room = RoomItem(len(self.room_list), room_data, i.outline, i.fill, i.opacity, True, [], self)
                self.scene.addItem(room)
                self.room_list.append(room)
                self.add_room_items(room)
                self.room_search_list.addItem(room_data.name)
                self.use_restr_action()
                self.show_out_action()
                self.show_name_action()
                room.setSelected(True)
    
    def delete_action(self):
        #Only delete rooms that were previously added by the user
        for i in self.scene.selectedItems():   
            current_inst = int(i.room_data.name.split("_")[-1])
            if current_inst//100 == 13:
                self.scene.removeItem(i)
                self.room_list.remove(i)
                self.room_search_list.takeItem(self.room_search_list.row(self.room_search_list.findItems(i.room_data.name, Qt.MatchExactly)[0]))
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
    
    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Space:
            self.map_limit.setVisible(True)
    
    def keyReleaseEvent(self, event):
        super().keyReleaseEvent(event)
        if event.key() == Qt.Key_Space:
            self.map_limit.setVisible(False)
    
    def room_search_list_change(self, item):
        for i in self.room_list:
            i.set_theme(RoomTheme.Dark)
        self.room_list[self.room_search_list.currentRow()].set_theme(RoomTheme.Default)
    
    def area_order_list_change(self, item):
        for i in self.room_list:
            if i.room_data.area == "EAreaID::" + item.text():
                i.set_theme(RoomTheme.Default)
            else:
                i.set_theme(RoomTheme.Dark)
        self.set_unsaved()
    
    def key_drop_down_change(self, index):
        for i in self.room_list:
            if i.room_data.name in self.log["Key"][self.key_drop_down.itemText(index)]:
                i.set_theme(RoomTheme.Default)
            else:
                i.set_theme(RoomTheme.Dark)
    
    def music_drop_down_change(self, index):
        for i in self.scene.selectedItems():
            i.room_data.music = music_id[index]
        self.set_unsaved()
    
    def play_drop_down_change(self, index):
        for i in self.scene.selectedItems():
            i.room_data.play = play_id[index]
        self.set_unsaved()
    
    def restore_music_action(self):
        #Confirm
        choice = QMessageBox.question(self, "Confirm", "This will set all music settings back to default.\nProceed ?", QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.No:
            return
        #Copy music from the vanilla map
        with open(DEFAULT_MAP, "r") as file_reader:
            copy_from = json.load(file_reader)
        for i in self.room_list:
            if i.room_data.name in copy_from["MapData"]:
                i.room_data.music = copy_from["MapData"][i.room_data.name]["BgmID"]
                i.room_data.play  = copy_from["MapData"][i.room_data.name]["BgmType"]
            else:
                area_save = i.room_data.name.split("_")[0] + "_1000"
                i.room_data.music = copy_from["MapData"][area_save]["BgmID"]
                i.room_data.play  = copy_from["MapData"][area_save]["BgmType"]
            i.setSelected(False)
        self.set_unsaved()
    
    def reset_rooms(self):
        for i in self.room_list:
            if not i.room_data.out_of_map:
                i.setVisible(True)
            i.setSelected(False)
            i.set_theme(RoomTheme.Default)
            i.reset_flags()
    
    def change_title(self, suffix):
        self.setWindowTitle(script_name + self.title_string + suffix)
    
    def set_unsaved(self):
        if not self.unsaved:
            self.change_title("*")
            self.unsaved = True

    def selection_event(self):
        self.set_unsaved()
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
        no_traverse = self.convert_no_traverse_to_block(json["NoTraverse"], width)
        music       = json["BgmID"]
        play        = json["BgmType"]
        
        room = Room(name, area, out_of_map, room_type, room_path, width, height, offset_x, offset_z, door_flag, no_traverse, music, play)
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
    
    def convert_no_traverse_to_block(self, no_traverse, width):
        void_list = []
        for i in no_traverse:
            tile_index = i - 1
            if width == 0:
                x_block = tile_index
                z_block = 0
            else:
                x_block = tile_index % width
                z_block = tile_index // width
            void = Void(x_block, z_block)
            void_list.append(void)
        return void_list
    
    def convert_block_to_no_traverse(self, block, width):
        no_traverse_list = []
        for i in block:
            no_traverse_list.append(i.x_block + i.z_block*width + 1)
        return no_traverse_list
    
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
        
        self.map_limit = self.scene.addRect(0, -24*TILEHEIGHT, 136*TILEWIDTH, 72*TILEHEIGHT, QPen("#00000000"), QColor("#320288ff"))
        self.map_limit.setVisible(False)
        
        index = 0
        for i in self.json_file["MapData"]:
            
            #Converting data
            
            room_data = self.convert_json_to_room(i, self.json_file["MapData"][i])
            self.room_search_list.addItem(room_data.name)
            group_list = []
            can_move = True
            
            #No width rooms
            
            if room_data.width == 0:
                room_data.width = 0.5
            if room_data.height == 0:
                room_data.height = 0.5
            
            #Area color
            
            if room_data.out_of_map:
                fill = area_color[18]
            else:
                fill = area_color[int(room_data.area.split("::")[-1][1:3]) - 1]
            
            #Room outline
            
            outline = "#ffffff"
            
            #Room group
            
            for e in connected_room:
                if room_data.name in e["Room"]:
                    group_list = e["Room"]
                    can_move = e["CanMove"]
                    break
            
            #Room opacity
            
            if room_data.room_type == "ERoomType::Load"or room_data.name == "m02VIL_000":
                opacity = 0.5
            else:
                opacity = 1
            
            #Creating room
            
            room = RoomItem(index, room_data, outline, fill, opacity, can_move, self.convert_group_to_index(group_list), self)
            self.scene.addItem(room)
            self.room_list.append(room)
            self.add_room_items(room)
            
            index += 1
            
    def add_room_items(self, room):
        outline = QPen("#00000000")
        outline.setWidth(OUTLINE)
        outline.setJoinStyle(Qt.MiterJoin)
        default_fill = room.room_theme[room.current_theme]
        
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
        if room.room_data.name == "m05SAN_019":
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
        
        if room.room_data.name in ["m11UGD_021", "m11UGD_022", "m11UGD_023", "m11UGD_024", "m11UGD_025", "m11UGD_026", "m11UGD_044", "m11UGD_045"]:
            for e in range(room.room_data.width):
                for o in range(room.room_data.height):
                    icon = self.scene.addPixmap(QPixmap("Data\\Icon\\bubble.png"))
                    icon.setTransform(QTransform.fromScale(1, -1))
                    icon.setPos(e*TILEWIDTH + 6, o*TILEHEIGHT + 13.5)
                    icon.setParentItem(room)
        if room.room_data.name in ["m11UGD_005", "m11UGD_036"]:
            for e in range(room.room_data.width):
                icon = self.scene.addPixmap(QPixmap("Data\\Icon\\wave.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(e*TILEWIDTH + 6, 20.5)
                icon.setParentItem(room)
        if room.room_data.name in ["m11UGD_019", "m11UGD_040"]:
            for e in range(room.room_data.width):
                icon = self.scene.addPixmap(QPixmap("Data\\Icon\\wave.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(e*TILEWIDTH + 6, 28.5)
                icon.setParentItem(room)
        if room.room_data.name in ["m11UGD_042", "m11UGD_046"]:
            for e in range(room.room_data.width):
                icon = self.scene.addPixmap(QPixmap("Data\\Icon\\wave.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(e*TILEWIDTH + 6, 43.5)
                icon.setParentItem(room)
        if room.room_data.name in ["m11UGD_043"]:
            for e in range(room.room_data.width - 1):
                icon = self.scene.addPixmap(QPixmap("Data\\Icon\\wave.png"))
                icon.setTransform(QTransform.fromScale(1, -1))
                icon.setPos(e*TILEWIDTH + 6, 13.5)
                icon.setParentItem(room)
        
        #No traverse
        
        for e in room.room_data.no_traverse:
            icon = self.scene.addPixmap(QPixmap("Data\\Icon\\void.png"))
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
        text.setPos(room.room_data.width*TILEWIDTH/2 - text.document().size().width()/8, room.room_data.height*TILEHEIGHT/2 + TILEHEIGHT/2 - 0.5)
        text.setParentItem(room)
    
    def fill_area(self):
        for i in self.json_file["AreaOrder"]:
            self.area_order_list.addItem(i)

    def update_map(self):
        self.json_file["MapData"].clear()
        for i in self.room_list:
            self.json_file["MapData"][i.room_data.name] = {}
            self.json_file["MapData"][i.room_data.name]["AreaID"]         = i.room_data.area
            self.json_file["MapData"][i.room_data.name]["OutOfMap"]       = i.room_data.out_of_map
            self.json_file["MapData"][i.room_data.name]["RoomType"]       = i.room_data.room_type
            self.json_file["MapData"][i.room_data.name]["RoomPath"]       = i.room_data.room_path
            self.json_file["MapData"][i.room_data.name]["AreaWidthSize"]  = i.room_data.width
            self.json_file["MapData"][i.room_data.name]["AreaHeightSize"] = i.room_data.height
            self.json_file["MapData"][i.room_data.name]["OffsetX"]        = round(i.room_data.offset_x * 12.6, 1)
            self.json_file["MapData"][i.room_data.name]["OffsetZ"]        = round(i.room_data.offset_z *  7.2, 1)
            self.json_file["MapData"][i.room_data.name]["DoorFlag"]       = self.convert_door_to_flag(i.room_data.door_flag, self.json_file["MapData"][i.room_data.name]["AreaWidthSize"])
            self.json_file["MapData"][i.room_data.name]["NoTraverse"]     = self.convert_block_to_no_traverse(i.room_data.no_traverse, self.json_file["MapData"][i.room_data.name]["AreaWidthSize"])
            self.json_file["MapData"][i.room_data.name]["BgmID"]          = i.room_data.music
            self.json_file["MapData"][i.room_data.name]["BgmType"]        = i.room_data.play
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
        for i in range(self.area_order_list.count()):
            self.json_file["AreaOrder"].append(self.area_order_list.item(i).text())
    
    def update_json(self):
        #Update 2.9.0
        if "KeyLogic" in self.json_file:
            del self.json_file["KeyLogic"]
        for i in self.json_file["MapData"]:
            if "Unused" in self.json_file["MapData"][i]:
                del self.json_file["MapData"][i]["Unused"]
        #Update 2.9.1
        offset = 2
        for i in ["m11UGD_013", "m11UGD_031"]:
            no_traverse = []
            outdated = False
            for e in self.json_file["MapData"][i]["NoTraverse"]:
                no_traverse.append(e + offset*self.json_file["MapData"][i]["AreaWidthSize"])
                if e < 0:
                    outdated = True
            if outdated:
                self.json_file["MapData"][i]["NoTraverse"] = sorted(no_traverse)
            offset += 1
        #Update 2.9.2
        for i in os.listdir("Data\\ExtraRoom"):
            name, extension = os.path.splitext(i)
            if not name in self.json_file["MapData"]:
                with open("Data\\ExtraRoom\\" + i, "r", encoding="utf8") as file_reader:
                    extra_room = json.load(file_reader)
                self.json_file["MapData"][name] = extra_room

def main():
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()