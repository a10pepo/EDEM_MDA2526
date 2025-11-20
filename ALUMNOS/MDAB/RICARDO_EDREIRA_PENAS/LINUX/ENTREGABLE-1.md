Ejercicio de comandos en la consola de linux.

1.Listar todos los archivos del directorio bin.
root@429546a995ce:/# pwd
/
root@429546a995ce:/# cd bin
root@429546a995ce:/bin# cd tmp
bash: cd: tmp: No such file or directory
root@429546a995ce:/bin# cd /tmp
root@429546a995ce:/tmp# cd /bin
root@429546a995ce:/bin# ls
'['                        expiry             mount               skill
 addpart                   expr               mountpoint          slabtop
 apt                       factor             mv                  sleep
 apt-cache                 faillog            namei               snice
 apt-cdrom                 fallocate          nawk                sort
 apt-config                false              newgrp              split
 apt-get                   fgrep              nice                stat
 apt-key                   find               nisdomainname       stdbuf
 apt-mark                  findmnt            nl                  stty
 arch                      flock              nohup               su
 awk                       fmt                nproc               sum
 b2sum                     fold               nsenter             sync
 base32                    free               numfmt              tabs
 base64                    getconf            od                  tac
 basename                  getent             pager               tail
 basenc                    getopt             partx               tar
 bash                      gpasswd            passwd              taskset
 bashbug                   gpgv               paste               tee
 captoinfo                 grep               pathchk             tempfile
 cat                       groups             perl                test
 chage                     gunzip             perl5.38.2          tic
 chattr                    gzexe              pgrep               timeout
 chcon                     gzip               pidof               tload
 chfn                      hardlink           pidwait             toe
 chgrp                     head               pinky               top
 chmod                     hostid             pkill               touch
 choom                     hostname           pldd                tput
 chown                     iconv              pmap                tr
 chrt                      id                 pr                  true
 chsh                      infocmp            printenv            truncate
 cksum                     infotocap          printf              tset
 clear                     install            prlimit             tsort
 clear_console             ionice             ps                  tty
 cmp                       ipcmk              ptx                 tzselect
 comm                      ipcrm              pwd                 uclampset
 cp                        ipcs               pwdx                umount
 csplit                    ischroot           rbash               uname
 cut                       join               readlink            uncompress
 dash                      kill               realpath            unexpand
 date                      last               rename.ul           uniq
 dd                        lastb              renice              unlink
 deb-systemd-helper        lastlog            reset               unminimize
 deb-systemd-invoke        ld.so              resizepart          unshare
 debconf                   ldd                rev                 update-alternatives
 debconf-apt-progress      link               rgrep               uptime
 debconf-communicate       linux32            rm                  users
 debconf-copydb            linux64            rmdir               utmpdump
 debconf-escape            ln                 run-parts           vdir
 debconf-set-selections    locale             runcon              vmstat
 debconf-show              locale-check       savelog             w
 delpart                   localedef          script              wall
 df                        logger             scriptlive          watch
 diff                      login              scriptreplay        wc
 diff3                     logname            sdiff               wdctl
 dir                       ls                 sed                 whereis
 dircolors                 lsattr             select-editor       which
 dirname                   lsblk              sensible-browser    which.debianutils
 dmesg                     lscpu              sensible-editor     who
 dnsdomainname             lsipc              sensible-pager      whoami
 domainname                lslocks            sensible-terminal   xargs
 dpkg                      lslogins           seq                 yes
 dpkg-deb                  lsmem              setarch             ypdomainname
 dpkg-divert               lsns               setpriv             zcat
 dpkg-maintscript-helper   man                setsid              zcmp
 dpkg-query                mawk               setterm             zdiff
 dpkg-realpath             mcookie            sg                  zdump
 dpkg-split                md5sum             sh                  zegrep
 dpkg-statoverride         md5sum.textutils   sha1sum             zfgrep
 dpkg-trigger              mesg               sha224sum           zforce
 du                        mkdir              sha256sum           zgrep
 echo                      mkfifo             sha384sum           zless
 egrep                     mknod              sha512sum           zmore
 env                       mktemp             shred               znew
 expand                    more               shuf
