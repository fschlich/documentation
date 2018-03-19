%global commit0 5fb3059e55a615c7d7836904434277c83ef2faa4
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:           php-fkooman-oauth2-server
Version:        3.0.0
Release:        1%{?dist}
Summary:        Very simple OAuth 2.0 server

License:        MIT
URL:            https://github.com/fkooman/php-oauth2-server
Source0:        https://github.com/fkooman/php-oauth2-server/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz

BuildArch:      noarch

#        "php": ">=5.4",
BuildRequires:  php(language) >= 5.4.0
#    "suggest": {
#        "ext-libsodium": "PHP < 7.2 sodium implementation",
#        "ext-sodium": "PHP >= 7.2 sodium implementation"
#    },
%if 0%{?fedora} >= 28
BuildRequires:  php-sodium
%else
BuildRequires:  php-libsodium
%endif
#        "ext-date": "*",
#        "ext-hash": "*",
#        "ext-json": "*",
#        "ext-pcre": "*",
#        "ext-pdo": "*",
#        "ext-spl": "*",
BuildRequires:  php-date
BuildRequires:  php-hash
BuildRequires:  php-json
BuildRequires:  php-pcre
BuildRequires:  php-pdo
#        "paragonie/constant_time_encoding": "^1|^2",
#        "paragonie/random_compat": "^1|^2",
#        "symfony/polyfill-php56": "^1"
BuildRequires:  php-composer(paragonie/constant_time_encoding)
BuildRequires:  php-composer(paragonie/random_compat)
BuildRequires:  php-composer(symfony/polyfill-php56)
BuildRequires:  %{_bindir}/phpunit
BuildRequires:  %{_bindir}/phpab

#        "php": ">=5.4",
Requires:       php(language) >= 5.4.0
#    "suggest": {
#        "ext-libsodium": "PHP < 7.2 sodium implementation",
#        "ext-sodium": "PHP >= 7.2 sodium implementation"
#    },
%if 0%{?fedora} >= 28
Requires:       php-sodium
%else
Requires:       php-libsodium
%endif
#        "ext-date": "*",
#        "ext-hash": "*",
#        "ext-json": "*",
#        "ext-pcre": "*",
#        "ext-pdo": "*",
#        "ext-spl": "*",
Requires:       php-date
Requires:       php-hash
Requires:       php-json
Requires:       php-pcre
Requires:       php-pdo
#        "paragonie/constant_time_encoding": "^1|^2",
#        "paragonie/random_compat": "^1|^2",
#        "symfony/polyfill-php56": "^1"
Requires:       php-composer(paragonie/constant_time_encoding)
Requires:       php-composer(paragonie/random_compat)
Requires:       php-composer(symfony/polyfill-php56)

Provides:       php-composer(fkooman/oauth2-server) = %{version}

%description
This is a very simple OAuth 2.0 server for integration in your own 
application. It has minimal dependencies, but still tries to be secure. 
The main purpose is to be compatible with PHP 5.4.

%prep
%autosetup -n php-oauth2-server-%{commit0}

%build
%{_bindir}/phpab -o src/autoload.php src
cat <<'AUTOLOAD' | tee -a src/autoload.php
require_once sprintf('%s/sodium_compat.php', __DIR__);
require_once '%{_datadir}/php/ParagonIE/ConstantTime/autoload.php';
require_once '%{_datadir}/php/random_compat/autoload.php';
require_once '%{_datadir}/php/Symfony/Polyfill/autoload.php';
AUTOLOAD

%install
mkdir -p %{buildroot}%{_datadir}/php/fkooman/OAuth/Server
cp -pr src/* %{buildroot}%{_datadir}/php/fkooman/OAuth/Server

%check
%{_bindir}/phpab -o tests/autoload.php tests
cat <<'AUTOLOAD' | tee -a tests/autoload.php
require_once 'src/autoload.php';
AUTOLOAD

%{_bindir}/phpunit tests --verbose --bootstrap=tests/autoload.php

%files
%license LICENSE
%doc composer.json CHANGES.md README.md
%dir %{_datadir}/php/fkooman
%dir %{_datadir}/php/fkooman/OAuth
%{_datadir}/php/fkooman/OAuth/Server

%changelog
* Mon Mar 19 2018 François Kooman <fkooman@tuxed.net> - 3.0.0-1
- update to 3.0.0

* Wed Jan 10 2018 François Kooman <fkooman@tuxed.net> - 2.2.0-1
- update to 2.2.0

* Thu Dec 07 2017 François Kooman <fkooman@tuxed.net> - 2.1.0-2
- use phpab to generate the classloader

* Thu Nov 30 2017 François Kooman <fkooman@tuxed.net> - 2.1.0-1
- update to 2.1.0

* Wed Nov 29 2017 François Kooman <fkooman@tuxed.net> - 2.0.1-1
- update to 2.0.1

* Tue Nov 14 2017 François Kooman <fkooman@tuxed.net> - 2.0.0-1
- update to 2.0.0

* Mon Sep 18 2017 François Kooman <fkooman@tuxed.net> - 1.1.0-1
- update to 1.1.0 

* Thu Jul 06 2017 François Kooman <fkooman@tuxed.net> - 1.0.0-1
- initial package
