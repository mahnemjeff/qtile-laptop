# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess
import socket
import re
from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.command import lazy

# Colors

colors = {
    "rosewater"   : "#f4dbd6",
    "flamingo"    : "#f0c6c6",
    "pink"        : "#f5bde6",
    "mauve"       : "#c6a0f6",
    "red"         : "#ed8796",
    "maroon"      : "#ee99a0",
    "peach"       : "#f5a97f",
    "yellow"      : "#eed49f",
    "green"       : "#a6da95",
    "teal"        : "#8bd5ca",
    "sky"         : "#91d7e3",
    "sapphire"    : "#7dc4e4",
    "blue"        : "#8aadf4",
    "lavender"    : "#b7bdf8",
    "text"        : "#cad3f5",
    "subtext1"    : "#b8c0e0",
    "subtext0"    : "#a5adcb",
    "overlay2"    : "#939ab7",
    "overlay1"    : "#8087a2",
    "overlay0"    : "#6e738d",
    "surface2"    : "#5b6078",
    "surface1"    : "#494d64",
    "surface0"    : "#363a4f",
    "base"        : "#24273a",
    "mantle"      : "#1e2030",
    "crust"       : "#181926"
}


mod = "mod4"
terminal = "alacritty"

# ????????? ????????? ????????? ????????? ??? ???????????? ????????? ??????
# ????????? ????????? ????????? ????????? ??? ???????????? ????????? ??????



keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"],"Return",lazy.layout.toggle_split(),desc="Toggle between split and unsplit sides of stack",),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("rofi -show combi"), desc="Spawn a command using a prompt widget"),

    ##CUSTOM
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume 0 +5%"), desc='Volume Up'),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume 0 -5%"), desc='volume down'),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute 0 toggle"), desc='Volume Mute'),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc='playerctl'),
    Key([mod], "XF86AudioLowerVolume", lazy.spawn("playerctl previous"), desc='playerctl'),
    Key([mod], "XF86AudioRaiseVolume", lazy.spawn("playerctl next"), desc='playerctl'),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl s 5%+"), desc='brightness UP'),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl s 5%-"), desc='brightness Down'),
    Key([mod, "shift"], "f", lazy.window.toggle_floating(),  desc="Toggle floating window."),
    #Key([mod], "m",lazy.layout.maximize(),desc='toggle window between minimum and maximum sizes'),
    Key([mod, "shift" ], "q", lazy.spawn("rofi -show power-menu -modi power-menu:rofi-power-menu"), desc='power menu'),
    Key([mod], "e", lazy.spawn("thunar"), desc='file browser'),
    Key([mod], "s", lazy.spawn("flatpak run com.spotify.Client "), desc='music player'),
    Key([mod, "shift"], "b", lazy.spawn("firefox --private-window"), desc='firefox incognito'),
    Key([mod], "b", lazy.spawn("firefox"), desc='firefox browser'),
    Key([mod, "shift"], "x",lazy.spawn("alacritty -e betterlockscreen -l"), desc='lockscreen'),
    Key([mod, "shift"], "e", lazy.spawn("flatpak run com.microsoft.Edge"), desc='Microsoft edge'),
    Key([mod, "shift"], "s", lazy.spawn("flameshot gui"), desc='screenshot'),
]





# ????????? ????????? ????????? ????????? ????????? ??????
# ????????? ????????? ????????? ????????? ????????? ??????


groups = [Group(f"{i+1}", label="???") for i in range(8)]

for i in groups:
    keys.extend(
            [
                Key(
                    [mod],
                    i.name,
                    lazy.group[i.name].toscreen(),
                    desc="Switch to group {}".format(i.name),
                    ),
                Key(
                    [mod, "shift"],
                    i.name,
                    lazy.window.togroup(i.name, switch_group=True),
                    desc="Switch to & move focused window to group {}".format(i.name),
                    ),
                ]
            )

# Append scratchpad with dropdowns to groups
groups.append(ScratchPad('scratchpad', [
    DropDown('term', 'alacritty',  width=0.8, height=0.8, x=0.1, y=0.1, opacity=1),
    DropDown('mixer', 'pavucontrol', width=0.8, height=0.8, x=0.1, y=0.1, opacity=0.9),
    DropDown('ranger', 'alacritty --class=ranger -e ranger',  width=0.8, height=0.8, x=0.1, y=0.1, opacity=0.9),
]))
# extend keys list with keybinding for scratchpad
keys.extend([
    Key(["control"], "1", lazy.group['scratchpad'].dropdown_toggle('term')),
    Key(["control"], "2", lazy.group['scratchpad'].dropdown_toggle('mixer')),
    Key(["control"], "3", lazy.group['scratchpad'].dropdown_toggle('ranger')),
])



