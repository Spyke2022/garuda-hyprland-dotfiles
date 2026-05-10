#!/bin/bash
WORKSPACE=$1
WALLPAPER_DEFAULT="/home/silas/Imagens/papeis-de-parede/Garuda-TilliDie-cube-105.png"
WALLPAPER_HACKER="/home/silas/Imagens/papeis-de-parede/Garuda_Hacker_Padrao.png"
BORDER_DEFAULT="rgba(33ccffee) rgba(8f00ffee) 45deg"
BORDER_HACKER="rgba(00ff41ee) rgba(008f11ee) 45deg"

if [ "$WORKSPACE" = "5" ]; then
    WALL="$WALLPAPER_HACKER"
    BORDER="$BORDER_HACKER"
else
    WALL="$WALLPAPER_DEFAULT"
    BORDER="$BORDER_DEFAULT"
fi

echo "[eDP-1]" > ~/.config/wpaperd/wallpaper.toml
echo "path = "$WALL"" >> ~/.config/wpaperd/wallpaper.toml
echo "[HDMI-A-1]" >> ~/.config/wpaperd/wallpaper.toml
echo "path = "$WALL"" >> ~/.config/wpaperd/wallpaper.toml
wpaperctl reload
hyprctl keyword general:col.active_border "$BORDER"
