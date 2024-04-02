#!/usr/bin/env python3

# *********************************************** #

# *** TARIK VARDAR tarafından hazırlanmıştır. *** #

# tarikvardar@gmail.com
# github.com/tvardar



#    GPL V.3 LİSANSINA GÖRE KULLANILABİLİR
#    Mümkün oluğunca çok açıklama eklenmiştir.
#    Pardus Linux için hazırlanmıştır. Gnome - Xfce - Kde desteklemektedir.
#    Program her hangi bir sorumluluk kabul etmemektedir.

# *********************************************** #






# GEREKLI KUTUPHANELERI ICE AKTARIYORUZ #
# ------------------------------------- #

import sys
import os
from PyQt5.QtWidgets import *
from AnaSayfaUI import *
import subprocess
import socket
import requests
import psutil


#----------------------UYGULAMA OLUŞTUR-------------------#
#---------------------------------------------------------#
Uygulama=QApplication(sys.argv)
penAna=QMainWindow()
ui=Ui_MainWindow()
ui.setupUi(penAna)
penAna.show()




# ************************************************************************* #
# *** **** *** **** SİSTEM VE AĞ BİLGİLERİ SEKMESİ BÖLÜMÜ **** *** **** *** #
# ************************************************************************* #




# ---- SİSTEM BİLGİLERİ BÖLÜMÜ ---- #
# --------------------------------- #
def sistem ():
    sistem = os.name
    sistem_tur = [sistem]
    if sistem_tur [0]== ("posix"):

        # uname -a çıktısını alıyoruz
        uname_info = os.uname()

        # Ayrı ayrı bilgilere erişim
        system = uname_info.sysname
        node = uname_info.nodename
        release = uname_info.release
        #version = uname_info.version
        #machine = uname_info.machine
        ui.lblSistem.setText(system)
        ui.lblPcadi.setText(node)
        ui.lblKernel.setText(release)

    else:
        ui.lblSistem.setText("Program Linux Debian Sürümleri için hazırlanmıştır")


# ---- INTERNET BAGLANTISI BÖLÜMÜ ---- #
# ------------------------------------ #

# a) Bir def (fonksiyon) icerisinde internet baglantimiz kontrol edecegiz.
# b) Baglanti var ise Yerel IP, Harici IP, Konum ve Wifi Sifre bilgilerini alacagiz
# c) Baglanti yoksa ilgili bolumlerde "Internet Baglantiniz Yok !!" uyarısı verecegiz.

def internet_baglanti():
    try:
        # Bir web sitesine GET isteği göndererek internet bağlantısını kontrol ediyoruz
        response = requests.get("http://www.google.com", timeout=5)
        return True # HTTP başarılı bir şekilde dönerse, internet bağlantısı olduğunu anlıyoruz.
    except requests.ConnectionError:
        return False # Baglanti hatasi var ise Internet baglantisinin olmadigini anliyoruz.


# Baglanti var ise, OpenDns 'ten aldıgimiz Harici Ip bilgimizi degiskene atiyoruz
if internet_baglanti():
    Harici_Ip = "dig +short myip.opendns.com @resolver1.opendns.com"
    ip= subprocess.getoutput(Harici_Ip)

    # OpenDns iceriginden ulke, sehir ve servis saglayici bilgilerimizi ayiriyoruz.
    # Gelen verilerden bolge, zaman dilimi, posta kodu ve koordinat verilerini almadim.
    # Bilgi icin satir icinde durmakta, kullanmak isteyenler yorum isareti olan # kaldirip kullanabilir.

    country = requests.get("https://ipinfo.io/{}/country/".format(
        ip)).text  # ! {} kullanarak ip adresini yazdırıp hedeften .text fonksiyonu ile yazıyı çekiyoruz.
    city = requests.get("https://ipinfo.io/{}/city/".format(ip)).text  # ! Aynı işlemleri uyguluyoruz.
    #region = requests.get("https://ipinfo.io/{}/region/".format(ip)).text
    #postal = requests.get("https://ipinfo.io/{}/postal/".format(ip)).text
    #timezone = requests.get("https://ipinfo.io/{}/timezone/".format(ip)).text
    orgination = requests.get("https://ipinfo.io/{}/org/".format(ip)).text
    #location = requests.get("https://ipinfo.io/{}/loc/".format(ip)).text

    # Baglanti varsa, line ve label alanlarina ip, ulke, sehir ve servis saglayiciyi yazdiriyoruz
    ui.lineip.setText(ip)
    ui.lblUlke.setText(country)
    ui.lblSehir.setText(city)
    ui.lblServissagla.setText(orgination)


    # Göster tıklanınca Harici ip'yi göstersin. Tıklanmazsa Yıldızlı kalsın
    def goster():
        if ui.lineip.echoMode() == QLineEdit.Password:
            ui.lineip.setEchoMode(QLineEdit.Normal)
            ui.lineip.setText(ip)
        else:
            ui.lineip.setEchoMode(QLineEdit.Password)

    # Butona tiklandiginda calismasi icin, goster fonksiyonu baglantisini yaptik.
    ui.btngoster.clicked.connect(goster)

    # Bu kisimda baglanti yoksa, line ve label iclerine kırmızı olarak baglanti yok yazacak.