root@429546a995ce:/bin#1.

2.Listar todos los archivos del directorio tmp.
root@429546a995ce:/bin# cd /tmp
root@429546a995ce:/tmp# ls
PRUEBA
root@429546a995ce:/tmp# 

3.Listar todos los archivos del directorio etc que empiecen por t
root@429546a995ce:/tmp# cd /etc
root@429546a995ce:/etc# ls /etc/t*
README
root@429546a995ce:/etc# 

4.Listar todos los archivos del directorio dev que empiecen por tty.
root@429546a995ce:/etc# cd /dev
root@429546a995ce:/dev# ls /dev/tty 
/dev/tty
root@429546a995ce:/dev# 

5.Listar todos los archivos del directorio dev que empiecen por tty y acaben en 3.
root@429546a995ce:/dev# ls /dev/tty*3
ls: cannot access '/dev/tty*3': No such file or directory
root@429546a995ce:/dev# 

6.Listar todos los archivos del directorio dev que empiecen por t y acaben en C1.
root@429546a995ce:/dev# ls /dev/t*C1
ls: cannot access '/dev/t*C1': No such file or directory
root@429546a995ce:/dev# 

7.Listar todos los archivos, incluidos los ocultos, del directorio raíz.
root@429546a995ce:/# pwd
/
root@429546a995ce:/# ls -la
total 64
drwxr-xr-x   1 root root 4096 Sep 26 14:01 .
drwxr-xr-x   1 root root 4096 Sep 26 14:01 ..
-rwxr-xr-x   1 root root    0 Sep 24 16:40 .dockerenv
drwxr-xr-x   2 root root 4096 Sep 24 17:57 Prueba
lrwxrwxrwx   1 root root    7 Apr 22  2024 bin -> usr/bin
drwxr-xr-x   2 root root 4096 Apr 22  2024 boot
drwxrwxrwx   2 root root 4096 Sep 26 14:01 carpetaNueva
drwxr-xr-x   5 root root  360 Sep 26 13:46 dev
drwxr-xr-x   1 root root 4096 Sep 24 16:40 etc
drwxr-xr-x   3 root root 4096 Sep 10 02:20 home
lrwxrwxrwx   1 root root    7 Apr 22  2024 lib -> usr/lib
drwxr-xr-x   2 root root 4096 Sep 10 02:14 media
drwxr-xr-x   2 root root 4096 Sep 10 02:14 mnt
drwxr-xr-x   2 root root 4096 Sep 10 02:14 opt
dr-xr-xr-x 229 root root    0 Sep 26 13:46 proc
drwx------   2 root root 4096 Sep 10 02:20 root
drwxr-xr-x   4 root root 4096 Sep 10 02:20 run
lrwxrwxrwx   1 root root    8 Apr 22  2024 sbin -> usr/sbin
drwxr-xr-x   2 root root 4096 Sep 10 02:14 srv
dr-xr-xr-x  11 root root    0 Sep 26 14:02 sys
drwxrwxrwt   1 root root 4096 Sep 24 16:59 tmp
drwxr-xr-x  11 root root 4096 Sep 10 02:14 usr
drwxr-xr-x  11 root root 4096 Sep 10 02:20 var
root@429546a995ce:/# 

8.Listar todos los archivos del directorio etc que no empiecen por t.
root@429546a995ce:/# ls /etc/[!t]*
/etc/bash.bashrc             /etc/gshadow-       /etc/lsb-release    /etc/resolv.conf
/etc/bindresvport.blacklist  /etc/host.conf      /etc/machine-id     /etc/rmt
/etc/debconf.conf            /etc/hostname       /etc/mke2fs.conf    /etc/shadow
/etc/debian_version          /etc/hosts          /etc/mtab           /etc/shadow-
/etc/e2scrub.conf            /etc/issue          /etc/networks       /etc/shells
/etc/environment             /etc/issue.net      /etc/nsswitch.conf  /etc/subgid
/etc/fstab                   /etc/ld.so.cache    /etc/os-release     /etc/subgid-
/etc/gai.conf                /etc/ld.so.conf     /etc/pam.conf       /etc/subuid
/etc/group                   /etc/legal          /etc/passwd         /etc/subuid-
/etc/group-                  /etc/libaudit.conf  /etc/passwd-        /etc/sysctl.conf
/etc/gshadow                 /etc/login.defs     /etc/profile        /etc/xattr.conf

