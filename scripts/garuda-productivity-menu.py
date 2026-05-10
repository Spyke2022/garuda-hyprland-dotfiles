#!/usr/bin/env python3
"""
Garuda Sway Tools — Menu de Produtividade
===========================================
Menu interativo estilizado para ferramentas de produtividade.
Executa no terminal com interface ASCII/ANSI art.
"""

import os
import shutil
import subprocess
import sys

# ── Cores ANSI ──────────────────────────────────────────────
RESET   = "\033[0m"
BOLD    = "\033[1m"
DIM     = "\033[2m"
ITALIC  = "\033[3m"
UNDER   = "\033[4m"

RED     = "\033[38;5;203m"
GREEN   = "\033[38;5;114m"
YELLOW  = "\033[38;5;221m"
BLUE    = "\033[38;5;74m"
CYAN    = "\033[38;5;80m"
MAGENTA = "\033[38;5;176m"
ORANGE  = "\033[38;5;209m"
WHITE   = "\033[38;5;255m"
GRAY    = "\033[38;5;245m"

BG_DARK = "\033[48;5;235m"
BG_SEL  = "\033[48;5;238m"

# ── Definição do menu ───────────────────────────────────────
MENU = [
    {
        "category": "Escritorio",
        "icon": "\U0001f4dd",  # 📝
        "color": BLUE,
        "items": [
            ("OnlyOffice",   "onlyoffice-desktopeditors",
             "Suite de escritorio com boa compatibilidade MS Office"),
            ("LibreOffice",  "libreoffice",
             "Suite de escritorio completa e livre"),
        ],
    },
    {
        "category": "Notas e Organizacao",
        "icon": "\U0001f4d3",  # 📓
        "color": MAGENTA,
        "items": [
            ("Obsidian",   "obsidian",
             "Notas em Markdown e base de conhecimento pessoal"),
            ("Joplin",     "joplin-desktop",
             "Notas, cadernos e listas de tarefas com sincronizacao"),
            ("QOwnNotes",  "QOwnNotes",
             "Notas em Markdown com integracao Nextcloud"),
        ],
    },
    {
        "category": "E-mail e Agenda",
        "icon": "\U0001f4e7",  # 📧
        "color": CYAN,
        "items": [
            ("Thunderbird",  "thunderbird",
             "Cliente de e-mail, calendario, contatos e tarefas"),
            ("Evolution",    "evolution",
             "E-mail, calendario e contatos integrados ao GNOME"),
            ("KOrganizer",   "korganizer",
             "Calendario e agenda do KDE"),
        ],
    },
    {
        "category": "PDF e Leitura",
        "icon": "\U0001f4d6",  # 📖
        "color": GREEN,
        "items": [
            ("Okular",        "okular",
             "Leitor e anotador de PDF/documentos"),
            ("Zathura",       "zathura",
             "Visualizador de documentos leve e minimalista"),
            ("Calibre",       "calibre",
             "Gerenciador de e-books, PDFs e biblioteca digital"),
            ("Foliate",       "foliate",
             "Leitor de EPUB leve e agradavel"),
            ("PDF Arranger",  "pdfarranger",
             "Reorganizar, juntar, dividir e girar paginas de PDFs"),
            ("Xournal++",     "xournalpp",
             "Anotacoes manuscritas em PDFs"),
        ],
    },
    {
        "category": "Sincronizacao e Backup",
        "icon": "\U0001f504",  # 🔄
        "color": YELLOW,
        "items": [
            ("Nextcloud Client", "nextcloud",
             "Sincronizacao de arquivos com Nextcloud"),
            ("Syncthing",        "syncthing-gtk",
             "Sincronizacao direta entre dispositivos"),
            ("Timeshift",        "timeshift-launcher",
             "Snapshots/backup do sistema"),
            ("Pika Backup",      "pika-backup",
             "Backup grafico simples para arquivos pessoais"),
        ],
    },
    {
        "category": "Captura e Clipboard",
        "icon": "\U0001f4f7",  # 📷
        "color": ORANGE,
        "items": [
            ("Flameshot", "flameshot",
             "Capturas de tela com anotacao"),
            ("CopyQ",     "copyq",
             "Gerenciador de area de transferencia"),
        ],
    },
    {
        "category": "Seguranca Pessoal",
        "icon": "\U0001f512",  # 🔒
        "color": RED,
        "items": [
            ("KeePassXC", "keepassxc",
             "Gerenciador de senhas local"),
        ],
    },
    {
        "category": "Graficos e Documentos",
        "icon": "\U0001f3a8",  # 🎨
        "color": MAGENTA,
        "items": [
            ("GIMP",          "gimp",
             "Edicao de imagens avancada"),
            ("Inkscape",      "inkscape",
             "Desenhos vetoriais, diagramas e logos"),
            ("Krita",         "krita",
             "Desenho, ilustracao e edicao criativa"),
            ("Simple Scan",   "simple-scan",
             "Digitalizacao de documentos"),
            ("OCRmyPDF",      "ocrmypdf",
             "Transforma PDFs escaneados em pesquisaveis"),
            ("Tesseract OCR", "tesseract",
             "Reconhecimento de texto em imagens"),
        ],
    },
    {
        "category": "Acesso Remoto e Transferencia",
        "icon": "\U0001f5a5\ufe0f",  # 🖥️
        "color": BLUE,
        "items": [
            ("Remmina",   "remmina",
             "Acesso remoto por RDP/VNC/SSH"),
            ("FileZilla", "filezilla",
             "Cliente FTP/SFTP grafico"),
        ],
    },
    {
        "category": "Editor de Texto",
        "icon": "\u270f\ufe0f",  # ✏️
        "color": GRAY,
        "items": [
            ("Kate", "kate",
             "Editor avancado para anotacoes, scripts e configs"),
        ],
    },
    {
        "category": "Tarefas",
        "icon": "\u2705",  # ✅
        "color": GREEN,
        "items": [
            ("Planner / Errands", "errands",
             "Gerenciador de tarefas simples"),
        ],
    },
]