else:
    ui.lblUlke.setText('<font color="red">İnternete Bağlı Değilsiniz !!</font>')
    ui.lblSehir.setText('<font color="red">İnternete Bağlı Değilsiniz !!</font>')
    ui.lblServissagla.setText('<font color="red">İnternete Bağlı Değilsiniz !!</font>')



# ---- WI-FI SIFRESI BOLUMU ---- #
# ------------------------------ #

# Sifre adinda bir fonksiyon tanımlayıp, Subprocess modulu ile nmcli üzerindeki verileri aliyoruz.
def wifisifre ():
    if internet_baglanti():
        wsifre = subprocess.check_output(['nmcli', 'device', 'wifi', 'show-password'])
        wsifre = wsifre.decode('utf-8')  # Çıktıyı UTF-8 formatına çevir

        lines = wsifre.split('\n') # Çıktıyı satırlara ayır

        # For döngüsü ile verileri geziyoruz ve,
        for line in lines:
            # 'Parola' ifadelerini içeren satırı bulup,
            if 'Parola' in line:
                Parola = line.split(':', 1)[1] # : İşaretinden itibaren içerikleri böldük.
                password = Parola.strip()  # Boşlukları temizle

        def gosterwifi():
            if ui.linewifi.echoMode() == QLineEdit.Password:
                ui.linewifi.setEchoMode(QLineEdit.Normal)
                ui.linewifi.setText(password)
            else:
                ui.linewifi.setEchoMode(QLineEdit.Password)

        ui.btngoster2.clicked.connect(gosterwifi)
    else:
        pass


# ---- DAĞITIM BİLGİLERİ BÖLÜMÜ ---- #
# ---------------------------------- #
def dagitim ():
    # Komutu çalıştırarak çıktıyı alıyoruz
    gdagitim = subprocess.check_output(['lsb_release', '-d']).decode('utf-8')

    # Çıktıyı satır bazında böleriz
    cikti = gdagitim.split('\n')

    # Bilgileri depolamak için bir sözlük oluşturuyoruz
    icerik = {}

    # Her satırı işleyerek anahtar-değer çiftlerini sözlüğe ekliyoruz
    for i in cikti:
        if ':' in i:
            key, value = i.split(':', 1)
            icerik[key.strip()] = value.strip()

    # Bilgileri yazdırma
    for key, value in icerik.items():
        ui.lblDagitim.setText(value)



# ---- KULLANICI BİLGİLERİ BÖLÜMÜ ---- #
# ------------------------------------ #

def kullanici():
    kullaniciadi1 = "whoami"
    kullaniciadi2 = subprocess.getoutput(kullaniciadi1)
    ui.lblKullanici.setText(kullaniciadi2)


# ---- YEREL IP (Modem) BİLGİLERİ BÖLÜMÜ ---- #
# ------------------------------------------- #

def yerelip ():
    Yerel_Ip1 = "hostname -I"
    Yerel_Ip2 = subprocess.getoutput(Yerel_Ip1)
    ui.lblYerelip.setText(Yerel_Ip2)


# ---- LOCAL IP (Cihazımız) BİLGİLERİ BÖLÜMÜ ---- #
# ----------------------------------------------- #

def localhost ():
    Localhost = (socket.gethostbyname(socket.gethostname()))
    ui.lblLocalhost.setText(Localhost)









# ******************************************************************** #
# *** **** *** **** DONANIM BİLGİLERİ SEKMESİ BÖLÜMÜ **** *** **** *** #
# ******************************************************************** #



# ---- İŞLEMCİ BİLGİLERİ BÖLÜMÜ ---- #
# ---------------------------------- #

def islemci():
    try:
        # lscpu komutunu çağırarak işlemci bilgilerini al
        lscpu_output = subprocess.check_output(['lscpu']).decode('utf-8')
        lines = lscpu_output.split('\n')

        # İstenen verileri al
        model_name = None
        architecture = None
        cpu_mhz = None

        for line in lines:
            if "Model name" in line:
                model_name = line.split(':')[1].strip()
            elif "Architecture" in line:
                architecture = line.split(':')[1].strip()
            elif "CPU MHz" in line:
                cpu_mhz = line.split(':')[1].strip()

        # Alınan verileri yazdır
            ui.lblIslemci.setText(model_name)

    except FileNotFoundError:
        ui.lblIslemci.setText("İşlemci bilgileri alınamadı. lscpu komutunun sisteminizde mevcut olduğundan emin olun.")




