%global pkg_name xml-commons-apis12
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}


# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

Name:           %{?scl_prefix}xml-commons-apis12
Epoch:          0
Version:        1.2.04
Release:        10.9%{?dist}
Summary:        JAXP 1.2, DOM 2, SAX 2.0.1, SAX2-ext 1.0 apis
Group:          System Environment/Libraries
URL:            http://xml.apache.org/commons/
# src/org/xml/sax/helpers/SecuritySupport* is ASL 1.1
# java/external/src/javax/xml/parsers/ and transform/ is ASL 2.0
License:        ASL 2.0 and W3C and Public Domain and ASL 1.1
Source0:        xml-commons-external-1.2.04.tar.gz
# svn export http://svn.apache.org/repos/asf/xml/commons/tags/xml-commons-external-1_2_04/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       %{?scl_prefix_java_common}jpackage-utils >= 0:1.6
Requires:       maven30-runtime

BuildRequires:  %{?scl_prefix_java_common}ant
BuildRequires:  %{?scl_prefix_java_common}jpackage-utils >= 0:1.6
BuildArch:      noarch

%description 
DOM 2 org.w3c.dom and SAX XML 2.0 org.xml.sax processor apis used 
by several pieces of Apache software. XSLT 1.0.
This version includes the JAXP 1.2 APIs -- Java API for XML 
Processing 1.2, i.e. javax.xml{.parsers,.transform}

%package javadoc
Group:          Documentation
Summary:        Javadoc for %{pkg_name}

%description javadoc
%{summary}.

%package manual
Group:          Documentation
Summary:        Documents for %{pkg_name}
Requires:       maven30-runtime

%description manual
%{summary}.

%prep
%setup -q -c

%build
%{?scl:scl enable maven30 %{scl} - <<"EOF"}
set -e -x
ant -f xml-commons-external-1_2_04/java/external/build.xml jar javadoc
%{?scl:EOF}

%install
%{?scl:scl enable maven30 %{scl} - <<"EOF"}
set -e -x
rm -rf $RPM_BUILD_ROOT

install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 xml-commons-external-1_2_04/java/external/build/xml-apis.jar \
    $RPM_BUILD_ROOT%{_javadir}/%{pkg_name}-%{version}.jar

pushd $RPM_BUILD_ROOT%{_javadir}
for jar in *-%{version}*; do
ln -sf ${jar} $(echo $jar | sed -e 's|-%{version}\.jar|.jar|');
done

ln -sf %{pkg_name}.jar xml-commons-jaxp-1.2-apis.jar
ln -sf %{pkg_name}.jar jaxp12.jar
ln -sf %{pkg_name}.jar dom2.jar
popd


# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{pkg_name}-%{version}
cp -pr xml-commons-external-1_2_04/java/external/build/docs/javadoc/* \
    $RPM_BUILD_ROOT%{_javadocdir}/%{pkg_name}-%{version}
ln -s %{pkg_name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{pkg_name}
rm -rf xml-commons-external-1_2_04/java/external/build/docs/javadoc

# manuals
install -d -m 755 $RPM_BUILD_ROOT%{_docdir}/%{pkg_name}-%{version}
cp -pr xml-commons-external-1_2_04/java/external/build/docs/* $RPM_BUILD_ROOT%{_docdir}/%{pkg_name}-%{version}

# -----------------------------------------------------------------------------
%{?scl:EOF}

%clean
rm -rf $RPM_BUILD_ROOT

# -----------------------------------------------------------------------------

%files 
%defattr(0644,root,root,0755)
%{_javadir}/%{pkg_name}*.jar
%{_javadir}/jaxp12.jar
%{_javadir}/dom2.jar
%{_javadir}/xml-commons-jaxp-1.2-apis.jar
%doc xml-commons-external-1_2_04/java/external/LICENSE
%doc xml-commons-external-1_2_04/java/external/LICENSE.dom-documentation.txt
%doc xml-commons-external-1_2_04/java/external/LICENSE.dom-software.txt
%doc xml-commons-external-1_2_04/java/external/LICENSE.sax.txt
%doc xml-commons-external-1_2_04/java/external/README.dom.txt
%doc xml-commons-external-1_2_04/java/external/README-sax
%doc xml-commons-external-1_2_04/java/external/README.sax.txt
%doc xml-commons-external-1_2_04/java/external/NOTICE

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{pkg_name}-%{version}
%{_javadocdir}/%{pkg_name}

%files manual
%defattr(0644,root,root,0755)
%{_docdir}/%{pkg_name}-%{version}

# -----------------------------------------------------------------------------

%changelog
* Sat Jan 09 2016 Michal Srb <msrb@redhat.com> - 0:1.2.04-10.9
- maven33 rebuild

* Fri Jan 16 2015 Michal Srb <msrb@redhat.com> - 0:1.2.04-10.8
- Add missing requires on maven30-runtime

* Wed Jan 14 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2.04-10.7
- Add requires on SCL filesystem package

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 0:1.2.04-10.6
- Mass rebuild 2015-01-13

* Mon Jan 12 2015 Michal Srb <msrb@redhat.com> - 0:1.2.04-10.5
- Fix BR/R

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 0:1.2.04-10.4
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2.04-10.3
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2.04-10.2
- Mass rebuild 2014-02-19

* Fri Feb 14 2014 Michal Srb <msrb@redhat.com> - 0:1.2.04-10.1
- SCL maven30

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 01.2.04-10
- Mass rebuild 2013-12-27

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2.04-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 16 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.2.04-8
- Fix up license tag

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2.04-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2.04-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2.04-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 30 2010 Alexander Kurtakov <akurtako@redhat.com> 0:1.2.04-4
- Drop gcj.

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2.04-3.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2.04-2.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.2.04-1.5
- drop repotag
- fix license tag

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0:1.2.04-1jpp.4
- Autorebuild for GCC 4.3

* Sun Jun 03 2007 Florian La Roche <laroche@redhat.com> - 0:1.2.04-0jpp.4
- the javadoc subrpm used an undefined macro

* Tue Apr 12 2007 Matt Wringe <mwringe@redhat.com> - 0:1.2.04-0jpp.3
- Remove the provides on xml-commons-apis = 1.2 since this will not
  work properly with our other xml-commons-apis package.

* Tue Mar 13 2007 Matt Wringe <mwringe@redhat.com> - 0:1.2.04-0jpp.2
- Enable gcj option

* Thu Feb 16 2007 Matt Wringe <mwringe@redhat.com> - 0:1.2.04-0jpp.1
- Initial build. Based heavily on the xml-commons 1.3.03-7jpp spec file.
