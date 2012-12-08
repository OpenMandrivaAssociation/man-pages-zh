%define LANG zh

%define fname man-pages-zh_CN

#####################
#
# I have no idea where to get newer pages; there is no URL
# AdamW: There's http://www.linux.org.tw/CLDP/man/ , but nothing there
# at present (May 2007)
#
#####################

Summary: Chinese Man Pages
Name: man-pages-%{LANG}
Version: 1.5
Release: 12
License: FDL
Group: System/Internationalization
Source: http://download.sf.linuxforum.net/cmpp/%fname-%version.tar.bz2
Source1: makewhatis.%{LANG}_CN.UTF-8.bz2
Source2: makewhatis.%{LANG}_CN.bz2
Buildroot: %_tmppath/%{name}
BuildRequires: man => 1.5j-8mdk
Requires: locales-%{LANG}, man => 1.5j-8mdk
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

%files
%defattr(0644,root,man,755)
%_mandir/%{LANG}_CN.UTF-8
%attr(755,root,root)/usr/sbin/makewhatis.%{LANG}_CN.UTF-8
%config(noreplace) %attr(755,root,root)/etc/cron.weekly/makewhatis-%{LANG}_CN.UTF-8.cron
#
%_mandir/%{LANG}_CN
%attr(755,root,root)/usr/sbin/makewhatis.%{LANG}_CN
%config(noreplace) %attr(755,root,root)/etc/cron.weekly/makewhatis-%{LANG}_CN.cron
%_sysconfdir/cman.conf
%_sysconfdir/profile.d/cman.csh
%_sysconfdir/profile.d/cman.sh



%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 1.5-9mdv2011.0
+ Revision: 666377
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 1.5-8mdv2011.0
+ Revision: 606626
- rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 1.5-7mdv2010.1
+ Revision: 521778
- rebuilt for 2010.1

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 1.5-6mdv2009.1
+ Revision: 351587
- rebuild

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 1.5-5mdv2009.0
+ Revision: 223195
- rebuild

* Tue Jan 15 2008 Thierry Vignaud <tv@mandriva.org> 1.5-4mdv2008.1
+ Revision: 152998
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Fri Jun 01 2007 Adam Williamson <awilliamson@mandriva.org> 1.5-2mdv2008.0
+ Revision: 33501
- rebuild for new era; drop /var/catman (wildly obsolete)


* Thu Jul 07 2005 Thierry Vignaud <tvignaud@mandrakesoft.com> 1.5-1mdk
- new upstream source (#16295)

* Thu Jul 24 2003 Per Øyvind Karlsen <peroyvind@sintrax.net> 0.2.24-5mdk
- rebuild

* Mon Jan 20 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.2.24-4mdk
- build release

* Fri Mar 08 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.2.24-3mdk
- fix permission on /usr/share/man/id/*
- provides manpages-%%{LANG}
- don't overwrite crontab if user altered it

* Tue May 01 2001 David BAUDENS <baudens@mandrakesoft.com> 0.2.24-2mdk
- Use %%_tmppath for BuildRoot

* Thu Jul 20 2000 Pablo Saratxaga <pablo@mandrakesoft.com> 0.2.24-1mdk
- First rpm for Mandrake

