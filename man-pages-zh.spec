#####################
#
# I have no idea where to get newer pages; there is no URL
# AdamW:	There's http://www.linux.org.tw/CLDP/man/ , but nothing there
# at present (May 2007)
#
#####################

%define LANG zh
%define fname man-pages-zh_CN

Summary:	Chinese Man Pages
Name:		man-pages-%{LANG}
Version:	1.5
Release:	24
License:	FDL
Group:		System/Internationalization
Source0:	http://download.sf.linuxforum.net/cmpp/%{fname}-%{version}.tar.bz2
Source1:	makewhatis.%{LANG}_CN.UTF-8.bz2
Source2:	makewhatis.%{LANG}_CN.bz2
BuildArch:	noarch
BuildRequires:	man
Requires:	locales-%{LANG}
Requires:	man
Requires:	locales-%{LANG}
Autoreq:	false
Conflicts:	filesystem < 3.0-17

%description
Set of man pages translated into Chinese language

%prep
%setup -qn %{fname}-%{version}
%make u8
%make gb
# fix conflict with mplayer:
rm -f */man1/mplayer.1

%install
mkdir -p %{buildroot}/etc
make DESTDIR=%{buildroot}%{_usr}/share install-u8
make DESTDIR=%{buildroot}%{_usr}/share install-gb CONFDIR=%{buildroot}/etc

mkdir -p %{buildroot}/usr/sbin
bzcat %SOURCE1 > %{buildroot}/usr/sbin/makewhatis.%{LANG}_CN.UTF-8
chmod a+rx %{buildroot}/usr/sbin/makewhatis.%{LANG}_CN.UTF-8
bzcat %SOURCE2 > %{buildroot}/usr/sbin/makewhatis.%{LANG}_CN
chmod a+rx %{buildroot}/usr/sbin/makewhatis.%{LANG}_CN

%{buildroot}/usr/sbin/makewhatis.%{LANG}_CN.UTF-8 \
        %{buildroot}/%{_mandir}/%{LANG}_CN.UTF-8
%{buildroot}/usr/sbin/makewhatis.%{LANG}_CN \
        %{buildroot}/%{_mandir}/%{LANG}_CN

mkdir -p %{buildroot}/etc/cron.weekly
cat > %{buildroot}/etc/cron.weekly/makewhatis-%{LANG}_CN.UTF-8.cron << EOF
#!/bin/bash
/usr/sbin/makewhatis.%{LANG}_CN.UTF-8 %{_mandir}/%{LANG}_CN.UTF-8
exit 0
EOF
chmod a+x %{buildroot}/etc/cron.weekly/makewhatis-%{LANG}_CN.UTF-8.cron
cat > %{buildroot}/etc/cron.weekly/makewhatis-%{LANG}_CN.cron << EOF
#!/bin/bash
/usr/sbin/makewhatis.%{LANG}_CN %{_mandir}/%{LANG}_CN
exit 0
EOF
chmod a+x %{buildroot}/etc/cron.weekly/makewhatis-%{LANG}_CN.cron

%post
/etc/cron.weekly/makewhatis-%{LANG}_CN.UTF-8.cron
/etc/cron.weekly/makewhatis-%{LANG}_CN.cron
touch %{_mandir}/%{LANG}_CN.UTF-8/whatis
touch %{_mandir}/%{LANG}_CN/whatis

%files
%{_mandir}/%{LANG}_CN.UTF-8/*
%attr(755,root,root)/usr/sbin/makewhatis.%{LANG}_CN.UTF-8
%config(noreplace) %attr(755,root,root)/etc/cron.weekly/makewhatis-%{LANG}_CN.UTF-8.cron
#
%{_mandir}/%{LANG}_CN/*
%attr(755,root,root)/usr/sbin/makewhatis.%{LANG}_CN
%config(noreplace) %attr(755,root,root)/etc/cron.weekly/makewhatis-%{LANG}_CN.cron
%{_sysconfdir}/cman.conf
%{_sysconfdir}/profile.d/cman.csh
%{_sysconfdir}/profile.d/cman.sh

