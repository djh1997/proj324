#!/usr/bin/env bash
if [ -z "$BASH" ] ; then
   bash  $0
   exit
fi



my_name=$0


function setup_environment {
  bf=""
  n=""
  ORGANISATION="University of Plymouth"
  URL="https://www.plymouth.ac.uk/eduroam"
  SUPPORT="servicedesk@plymouth.ac.uk"
if [ ! -z "$DISPLAY" ] ; then
  if which zenity 1>/dev/null 2>&1 ; then
    ZENITY=`which zenity`
  elif which kdialog 1>/dev/null 2>&1 ; then
    KDIALOG=`which kdialog`
  else
    if tty > /dev/null 2>&1 ; then
      if  echo $TERM | grep -E -q "xterm|gnome-terminal|lxterminal"  ; then
        bf="[1m";
        n="[0m";
      fi
    else
      find_xterm
      if [ -n "$XT" ] ; then
        $XT -e $my_name
      fi
    fi
  fi
fi
}

function split_line {
echo $1 | awk  -F '\\\\n' 'END {  for(i=1; i <= NF; i++) print $i }'
}

function find_xterm {
terms="xterm aterm wterm lxterminal rxvt gnome-terminal konsole"
for t in $terms
do
  if which $t > /dev/null 2>&1 ; then
  XT=$t
  break
  fi
done
}


function ask {
     T="eduroam CAT"
#  if ! [ -z "$3" ] ; then
#     T="$T: $3"
#  fi
  if [ ! -z $KDIALOG ] ; then
     if $KDIALOG --yesno "${1}\n${2}?" --title "$T" ; then
       return 0
     else
       return 1
     fi
  fi
  if [ ! -z $ZENITY ] ; then
     text=`echo "${1}" | fmt -w60`
     if $ZENITY --no-wrap --question --text="${text}\n${2}?" --title="$T" 2>/dev/null ; then
       return 0
     else
       return 1
     fi
  fi

  yes=Y
  no=N
  yes1=`echo $yes | awk '{ print toupper($0) }'`
  no1=`echo $no | awk '{ print toupper($0) }'`

  if [ $3 == "0" ]; then
    def=$yes
  else
    def=$no
  fi

  echo "";
  while true
  do
  split_line "$1"
  read -p "${bf}$2 ${yes}/${no}? [${def}]:$n " answer
  if [ -z "$answer" ] ; then
    answer=${def}
  fi
  answer=`echo $answer | awk '{ print toupper($0) }'`
  case "$answer" in
    ${yes1})
       return 0
       ;;
    ${no1})
       return 1
       ;;
  esac
  done
}

function alert {
  if [ ! -z $KDIALOG ] ; then
     $KDIALOG --sorry "${1}"
     return
  fi
  if [ ! -z $ZENITY ] ; then
     $ZENITY --warning --text="$1" 2>/dev/null
     return
  fi
  echo "$1"

}

function show_info {
  if [ ! -z $KDIALOG ] ; then
     $KDIALOG --msgbox "${1}"
     return
  fi
  if [ ! -z $ZENITY ] ; then
     $ZENITY --info --width=500 --text="$1" 2>/dev/null
     return
  fi
  split_line "$1"
}

function confirm_exit {
  if [ ! -z $KDIALOG ] ; then
     if $KDIALOG --yesno "Really quit?"  ; then
     exit 1
     fi
  fi
  if [ ! -z $ZENITY ] ; then
     if $ZENITY --question --text="Really quit?" 2>/dev/null ; then
        exit 1
     fi
  fi
}



function prompt_nonempty_string {
  prompt=$2
  if [ ! -z $ZENITY ] ; then
    if [ $1 -eq 0 ] ; then
     H="--hide-text "
    fi
    if ! [ -z "$3" ] ; then
     D="--entry-text=$3"
    fi
  elif [ ! -z $KDIALOG ] ; then
    if [ $1 -eq 0 ] ; then
     H="--password"
    else
     H="--inputbox"
    fi
  fi


  out_s="";
  if [ ! -z $ZENITY ] ; then
    while [ ! "$out_s" ] ; do
      out_s=`$ZENITY --entry --width=300 $H $D --text "$prompt" 2>/dev/null`
      if [ $? -ne 0 ] ; then
        confirm_exit
      fi
    done
  elif [ ! -z $KDIALOG ] ; then
    while [ ! "$out_s" ] ; do
      out_s=`$KDIALOG $H "$prompt" "$3"`
      if [ $? -ne 0 ] ; then
        confirm_exit
      fi
    done  
  else
    while [ ! "$out_s" ] ; do
      read -p "${prompt}: " out_s
    done
  fi
  echo "$out_s";
}

function user_cred {
  PASSWORD="a"
  PASSWORD1="b"

  if ! USER_NAME=`prompt_nonempty_string 1 "enter your userid"` ; then
    exit 1
  fi

  while [ "$PASSWORD" != "$PASSWORD1" ]
  do
    if ! PASSWORD=`prompt_nonempty_string 0 "enter your password"` ; then
      exit 1
    fi
    if ! PASSWORD1=`prompt_nonempty_string 0 "repeat your password"` ; then
      exit 1
    fi
    if [ "$PASSWORD" != "$PASSWORD1" ] ; then
      alert "passwords do not match"
    fi
  done
}
setup_environment
show_info "This installer has been prepared for ${ORGANISATION}\n\nMore information and comments:\n\nEMAIL: ${SUPPORT}\nWWW: ${URL}\n\nInstaller created with software from the GEANT project."
if ! ask "This installer will only work properly if you are a member of ${bf}University of Plymouth.${n}" "Continue" 1 ; then exit; fi
if [ -d $HOME/.cat_installer ] ; then
   if ! ask "Directory $HOME/.cat_installer exists; some of its files may be overwritten." "Continue" 1 ; then exit; fi