/etc/alternatives:
README  awk  nawk  pager  rmt  which

/etc/apt:
apt.conf.d  auth.conf.d  keyrings  preferences.d  sources.list  sources.list.d  trusted.gpg.d

/etc/cloud:
build.info

/etc/cron.d:
e2scrub_all

/etc/cron.daily:
apt-compat  dpkg

/etc/default:
locale  useradd

/etc/dpkg:
dpkg.cfg  dpkg.cfg.d  origins

/etc/gnutls:
config

/etc/init.d:
procps

/etc/kernel:
postinst.d

/etc/ld.so.conf.d:
aarch64-linux-gnu.conf  libc.conf

/etc/logrotate.d:
alternatives  apt  dpkg

/etc/opt:

/etc/pam.d:
chfn      common-account   common-session                 newusers  runuser    su-l
chpasswd  common-auth      common-session-noninteractive  other     runuser-l
chsh      common-password  login                          passwd    su

/etc/profile.d:
01-locale-fix.sh

/etc/rc0.d:

/etc/rc1.d:

/etc/rc2.d:

/etc/rc3.d:

/etc/rc4.d:

/etc/rc5.d:

/etc/rc6.d:

/etc/rcS.d:
S01procps

/etc/security:
access.conf    group.conf   limits.d        namespace.d     opasswd       pwhistory.conf  time.conf
faillock.conf  limits.conf  namespace.conf  namespace.init  pam_env.conf  sepermit.conf

/etc/selinux:
semanage.conf

/etc/skel:

/etc/sysctl.d:
10-bufferbloat.conf       10-kernel-hardening.conf  10-network-security.conf  README.sysctl
10-console-messages.conf  10-magic-sysrq.conf       10-ptrace.conf
10-ipv6-privacy.conf      10-map-count.conf         10-zeropage.conf

/etc/systemd:
system  user

/etc/update-motd.d:
00-header  10-help-text  50-motd-news  60-unminimize
root@429546a995ce:/# 

9.Listar todos los archivos del directorio usr y sus subdirectorios.
Ls -R /usr 
10.Cambiarse al directorio tmp, crear directorio PRUEBA.
root@429546a995ce:/# cd tmp
root@429546a995ce:/tmp# mkdir PRUEBA
root@429546a995ce:/tmp# ls -l
total 4
drwxr-xr-x 2 root root 4096 Sep 24 16:59 PRUEBA
root@429546a995ce:/tmp# 

11.Verificar que el directorio actual ha cambiado.
root@429546a995ce:/tmp# ls          
PRUEBA



12.Mostrar el día y la hora actual.
root@429546a995ce:/tmp# date
Wed Oct  1 17:24:20 UTC 2025



13.Con un solo comando posicionarse en el directorio $HOME.

root@429546a995ce:/tmp# cd ~
root@429546a995ce:/home# 

14.Verificar que se está en él.
root@429546a995ce:/home# pwd
/home

15.Listar todos los ficheros del directorio HOME mostrando sus permisos.
root@429546a995ce:/home# ls -l
total 4
drwxr-x--- 2 ubuntu ubuntu 4096 Sep 10 02:20 ubuntu

16.Borrar todos los archivos y directorios visibles de vuestro directorio PRUEBA.
root@429546a995ce:/home# cd /tmp/PRUEBA
root@429546a995ce:/tmp/PRUEBA# ls
root@429546a995ce:/tmp/PRUEBA#   

