#!/bin/bash
grub-mkimage -O x86_64-efi -o /efi/EFI/Garuda/grubx64.efi -p /EFI/Garuda -d /usr/lib/grub/x86_64-efi part_gpt fat ext2 btrfs normal boot linux echo all_video test search search_label search_fs_uuid gfxmenu gfxterm help loadenv ls reboot halt png jpeg
