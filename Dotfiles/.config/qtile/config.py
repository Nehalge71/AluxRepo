# -*- coding: utf-8 -*-
import os
import re
import socket
import subprocess

from libqtile.config import KeyChord, Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from libqtile import qtile


from typing import List  # noqa: F401

mod = "mod4"                                     # Sets mod key to SUPER/WINDOWS
myTerm = "alacritty"

def htop():
	qtile.cmd_spawn(myTerm + ' -e htop')

def sys_mon():
    qtile.cmd_spawn(myTerm + ' -e gnome-system-monitor')

def vol_tog():
    qtile.cmd_spawn('amixer set Master toggle')

def open_rofi():
    qtile.cmd_spawn('bash /home/alux/.config/qtile/rofi-apps')

def upd():
    qtile.cmd_spawn(myTerm + ' -e sudo pacman -Syyuu')

keys = [

        # Switch between windows in current stack pane
        Key([mod], "k", lazy.layout.down(),                             desc="Move focus down in stack pane"),
        Key([mod], "j", lazy.layout.up(),                               desc="Move focus up in stack pane"),
        Key([mod, "shift"], "Return", lazy.layout.toggle_split(),       desc="Toggle between split and unsplit sides of stack"),
        Key([mod, 'shift'], 'space', lazy.layout.flip()),

        # Swap panes of split stack
        Key([mod, "shift"], "space", lazy.layout.rotate(),              desc="Swap panes of split stack"),

        # Move windows up or down in current stack for Monad Tall Layout
        Key([mod, "control"], "k", lazy.layout.shuffle_down(),          desc="Move window down in current stack "),
        Key([mod, "control"], "j", lazy.layout.shuffle_up(),            desc="Move window up in current stack "),

        # Switch window focus to other pane(s) of stack
        Key([mod], "space", lazy.layout.next(),                         desc="Switch window focus to other pane(s) of stack"),
        Key([mod], "Tab", lazy.next_layout(),                           desc="Toggle between layouts"),
        Key([mod], "e", lazy.to_screen(0),                              desc='Switch Focus to Screen 0'),
        Key([mod], "d", lazy.to_screen(1),                              desc='Switch Focus to Screen 1'),


        # Lazy Boot
        Key([mod, "control"], "r", lazy.restart(),                      desc="Restart qtile"),
        Key([mod, "control"], "Escape", lazy.shutdown(),                     desc="Shutdown qtile"),
        Key([mod], "w", lazy.window.kill(),                             desc="Kill focused window"),


        # Lazy Spawn
        Key([mod, "control"], "Return", lazy.spawn("bash /home/alux/.config/qtile/rofi-apps"),desc='Rofi Run Launcher'),
        Key([mod], "Return", lazy.spawn(myTerm),                        desc="Launch terminal"),
        Key([mod], "r", lazy.spawncmd(),                                desc="Launch run"),
        Key([], 'XF86Mail', lazy.spawn('prospect-mail'),           desc="Launch terminal"),
        Key([], 'XF86Calculator', lazy.spawn('teams-insiders'),           desc="Launch terminal"),
        Key([], 'XF86Tools', lazy.spawn('alacritty -e bash /home/alux/.config/qtile/msp.sh'),           desc="Launch terminal"),
        Key([], 'XF86AudioMute', lazy.spawn('amixer set Master toggle'),           desc="Launch terminal"),

        # Personal KeyBindings

        Key([mod, "control"], 'p', lazy.spawn('clipmenu')),
        Key([mod], 'Escape', lazy.spawn('bash /home/alux/.config/qtile/xss.sh')),
        Key([mod, "control"], 'x', lazy.hide_show_bar("bottom")),
        Key([mod, "control"], "KP_Multiply", lazy.spawn("amixer -D pulse sset Master 2%+")),
        Key([mod, "control"], "KP_Divide", lazy.spawn("amixer -D pulse sset Master 2%-")),
        Key([], "Print", lazy.spawn("gnome-screenshot")),
]

groups = [Group(i) for i in "123450"]

for i in groups:
        keys.extend([
                # mod1 + letter of group = switch to group
                Key([mod], i.name, lazy.group[i.name].toscreen(),               desc="Switch to group {}".format(i.name)),
                        # mod1 + shift + letter of group = switch to & move focused window to group
                Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name)),
                Key([mod, "control"], i.name, lazy.window.togroup(i.name, switch_group=False),
                desc="Switch to & move focused window to group {}".format(i.name)),
        ])

layout_theme = {"border_width": 2,
                "margin": 2,
                "border_focus": "55eedd",
                "border_normal": "30004a"
                }

layouts = [
        layout.Max(),
        layout.Stack(num_stacks=2,margin=1, border_width=1, border_focus="55eedd",border_normal= "30004a" ),
        layout.MonadTall(**layout_theme),
        layout.Max(**layout_theme),
        layout.Tile(shift_windows=True, **layout_theme),
        layout.Floating(**layout_theme)
]

colors = [
        ["#0C0D12", "#0C0D12"], # panel background
        ["#434758", "#434758"], # background for current screen tab
        ["#ffffff", "#ffffff"], # font color for group names
        ["#ff5555", "#ff5555"], # border line color for current tab
        ["#1C1321", "#1C1321"], # border line color for other tab and odd widgets
        ["#271C0D", "#271C0D"], # color for the even widgets
        ["#e1acff", "#e1acff"] # window name '''
]

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
        font="Ubuntu Mono",
        fontsize = 12,
        padding = 2,
        background=colors[2]
)
extension_defaults = widget_defaults.copy()

