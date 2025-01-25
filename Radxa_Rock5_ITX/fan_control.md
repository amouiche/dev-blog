# Fan Control

## Observations

- Fans full speed during boot
- Not running once boot is done. if cpu is cold
- Automatically starts when increasing the CPU temperature with CPU load.



Control is done by the kernel:

- pwn-fan driver
- thermal control

=> configuration is done through DTS

A dump of runtime device tree with `dtc -I fs /sys/firmware/devicetree/base` shows: 

```
	pwm-fan {
		cooling-levels = <0x00 0x40 0x80 0xc0 0xff>;
		}
		
		
```

## Documentation

Various Doc about configuration

https://forum.radxa.com/t/guide-on-how-to-customize-you-pwm-fan-curve/17442

https://emlogic.no/2024/09/step-by-step-thermal-management/



Kernel doc: https://www.kernel.org/doc/html/v6.11/driver-api/thermal/sysfs-api.html

## Testing

Looking at /sys

- `/sys/class/thermal/cooling_device4` => our fan 
  `cat /sys/class/thermal/cooling_device4/cur_state` indique le 'cooling-level' courant
- `/sys/class/thermal/thermal_zone0` => thermal that is controlling our fan
  - We have 3 trip points : 50° 65° 115°

Current temperature can be read with:

```
cat /sys/class/thermal/thermal_zone0/temp
cat_temp() { cat /sys/class/thermal/thermal_zone0/temp; }
```

We can test the curve with

```
# emulate 60°C
echo 60000 > /sys/class/thermal/thermal_zone0/emul_temp

emul_temp() { echo $(($1*1000)) > /sys/class/thermal/thermal_zone0/emul_temp; }
```

(note: powering the device off if trying to write 115000)

- level 1 at 50°
- level 2 at 65°
- level 3 above ... ()

The way levels are selected is not very clear. looks like there is no direct matching of cooling-levels to trip points, but more a spread of cooling-levels over the trip points.



## First goal: Updating cooling levels

For example, if we want to also have the fan running at minimal speed, whater the temperature is, we can use a  DeviceTree overlay for that:

Creates a `pwm-fan-new-levels.dts` and apply with `armbian-add-overlay pwm-fan-new-levels.dts` 

```
/dts-v1/;
/plugin/;

/ {
    compatible = "radxa,rock-5-itx";

	fragment@1 {
		target-path = "/pwm-fan";
		__overlay__ {
			 cooling-levels = <0x20 0x40 0x80 0xc0 0xff>;
		 };
	 };
};

```

Here, the minimal cooling level is **0x20** instread of default 0