else
  mkdir $HOME/.cat_installer
fi
# save certificates
echo "-----BEGIN CERTIFICATE-----
MIIFTDCCAzSgAwIBAgIUSJgt4qkssznhyPkzNYJ10+T4glUwDQYJKoZIhvcNAQEL
BQAwRTELMAkGA1UEBhMCQk0xGTAXBgNVBAoTEFF1b1ZhZGlzIExpbWl0ZWQxGzAZ
BgNVBAMTElF1b1ZhZGlzIFJvb3QgQ0EgMjAeFw0xMzA2MDExMzM1MDVaFw0yMzA2
MDExMzM1MDVaME0xCzAJBgNVBAYTAkJNMRkwFwYDVQQKExBRdW9WYWRpcyBMaW1p
dGVkMSMwIQYDVQQDExpRdW9WYWRpcyBHbG9iYWwgU1NMIElDQSBHMjCCASIwDQYJ
KoZIhvcNAQEBBQADggEPADCCAQoCggEBAOHhhWmUwI9X+jT+wbho5JmQqYh6zle3
0OS1VMIYfdDDGeipY4D3t9zSGaNasGDZdrQdMlY18WyjnEKhi4ojNZdBewVphCiO
zh5Ni2Ak8bSI/sBQ9sKPrpd0+UCqbvaGs6Tpx190ZRT0Pdy+TqOYZF/jBmzBj7Yf
XJmWxlfCy62UiQ6tvv+4C6W2OPu1R4HUD8oJ8Qo7Eg0cD+GFsBM2w8soffyl+Dc6
pKtARmOClUC7EqyWP0V9953lA34kuJZlYxxdgghBTn9rWoaQw/Lr5Fn0Xgd7fYS3
/zGhmXYvVsuAxIn8Gk+YaeoLZ8H9tUvnDD3lEHzvIsMPxqtd7IgcVaMCAwEAAaOC
ASowggEmMBIGA1UdEwEB/wQIMAYBAf8CAQAwEQYDVR0gBAowCDAGBgRVHSAAMHIG
CCsGAQUFBwEBBGYwZDAqBggrBgEFBQcwAYYeaHR0cDovL29jc3AucXVvdmFkaXNn
bG9iYWwuY29tMDYGCCsGAQUFBzAChipodHRwOi8vdHJ1c3QucXVvdmFkaXNnbG9i
YWwuY29tL3F2cmNhMi5jcnQwDgYDVR0PAQH/BAQDAgEGMB8GA1UdIwQYMBaAFBqE
YrxITDMlBNTu0PYDxBlG0ZRrMDkGA1UdHwQyMDAwLqAsoCqGKGh0dHA6Ly9jcmwu
cXVvdmFkaXNnbG9iYWwuY29tL3F2cmNhMi5jcmwwHQYDVR0OBBYEFJEZYq1bF6cw
+/DeOSWxvYy5uFEnMA0GCSqGSIb3DQEBCwUAA4ICAQB8CmCCAEG1Lcw55fTba84A
ipwMieZydFO5bcIh5UyXWgWZ6OP4jb/6LaifEMLjRCC0mU14G6PrPU+iZQiIae7X
5EavhmETEA8JbLICjiD4c9Y6+bgMt4szEPiZ2SALOQj10Br4HKQfy/OvbedRbLax
p9qlDG4qJgSt3uikDIJSarx6mpgEQXu00UZNkiEYUfeO8hXGXrZbtDnkuaiVDtM6
s9yYpcoyFxFOrORrEgViaI7P3EJaDYmI6IDUIPaSBM6GrVMiaINYEMBL1v2jZi8r
XDY0yVsZ/0DAIQiCBNNvT1NjQ5Sn1E+O+ZBiqDD+rBvBoPsI6ydfdKtJur5YL+Oo
kJK2eLrce8287awIcd8FMRDcZw/NX1bc8uKye5OCtwpQ0d4jL4emuXwFv8TqUbZh
2xJShyy57cqw3qWoBOs/WWza29/Hun8PXkQoZepwY/xc+9nI1NaKM8NqhSqJNTJl
vXj7zb3mdpbe3YR9BkSXProlN7l5KOx54gJ7kJ7r6qJYJux03HyPM11Kp4wfdn1R
sC2UQ5awC6fg/3XE2HZVkyqJjKwqh4nFaiK5EMV7DHQ4oJx9ckmDw6pBvDaoPokX
yzdfJ72n+1JfHGP+workciKNldgqYX6J4jPrCIEIBrtDta4QxP10Tyd9RFu13XmE
8SYi/VXvrf3nriQfAZ/nSA==
-----END CERTIFICATE-----