# ---- EKRAN KARTI BİLGİLERİ BÖLÜMÜ ---- #
# -------------------------------------- #


def ekrankarti():
    try:
        # lspci komutunu çağırarak ekran kartı bilgilerini al
        lspci_output = subprocess.check_output(['lspci']).decode('utf-8')

        # Sadece grafik kartı bilgilerini al
        gpu_info = [line.strip() for line in lspci_output.split('\n') if 'VGA compatible controller' in line]

        # Grafik kartı bilgilerini yazdır
        for info in gpu_info:
            kart = info.split(":")
            kartadi = kart [2]
            ui.lblekrankart.setText(kartadi)
    except FileNotFoundError:
        ui.lblekrankart.setText("Ekran kartı bilgileri alınamadı. lspci komutunun sisteminizde mevcut olduğundan emin olun.")



# ---- SES KARTI BİLGİLERİ BÖLÜMÜ ---- #
# ------------------------------------ #

def seskarti():
    try:
        output = subprocess.check_output(["lspci", "-v"]).decode("utf-8")

        # "Multimedia audio controller" satırını bul
        audio_controller_line = None

        for line in output.split("\n"):
            if "Multimedia audio controller" in line:
                audio_controller_line = line.strip()
                break

        # ":" işaretinden sonraki kısmı al
        if audio_controller_line:
            info_after_colon = audio_controller_line.split(":", 2)[-1].strip()
            ui.lblseskart.setText(info_after_colon)
        else:
            pass
    except FileNotFoundError:
        ui.lblseskart.setText("Ses kartı bilgileri alınamadı:")




# ---- RAM BİLGİLERİ BÖLÜMÜ ---- #
# ------------------------------ #

def ram ():
    toplamram = (psutil.virtual_memory().total)
    ui.lblRamtoplam.setText(str(toplamram))
    kullanilanram = (psutil.virtual_memory().used)
    ui.lblRamkullanilan.setText(str(kullanilanram))



# ---- HDD BİLGİLERİ BÖLÜMÜ ---- #
# ------------------------------ #

def hdd ():
    toplamhdd = (psutil.disk_usage('/').total)
    ui.lblHddtoplam.setText(str(toplamhdd))
    kullanilanhdd = (psutil.disk_usage('/').used)
    ui.lblHddkullanilan.setText(str(kullanilanhdd))






# ***************************************************************** #
# *** **** *** **** TEMEL İŞLEMLER SEKMESİ BÖLÜMÜ **** *** **** *** #
# ***************************************************************** #





# ---- SİSTEMİ GÜNCELLE (Masaüstü Kontrol) ---- #
# --------------------------------------------- #
def masaustu_kontrol():
    # Masaüstü ortamını kontrol etmek için çeşitli komutları çalıştır
    # Hangi masaüstü ortamının kullanıldığını belirlemek için sistem ortam değişkenlerini kontrol ederiz.
    desktop_session = os.environ.get("DESKTOP_SESSION")
    xdg_current_desktop = os.environ.get("XDG_CURRENT_DESKTOP")
    # Wayland kullanılıyorsa, diğer masaüstü ortamlarına bakmaya gerek yok.
    if os.getenv("XDG_SESSION_TYPE") == "wayland":
        return "wayland"
    elif desktop_session is not None and "xfce" in desktop_session.lower():
        return "xfce"
    elif xdg_current_desktop is not None and "xfce" in xdg_current_desktop.lower():
        return "xfce"
    elif desktop_session is not None and "gnome" in desktop_session.lower():
        return "gnome"
    elif xdg_current_desktop is not None and "gnome" in xdg_current_desktop.lower():
        return "gnome"
    elif desktop_session is not None and "kde" in desktop_session.lower():
        return "kde"
    elif xdg_current_desktop is not None and "kde" in xdg_current_desktop.lower():
        return "kde"
    else:
        return None


# ---- SİSTEMİ GÜNCELLE (Update & Upgrade) ---- #
# --------------------------------------------- #
def apt_update():
# Sudo apt update komutunu çalıştırmak için terminali aç
    masaustu = masaustu_kontrol()
    if masaustu == "xfce":
        subprocess.run(["xfce4-terminal", "--hold", "-e", "sudo apt update && sudo apt upgrade -y"])
    elif masaustu == "gnome":
        subprocess.run(["x-terminal-emulator", "-e", "sudo apt update && sudo apt upgrade -y"])
    elif masaustu == "kde":
        subprocess.run(["konsole", "-e", "sudo apt update && sudo apt upgrade -y"])
    else:
        print("Bilinmeyen masaüstü ortamı. Terminal açılamadı.")