layouts = [
    layout.Columns( margin=4, border_focus='#1F1D2E',
	    border_normal='#1F1D2E', 
        border_width=0
    ),
    
    layout.Max(	border_focus='#1F1D2E',
	    border_normal='#1F1D2E',
	    margin=4,
	    border_width=0,
    ),
    
    layout.Floating(	border_focus='#1F1D2E',
	    border_normal='#1F1D2E',
	    margin=4,
	    border_width=0,
	),
    # Try more layouts by unleashing below layouts
   #  layout.Stack(num_stacks=2),
   #  layout.Bsp(),
     layout.Matrix(	border_focus='#1F1D2E',
	    border_normal='#1F1D2E',
	    margin=4,
	    border_width=0,
	),
     layout.MonadTall(	border_focus='#1F1D2E',
	    border_normal='#1F1D2E',
        margin=4,
	    border_width=0,
	),
    layout.MonadWide(	border_focus='#1F1D2E',
	    border_normal='#1F1D2E',
	    margin=4,
	    border_width=0,
	),
   #  layout.RatioTile(),
     layout.Tile(	border_focus='#1F1D2E',
	    border_normal='#1F1D2E',
    ),
   #  layout.TreeTab(),
   #  layout.VerticalTile(),
   #  layout.Zoomy(),
]

def open_launcher():
    qtile.cmd_spawn("rofi -show drun")


widget_defaults = dict(
    font="JetBrainsMono Nerd Font",
    fontsize=13,
    padding=3,
)
extension_defaults = widget_defaults.copy()

# ????????? ????????? ?????????
# ????????? ????????? ?????????
 
# screens = [

#     Screen(
#         top=bar.Bar(
#             [
# 				widget.Spacer(length=20,
#                     background='#1F1D2E',
#                 ),
				

#                 widget.Image(
#                     filename='~/.config/qtile/Assets/launch_Icon.png',
#                     margin=2,
#                     background='#1F1D2E',
#                     mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("rofi -show drun")}
#                 ),

#                 widget.Image(
#                     filename='~/.config/qtile/Assets/6.png',
#                 ),

#                 widget.GroupBox(
#                     fontsize=16,
#                     borderwidth=3,
#                     highlight_method='block',
#                     active='#7F61A7',
#                     block_highlight_text_color="#CFB3E5",
#                     highlight_color='#4B427E',
#                     inactive='#BD85CB',
#                     foreground='#4B427E',
#                     background='#4B427E',
#                     this_current_screen_border='#52548D',
#                     this_screen_border='#52548D',
#                     other_current_screen_border='#52548D',
#                     other_screen_border='#52548D',
#                     urgent_border='#52548D',
#                     rounded=True,
#                     disable_drag=True,
#                  ),

#                 widget.Image(
#                     filename='~/.config/qtile/Assets/5.png',
#                 ),

#                 widget.CurrentLayoutIcon(
#                     background='#52548D',
#                     padding = 0,
#                     scale = 0.5,
#                 ),

#                     widget.CurrentLayout(
#                     background='#52548D',
#                     font= 'JetBrains Mono Bold',
#                 ),

#                 widget.Image(
#                     filename='~/.config/qtile/Assets/4.png',                
#                 ),

#                 widget.WindowName(
#                     background = '#7676B2',
#                     format = "{name}",
#                     font='JetBrains Mono Bold',
#                     empty_group_string = 'Desktop',
#                 ),


#                 widget.Image(
#                     filename='~/.config/qtile/Assets/3.png',                
#                 ),   

#                 widget.Systray(
#                     background='#52548D',
#                     fontsize=2,
#                 ),

#                 widget.TextBox(
#                     text=' ',
#                     background='#52548D',
#                 ),


#                 widget.Image(
#                     filename='~/.config/qtile/Assets/2.png',                
#                     background='#52548D',
#                 ),                       
                                                
#                 widget.TextBox(
#                     text='???',
#                     size=20,
#                     font='JetBrains Mono Bold',
#                     background='#4B427E',
#                 ),

                
#                 widget.Battery(format=' {percent:2.0%}',
#                     font="JetBrains Mono ExtraBold",
#                     fontsize=12,
#                     charge_char='???',
#                     discharge_char='',
#                     low_percentage=0.25,
#                     low_background='#82aaff',
#                     low_foreground='#282d3e',
#                     update_interval=1,
#                     padding=10,
#                     background='#4b427E',
#                 ),                     
                
#                 widget.Memory(format='???{MemUsed: .0f}{mm}',
#                     font="JetBrains Mono Bold",
#                     fontsize=12,
#                     padding=10,
#                     background='#4B427E',
#                 ),

