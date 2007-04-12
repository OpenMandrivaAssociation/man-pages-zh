%define LANG zh
%define version 1.5
%define release 1mdk

%define fname man-pages-zh_CN

#####################
#
# I have no idea where to get newer pages; there is no URL
#
#####################

Summary: Chinese Man Pages
Name: man-pages-%{LANG}
Version: %{version}
Release: %{release}
License: FDL
Group: System/Internationalization
Source: http://download.sf.linuxforum.net/cmpp/%fname-%version.tar.bz2
Source1: makewhatis.%{LANG}_CN.UTF-8.bz2
Source2: makewhatis.%{LANG}_CN.bz2
#Icon: books-%{LANG}.xpm
Buildroot: %_tmppath/%{name}
Prereq: sed grep man
Autoreq: false
BuildArch: noarch
Requires: locales-%{LANG}
Obsoletes: man-%{LANG}, manpages-%{LANG}
Provides: man-%{LANG}, manpages-%{LANG}

%description
Set of man pages translated into Chinese language

%prep
%setup -q -n %fname-%version
%make u8
%make gb
# fix conflict with mplayer:
rm -f */man1/mplayer.1

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/etc
make DESTDIR=$RPM_BUILD_ROOT%{_usr}/share install-u8
make DESTDIR=$RPM_BUILD_ROOT%{_usr}/share install-gb CONFDIR=$RPM_BUILD_ROOT/etc
mkdir -p $RPM_BUILD_ROOT/var/catman/%{LANG}_CN.UTF-8/cat{1,2,3,4,5,6,7,8,9,n}
mkdir -p $RPM_BUILD_ROOT/var/catman/%{LANG}_CN/cat{1,2,3,4,5,6,7,8,9,n}

mkdir -p $RPM_BUILD_ROOT/usr/sbin
bzcat %SOURCE1 > $RPM_BUILD_ROOT/usr/sbin/makewhatis.%{LANG}_CN.UTF-8
chmod a+rx $RPM_BUILD_ROOT/usr/sbin/makewhatis.%{LANG}_CN.UTF-8
bzcat %SOURCE2 > $RPM_BUILD_ROOT/usr/sbin/makewhatis.%{LANG}_CN
chmod a+rx $RPM_BUILD_ROOT/usr/sbin/makewhatis.%{LANG}_CN

$RPM_BUILD_ROOT/usr/sbin/makewhatis.%{LANG}_CN.UTF-8 \
        $RPM_BUILD_ROOT/%{_mandir}/%{LANG}_CN.UTF-8
$RPM_BUILD_ROOT/usr/sbin/makewhatis.%{LANG}_CN \
        $RPM_BUILD_ROOT/%{_mandir}/%{LANG}_CN

mkdir -p $RPM_BUILD_ROOT/etc/cron.weekly
cat > $RPM_BUILD_ROOT/etc/cron.weekly/makewhatis-%{LANG}_CN.UTF-8.cron << EOF
#!/bin/bash
/usr/sbin/makewhatis.%{LANG}_CN.UTF-8 %{_mandir}/%{LANG}_CN.UTF-8
exit 0
EOF
chmod a+x $RPM_BUILD_ROOT/etc/cron.weekly/makewhatis-%{LANG}_CN.UTF-8.cron
cat > $RPM_BUILD_ROOT/etc/cron.weekly/makewhatis-%{LANG}_CN.cron << EOF
#!/bin/bash
/usr/sbin/makewhatis.%{LANG}_CN %{_mandir}/%{LANG}_CN
exit 0
EOF
chmod a+x $RPM_BUILD_ROOT/etc/cron.weekly/makewhatis-%{LANG}_CN.cron

%post
/etc/cron.weekly/makewhatis-%{LANG}_CN.UTF-8.cron
/etc/cron.weekly/makewhatis-%{LANG}_CN.cron
touch %{_mandir}/%{LANG}_CN.UTF-8/whatis
touch %{_mandir}/%{LANG}_CN/whatis

%postun
# 0 means deleting the package
if [ "$1" = "0" ]; then
   ## Force removing of /var/catman/%{LANG}_CN.GB2312, if there isn't any man page
   ## directory /%{_mandir}/%{LANG}_CN.GB2312
   if [ ! -d /%{_mandir}/%{LANG}_CN.GB2312 ] ; then
       rm -rf /var/catman/%{LANG}_CN.GB2312
   fi
   ## Force removing of /var/catman/%{LANG}_TW.Big5, if there isn't any man page
   ## directory /%{_mandir}/%{LANG}_TW.Big5
   if [ ! -d /%{_mandir}/%{LANG}_TW.Big5 ] ; then
       rm -rf /var/catman/%{LANG}_TW.Big5
   fi
fi

%clean
rm -r $RPM_BUILD_ROOT

%files
%defattr(0644,root,man,755)
%ghost %{_mandir}/%{LANG}_CN.UTF-8/whatis
%_mandir/%{LANG}_CN.UTF-8
%attr(775,root,man)/var/catman/%{LANG}_CN.UTF-8
%attr(755,root,root)/usr/sbin/makewhatis.%{LANG}_CN.UTF-8
%config(noreplace) %attr(755,root,root)/etc/cron.weekly/makewhatis-%{LANG}_CN.UTF-8.cron
#
%ghost %{_mandir}/%{LANG}_CN/whatis
%_mandir/%{LANG}_CN
%attr(775,root,man)/var/catman/%{LANG}_CN
%attr(755,root,root)/usr/sbin/makewhatis.%{LANG}_CN
%config(noreplace) %attr(755,root,root)/etc/cron.weekly/makewhatis-%{LANG}_CN.cron
%_sysconfdir/cman.conf
%_sysconfdir/profile.d/cman.csh
%_sysconfdir/profile.d/cman.sh


