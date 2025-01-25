#!/usr/bin/env python3

import os


other_paths = """
/es8316-sound 
/rkvenc-ccu 
/rga@fdb70000 
/dmc

/jpege-core@fdbac000
/rkvdec-core@fdc48000
/vdpu@fdb50400
/jpege-core@fdba0000
/vop@fdd90000
/rga@fdb80000

/iep@fdbb0000
/dfi@fe060000 
/mpp-srv 
/jpege-core@fdba8000
/spdif-tx1-sound 
/spdif-tx@fddb0000
/jpegd@fdb90000
/rkvenc-core@fdbd0000
/jpege-ccu
/av1d@fdc70000 
/rkvdec-ccu@fdc30000
/rga@fdb60000
/vepu@fdb50000
/spdif-tx@fe4f0000 
/rkvenc-core@fdbe0000
/jpege-core@fdba4000
/rkvdec-core@fdc38000
"""




paths = """
/npu@fdab0000
/gpu@fb000000
/hdmirx-controller@fdee0000
/hdmiin-sound
/hdmiphy@fed60000
/hdmi@fdea0000
/hdmiphy@fed70000
/hdmi1-sound
/dp@fde50000
/dp1-sound
/dp0-sound

/dp@fde60000

""".split()

localdir = os.path.dirname(__file__)
with open( localdir+"/display-disable.dts", "w") as F:
    F.write("""
/dts-v1/;
/plugin/;

/ {
    compatible = "radxa,rock-5-itx";
""")

    
    for num, path in enumerate(paths, start=1):
        if path.startswith("#"):
            continue
        F.write("""
	fragment@%d {
		target-path = "%s";
		__overlay__ {
			 status = "disabled";
		 };
	 };
""" % (num, path))
    
    
    F.write("};\n")