def term_width():
    return shutil.get_terminal_size((80, 24)).columns


def clear():
    os.system("clear")


def draw_header():
    w = term_width()
    line = "═" * (w - 2)
    print(f"{BLUE}{BOLD}╔{line}╗{RESET}")
    title = "PRODUTIVIDADE"
    subtitle = "Garuda Sway Tools"
    pad_t = (w - 2 - len(title)) // 2
    pad_s = (w - 2 - len(subtitle)) // 2
    print(f"{BLUE}{BOLD}║{' ' * pad_t}{WHITE}{BOLD}{title}{' ' * (w - 2 - pad_t - len(title))}{BLUE}║{RESET}")
    print(f"{BLUE}{BOLD}║{' ' * pad_s}{GRAY}{ITALIC}{subtitle}{' ' * (w - 2 - pad_s - len(subtitle))}{BLUE}║{RESET}")
    print(f"{BLUE}{BOLD}╚{line}╝{RESET}")
    print()


def draw_tree():
    """Desenha o menu em formato de arvore com numeros."""
    num = 1
    item_map = {}
    total_cats = len(MENU)

    for ci, cat in enumerate(MENU):
        is_last_cat = ci == total_cats - 1
        branch = "└── " if is_last_cat else "├── "
        cont   = "    " if is_last_cat else "│   "

        print(f"  {GRAY}{branch}{cat['color']}{BOLD}{cat['icon']}  {cat['category']}{RESET}")

        items = cat["items"]
        for ii, (name, cmd, desc) in enumerate(items):
            is_last_item = ii == len(items) - 1
            item_branch = "└── " if is_last_item else "├── "

            num_str = f"{YELLOW}{BOLD}[{num:2d}]{RESET}"
            print(f"  {GRAY}{cont}{item_branch}{num_str} {WHITE}{name}{RESET}")
            print(f"  {GRAY}{cont}{'    ' if is_last_item else '│   '}{DIM}{desc}{RESET}")

            item_map[num] = (name, cmd)
            num += 1

        if not is_last_cat:
            print(f"  {GRAY}│{RESET}")

    return item_map


def draw_footer():
    print()
    print(f"  {GRAY}{'─' * (term_width() - 4)}{RESET}")
    print(f"  {BLUE}Digite o numero do aplicativo para executar{RESET}")
    print(f"  {GRAY}[{WHITE}q{GRAY}] Sair  {GRAY}[{WHITE}r{GRAY}] Recarregar  {GRAY}[{WHITE}i{GRAY}] Instalar ferramenta{RESET}")
    print()


def check_installed(cmd):
    """Verifica se o comando esta instalado."""
    return shutil.which(cmd) is not None


