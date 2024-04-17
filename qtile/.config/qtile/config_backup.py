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

from distutils.spawn import spawn
from typing import List  # noqa: F401
from libqtile import bar, layout, widget, extension
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import hook, notify
from libqtile.widget import battery
import os
import subprocess
import json


from libqtile import hook

mod = "mod4"
terminal = guess_terminal("qterminal")

mod = "mod4"
terminal = guess_terminal("alacritty")

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "Left", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "space", lazy.next_screen()),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Custom Keys
    Key([mod], "f", lazy.spawn("firefox"), desc="Ejecutar Firefox"),
    Key([mod], "r", lazy.spawn("rofi -show drun"), desc="Ejecutar Rofi"),
    Key([mod], "c", lazy.spawn("code"), desc="Ejecutar VSCode"),
    Key([mod], "b", lazy.spawn("brave-browser"), desc="Ejecutar Brave"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),


    # Audio
    Key([], "XF86AudioRaiseVolume", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ +5%")),
    Key([], "XF86AudioLowerVolume", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ -5%")),
    Key([], "XF86AudioMute", lazy.spawn(
        "pactl set-sink-mute @DEFAULT_SINK@ toggle")),

    # Brillo
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl s +10%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl s 10%-")),
]

__groups = {
    # Net
    1: Group("", layout="monadtall", spawn='brave-browser', matches=[Match(wm_class=["brave-browser", "Firefox-esr"])]),
    # Dev
    2: Group("", layout="monadtall", spawn="code", matches=[Match(wm_class=["code"])]),
    # Term 1
    3: Group("", layout="bsp", spawn=["alacritty", "alacritty"]),
    # Term 2
    4: Group("", layout="matrix", spawn=["alacritty", "alacritty", "alacritty", "alacritty"]),
    # Music
    5: Group("󰝚", layout="monadtall", spawn="/snap/bin/spotify", matches=[Match(wm_class=["Spotify"])]),
    # Message
    6: Group("󱅰", layout="monadtall"),
    # Folder
    7: Group("", layout="monadtall", spawn="thunar"),

}

groups = [__groups[i] for i in __groups]


def get_group_key(name):
    return [k for k, g in __groups.items() if g.name == name][0]


for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                str(get_group_key(i.name)),
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                str(get_group_key(i.name)),
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(
                    i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    # layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.MonadTall(
        border_focus="8100d5",
        border_normal="1D2330",
        margin=5,
        border_width=2,
        single_border_width=0,
    ),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    layout.Bsp(
        border_focus="8100d5",
        border_normal="1D2330",
        margin=5,
        border_width=2,
        fair=False,
    ),
    layout.Matrix(
        border_focus="8100d5",
        border_normal="1D2330",
        margin=5,
        border_width=2,
    ),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

# Funciones


def get_script_output():
    # Ejecuta el script y obtén su salida
    output = subprocess.check_output(
        ["python", "/home/omega/.config/qtile/ip_privada.py"])
    output = output.strip().decode("utf-8")
    return output


widget_defaults = dict(
    font="Ubuntu Mono Nerd Fonts",
    fontsize=16,
    padding=4,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayout(),
                widget.GroupBox(
                    active="f4f4f4",
                    border_width=1,
                    fontsize=19,
                    highlight_method="text",
                    this_current_screen_border="#8100d5",
                ),
                widget.Prompt(),
                widget.WindowName(
                    foreground="#8100d5",
                    max_chars=50,
                    fontsize=14
                ),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.Systray(
                    icon_size=25,
                ),
                widget.TextBox(
                    text='',
                    foreground='#8100d5',
                    fontsize=20,
                    padding=0,
                    antialias=True,
                    font='Ubuntu Nerd Font'
                ),
                widget.TextBox(
                    text=f'󰲐{get_script_output()}',
                    fontsize=20,
                    font="Arial",
                    padding=5,
                    background="#8100d5",
                ),
                widget.TextBox(
                    text='',
                    foreground='#8100d5',
                    fontsize=20,
                    padding=0,
                    antialias=True,
                    font='Ubuntu Nerd Font'
                ),
                widget.TextBox(
                    text='',
                    foreground='#008000',
                    fontsize=20,
                    padding=0,
                    antialias=True,
                    font='Ubuntu Nerd Font'
                ),
                battery.Battery(
                    background="#008000",  # verde
                    charge_char="󰂄",
                    discharge_char="󰂃",
                    format='{char} {percent:2.0%}',
                    full_char="󱟢",
                    fontsize=16
                ),
                widget.TextBox(
                    text='',
                    foreground='#008000',
                    fontsize=20,
                    padding=0,
                    antialias=True,
                    font='Ubuntu Nerd Font'
                ),
                widget.TextBox(
                    text='',
                    foreground='#0000FF',
                    fontsize=20,
                    padding=0,
                    shadow=True,
                    antialias=True,
                    dgroups_key_binder=None,
                    font='Ubuntu Nerd Font'
                ),
                widget.Clock(
                    format="<span>%a %d %b %I:%M %p</span>",
                    fontsize=16,
                    font="DejaVu Sans Mono",
                    background="#0000FF",
                    shadow=True,
                ),
                widget.TextBox(
                    text='',
                    foreground='#0000FF',
                    fontsize=20,
                    padding=0,
                    antialias=True,
                    font='Ubuntu Nerd Font'
                ),
            ],
            24,
        ),  # Cierre del paréntesis de bar.Bar
    ),
]


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_app_rules = []  # type: List
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
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.run([home])


@hook.subscribe.screen_change
def restart_picom(qtile, ev):
    qtile.cmd_spawn("pkill picom")
    qtile.cmd_spawn("picom -b")
