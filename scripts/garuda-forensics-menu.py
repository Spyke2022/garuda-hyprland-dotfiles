#!/usr/bin/env python3
"""
Garuda Sway Tools — Menu Forense Digital
==========================================
Menu interativo estilizado para ferramentas de análise forense.
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
        "category": "Analise de Disco",
        "icon": "\U0001f4bf",  # 💿
        "color": CYAN,
        "items": [
            ("Autopsy",     "autopsy",
             "Interface grafica para analise forense de discos e artefatos"),
            ("Sleuth Kit",  "tsk_recover",
             "Ferramentas CLI para analise de sistemas de arquivos"),
            ("TestDisk",    "testdisk",
             "Recuperacao de particoes e arquivos apagados"),
            ("PhotoRec",    "photorec",
             "Recuperacao por assinatura de arquivos"),
        ],
    },
    {
        "category": "Memoria",
        "icon": "\U0001f9e0",  # 🧠
        "color": MAGENTA,
        "items": [
            ("Volatility 3", "vol3",
             "Analise de memoria RAM e dumps de memoria"),
        ],
    },
    {
        "category": "Rede",
        "icon": "\U0001f310",  # 🌐
        "color": BLUE,
        "items": [
            ("Wireshark", "wireshark",
             "Analise grafica de trafego de rede e pacotes"),
        ],
    },
    {
        "category": "Malware e Binarios",
        "icon": "\U0001f41b",  # 🐛
        "color": RED,
        "items": [
            ("YARA",    "yara",
             "Regras para identificar padroes em arquivos e malware"),
            ("Binwalk", "binwalk",
             "Analise de firmware e extracao de arquivos embutidos"),
            ("GHex",    "ghex",
             "Editor hexadecimal grafico"),
            ("Bless",   "bless",
             "Editor hexadecimal grafico para analise binaria"),
        ],
    },
    {
        "category": "Recuperacao",
        "icon": "\U0001f504",  # 🔄
        "color": GREEN,
        "items": [
            ("Foremost", "foremost",
             "Recuperacao de arquivos por assinatura / carving"),
            ("Scalpel",  "scalpel",
             "File carving seletivo de imagens e discos"),
        ],
    },
    {
        "category": "Aquisicao de Evidencias",
        "icon": "\U0001f50d",  # 🔍
        "color": YELLOW,
        "items": [
            ("dc3dd",     "dc3dd",
             "Criacao de imagens forenses com recursos extras"),
            ("dcfldd",    "dcfldd",
             "Aquisicao forense com hashing durante a copia"),
            ("Guymager",  "guymager",
             "Criacao de imagens forenses com interface grafica"),
        ],
    },
    {
        "category": "Metadados e Hashes",
        "icon": "\U0001f3f7\ufe0f",  # 🏷️
        "color": ORANGE,
        "items": [
            ("ExifTool",  "exiftool",
             "Leitura/edicao de metadados de imagens e documentos"),
            ("Hashdeep",  "hashdeep",
             "Calculo e verificacao de hashes em massa"),
        ],
    },
    {
        "category": "Linha do Tempo",
        "icon": "\u23f0",  # ⏰
        "color": CYAN,
        "items": [
            ("Plaso / log2timeline", os.path.expanduser("~/.local/share/garuda-sway-tools/log2timeline"),
             "Criacao de linhas do tempo a partir de logs e artefatos"),
            ("Timesketch", os.path.expanduser("~/.local/share/garuda-sway-tools/timesketch-launch"),
             "Analise visual de linhas do tempo forenses"),
        ],
    },
    {
        "category": "Extracao em Massa",
        "icon": "\U0001f4e6",  # 📦
        "color": MAGENTA,
        "items": [
            ("Bulk Extractor", os.path.expanduser("~/.local/share/garuda-sway-tools/bulk-extractor-launch"),
             "Extracao de e-mails, URLs, metadados de grandes volumes"),
        ],
    },
    {
        "category": "Formato de Imagem Forense",
        "icon": "\U0001f4be",  # 💾
        "color": GRAY,
        "items": [
            ("AFFLIB Tools", os.path.expanduser("~/.local/share/garuda-sway-tools/afflib-launch"),
             "Ferramentas para formato AFF de imagens forenses"),
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
    print(f"{RED}{BOLD}╔{line}╗{RESET}")
    title = "FORENSE DIGITAL"
    subtitle = "Garuda Sway Tools"
    pad_t = (w - 2 - len(title)) // 2
    pad_s = (w - 2 - len(subtitle)) // 2
    print(f"{RED}{BOLD}║{' ' * pad_t}{WHITE}{BOLD}{title}{' ' * (w - 2 - pad_t - len(title))}{RED}║{RESET}")
    print(f"{RED}{BOLD}║{' ' * pad_s}{GRAY}{ITALIC}{subtitle}{' ' * (w - 2 - pad_s - len(subtitle))}{RED}║{RESET}")
    print(f"{RED}{BOLD}╚{line}╝{RESET}")
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
    print(f"  {CYAN}Digite o numero do aplicativo para executar{RESET}")
    print(f"  {GRAY}[{WHITE}q{GRAY}] Sair  {GRAY}[{WHITE}r{GRAY}] Recarregar  {GRAY}[{WHITE}i{GRAY}] Instalar ferramenta{RESET}")
    print()


def check_installed(cmd):
    """Verifica se o comando esta instalado."""
    return shutil.which(cmd) is not None


def install_tool(name, cmd):
    """Tenta instalar uma ferramenta via pacman/yay."""
    print(f"\n  {YELLOW}Tentando instalar {WHITE}{name}{YELLOW}...{RESET}")
    pkg_map = {
        "autopsy": "autopsy",
        "tsk_recover": "sleuthkit",
        "testdisk": "testdisk",
        "photorec": "testdisk",
        "vol3": "volatility3",
        "wireshark": "wireshark-qt",
        "yara": "yara",
        "binwalk": "binwalk",
        "ghex": "ghex",
        "bless": "bless",
        "foremost": "foremost",
        "scalpel": "scalpel",
        "dc3dd": "dc3dd",
        "dcfldd": "dcfldd",
        "guymager": "guymager",
        "exiftool": "perl-image-exiftool",
        "hashdeep": "hashdeep",
        "log2timeline": "plaso",
        "timesketch": "timesketch",
        "bulk_extractor": "bulk-extractor",
        "affinfo": "afflib",
    }
    pkg = pkg_map.get(cmd, cmd)

    # Tenta pacman primeiro, depois yay (AUR)
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

    # Aplicativos gráficos rodam em background
    gui_apps = {"autopsy", "wireshark", "ghex", "bless", "guymager", "timesketch"}
    if cmd in gui_apps:
        print(f"\n  {GREEN}Iniciando {name}...{RESET}")
        subprocess.Popen([cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        input(f"  {GRAY}Pressione Enter para continuar...{RESET}")
    else:
        # Aplicativos CLI rodam no terminal atual
        print(f"\n  {GREEN}Executando {name}...{RESET}")
        print(f"  {GRAY}(Ctrl+C para retornar ao menu){RESET}\n")
        try:
            subprocess.run([cmd])
        except KeyboardInterrupt:
            pass
        input(f"\n  {GRAY}Pressione Enter para retornar ao menu...{RESET}")


def main():
    while True:
        clear()
        draw_header()
        item_map = draw_tree()
        draw_footer()

        try:
            choice = input(f"  {CYAN}{BOLD}>>> {RESET}").strip().lower()
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
                num = int(input(f"  {CYAN}>>> {RESET}").strip())
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
    print(f"{GRAY}Garuda Sway Tools — Forense Digital encerrado.{RESET}")


if __name__ == "__main__":
    main()
