# fdisk分区硬盘并shell脚本自动化 #

最近工作需要用到对硬盘进行shell脚本自动化分区和mount的操作，google了一些资料，下面做个总结。

如果硬盘没有进行分区（逻辑分区或者扩展分区，关于两者概念，自行google），我们将无法将使用该硬盘来进行读写。我们要使用一块硬盘需要进行下面三步：

1. 将该硬盘进行分区；
2. 对分区进行格式化；
3. 将分区mount到系统某个目录，便可以访问。

本笔记会着重讲一下第一步中涉及的fdisk分区功能以及如何来使用shell进行自动化处理，过程也会涉及后面两步操作的简单说明。

## fdisk对硬盘进行分区 ##
fdisk是linux系统提供的硬盘分区工具。关于fdisk的详细说明可以自行google或者man fdisk。下面我们直接说明操作步骤。

先查看一下当前系统有哪些硬盘：
```
ubuntu@i-idh5qfpk:~$ ls /dev | grep sd
sda
sda1
sdb
sdc
sdd
sdd1
```

我们就选择/dev/sdc进行下手吧。通过fdisk -l查看一下该硬盘的分区表：
```
ubuntu@i-idh5qfpk:~$ sudo fdisk -l /dev/sdc

Disk /dev/sdc: 10.7 GB, 10737418240 bytes
64 heads, 32 sectors/track, 10240 cylinders, total 20971520 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0xacb1d488

   Device Boot      Start         End      Blocks   Id  System
```

通过上面的信息，我们可以看到该硬盘总共有10.7GB，但是分区表为空（命令最后面的输出信息即是分区表信息）。下面我们通过运行fdisk命令来对该硬盘进行交互式的分区操作。输入fdisk /dev/sdc命令之后，会提示你进行什么操作，如果不清楚的话，可以输入m然后回车查看操作说明。如下所示，
```
ubuntu@i-idh5qfpk:~$ sudo fdisk /dev/sdc

Command (m for help): m
Command action
   a   toggle a bootable flag
   b   edit bsd disklabel
   c   toggle the dos compatibility flag
   d   delete a partition
   l   list known partition types
   m   print this menu
   n   add a new partition
   o   create a new empty DOS partition table
   p   print the partition table
   q   quit without saving changes
   s   create a new empty Sun disklabel
   t   change a partition's system id
   u   change display/entry units
   v   verify the partition table
   w   write table to disk and exit
   x   extra functionality (experts only)

Command (m for help): 
```

我们要新建分区，输入n，然后回车。提示该硬盘当前有0个主要分区（primary）、0个扩展分区（extended），可以创建4个分区，然后让我们选择创建主要分区还是扩展分区。输入p并回车（或者直接回车），选择创建主要分区。
```
Command (m for help): n
Partition type:
   p   primary (0 primary, 0 extended, 4 free)
   e   extended
Select (default p): p
```

然后提示输入分区编号（只能1到4，默认为1），我们输入1并回车，
```
Partition number (1-4, default 1): 1
```

输入分区的开始扇区，我们直接回车采用默认配置，
```
First sector (2048-20971519, default 2048): 
Using default value 2048
```

输入分区的结束扇区，也直接回车采用默认配置，
```
Last sector, +sectors or +size{K,M,G} (2048-20971519, default 20971519): 
Using default value 20971519
```

此时我们的分区建好了，但还需要输入w并回车来进行保存。
```
Command (m for help): w
The partition table has been altered!

Calling ioctl() to re-read partition table.
Syncing disks.
```

该硬盘的分区建立完毕，通过fdisk -l查看一下最后的效果，
```
ubuntu@i-idh5qfpk:~$ sudo  fdisk -l /dev/sdc

Disk /dev/sdc: 10.7 GB, 10737418240 bytes
64 heads, 32 sectors/track, 10240 cylinders, total 20971520 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0xacb1d488

   Device Boot      Start         End      Blocks   Id  System
 /dev/sdc1            2048    20971519    10484736   83  Linux
```

我们新建的分区就是/dev/sdc1。接下来，我们对该分区进行格式化，
```
ubuntu@i-idh5qfpk:~$ sudo mkfs -t ext3 /dev/sdc1
mke2fs 1.42.9 (4-Feb-2014)
Discarding device blocks: done                            
Filesystem label=
OS type: Linux
Block size=4096 (log=2)
Fragment size=4096 (log=2)
Stride=0 blocks, Stripe width=0 blocks
655360 inodes, 2621184 blocks
131059 blocks (5.00%) reserved for the super user
First data block=0
Maximum filesystem blocks=2684354560
80 block groups
32768 blocks per group, 32768 fragments per group
8192 inodes per group
Superblock backups stored on blocks: 
    32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632
    
Allocating group tables: done
Writing inode tables: done
Creating journal (32768 blocks): done
Writing superblocks and filesystem accounting information: done 
```

格式化完毕。然后将该分区挂载到目录/mysdc，
```
ubuntu@i-idh5qfpk:~$ sudo mkdir -p /mysdc
ubuntu@i-idh5qfpk:~$ sudo mount /dev/sdc1 /mysdc
```

通过df命令查看一下。
```
ubuntu@i-idh5qfpk:~$ sudo df -k
Filesystem     1K-blocks     Used Available Use% Mounted on
/dev/sda1       20509308 13221580   6222872  68% /
none                   4        0         4   0% /sys/fs/cgroup
udev             2013184        4   2013180   1% /dev
tmpfs             404808      576    404232   1% /run
none                5120        0      5120   0% /run/lock
none             2024032     2084   2021948   1% /run/shm
none              102400        0    102400   0% /run/user
/dev/sdc1       10189112    23160   9641716   1% /mysdc
```

完成。

## shell脚本自动化 ##
上面我们是通过fdisk工具交互式地进行对硬盘进行分区的。那我们如何将其写成shell脚本自动化。回顾一下，我们刚刚交互式分区时输入的操作序列，然后自己阅读下面的脚本吧，太简单了，没什么好讲的。
``` shell
#!/bin/bash

echo "n
p
1


w
" | fdisk /dev/sdc && mkfs -t /dev/sdc1
```

*注意：1和w之间是两个空行。*

## 删除分区 ##
同样通过fdisk来删除分区，操作如下，不细说了，
```
ubuntu@i-idh5qfpk:~$ sudo fdisk /dev/sdc

Command (m for help): d
Selected partition 1

Command (m for help): w
The partition table has been altered!

Calling ioctl() to re-read partition table.
Syncing disks.
```

shell自动化脚本请参考创建分区的shell脚本自行编写。


(done)