-----BEGIN CERTIFICATE-----
MIIFtzCCA5+gAwIBAgICBQkwDQYJKoZIhvcNAQEFBQAwRTELMAkGA1UEBhMCQk0x
GTAXBgNVBAoTEFF1b1ZhZGlzIExpbWl0ZWQxGzAZBgNVBAMTElF1b1ZhZGlzIFJv
b3QgQ0EgMjAeFw0wNjExMjQxODI3MDBaFw0zMTExMjQxODIzMzNaMEUxCzAJBgNV
BAYTAkJNMRkwFwYDVQQKExBRdW9WYWRpcyBMaW1pdGVkMRswGQYDVQQDExJRdW9W
YWRpcyBSb290IENBIDIwggIiMA0GCSqGSIb3DQEBAQUAA4ICDwAwggIKAoICAQCa
GMpLlA0ALa8DKYrwD4HIrkwZhR0In6spRIXzL4GtMh6QRr+jhiYaHv5+HBg6XJxg
Fyo6dIMzMH1hVBHL7avg5tKifvVrbxi3Cgst/ek+7wrGsxDp3MJGF/hd/aTa/55J
WpzmM+Yklvc/ulsrHHo1wtZn/qtmUIttKGAr79dgw8eTvI02kfN/+NsRE8Scd3bB
rrcCaoF6qUWD4gXmuVbBlDePSHFjIuwXZQeVikvfj8ZaCuWw419eaxGrDPmF60Tp
+ARz8un+XJiM9XOva7R+zdRcAitMOeGylZUtQofX1bOQQ7dsE/He3fbE+Ik/0XX1
ksOR1YqI0JDs3G3eicJlcZaLDQP9nL9bFqyS2+r+eXyt66/3FsvbzSUr5R/7mp/i
Ucw6UwxI5g69ybR2BlLmEROFcmMDBOAENisgGQLodKcftslWZvB1JdxnwQ5hYIiz
PtGo/KPaHbDRsSNU30R2be1B2MGyIrZTHN81Hdyhdyox5C315eXbyOD/5YDXC2Og
/zOhD7osFRXql7PSorW+8oyWHhqPHWykYTe5hnMz15eWniN9gqRMgeKh0bpnX5UH
oycR7hYQe7xFSkyyBNKr79X9DFHOUGoIMfmR2gyPZFwDwzqLID9ujWc9Otb+fVuI
yV77zGHcizN300QyNQliBJIWENieJ0f7OyHj+OsdWwIDAQABo4GwMIGtMA8GA1Ud
EwEB/wQFMAMBAf8wCwYDVR0PBAQDAgEGMB0GA1UdDgQWBBQahGK8SEwzJQTU7tD2
A8QZRtGUazBuBgNVHSMEZzBlgBQahGK8SEwzJQTU7tD2A8QZRtGUa6FJpEcwRTEL
MAkGA1UEBhMCQk0xGTAXBgNVBAoTEFF1b1ZhZGlzIExpbWl0ZWQxGzAZBgNVBAMT
ElF1b1ZhZGlzIFJvb3QgQ0EgMoICBQkwDQYJKoZIhvcNAQEFBQADggIBAD4KFk2f
BluornFdLwUvZ+YTRYPENvbzwCYMDbVHZF34tHLJRqUDGCdViXh9duqWNIAXINzn
g/iN/Ae42l9NLmeyhP3ZRPx3UIHmfLTJDQtyU/h2BwdBR5YM++CCJpNVjP4iH2Bl
fF/nJrP3MpCYUNQ3cVX2kiF495V5+vgtJodmVjB3pjd4M1IQWK4/YY7yarHvGH5K
WWPKjaJW1acvvFYfzznB4vsKqBUsfU16Y8Zsl0Q80m/DShcK+JDSV6IZUaUtl0Ha
B0+pUNqQjZRG4T7wlP0QADj1O+hA4bRuVhogzG9Yje0uRY/W6ZM/57Es3zrWIozc
hLsib9D45MY56QSIPMO661V6bYCZJPVsAfv4l7CUW+v90m/xd2gNNWQjrLhVoQPR
TUIZ3Ph1WVaj+ahJefivDrkRoHy3au000LYmYjgahwz46P0u05B/B5EqHdZ+XIWD
mbA4CD/pXvk1B+TJYm5Xf6dQlfe6yJvmjqIBxdZmv3lh8zwc4bmCXF2gw+nYSL0Z
ohEUGW6yhhtoPkg3Goi3XZZenMfvJ2II4pEZXNLxId26F0KCl3GBUzGpn/Z9Yr9y
4aOTHcyKJloJONDO1w2AFrR4pTqHTI2KpdVGl/IsELm8VCLAAVBpQ570su9t+Oza
8eOx79+Rj1QqCyXBJhnEUhAFZdWCEOrCMc0u
-----END CERTIFICATE-----

