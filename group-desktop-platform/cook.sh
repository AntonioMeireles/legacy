#!/bin/bash

cvc cook --build-label=foresight.rpath.org@fl:2-devel 'group-desktop-platform=@fl:2-devel[~!bootstrap,~builddocs,~buildtests,~!cross,desktop,~!dom0,~!domU,~!gcc.core,gcj,~group-dist.devel,~grub.static,~!kernel.core,~!kernel.debug,~kernel.debugdata,~!kernel.numa,~!kernel.pae,~kernel.smp,~!vmware,~!xen  is: x86 x86_64]' 'group-desktop-platform=@fl:2-devel[~!bootstrap,~!builddocs,~buildtests,desktop,~!dom0,~!domU,gcj,~group-dist.devel,~grub.static,~!kernel.debug,~!kernel.debugdata,~!kernel.numa,~kernel.smp,~!xen is: x86]'