ui.btnupdate.clicked.connect(apt_update)



# ---- SİSTEMİ TEMİZLE (Autoremove) ---- #
# -------------------------------------- #
def apt_autoremove():
    masaustu = masaustu_kontrol()
    if masaustu == "xfce":
        subprocess.run(["xfce4-terminal", "--hold", "-e", "sudo apt autoremove"])
    elif masaustu == "gnome":
        subprocess.run(["x-terminal-emulator", "-e", "sudo apt autoremove"])
    elif masaustu == "kde":
        subprocess.run(["konsole", "-e", "sudo apt autoremove"])
    else:
        print("Bilinmeyen masaüstü ortamı. Terminal açılamadı.")


ui.btnremove.clicked.connect(apt_autoremove)


# ---- PIP KURULUMU (Python Packet İnstaller ) ---- #
# ------------------------------------------------- #
def pip_install():
    masaustu = masaustu_kontrol()
    if masaustu == "xfce":
        subprocess.run(["xfce4-terminal", "--hold", "-e", "sudo apt-get install pyhton3-pip"])
    elif masaustu == "gnome":
        subprocess.run(["x-terminal-emulator", "-e", "sudo apt-get install pyhton3-pip"])
    elif masaustu == "kde":
        subprocess.run(["konsole", "-e", "sudo apt-get install pyhton3-pip"])
    else:
        print("Bilinmeyen masaüstü ortamı. Terminal açılamadı.")


ui.btnpipkur.clicked.connect(pip_install)




# ---- PIP GÜNCELLE (Pip Upgrade ) ---- #
# ------------------------------------------------- #
def pip_guncelle():
    masaustu = masaustu_kontrol()
    if masaustu == "xfce":
        subprocess.run(["xfce4-terminal", "--hold", "-e", "sudo pip install --upgrade pip"])
    elif masaustu == "gnome":
        subprocess.run(["x-terminal-emulator", "-e", "sudo pip install --upgrade pip"])
    elif masaustu == "kde":
        subprocess.run(["konsole", "-e", "sudo pip install --upgrade pip"])
    else:
        print("Bilinmeyen masaüstü ortamı. Terminal açılamadı.")


ui.btnPipGuncelle.clicked.connect(pip_guncelle)





# ---- PIP VERSİYON SORUGULAMA (Pip3 --version) --- #
# ------------------------------------------------- #
def pip_version():
    masaustu = masaustu_kontrol()
    if masaustu == "xfce":
        subprocess.run(["xfce4-terminal", "--hold", "-e", "pip3 --version"])
    elif masaustu == "gnome":
        subprocess.run(["x-terminal-emulator", "-e", "pip3 --version"])
    elif masaustu == "kde":
        subprocess.run(["konsole", "-e", "pip3 --version"])
    else:
        print("Bilinmeyen masaüstü ortamı. Terminal açılamadı.")


ui.btnpipversion.clicked.connect(pip_version)



# ---- PYTHON VERSİYON SORUGULAMA (Python3 --version) --- #
# ------------------------------------------------------- #
def python_version():
    masaustu = masaustu_kontrol()
    if masaustu == "xfce":
        subprocess.run(["xfce4-terminal", "--hold", "-e", "python3 --version"])
    elif masaustu == "gnome":
        subprocess.run(["x-terminal-emulator", "-e", "python3 --version"])
    elif masaustu == "kde":
        subprocess.run(["konsole", "-e", "python3 --version"])
    else:
        print("Bilinmeyen masaüstü ortamı. Terminal açılamadı.")


ui.btnpythonver.clicked.connect(python_version)





# ***************************************************************** #
# *** **** *** **** TEMEL İŞLEMLERİ SEKMESİ BÖLÜMÜ **** *** **** *** #
# ***************************************************************** #





















# ---- MENU / HAKKINDA Penceresi --- #
# ---------------------------------- #
def gosterHakkinda():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle("Hakkında")
    msg.setText("Tarık VARDAR tarafından hazırlanmıştır.\n tarikvardar@gmail.com\n github.com/tvardar\n")
    retval = msg.exec_()


ui.menuhakkinda.triggered.connect(gosterHakkinda)




#----- FONKSIYONLARI CAGIRIYORUZ----#
#-----------------------------------#
internet_baglanti()
sistem()
wifisifre()
dagitim()
kullanici()
yerelip()
localhost()
islemci()
ekrankarti()
seskarti()
ram()
hdd()



#------------------------ SON -----------------------------#
#----------------------------------------------------------#


sys.exit(Uygulama.exec_())