-----BEGIN CERTIFICATE-----
MIIGFzCCA/+gAwIBAgIUftbnnMmtgcTIGT75XUQodw40ExcwDQYJKoZIhvcNAQEL
BQAwSDELMAkGA1UEBhMCQk0xGTAXBgNVBAoTEFF1b1ZhZGlzIExpbWl0ZWQxHjAc
BgNVBAMTFVF1b1ZhZGlzIFJvb3QgQ0EgMiBHMzAeFw0xMjExMDYxNDUwMThaFw0y
MjExMDYxNDUwMThaME0xCzAJBgNVBAYTAkJNMRkwFwYDVQQKExBRdW9WYWRpcyBM
aW1pdGVkMSMwIQYDVQQDExpRdW9WYWRpcyBHbG9iYWwgU1NMIElDQSBHMzCCAiIw
DQYJKoZIhvcNAQEBBQADggIPADCCAgoCggIBANf8Od17be6c6lTGJDhEXpmkTs4y
Q39Rr5VJyBeWCg06nSS71s6xF3sZvKcV0MbXlXCYM2ZX7cNTbJ81gs7uDsKFp+vK
EymiKyEiI2SImOtECNnSg+RVR4np/xz/UlC0yFUisH75cZsJ8T1pkGMfiEouR0EM
7O0uFgoboRfUP582TTWy0F7ynSA6YfGKnKj0OFwZJmGHVkLs1VevWjhj3R1fsPan
H05P5moePFnpQdj1FofoSxUHZ0c7VB+sUimboHm/uHNY1LOsk77qiSuVC5/yrdg3
2EEfP/mxJYT4r/5UiD7VahySzeZHzZ2OibQm2AfgfMN3l57lCM3/WPQBhMAPS1jz
kE+7MjajM2f0aZctimW4Hasrj8AQnfAdHqZehbhtXaAlffNEzCdpNK584oCTVR7N
UR9iZFx83ruTqpo+GcLP/iSYqhM4g7fy45sNhU+IS+ca03zbxTl3TTlkofXunI5B
xxE30eGSQpDZ5+iUJcEOAuVKrlYocFbB3KF45hwcbzPWQ1DcO2jFAapOtQzeS+MZ
yZzT2YseJ8hQHKu8YrXZWwKaNfyl8kFkHUBDICowNEoZvBwRCQp8sgqL6YRZy0uD
JGxmnC2e0BVKSjcIvmq/CRWH7yiTk9eWm73xrsg9iIyD/kwJEnLyIk8tR5V8p/hc
1H2AjDrZH12PsZ45AgMBAAGjgfMwgfAwEgYDVR0TAQH/BAgwBgEB/wIBATARBgNV
HSAECjAIMAYGBFUdIAAwOgYIKwYBBQUHAQEELjAsMCoGCCsGAQUFBzABhh5odHRw
Oi8vb2NzcC5xdW92YWRpc2dsb2JhbC5jb20wDgYDVR0PAQH/BAQDAgEGMB8GA1Ud
IwQYMBaAFO3nb3Zav2DsSVvGpXe7chZxm8Q9MDsGA1UdHwQ0MDIwMKAuoCyGKmh0
dHA6Ly9jcmwucXVvdmFkaXNnbG9iYWwuY29tL3F2cmNhMmczLmNybDAdBgNVHQ4E
FgQUsxKJtalLNbwVAPCA6dh4h/ETfHYwDQYJKoZIhvcNAQELBQADggIBAFGm1Fqp
RMiKr7a6h707M+km36PVXZnX1NZocCn36MrfRvphotbOCDm+GmRkar9ZMGhc8c/A
Vn7JSCjwF9jNOFIOUyNLq0w4luk+Pt2YFDbgF8IDdx53xIo8Gv05e9xpTvQYaIto
qeHbQjGXfSGc91olfX6JUwZlxxbhdJH+rxTFAg0jcbqToJoScWTfXSr1QRcNbSTs
Y4CPG6oULsnhVvrzgldGSK+DxFi2OKcDsOKkV7W4IGg8Do2L/M588AfBnV8ERzpl
qgMBBQxC2+0N6RdFHbmZt0HQE/NIg1s0xcjGx1XW3YTOfje31rmAXKHOehm4Bu48
gr8gePq5cdQ2W9tA0Dnytb9wzH2SyPPIXRI7yNxaX9H8wYeDeeiKSSmQtfh1v5cV
7RXvm8F6hLJkkco/HOW3dAUwZFcKsUH+1eUJKLN18eDGwB8yGawjHvOKqcfg5Lf/
TvC7hgcx7pDYaCCaqHaekgUwXbB2Enzqr1fdwoU1c01W5YuQAtAx5wk1bf34Yq/J
ph7wNXGvo88N0/EfP9AdVGmJzy7VuRXeVAOyjKAIeADMlwpjBRhcbs9m3dkqvoMb
SXKJxv/hFmNgEOvOlaFsXX1dbKg1v+C1AzKAFdiuAIa62JzASiEhigqNSdqdTsOh
8W8hdONuKKpe9zKedhBFAvuxhDgKmnySglYc
-----END CERTIFICATE-----

-----BEGIN CERTIFICATE-----
MIIFYDCCA0igAwIBAgIURFc0JFuBiZs18s64KztbpybwdSgwDQYJKoZIhvcNAQEL
BQAwSDELMAkGA1UEBhMCQk0xGTAXBgNVBAoTEFF1b1ZhZGlzIExpbWl0ZWQxHjAc
BgNVBAMTFVF1b1ZhZGlzIFJvb3QgQ0EgMiBHMzAeFw0xMjAxMTIxODU5MzJaFw00
MjAxMTIxODU5MzJaMEgxCzAJBgNVBAYTAkJNMRkwFwYDVQQKExBRdW9WYWRpcyBM
aW1pdGVkMR4wHAYDVQQDExVRdW9WYWRpcyBSb290IENBIDIgRzMwggIiMA0GCSqG
SIb3DQEBAQUAA4ICDwAwggIKAoICAQChriWyARjcV4g/Ruv5r+LrI3HimtFhZiFf
qq8nUeVuGxbULX1QsFN3vXg6YOJkApt8hpvWGo6t/x8Vf9WVHhLL5hSEBMHfNrMW
n4rjyduYNM7YMxcoRvynyfDStNVNCXJJ+fKH46nafaF9a7I6JaltUkSs+L5u+9ym
c5GQYaYDFCDy54ejiK2toIz/pgslUiXnFgHVy7g1gQyjO/Dh4fxaXc6AcW34Sas+
O7q414AB+6XrW7PFXmAqMaCvN+ggOp+oMiwMzAkd056OXbxMmO7FGmh77FOm6RQ1
o9/NgJ8MSPsc9PG/Srj61YxxSscfrf5BmrODXfKEVu+lV0POKa2Mq1W/xPtbAd0j
IaFYAI7D0GoT7RPjEiuA3GfmlbLNHiJuKvhB1PLKFAeNilUSxmn1uIZoL1NesNKq
IcGY5jDjZ1XHm26sGahVpkUG0CM62+tlXSoREfA7T8pt9DTEceT/AFr2XK4jYIVz
8eQQsSWu1ZK7E8EM4DnatDlXtas1qnIhO4M15zHfeiFuuDIIfR0ykRVKYnLP43eh
vNURG3YBZwjgQQvD6xVu+KQZ2aKrr+InUlYrAoosFCT5v0ICvybIxo/gbjh9Uy3l
7ZizlWNof/k19N+IxWA1ksB8aRxhlRbQ694Lrz4EEEVlWFA4r0jyWbYW8jwNkALG
cC4BrTwV1wIDAQABo0IwQDAPBgNVHRMBAf8EBTADAQH/MA4GA1UdDwEB/wQEAwIB
BjAdBgNVHQ4EFgQU7edvdlq/YOxJW8ald7tyFnGbxD0wDQYJKoZIhvcNAQELBQAD
ggIBAJHfgD9DCX5xwvfrs4iP4VGyvD11+ShdyLyZm3tdquXK4Qr36LLTn91nMX66
AarHakE7kNQIXLJgapDwyM4DYvmL7ftuKtwGTTwpD4kWilhMSA/ohGHqPHKmd+RC
roijQ1h5fq7KpVMNqT1wvSAZYaRsOPxDMuHBR//47PERIjKWnML2W2mWeyAMQ0Ga
W/ZZGYjeVYg3UQt4XAoeo0L9x52ID8DyeAIkVJOviYeIyUqAHerQbj5hLja7NQ4n
lv1mNDthcnPxFlxHBlRJAHpYErAK74X9sbgzdWqTHBLmYF5vHX/JHyPLhGGfHoJE
+V+tYlUkmlKY7VHnoX6XOuYvHxHaU4AshZ6rNRDbIl9qxV6XU/IyAgkwo1jwDQHV
csaxfGl7w/U2Rcxhbl5MlMVerugOXou/983g7aEOGzPuVBj+D77vfoRrQ+NwmNtd
dbINWQeFFSM51vHfqSYP1kjHs6Yi9TM3WpVHn3u6GBVv/9YUZINJ0gpnIdsPNWNg
KCLjsZWDzYWm3S8P52dSbrsvhXz1SnPnxT7AvSESBT/8twNJAlvIJebiVDj1eYeM
HVOyToV7BjjHLPj4sHKNJeV3UvQDHEimUF+IIDBu8oJDqz2XhOdT+yHBTw8imoa4
WSr2Rz0ZiC3oheGe7IUIarFsNMkd7EgrO3jtZsSOeWmD3n+M
-----END CERTIFICATE-----

