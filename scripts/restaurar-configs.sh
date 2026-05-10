#!/bin/bash
# Script de restauração das configs do Garuda Hyprland
# Autor: Silas de Albuquerque Falcão
# Data: 2026-05-10

echo "Restaurando configs..."

mkdir -p ~/.config/foot
mkdir -p ~/.config/fastfetch
mkdir -p ~/.config/hypr
mkdir -p ~/.config/waybar

cp -r ~/dotfiles/foot/* ~/.config/foot/
cp -r ~/dotfiles/fastfetch/* ~/.config/fastfetch/
cp -r ~/dotfiles/hypr/* ~/.config/hypr/
cp -r ~/dotfiles/waybar/* ~/.config/waybar/

echo "Recarregando Hyprland..."
hyprctl reload

echo "Pronto! Configs restauradas com sucesso."

mkdir -p ~/.config/fish
cp ~/dotfiles/fish/config.fish ~/.config/fish/
