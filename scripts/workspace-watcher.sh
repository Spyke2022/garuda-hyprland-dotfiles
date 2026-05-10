#!/bin/bash
handle() {
    case $1 in
        workspace*)
            WS=$(echo "$1" | grep -oP "workspace>>\K.*")
            ~/.local/bin/workspace-theme.sh "$WS"
            ;;
    esac
}
socat - UNIX-CONNECT:$XDG_RUNTIME_DIR/hypr/$HYPRLAND_INSTANCE_SIGNATURE/.socket2.sock | while read -r line; do
    handle "$line"
done