-----BEGIN CERTIFICATE-----
MIIF+TCCA+GgAwIBAgIRALD/zzodgkSYFWKdZIhqQWUwDQYJKoZIhvcNAQEMBQAw
gYgxCzAJBgNVBAYTAlVTMRMwEQYDVQQIEwpOZXcgSmVyc2V5MRQwEgYDVQQHEwtK
ZXJzZXkgQ2l0eTEeMBwGA1UEChMVVGhlIFVTRVJUUlVTVCBOZXR3b3JrMS4wLAYD
VQQDEyVVU0VSVHJ1c3QgUlNBIENlcnRpZmljYXRpb24gQXV0aG9yaXR5MB4XDTE0
MTAwOTAwMDAwMFoXDTI0MTAwODIzNTk1OVowZDELMAkGA1UEBhMCTkwxFjAUBgNV
BAgTDU5vb3JkLUhvbGxhbmQxEjAQBgNVBAcTCUFtc3RlcmRhbTEPMA0GA1UEChMG
VEVSRU5BMRgwFgYDVQQDEw9URVJFTkEgU1NMIENBIDIwggEiMA0GCSqGSIb3DQEB
AQUAA4IBDwAwggEKAoIBAQCwOm1/qbgAnvOFOghkLPlEDCC0sxVNBi2m8JPJSL73
ZK2kjhWzMYEUF/xu4osZdYs2Es8HbXZ4Jl4nvywWukL73R5Qj2SvdZsKOoKpMSVR
jn/EQt0fXJORu5T6cFf65/24uGjKm2oZJFQ3/jJhifciwY9j1dFpfklNvNfQ20zW
9g+9wYhCk9aR+Z+WmRHqbnLngCFs8U6O7GO4Pa9lOdCFkip5Og7W6K2bJYmi1C5y
a3Oh0uLfzlhw/8BUAXdd+XadL0PaoibdHUKaTTixVv46tMtrbPJqnz+zrjun0BU+
rCd/G/RZYFBWfp11JZ4/xna//5nM2PGpaolf3ucHzY2LAgMBAAGjggF/MIIBezAf
BgNVHSMEGDAWgBRTeb9aqitKz1SA4dibwJ3ysgNmyzAdBgNVHQ4EFgQUW9CKHJoy
W+C13ZZUG+GGKLD9tr0wDgYDVR0PAQH/BAQDAgGGMBIGA1UdEwEB/wQIMAYBAf8C
AQAwHQYDVR0lBBYwFAYIKwYBBQUHAwEGCCsGAQUFBwMCMCwGA1UdIAQlMCMwDQYL
KwYBBAGyMQECAh0wCAYGZ4EMAQIBMAgGBmeBDAECAjBQBgNVHR8ESTBHMEWgQ6BB
hj9odHRwOi8vY3JsLnVzZXJ0cnVzdC5jb20vVVNFUlRydXN0UlNBQ2VydGlmaWNh
dGlvbkF1dGhvcml0eS5jcmwwdgYIKwYBBQUHAQEEajBoMD8GCCsGAQUFBzAChjNo
dHRwOi8vY3J0LnVzZXJ0cnVzdC5jb20vVVNFUlRydXN0UlNBQWRkVHJ1c3RDQS5j
cnQwJQYIKwYBBQUHMAGGGWh0dHA6Ly9vY3NwLnVzZXJ0cnVzdC5jb20wDQYJKoZI
hvcNAQEMBQADggIBAH2QaWZWVBxrPK5/JQgT6btkbPVniC+9wVEKrtNj9i3bcDEJ
AH4di9rkMyGY4CGT28COJY5VBswqZeMD6FlyJ643mph8wvQTWhJxLW2r3zJpgacG
oosgHaiQ0iiqYdT2/6W/hoCOZ5EqIn4dlC0aYbsgIZCJ6NUKEQr2CLpeG8tsKIU+
xRYPZf230bFhwaYl2Ia/Dvqb+tH1IqdnuBUu+Qitt3UCOfQpYfm/wKoX60LeJo+d
ZWQyB95sPTLTA+xH1XRpIDp+uHDvqaIqnFVCtuM+i9j/Jlr7fCZsiIWG15M+UPhE
h9RQ0R1DMDK60rqNIQjK9+7Gbs6SWQgcU3N0j5z4160avk1G7qzEuYHrp1DMHWb8
Dg1+Bh24DtN+u5qHrgu2m4QEzsGgexbfArIYQ62ruSYJq6oEHVA37iq9IkGKALXc
n8MF1OaCTGfaKwL1ZaxZKbt6DE5Ut9I7fQM7IGTGxehQKpKwX6BHl3JYX8EKb5/1
PQnV5whodZLi1biej76NGztDjPNO1VSrdu3MUH8ume20tUn643V9ixFoDdU6+l1Q
sCuBA3gstNuPv0xAW5KjohoKQV2sV/puV070B1XrYwgykwAkSl2dwsFSKJPByCQa
ppP7zX0/pnO8z2ideWMu5yUrQjg2sQtWwopf965KMdnfagbNL6OYCbwFgBPH
-----END CERTIFICATE-----