#                 widget.TextBox(
#                     text="???",
#                     font="Font Awesome 6 Free Solid",
#                     fontsize=25,
#                     padding=10,
#                     background='#4B427E',
#                     mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("pavucontrol")}
#                    ),
                

#                 widget.Image(
#                     filename='~/.config/qtile/Assets/1.png',                
#                     background='#4B427E',
#                 ),
        
#                 widget.Clock(
#                     format='???  %I:%M %p',
#                     background='#1F1D2E',
#                     font="JetBrains Mono Bold",
#                 ),

#                 widget.Spacer(
#                     length=18,
#                     background='#1F1D2E',
#                 ),

                
#             ],
#             30,
#             margin = [6,6,6,6]
#         ),
#     ),
# ]

# ????????? ????????? ?????????
# ????????? ????????? ?????????
## from cufta22

screens = [
    Screen(
        top=bar.Bar(
            [
				widget.Spacer(
                    length = 10,
                ),

                widget.Image(
                    filename  = '~/.config/qtile/assets/bar/qtile.png',
                    margin    = 7,
                     mouse_callbacks  = {
                        'Button1': lambda: qtile.cmd_spawn('rofi -show drun')
                    }
                ),

                widget.Spacer(
                    length = 10,
                ),

                widget.GroupBox(
                    fontsize                    = 20,
                    margin_y                    = 3,
                    margin_x                    = 5,
                    borderwidth                 = 0,
                    font                        = "Roboto, Regular",
                    active                      = colors["green"],
                    block_highlight_text_color  = colors["red"],
                    inactive                    = colors["sapphire"],
                    rounded                     = True,
                    disable_drag                = True,
                 ),

                # ----------------------------------------

                widget.Spacer(
                    length = bar.STRETCH,
                ),

                # ----------------------------------------                 
  
                widget.Image(
                    filename  = '~/.config/qtile/assets/bar/sun.png',
                    margin    = 8,
                ),
                widget.Backlight(
                    font                 = "Roboto, Regular",
                    foreground           = colors["yellow"],
                    brightness_file      = "/sys/class/backlight/intel_backlight/actual_brightness",
                    max_brightness_file  = "/sys/class/backlight/intel_backlight/max_brightness",
                    fontsize             = 15,
                    padding              = 0,
                ),

                widget.Spacer(
                    length = 16,
                ), 

                widget.Image(
                    filename  = '~/.config/qtile/assets/bar/vol.png',
                    margin    = 8,
                ),
                widget.Volume(
                    font        = "Roboto, Regular",
                    foreground  = colors["blue"],
                    fontsize    = 15,
                    padding     = 0,
                ),

                widget.Spacer(
                    length = 16,
                ),      

                #widget.Memory{format='???{MemUsed: .0f}{mm}',
                #    font        = "Roboto, Regular",
                #    foreground  = colors["lavender"],
                #    fontsize    = 15,
                #    padding     = 0, 
                #        },

                widget.Image(
                    filename  = '~/.config/qtile/assets/bar/bat.png',
                    margin    = 7
                ),         
                widget.Battery(format=' {percent:2.0%}',
                    font        = "Roboto, Regular",
                    foreground  = colors["red"],
                    fontsize    = 15,
                    padding     = 0,
                ),         

                widget.Spacer(
                    length = 30,
                ),
                widget.Spacer(
                    length      =10,
                    background  = colors["surface0"]
                ), 
                widget.Systray(
                    icon_size   = 24,
                    padding     = 0,
                    background  = colors["surface0"]
                ),   
                widget.Spacer(
                    length      = 10,
                    background  = colors["surface0"]
                ), 
                widget.Spacer(
                    length = 20,
                ),
        
                widget.Clock(
                    format  ='%I:%M %p',
                    font    ="Roboto, Regular",
                    fontsize = 15,
                ),
                 widget.Spacer(
                    length = 10,
                ),

                widget.CurrentLayoutIcon(
                    padding  = 0,
                    scale    = 0.6,
                    custom_icon_paths = [
                        os.path.expanduser("~/.config/qtile/assets/layout/"),
                    ],
                ),

                widget.Image(
                    filename         = '~/.config/qtile/assets/bar/power.png',
                    margin           = 8,
                    mouse_callbacks  = {
                        'Button1': lambda: qtile.cmd_spawn('rofi -show power-menu -modi power-menu:rofi-power-menu')
                    }
                ),

                # qtile.cmd_spawn("rofi -show drun")

                widget.Spacer(
                    length = 10,
                ),
            ],
            32,
            margin      = [12, 12, 12, 12],
            background  = colors["base"]
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)

##autostart
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh') # path to my script, under my user directory
    subprocess.call([home])


auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

