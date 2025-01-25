# Powering the board on

### Outside of any case, simply plug 12V Jack and expect to have some signal on UART console to know which kind of voltage the UART is using.

Unfortunately, Rx and TX stay at 0V whereas the idle state of an UART is high.

Pluggin a HDMI... nothing on HDMI either.

The reason may be simple, like no bootloader in SPI or eMMC. In this case, we can guess the RK3588 as a recovery boot mode where the usb-C connector can be used to bootstrap the device.

Indeed, plugging a usb-c to the PC show:

```
Nov 21 21:01:07 amolinux kernel: usb 1-1.4.1: new high-speed USB device number 51 using xhci_hcd
Nov 21 21:01:07 amolinux kernel: usb 1-1.4.1: New USB device found, idVendor=2207, idProduct=350b, bcdDevice= 1.00
Nov 21 21:01:07 amolinux kernel: usb 1-1.4.1: New USB device strings: Mfr=0, Product=0, SerialNumber=0

$ lsusb 
[...]
Bus 001 Device 051: ID 2207:350b Fuzhou Rockchip Electronics Company 

```

At least, the CPU is not broken 😅

## Trying to boot on a microSD card.

This is the easiest way to test the hardware since the rk3588 should boot directly on microSD card without any  other requirement.

Let's download some images !
from https://docs.radxa.com/en/rock5/rock5itx/download