-----BEGIN CERTIFICATE-----
MIIFdzCCBF+gAwIBAgIQE+oocFv07O0MNmMJgGFDNjANBgkqhkiG9w0BAQwFADBv
MQswCQYDVQQGEwJTRTEUMBIGA1UEChMLQWRkVHJ1c3QgQUIxJjAkBgNVBAsTHUFk
ZFRydXN0IEV4dGVybmFsIFRUUCBOZXR3b3JrMSIwIAYDVQQDExlBZGRUcnVzdCBF
eHRlcm5hbCBDQSBSb290MB4XDTAwMDUzMDEwNDgzOFoXDTIwMDUzMDEwNDgzOFow
gYgxCzAJBgNVBAYTAlVTMRMwEQYDVQQIEwpOZXcgSmVyc2V5MRQwEgYDVQQHEwtK
ZXJzZXkgQ2l0eTEeMBwGA1UEChMVVGhlIFVTRVJUUlVTVCBOZXR3b3JrMS4wLAYD
VQQDEyVVU0VSVHJ1c3QgUlNBIENlcnRpZmljYXRpb24gQXV0aG9yaXR5MIICIjAN
BgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAgBJlFzYOw9sIs9CsVw127c0n00yt
UINh4qogTQktZAnczomfzD2p7PbPwdzx07HWezcoEStH2jnGvDoZtF+mvX2do2NC
tnbyqTsrkfjib9DsFiCQCT7i6HTJGLSR1GJk23+jBvGIGGqQIjy8/hPwhxR79uQf
jtTkUcYRZ0YIUcuGFFQ/vDP+fmyc/xadGL1RjjWmp2bIcmfbIWax1Jt4A8BQOujM
8Ny8nkz+rwWWNR9XWrf/zvk9tyy29lTdyOcSOk2uTIq3XJq0tyA9yn8iNK5+O2hm
AUTnAU5GU5szYPeUvlM3kHND8zLDU+/bqv50TmnHa4xgk97Exwzf4TKuzJM7UXiV
Z4vuPVb+DNBpDxsP8yUmazNt925H+nND5X4OpWaxKXwyhGNVicQNwZNUMBkTrNN9
N6frXTpsNVzbQdcS2qlJC9/YgIoJk2KOtWbPJYjNhLixP6Q5D9kCnusSTJV882sF
qV4Wg8y4Z+LoE53MW4LTTLPtW//e5XOsIzstAL81VXQJSdhJWBp/kjbmUZIO8yZ9
HE0XvMnsQybQv0FfQKlERPSZ51eHnlAfV1SoPv10Yy+xUGUJ5lhCLkMaTLTwJUdZ
+gQek9QmRkpQgbLevni3/GcV4clXhB4PY9bpYrrWX1Uu6lzGKAgEJTm4Diup8kyX
HAc/DVL17e8vgg8CAwEAAaOB9DCB8TAfBgNVHSMEGDAWgBStvZh6NLQm9/rEJlTv
A73gJMtUGjAdBgNVHQ4EFgQUU3m/WqorSs9UgOHYm8Cd8rIDZsswDgYDVR0PAQH/
BAQDAgGGMA8GA1UdEwEB/wQFMAMBAf8wEQYDVR0gBAowCDAGBgRVHSAAMEQGA1Ud
HwQ9MDswOaA3oDWGM2h0dHA6Ly9jcmwudXNlcnRydXN0LmNvbS9BZGRUcnVzdEV4
dGVybmFsQ0FSb290LmNybDA1BggrBgEFBQcBAQQpMCcwJQYIKwYBBQUHMAGGGWh0
dHA6Ly9vY3NwLnVzZXJ0cnVzdC5jb20wDQYJKoZIhvcNAQEMBQADggEBAJNl9jeD
lQ9ew4IcH9Z35zyKwKoJ8OkLJvHgwmp1ocd5yblSYMgpEg7wrQPWCcR23+WmgZWn
RtqCV6mVksW2jwMibDN3wXsyF24HzloUQToFJBv2FAY7qCUkDrvMKnXduXBBP3zQ
YzYhBx9G/2CkkeFnvN4ffhkUyWNnkepnB2u0j4vAbkN9w6GAbLIevFOFfdyQoaS8
Le9Gclc1Bb+7RrtubTeZtv8jkpHGbkD4jylW6l/VXxRTrPBPYer3IsynVgviuDQf
Jtl7GQVoP7o81DgGotPmjw7jtHFtQELFhLRAlSv0ZaBIefYdgWOWnU914Ph85I6p
0fKtirOMxyHNwu8=
-----END CERTIFICATE-----

