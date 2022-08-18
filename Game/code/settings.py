level_map = [
'                            ',
'                            ',
'                            ',
' XX    XXX            XX    ',
' XX P                       ',
' XXXX         XX         XX ',
' XXXX       XX              ',
' XX    X  XXXX    XX  XX    ',
'       X  XXXX    XX  XXX   ',
'    XXXX  XXXXXX  XX  XXXX  ',
'XXXXXXXX  XXXXXX  XX  XXXX  ']

## screen setting
tile_size = 64 # 64px
screen_width = 1200
screen_height = len(level_map) * tile_size # for making height responsive

## player setting

player_speed = 8

## frame settting
fps = 60 # frame per second