def install_tool(name, cmd):
    """Tenta instalar uma ferramenta via pacman/yay."""
    print(f"\n  {YELLOW}Tentando instalar {WHITE}{name}{YELLOW}...{RESET}")
    pkg_map = {
        "onlyoffice-desktopeditors": "onlyoffice-bin",
        "libreoffice": "libreoffice-fresh",
        "obsidian": "obsidian",
        "joplin-desktop": "joplin-desktop",
        "QOwnNotes": "qownnotes",
        "thunderbird": "thunderbird",
        "evolution": "evolution",
        "korganizer": "korganizer",
        "okular": "okular",
        "zathura": "zathura zathura-pdf-mupdf",
        "calibre": "calibre",
        "foliate": "foliate",
        "pdfarranger": "pdfarranger",
        "xournalpp": "xournalpp",
        "nextcloud": "nextcloud-client",
        "syncthing-gtk": "syncthing syncthing-gtk",
        "timeshift-launcher": "timeshift",
        "pika-backup": "pika-backup",
        "flameshot": "flameshot",
        "copyq": "copyq",
        "keepassxc": "keepassxc",
        "gimp": "gimp",
        "inkscape": "inkscape",
        "krita": "krita",
        "simple-scan": "simple-scan",
        "ocrmypdf": "ocrmypdf",
        "tesseract": "tesseract tesseract-data-por",
        "remmina": "remmina",
        "filezilla": "filezilla",
        "kate": "kate",
        "errands": "errands",
    }
    pkg = pkg_map.get(cmd, cmd)

    for mgr in ["sudo pacman -S --noconfirm", "yay -S --noconfirm"]:
        print(f"  {GRAY}> {mgr} {pkg}{RESET}")
        ret = os.system(f"{mgr} {pkg} 2>/dev/null")
        if ret == 0:
            print(f"  {GREEN}{name} instalado com sucesso!{RESET}")
            return True

    print(f"  {RED}Nao foi possivel instalar {name} automaticamente.{RESET}")
    print(f"  {GRAY}Tente: yay -S {pkg}{RESET}")
    return False


def launch(name, cmd):
    """Executa o aplicativo."""
    if not check_installed(cmd):
        print(f"\n  {RED}{name} nao esta instalado.{RESET}")
        resp = input(f"  {YELLOW}Deseja instalar? [s/N]: {RESET}").strip().lower()
        if resp in ("s", "sim", "y", "yes"):
            if not install_tool(name, cmd):
                input(f"  {GRAY}Pressione Enter para continuar...{RESET}")
                return
        else:
            input(f"  {GRAY}Pressione Enter para continuar...{RESET}")
            return

    # CLI tools (ocrmypdf, tesseract) ficam no terminal
    cli_tools = {"ocrmypdf", "tesseract"}
    if cmd in cli_tools:
        print(f"\n  {GREEN}Executando {name}...{RESET}")
        print(f"  {GRAY}(Ctrl+C para retornar ao menu){RESET}\n")
        try:
            subprocess.run([cmd, "--help"])
        except KeyboardInterrupt:
            pass
        input(f"\n  {GRAY}Pressione Enter para retornar ao menu...{RESET}")
    else:
        print(f"\n  {GREEN}Iniciando {name}...{RESET}")
        subprocess.Popen([cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        input(f"  {GRAY}Pressione Enter para continuar...{RESET}")


def main():
    while True:
        clear()
        draw_header()
        item_map = draw_tree()
        draw_footer()

        try:
            choice = input(f"  {BLUE}{BOLD}>>> {RESET}").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if choice in ("q", "quit", "sair", "exit"):
            break
        elif choice == "r":
            continue
        elif choice == "i":
            print(f"\n  {YELLOW}Digite o numero da ferramenta para instalar:{RESET}")
            try:
                num = int(input(f"  {BLUE}>>> {RESET}").strip())
            except (ValueError, EOFError, KeyboardInterrupt):
                continue
            if num in item_map:
                name, cmd = item_map[num]
                install_tool(name, cmd)
                input(f"  {GRAY}Pressione Enter para continuar...{RESET}")
            continue

        try:
            num = int(choice)
        except ValueError:
            continue

        if num in item_map:
            name, cmd = item_map[num]
            launch(name, cmd)

    clear()
    print(f"{GRAY}Garuda Sway Tools — Produtividade encerrado.{RESET}")


if __name__ == "__main__":
    main()