-----BEGIN CERTIFICATE-----
MIIENjCCAx6gAwIBAgIBATANBgkqhkiG9w0BAQUFADBvMQswCQYDVQQGEwJTRTEU
MBIGA1UEChMLQWRkVHJ1c3QgQUIxJjAkBgNVBAsTHUFkZFRydXN0IEV4dGVybmFs
IFRUUCBOZXR3b3JrMSIwIAYDVQQDExlBZGRUcnVzdCBFeHRlcm5hbCBDQSBSb290
MB4XDTAwMDUzMDEwNDgzOFoXDTIwMDUzMDEwNDgzOFowbzELMAkGA1UEBhMCU0Ux
FDASBgNVBAoTC0FkZFRydXN0IEFCMSYwJAYDVQQLEx1BZGRUcnVzdCBFeHRlcm5h
bCBUVFAgTmV0d29yazEiMCAGA1UEAxMZQWRkVHJ1c3QgRXh0ZXJuYWwgQ0EgUm9v
dDCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALf3GjPm8gAELTngTlvt
H7xsD821+iO2zt6bETOXpClMfZOfvUq8k+0DGuOPz+VtUFrWlymUWoCwSXrbLpX9
uMq/NzgtHj6RQa1wVsfwTz/oMp50ysiQVOnGXw94nZpAPA6sYapeFI+eh6FqUNzX
mk6vBbOmcZSccbNQYArHE504B4YCqOmoaSYYkKtMsE8jqzpPhNjfzp/haW+710LX
a0Tkx63ubUFfclpxCDezeWWkWaCUN/cALw3CknLa0Dhy2xSoRcRdKn23tNbE7qzN
E0S3ySvdQwAl+mG5aWpYIxG3pzOPVnVZ9c0p10a3CitlttNCbxWyuHv77+ldU9U0
WicCAwEAAaOB3DCB2TAdBgNVHQ4EFgQUrb2YejS0Jvf6xCZU7wO94CTLVBowCwYD
VR0PBAQDAgEGMA8GA1UdEwEB/wQFMAMBAf8wgZkGA1UdIwSBkTCBjoAUrb2YejS0
Jvf6xCZU7wO94CTLVBqhc6RxMG8xCzAJBgNVBAYTAlNFMRQwEgYDVQQKEwtBZGRU
cnVzdCBBQjEmMCQGA1UECxMdQWRkVHJ1c3QgRXh0ZXJuYWwgVFRQIE5ldHdvcmsx
IjAgBgNVBAMTGUFkZFRydXN0IEV4dGVybmFsIENBIFJvb3SCAQEwDQYJKoZIhvcN
AQEFBQADggEBALCb4IUlwtYj4g+WBpKdQZic2YR5gdkeWxQHIzZlj7DYd7usQWxH
YINRsPkyPef89iYTx4AWpb9a/IfPeHmJIZriTAcKhjW88t5RxNKWt9x+Tu5w/Rw5
6wwCURQtjr0W4MHfRnXnJK3s9EK0hZNwEGe6nQY1ShjTK3rMUUKhemPR5ruhxSvC
Nr4TDea9Y355e6cJDUCrat2PisP29owaQgVR1EX1n6diIWgVIEM8med8vSTYqZEX
c4g/VhsxOBi0cQ+azcgOno4uG+GMmIPLHzHxREzGBHNJdmAPx/i9F4BrLunMTA5a
mnkPIAou1Z5jJh5VkpTYghdae9C8x49OhgQ=
-----END CERTIFICATE-----