def init_widgets_list(face='enp0s31f6'):
        widgets_list = [
                widget.Sep(
                        linewidth = 0,
                        padding = 6,
                        foreground = colors[2],
                        background = colors[0]
                        ),
                widget.Image(
                        filename = "~/.config/qtile/icons/ico.png",
                        padding = 6,
                        mouse_callbacks = {'Button1': open_rofi}
                        ),
                widget.GroupBox(
                        font = "Ubuntu Bold",
                        fontsize = 9,
                        margin_y = 3,
                        margin_x = 0,
                        padding_y = 5,
                        padding_x = 3,
                        borderwidth = 3,
                        active = colors[2],
                        inactive = colors[2],
                        rounded = False,
                        highlight_color = colors[1],
                        highlight_method = "line",
                        this_current_screen_border = colors[3],
                        this_screen_border = colors [4],
                        other_current_screen_border = colors[0],
                        other_screen_border = colors[0],
                        foreground = colors[2],
                        background = colors[0]
                        ),
                widget.Prompt(
                        prompt = prompt,
                        font = "Ubuntu Mono",
                        padding = 10,
                        foreground = colors[3],
                        background = colors[1]
                        ),
                widget.Sep(
                        linewidth = 0,
                        padding = 40,
                        foreground = colors[2],
                        background = colors[0]
                        ),
                widget.WindowName(
                        foreground = colors[6],
                        background = colors[0],
                        padding = 0
                        ),
                widget.CPU(
                        background = colors[4],
                        foreground = colors[2]
                        ),
                widget.ThermalSensor(
                        foreground = colors[2],
                        background = colors[5],
                        threshold = 90,
                        padding = 5
                        ),
                widget.Memory(
                        foreground = colors[2],
                        background = colors[4],
                        mouse_callbacks = {'Button1': htop},
                        padding = 5
                        ),
                widget.Net(
                        interface = face,
                        format = '{down} ↓↑ {up}',
                        foreground = colors[2],
                        background = colors[5],
                        mouse_callbacks = {'Button1': sys_mon},
                        padding = 5
                        ),
                widget.TextBox(
                        text = " ⟳",
                        padding = 2,
                        foreground = colors[2],
                        background = colors[4],
                        mouse_callbacks = {'Button1': upd},
                        fontsize = 14
                        ),
                widget.CheckUpdates(
                        padding = 6,
                        distro='Arch',
                        mouse_callbacks = {'Button1':upd},
                        excute='sudo pacman -Syyuu',
                        update_interval = 1800,
                        no_update_string = 'N/A',
                        foreground = colors[2],
                        background = colors[4]
                        ),
                widget.TextBox(
                        text = " Vol:",
                        mouse_callbacks = {'Button1': vol_tog},
                        padding = 2,
                        foreground = colors[2],
                        background = colors[5],
                        fontsize = 11
                        ),
                widget.Volume(
                        padding = 5,
                        mouse_callbacks = {'Button1': vol_tog},
                        foreground = colors[2],
                        background = colors[5]
                        ),
                widget.CurrentLayoutIcon(
                        foreground = colors[0],
                        background = colors[4],
                        padding = 0,
                        scale = 0.5
                        ),
                widget.CurrentLayout(
                        foreground = colors[2],
                        background = colors[4],
                        padding = 5
                        ),
                widget.Clock(
                        foreground = colors[2],
                        background = colors[5],
                        format = "%A, %B %d  [ %H:%M ]"
                        ),
                widget.Sep(
                        linewidth = 0,
                        padding = 10,
                        foreground = colors[0],
                        background = colors[5]
                        ),
                widget.Systray(
                        background = colors[0],
                        padding = 5
                        ),
                ]
        return widgets_list

def init_widgets_screen1():
        widgets_screen1 = init_widgets_list()
        return widgets_screen1                       # Slicing removes unwanted widgets on Monitors 1,3

def init_widgets_screen2(face='enp0s20f0u6'):
        widgets_screen2 = init_widgets_list()
        return widgets_screen2                       # Monitor 2 will display all widgets in widgets_list

def init_screens():
        return [Screen(bottom=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=30)),
                Screen(bottom=bar.Bar(widgets=init_widgets_screen2(), opacity=1.0, size=30))]

if __name__ in ["config", "__main__"]:
        screens = init_screens()
        widgets_list = init_widgets_list()
        widgets_screen1 = init_widgets_screen1()
        widgets_screen2 = init_widgets_screen2()

def window_to_prev_group(qtile):
        if qtile.currentWindow is not None:
                i = qtile.groups.index(qtile.currentGroup)
                qtile.currentWindow.togroup(qtile.groups[i - 1].name)

def window_to_next_group(qtile):
        if qtile.currentWindow is not None:
                i = qtile.groups.index(qtile.currentGroup)
                qtile.currentWindow.togroup(qtile.groups[i + 1].name)

def window_to_previous_screen(qtile):
        i = qtile.screens.index(qtile.current_screen)
        if i != 0:
                group = qtile.screens[i - 1].group.name
                qtile.current_window.togroup(group)

def window_to_next_screen(qtile):
        i = qtile.screens.index(qtile.current_screen)
        if i + 1 != len(qtile.screens):
                group = qtile.screens[i + 1].group.name
                qtile.current_window.togroup(group)

def switch_screens(qtile):
        i = qtile.screens.index(qtile.current_screen)
        group = qtile.screens[i - 1].group
        qtile.current_screen.set_group(group)

mouse = [
        Drag([mod], "Button1", lazy.window.set_position_floating(),
                start=lazy.window.get_position()),
        Drag([mod], "Button3", lazy.window.set_size_floating(),
                start=lazy.window.get_size()),
        Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

auto_fullscreen = True
focus_on_window_activation = "smart"

@hook.subscribe.startup_once
def autostart():
        home = os.path.expanduser('~/.config/qtile/autostart.sh')
        subprocess.call([home])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