17.Crear los directorios dir1, dir2 y dir3 en el directorio PRUEBA. Dentro de dir1 crear el directorio dir11. Dentro del directorio dir3 crear el directorio dir31. Dentro del directorio dir31, crear los directorios dir311 y dir312.
root@429546a995ce:/home# cd /tmp/PRUEBA
root@429546a995ce:/tmp/PRUEBA# ls
root@429546a995ce:/tmp/PRUEBA# mkdir dir1 dir2 dir3 
root@429546a995ce:/tmp/PRUEBA# ls -l
total 12
drwxr-xr-x 2 root root 4096 Oct  1 17:31 dir1
drwxr-xr-x 2 root root 4096 Oct  1 17:31 dir2
drwxr-xr-x 2 root root 4096 Oct  1 17:31 dir3
root@429546a995ce:/tmp/PRUEBA# mkdir /dir1 dir11
root@429546a995ce:/tmp/PRUEBA# mkdir /dir3 dir31
root@429546a995ce:/tmp/PRUEBA# mkdir /dir3/dir31 dir311 dir312 
root@429546a995ce:/tmp/PRUEBA# ls -l
total 28
drwxr-xr-x 2 root root 4096 Oct  1 17:31 dir1
drwxr-xr-x 2 root root 4096 Oct  1 17:31 dir11
drwxr-xr-x 2 root root 4096 Oct  1 17:31 dir2
drwxr-xr-x 2 root root 4096 Oct  1 17:31 dir3
drwxr-xr-x 2 root root 4096 Oct  1 17:32 dir31
drwxr-xr-x 2 root root 4096 Oct  1 17:33 dir311
drwxr-xr-x 2 root root 4096 Oct  1 17:33 dir312
root@429546a995ce:/tmp/PRUEBA# 

18.Copiar el archivo /etc/mtab al directorio PRUEBA.
root@429546a995ce:/etc# cp /etc/mtab /tmp/PRUEBA
root@429546a995ce:/etc# cd /tmp/PRUEBA
root@429546a995ce:/tmp/PRUEBA# ls -l
total 32
drwxr-xr-x 2 root root 4096 Oct  1 17:31 dir1
drwxr-xr-x 2 root root 4096 Oct  1 17:31 dir11
drwxr-xr-x 2 root root 4096 Oct  1 17:31 dir2
drwxr-xr-x 2 root root 4096 Oct  1 17:31 dir3
drwxr-xr-x 2 root root 4096 Oct  1 17:32 dir31
drwxr-xr-x 2 root root 4096 Oct  1 17:33 dir311
drwxr-xr-x 2 root root 4096 Oct  1 17:33 dir312
-r--r--r-- 1 root root 1714 Oct  1 17:45 mtab
root@429546a995ce:/tmp/PRUEBA# 

19.Copiar /etc/mtab en dir1, dir2 y dir3.
root@429546a995ce:/tmp/PRUEBA# cp /tmp/PRUEBA/mtab /dir1          
root@429546a995ce:/tmp/PRUEBA# cp /tmp/PRUEBA/mtab /dir2     
root@429546a995ce:/tmp/PRUEBA# cp /tmp/PRUEBA/mtab /dir3

20.Comprobar el ejercicio anterior mediante un solo comando.

root@429546a995ce:/tmp/PRUEBA# ls -lR
.:
total 32
drwxr-xr-x 2 root root 4096 Oct  1 17:31 dir1
drwxr-xr-x 2 root root 4096 Oct  1 17:31 dir11
drwxr-xr-x 2 root root 4096 Oct  1 17:31 dir2
drwxr-xr-x 2 root root 4096 Oct  1 18:02 dir3
drwxr-xr-x 2 root root 4096 Oct  1 17:32 dir31
drwxr-xr-x 2 root root 4096 Oct  1 17:33 dir311
drwxr-xr-x 2 root root 4096 Oct  1 17:33 dir312
-r--r--r-- 1 root root 1714 Oct  1 17:45 mtab

./dir1:
total 0

./dir11:
total 0

./dir2:
total 0

./dir3:
total 4
-r--r--r-- 1 root root 1714 Oct  1 18:02 mtab

./dir31:
total 0

./dir311:
total 0

./dir312:
total 0
root@429546a995ce:/tmp/PRUEBA# 

