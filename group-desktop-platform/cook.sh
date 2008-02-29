#!/bin/sh

branch=$(grep -m 1 ^branch CONARY)
case $branch in
  */2-devel)
    BRANCH="foresight.rpath.org@fl:2-devel"
    CONTEXT="fl:2-devel"
    ;;
  */2-qa)
    BRANCH="foresight.rpath.org@fl:2-qa"
    CONTEXT="fl:2-qa"
    ;;
  */2)
    echo "DO NOT COOK ON STABLE LABEL!  SEE promote SCRIPT INSTEAD!"
    exit 1
    ;;
  *)
    echo "WHERE ARE YOU?"
    exit 1
    ;;
esac

exec time cvc cook --context $CONTEXT --build-label=$BRANCH 'group-desktop-platform=$BRANCH[~!bootstrap,~!builddocs,~!dom0,~!domU,~!vmware,~!xen  is: x86 x86_64]' 'group-desktop-platform=$BRANCH[~!bootstrap,~!builddocs,~!dom0,~!domU,~!vmware,~!xen is: x86]'
