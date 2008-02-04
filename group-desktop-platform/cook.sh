#!/bin/bash

time cvc cook --context fl:2-devel --build-label=foresight.rpath.org@fl:2-devel 'group-desktop-platform=@fl:2-devel[~!bootstrap,~!builddocs,~!dom0,~!domU,~!vmware,~!xen  is: x86 x86_64]' 'group-desktop-platform=@fl:2-devel[~!bootstrap,~!builddocs,~!dom0,~!domU,~!vmware,~!xen is: x86]'