" > $HOME/.cat_installer/ca.pem
function run_python_script {
PASSWORD=$( echo "$PASSWORD" | sed "s/'/\\\'/g" )
if python << EEE1 > /dev/null 2>&1
import dbus
EEE1
then
    PYTHON=python
elif python3 << EEE2 > /dev/null 2>&1
import dbus
EEE2
then
    PYTHON=python3
else
    PYTHON=none
    return 1
fi

$PYTHON << EOF > /dev/null 2>&1
#-*- coding: utf-8 -*-
import dbus
import re
import sys
import uuid
import os

class EduroamNMConfigTool:

    def connect_to_NM(self):
        #connect to DBus
        try:
            self.bus = dbus.SystemBus()
        except dbus.exceptions.DBusException:
            print("Can't connect to DBus")
            sys.exit(2)
        #main service name
        self.system_service_name = "org.freedesktop.NetworkManager"
        #check NM version
        self.check_nm_version()
        if self.nm_version == "0.9" or self.nm_version == "1.0":
            self.settings_service_name = self.system_service_name
            self.connection_interface_name = "org.freedesktop.NetworkManager.Settings.Connection"
            #settings proxy
            sysproxy = self.bus.get_object(self.settings_service_name, "/org/freedesktop/NetworkManager/Settings")
            #settings intrface
            self.settings = dbus.Interface(sysproxy, "org.freedesktop.NetworkManager.Settings")
        elif self.nm_version == "0.8":
            #self.settings_service_name = "org.freedesktop.NetworkManagerUserSettings"
            self.settings_service_name = "org.freedesktop.NetworkManager"
            self.connection_interface_name = "org.freedesktop.NetworkManagerSettings.Connection"
            #settings proxy
            sysproxy = self.bus.get_object(self.settings_service_name, "/org/freedesktop/NetworkManagerSettings")
            #settings intrface
            self.settings = dbus.Interface(sysproxy, "org.freedesktop.NetworkManagerSettings")
        else:
            print("This Network Manager version is not supported")
            sys.exit(2)

    def check_opts(self):
        self.cacert_file = '${HOME}/.cat_installer/ca.pem'
        self.pfx_file = '${HOME}/.cat_installer/user.p12'
        if not os.path.isfile(self.cacert_file):
            print("Certificate file not found, looks like a CAT error")
            sys.exit(2)

    def check_nm_version(self):
        try:
            proxy = self.bus.get_object(self.system_service_name, "/org/freedesktop/NetworkManager")
            props = dbus.Interface(proxy, "org.freedesktop.DBus.Properties")
            version = props.Get("org.freedesktop.NetworkManager", "Version")
        except dbus.exceptions.DBusException:
            version = "0.8"
        if re.match(r'^1\.', version):
            self.nm_version = "1.0"
            return
        if re.match(r'^0\.9', version):
            self.nm_version = "0.9"
            return
        if re.match(r'^0\.8', version):
            self.nm_version = "0.8"
            return
        else:
            self.nm_version = "Unknown version"
            return

    def byte_to_string(self, barray):
        return "".join([chr(x) for x in barray])


    def delete_existing_connections(self, ssid):
        "checks and deletes earlier connections"
        try:
            conns = self.settings.ListConnections()
        except dbus.exceptions.DBusException:
            print("DBus connection problem, a sudo might help")
            exit(3)
        for each in conns:
            con_proxy = self.bus.get_object(self.system_service_name, each)
            connection = dbus.Interface(con_proxy, "org.freedesktop.NetworkManager.Settings.Connection")
            try:
               connection_settings = connection.GetSettings()
               if connection_settings['connection']['type'] == '802-11-wireless':
                   conn_ssid = self.byte_to_string(connection_settings['802-11-wireless']['ssid'])
                   if conn_ssid == ssid:
                       connection.Delete()
            except dbus.exceptions.DBusException:
               pass

    def add_connection(self,ssid):
        server_alt_subject_name_list = dbus.Array({'DNS:ils025.uopnet.plymouth.ac.uk','DNS:ils024.uopnet.plymouth.ac.uk'})
        server_name = 'uopnet.plymouth.ac.uk'
        if self.nm_version == "0.9" or self.nm_version == "1.0":
             match_key = 'altsubject-matches'
             match_value = server_alt_subject_name_list
        else:
             match_key = 'subject-match'
             match_value = server_name
            
        s_con = dbus.Dictionary({
            'type': '802-11-wireless',
            'uuid': str(uuid.uuid4()),
            'permissions': ['user:$USER'],
            'id': ssid 
        })
        s_wifi = dbus.Dictionary({
            'ssid': dbus.ByteArray(ssid.encode('utf8')),
            'security': '802-11-wireless-security'
        })
        s_wsec = dbus.Dictionary({
            'key-mgmt': 'wpa-eap',
            'proto': ['rsn',],
            'pairwise': ['ccmp',],
            'group': ['ccmp', 'tkip']
        })
        s_8021x = dbus.Dictionary({
            'eap': ['peap'],
            'identity': '$USER_NAME',
            'ca-cert': dbus.ByteArray("file://{0}\0".format(self.cacert_file).encode('utf8')),
             match_key: match_value,
            'password': '$PASSWORD',
            'phase2-auth': 'mschapv2',
        })
        s_ip4 = dbus.Dictionary({'method': 'auto'})
        s_ip6 = dbus.Dictionary({'method': 'auto'})
        con = dbus.Dictionary({
            'connection': s_con,
            '802-11-wireless': s_wifi,
            '802-11-wireless-security': s_wsec,
            '802-1x': s_8021x,
            'ipv4': s_ip4,
            'ipv6': s_ip6
        })
        self.settings.AddConnection(con)

    def main(self):
        self.check_opts()
        ver = self.connect_to_NM()
        self.delete_existing_connections('eduroam')
        self.add_connection('eduroam')

if __name__ == "__main__":
    ENMCT = EduroamNMConfigTool()
    ENMCT.main()
EOF
}
function create_wpa_conf {
cat << EOFW >> $HOME/.cat_installer/cat_installer.conf

network={
  ssid="eduroam"
  key_mgmt=WPA-EAP
  pairwise=CCMP
  group=CCMP TKIP
  eap=PEAP
  ca_cert="${HOME}/.cat_installer/ca.pem"
  identity="${USER_NAME}"
  domain_suffix_match="uopnet.plymouth.ac.uk"
  phase2="auth=MSCHAPV2"
  password="${PASSWORD}"
}
EOFW
chmod 600 $HOME/.cat_installer/cat_installer.conf
}
#prompt user for credentials
  user_cred
  if run_python_script ; then
   show_info "Installation successful"
else
   show_info "Network Manager configuration failed, generating wpa_supplicant.conf"
   if ! ask "Network Manager configuration failed, but we may generate a wpa_supplicant configuration file if you wish. Be warned that your connection password will be saved in this file as clear text." "Write the file" 1 ; then exit ; fi

if [ -f $HOME/.cat_installer/cat_installer.conf ] ; then
  if ! ask "File $HOME/.cat_installer/cat_installer.conf exists; it will be overwritten." "Continue" 1 ; then confirm_exit; fi
  rm $HOME/.cat_installer/cat_installer.conf
  fi
   create_wpa_conf
   show_info "Output written to $HOME/.cat_installer/cat_installer.conf"
fi