- [rock-5-itx_debian_bullseye_kde_b6.img.xz](https://github.com/radxa-build/rock-5-itx/releases/download/b6/rock-5-itx_debian_bullseye_kde_b6.img.xz)

from https://www.armbian.com/radxa-rock-5-itx/

- Armbian_24.8.3_Rock-5-itx_bookworm_vendor_6.1.75_xfce_desktop.img.xz
- Armbian_24.8.3_Rock-5-itx_bookworm_vendor_6.1.75_minimal.img.xz

# Trying rock-5-itx_debian_bullseye_kde_b6

Image flashed with `gnome-disks --restore-disk-image rock-5-itx_debian_bullseye_kde_b6.img.xz`

It boots **fine** with HDMI screen enabled ! 🎉

And we also have the UART enabled, and we can measure the IO voltage : 3.3V 

#### Building a UART <=> USB Adapter

​	

Boot trace for `rock-5-itx_debian_bullseye_kde_b6` image. Uart console @ 1500000 bauds

```
DDR 9fffbe1e78 cym 24/02/04-10:09:20,fwver: v1.16
LPDDR5, 2400MHz
channel[0] BW=16 Col=10 Bk=16 CS0 Row=16 CS=1 Die BW=16 Size=2048MB
channel[1] BW=16 Col=10 Bk=16 CS0 Row=16 CS=1 Die BW=16 Size=2048MB
channel[2] BW=16 Col=10 Bk=16 CS0 Row=16 CS=1 Die BW=16 Size=2048MB
channel[3] BW=16 Col=10 Bk=16 CS0 Row=16 CS=1 Die BW=16 Size=2048MB
Manufacturer ID:0x6
CH0 RX Vref:31.4%, TX Vref:19.0%,0.0%
CH1 RX Vref:31.0%, TX Vref:22.0%,0.0%
CH2 RX Vref:31.8%, TX Vref:21.0%,0.0%
CH3 RX Vref:31.4%, TX Vref:20.0%,0.0%
change to F1: 534MHz
change to F2: 1320MHz
change to F3: 1968MHz
change to F0: 2400MHz
out
U-Boot SPL board init
U-Boot SPL rknext-2017.09-29-be2c5d5-ge5342b0 #runner (Jun 06 2024 - 03:20:16)
Trying to boot from MMC2
spl: partition error
Trying fit image at 0x4000 sector
## Verified-boot: 0
## Checking atf-1 0x00040000 ... sha256(a7d1d8d191...) + OK
## Checking uboot 0x00200000 ... sha256(e1e6316bce...) + OK
## Checking fdt 0x00328838 ... sha256(6538d5e789...) + OK
## Checking atf-2 0xff100000 ... sha256(4b2065349b...) + OK
## Checking atf-3 0x000f0000 ... sha256(aa71013e72...) + OK
Jumping to U-Boot(0x00200000) via ARM Trusted Firmware(0x00040000)
Total: 615.359/881.549 ms

INFO:    Preloader serial: 2
NOTICE:  BL31: v2.3():v2.3-682-g4ca8a8422:derrick.huang, fwver: v1.45
NOTICE:  BL31: Built : 10:11:21, Dec 27 2023
INFO:    spec: 0x1
INFO:    code: 0x88
INFO:    ext 32k is not valid
INFO:    ddr: stride-en 4CH
INFO:    GICv3 without legacy support detected.
INFO:    ARM GICv3 driver initialized in EL3
INFO:    valid_cpu_msk=0xff bcore0_rst = 0x0, bcore1_rst = 0x0
INFO:    l3 cache partition cfg-0
INFO:    system boots from cpu-hwid-0
INFO:    disable memory repair
INFO:    idle_st=0x21fff, pd_st=0x11fff9, repair_st=0xfff70001
INFO:    dfs DDR fsp_params[0].freq_mhz= 2400MHz
INFO:    dfs DDR fsp_params[1].freq_mhz= 534MHz
INFO:    dfs DDR fsp_params[2].freq_mhz= 1320MHz
INFO:    dfs DDR fsp_params[3].freq_mhz= 1968MHz
INFO:    BL31: Initialising Exception Handling Framework
INFO:    BL31: Initializing runtime services
WARNING: No OPTEE provided by BL2 boot loader, Booting device without OPTEE initialization. SMC`s destined for OPTEE will return SMC_UNK
ERROR:   Error initializing runtime service opteed_fast
INFO:    BL31: Preparing for EL3 exit to normal world
INFO:    Entry point address = 0x200000
INFO:    SPSR = 0x3c9


U-Boot rknext-2017.09-29-be2c5d5-ge5342b0 #runner (Jun 06 2024 - 03:20:14 +0000)

Model: Radxa ROCK 5 ITX
MPIDR: 0x81000000
PreSerial: 2, raw, 0xfeb50000
DRAM:  8 GiB
Sysmem: init
Relocation Offset: eda35000
Relocation fdt: eb9f8500 - eb9fecc8
CR: M/C/I
Using default environment

DM: v2
mmc@fe2c0000: 1, mmc@fe2e0000: 0
Bootdev(assign): mmc 0
MMC0: HS400 Enhanced Strobe, 200Mhz
## Unknown partition table type 0
PartType: <NULL>
No misc partition
boot mode: None
FIT: No boot partition
Failed to load DTB, ret=-2
No valid DTB, ret=-22
Failed to get kernel dtb, ret=-22
Model: Radxa ROCK 5 ITX
MPIDR: 0x81000000
starting USB...
Bus usb@fc800000: USB EHCI 1.00
Bus usb@fc840000: USB OHCI 1.0
Bus usb@fc880000: USB EHCI 1.00
Bus usb@fc8c0000: USB OHCI 1.0
scanning bus usb@fc800000 for devices... 2 USB Device(s) found
scanning bus usb@fc840000 for devices... 1 USB Device(s) found
scanning bus usb@fc880000 for devices... 1 USB Device(s) found
scanning bus usb@fc8c0000 for devices... 1 USB Device(s) found
       scanning usb for storage devices... 0 Storage Device(s) found
No usb mass storage found
CLK: (sync kernel. arm: enter 1008000 KHz, init 1008000 KHz, kernel 0N/A)
  b0pll 24000 KHz
  b1pll 24000 KHz
  lpll 24000 KHz
  v0pll 24000 KHz
  aupll 24000 KHz
  cpll 1500000 KHz
  gpll 1188000 KHz
  npll 24000 KHz
  ppll 1100000 KHz
  aclk_center_root 702000 KHz
  pclk_center_root 100000 KHz
  hclk_center_root 396000 KHz
  aclk_center_low_root 500000 KHz
  aclk_top_root 750000 KHz
  pclk_top_root 100000 KHz
  aclk_low_top_root 396000 KHz
Net:   No ethernet found.
Hit Ctrl+C key in 0 seconds to stop autoboot...

Device 0: unknown device
switch to partitions #0, OK
mmc1 is current device
Scanning mmc 1:2...
Scanning mmc 1:3...
Found /boot/extlinux/extlinux.conf
Retrieving file: /boot/extlinux/extlinux.conf
1201 bytes read in 10 ms (117.2 KiB/s)
U-Boot menu
1:	Debian GNU/Linux 11 (bullseye) 5.10.110-37-rockchip
2:	Debian GNU/Linux 11 (bullseye) 5.10.110-37-rockchip (rescue target)
Enter choice: 1:	Debian GNU/Linux 11 (bullseye) 5.10.110-37-rockchip
Retrieving file: /boot/initrd.img-5.10.110-37-rockchip
14531775 bytes read in 1182 ms (11.7 MiB/s)
Retrieving file: /boot/vmlinuz-5.10.110-37-rockchip
28312064 bytes read in 2291 ms (11.8 MiB/s)
append: root=UUID=9e383de3-7e73-4dcb-9e46-a69852973fc3 console=ttyFIQ0,1500000n8 quiet splash loglevel=4 rw earlycon consoleblank=0 console=tty1 coherent_pool=2M irqchip.gicv3_pseudo_nmi=0 cgroup_enable=cpuset cgroup_memory=1 cgroup_enable=memory swapaccount=1
Retrieving file: /usr/lib/linux-image-5.10.110-37-rockchip/rockchip/rk3588-rock-5-itx.dtb
253292 bytes read in 178 ms (1.4 MiB/s)
Fdt Ramdisk skip relocation
No misc partition
## Flattened Device Tree blob at 0x08300000
   Booting using the fdt blob at 0x08300000
   Using Device Tree in place at 0000000008300000, end 0000000008340d6b
WARNING: could not set reg FDT_ERR_BADOFFSET.
## reserved-memory:
  cma: addr=10000000 size=10000000
  ramoops@110000: addr=110000 size=f0000
Adding bank: 0x00200000 - 0xf0000000 (size: 0xefe00000)
Adding bank: 0x100000000 - 0x200000000 (size: 0x100000000)
Adding bank: 0x2f0000000 - 0x300000000 (size: 0x10000000)
Total: 9754.349/10694.701 ms

Starting kernel ...

[   11.343456] fiq_debugger fiq_debugger.0: IRQ fiq not found
[   11.343470] fiq_debugger fiq_debugger.0: IRQ wakeup not found
[   11.343478] fiq_debugger_probe: could not install nmi irq handler
[   12.133238] rk-pcie fe180000.pcie: IRQ msi not found
[   12.133282] rk-pcie fe180000.pcie: Missing *config* reg space
[...]
```

#### Console

- ubout can be halted with `ctrl+C`. You have access to the standard uboot "shell" without password

- linux login can be done with user `radxa` (pwd `radxa`). Has sudo powers.

- SSH server is not started by default. You must configure systemd 

  ```
  sudo systemctl enable ssh
  sudo systemctl start ssh.service
  ```

  





SPI is empty

```
radxa@rock-5-itx:~$ sudo hexdump /dev/mtd0
0000000 0000 0000 0000 0000 0000 0000 0000 0000
*
0100000 ffff ffff ffff ffff ffff ffff ffff ffff
*
1000000
```

SATA/NVME/MMC bus performances

- single 3.5 HDD (Seagate Ironwold)  

  ```
  root@rock-5-itx:~# hdparm -t /dev/sda
  /dev/sda:
   Timing buffered disk reads: 548 MB in  3.01 seconds = 182.32 MB/sec
  ```

- NVME : (Samsun SSD980)

  ```
  root@rock-5-itx:~# hdparm -t /dev/nvme0n1
  /dev/nvme0n1:
   Timing buffered disk reads: 3288 MB in  3.00 seconds = 1095.96 MB/sec
  ```

- Internal eMMC

  ```
  root@rock-5-itx:~# hdparm -t /dev/mmcblk0
  /dev/mmcblk0:
   Timing buffered disk reads: 908 MB in  3.00 seconds = 302.49 MB/sec
  ```

  

Power consumption @12V

Boot done, no HDMI screen plugged : 0.46A => 5.5W

# Trying Armbian_24.8.3_Rock-5-itx_bookworm_vendor_6.1.75_minimal

Write the image on microSD card with gnome-disks.

## Booting:

```
DDR 9fffbe1e78 cym 24/02/04-10:09:20,fwver: v1.16
LPDDR5, 2400MHz
channel[0] BW=16 Col=10 Bk=16 CS0 Row=16 CS=1 Die BW=16 Size=2048MB
channel[1] BW=16 Col=10 Bk=16 CS0 Row=16 CS=1 Die BW=16 Size=2048MB
channel[2] BW=16 Col=10 Bk=16 CS0 Row=16 CS=1 Die BW=16 Size=2048MB
channel[3] BW=16 Col=10 Bk=16 CS0 Row=16 CS=1 Die BW=16 Size=2048MB
Manufacturer ID:0x6
CH0 RX Vref:31.4%, TX Vref:20.0%,0.0%
CH1 RX Vref:31.0%, TX Vref:21.0%,0.0%
CH2 RX Vref:31.8%, TX Vref:21.0%,0.0%
CH3 RX Vref:31.0%, TX Vref:19.0%,0.0%
change to F1: 534MHz
change to F2: 1320MHz
change to F3: 1968MHz
change to F0: 2400MHz
out
U-Boot SPL board init
U-Boot SPL 2017.09-armbian-2017.09-S0674-Pc965-H8c72-Ve5ad-Bda0a-R448a (Sep 11 2024 - 17:20:06)
Trying to boot from MMC2
spl: partition error
Trying fit image at 0x4000 sector
## Verified-boot: 0
## Checking atf-1 0x00040000 ... sha256(a7d1d8d191...) + OK
## Checking uboot 0x00200000 ... sha256(36f9c4aad0...) + OK
## Checking fdt 0x00323440 ... sha256(959e3fb40d...) + OK
## Checking atf-2 0xff100000 ... sha256(4b2065349b...) + OK
## Checking atf-3 0x000f0000 ... sha256(aa71013e72...) + OK
Jumping to U-Boot(0x00200000) via ARM Trusted Firmware(0x00040000)
Total: 601.189/865.347 ms

INFO:    Preloader serial: 2
NOTICE:  BL31: v2.3():v2.3-682-g4ca8a8422:derrick.huang, fwver: v1.45
NOTICE:  BL31: Built : 10:11:21, Dec 27 2023
INFO:    spec: 0x1
INFO:    code: 0x88
INFO:    ext 32k is not valid
INFO:    ddr: stride-en 4CH
INFO:    GICv3 without legacy support detected.
INFO:    ARM GICv3 driver initialized in EL3
INFO:    valid_cpu_msk=0xff bcore0_rst = 0x0, bcore1_rst = 0x0
INFO:    l3 cache partition cfg-0
INFO:    system boots from cpu-hwid-0
INFO:    disable memory repair
INFO:    idle_st=0x21fff, pd_st=0x11fff9, repair_st=0xfff70001
INFO:    dfs DDR fsp_params[0].freq_mhz= 2400MHz
INFO:    dfs DDR fsp_params[1].freq_mhz= 534MHz
INFO:    dfs DDR fsp_params[2].freq_mhz= 1320MHz
INFO:    dfs DDR fsp_params[3].freq_mhz= 1968MHz
INFO:    BL31: Initialising Exception Handling Framework
INFO:    BL31: Initializing runtime services
WARNING: No OPTEE provided by BL2 boot loader, Booting device without OPTEE initialization. SMC`s destined for OPTEE will return SMC_UNK
ERROR:   Error initializing runtime service opteed_fast
INFO:    BL31: Preparing for EL3 exit to normal world
INFO:    Entry point address = 0x200000
INFO:    SPSR = 0x3c9


U-Boot 2017.09-armbian-2017.09-S0674-Pc965-H8c72-Ve5ad-Bda0a-R448a (Sep 11 2024 - 17:20:06 +0000)

Model: Radxa ROCK 5 ITX
MPIDR: 0x81000000
PreSerial: 2, raw, 0xfeb50000
DRAM:  8 GiB
Sysmem: init
Relocation Offset: eda3a000
Relocation fdt: eb9f9120 - eb9fece0
CR: M/C/I
Using default environment

DM: v2
mmc@fe2c0000: 1, mmc@fe2e0000: 0
Bootdev(assign): mmc 0
MMC0: HS400 Enhanced Strobe, 200Mhz
## Unknown partition table type 0
PartType: <NULL>
No misc partition
boot mode: None
FIT: No boot partition
Failed to load DTB, ret=-2
No valid DTB, ret=-22
Failed to get kernel dtb, ret=-22
Model: Radxa ROCK 5 ITX
MPIDR: 0x81000000
starting USB...
Bus usb@fc800000: USB EHCI 1.00
Bus usb@fc840000: USB OHCI 1.0
Bus usb@fc880000: USB EHCI 1.00
Bus usb@fc8c0000: USB OHCI 1.0
scanning bus usb@fc800000 for devices... 2 USB Device(s) found
scanning bus usb@fc840000 for devices... 1 USB Device(s) found
scanning bus usb@fc880000 for devices... 1 USB Device(s) found
scanning bus usb@fc8c0000 for devices... 1 USB Device(s) found
       scanning usb for storage devices... 0 Storage Device(s) found
No usb mass storage found
CLK: (sync kernel. arm: enter 1008000 KHz, init 1008000 KHz, kernel 0N/A)
  b0pll 24000 KHz
  b1pll 24000 KHz
  lpll 24000 KHz
  v0pll 24000 KHz
  aupll 24000 KHz
  cpll 1500000 KHz
  gpll 1188000 KHz
  npll 24000 KHz
  ppll 1100000 KHz
  aclk_center_root 702000 KHz
  pclk_center_root 100000 KHz
  hclk_center_root 396000 KHz
  aclk_center_low_root 500000 KHz
  aclk_top_root 750000 KHz
  pclk_top_root 100000 KHz
  aclk_low_top_root 396000 KHz
Net:   No ethernet found.
Hit key to stop autoboot('CTRL+C'):  0 

Device 0: unknown device
switch to partitions #0, OK
mmc1 is current device
Scanning mmc 1:1...
Found U-Boot script /boot/boot.scr
4231 bytes read in 12 ms (343.8 KiB/s)
## Executing script at 00500000
Boot script loaded from mmc 1
Testing for existence mmc 1 /boot/armbianEnv.txt ...
Found mmc 1 /boot/armbianEnv.txt - loading mmc 1 0x9000000 /boot/armbianEnv.txt ...
225 bytes read in 12 ms (17.6 KiB/s)
Loaded environment from mmc 1 /boot/armbianEnv.txt into 0x9000000 filesize 0xe1...
Importing into environment ...
armbianEnv.txt imported into environment
8949754 bytes read in 734 ms (11.6 MiB/s)
39287296 bytes read in 3175 ms (11.8 MiB/s)
273728 bytes read in 83 ms (3.1 MiB/s)
Trying kaslrseed command... Info: Unknown command can be safely ignored since kaslrseed does not apply to all boards.
Unknown command 'kaslrseed' - try 'help'
Fdt Ramdisk skip relocation
No misc partition
## Loading init Ramdisk from Legacy Image at 0a200000 ...
   Image Name:   uInitrd
   Image Type:   AArch64 Linux RAMDisk Image (gzip compressed)
   Data Size:    8949690 Bytes = 8.5 MiB
   Load Address: 00000000
   Entry Point:  00000000
   Verifying Checksum ... OK
## Flattened Device Tree blob at 0x08300000
   Booting using the fdt blob at 0x08300000
   reserving fdt memory region: addr=8300000 size=a9000
   Using Device Tree in place at 0000000008300000, end 00000000083abfff
WARNING: could not set reg FDT_ERR_BADOFFSET.
## reserved-memory:
  cma: addr=10000000 size=10000000
  ramoops@110000: addr=110000 size=e0000
Adding bank: 0x00200000 - 0xf0000000 (size: 0xefe00000)
Adding bank: 0x100000000 - 0x200000000 (size: 0x100000000)
Adding bank: 0x2f0000000 - 0x300000000 (size: 0x10000000)
Total: 9379.365/10302.613 ms

Starting kernel ...

```



The classical armbian "first boot" experience as usual: setup the root password, the first user, the localization...

SSH server is already running. Warning: root user ssh access is enabled with password control.

Avahi dameon is not installed. Installation + enabling with:

```
apt install avahi-daemon
```



## Test CPU fan control

Don't know if there is any automatic control somewhere but the fan doesn't turn.

At least, this command works.

```
echo 50 > /sys/devices/platform/pwm-fan/hwmon/hwmon9/pwm1
```



## Power consumption

Current measured at 12V PSU output.

Once booted, idle, Armbian_24.8.3_Rock-5-itx_bookworm_vendor_6.1.75_minimal consumes 0.40mA @ 12V



## Working on device tree

Dumping running device tree with

```
dtc -I fs /sys/firmware/devicetree/base
```

It is possible to create user overlays in order to enable or disable stuff.

For example, bluetooth kernel driver is loaded and tries to initialize a bcm4345c5 module even if none is connected. We simply need to to disable the serial device parent of the bluetooth node with a `bluetooth-disable.dts` overlay, build and applied with `armbian-add-overlay bluetooth-disable.dts`  

```
/dts-v1/;
/plugin/;

/ {
    compatible = "radxa,rock-5-itx";

	fragment@1 {
		target-path = "/serial@feb90000";
		__overlay__ {
			 status = "disabled";
		 };
	 };
};
```





```t
COMMON_CLK_DISABLED_UNUSED
```
