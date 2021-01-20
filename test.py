import random, string, os

def DapatSemuaNasabah():
    AksesDatNas = []
    Filnas = open("nasabah.txt")
    for so_nice in Filnas:
        if so_nice != "\n" or "":
            data = so_nice.split(",")
            norek = data[0]
            rekening_name = data[1]
            rekening_saldo = data[2]
            AksesDatNas.append([norek, rekening_name, rekening_saldo])
        else:
            continue
    Filnas.close()
    return AksesDatNas

def DapatSemuaTransfer():
    AksesDatTransfer = []
    Filnas = open("transfer.txt")
    for so_nice in Filnas:
        if so_nice != "\n" or "":
            data = so_nice.split(",")
            noTransfer = data[0]
            noreksumber = data[1]
            norektujuan = data[2]
            NoTransfer = data[3]
            AksesDatTransfer.append([noTransfer, noreksumber, norektujuan, NoTransfer])
        else:
            continue
    Filnas.close()
    return AksesDatTransfer

def NasabahValid(no_rek):
    DataSemuaNasabah = DapatSemuaNasabah()
    NasabahValid = False
    for nasabah in DataSemuaNasabah:
        if nasabah[0] == no_rek.upper():
            NasabahValid = True
            break
    return NasabahValid

def CariNasabah(no_rek):
    DataSemuaNasabah = DapatSemuaNasabah()
    cariNasabah = []
    for nasabah in DataSemuaNasabah:
        if nasabah[0] == no_rek.upper():
            cariNasabah.extend((nasabah[0],nasabah[1], nasabah[2]))
            break
    return cariNasabah

def KurangkanSaldo(no_rek, saldo, DataSemuaNasabah = DapatSemuaNasabah()):
    for i in range(0, len(DataSemuaNasabah)):
        if DataSemuaNasabah[i][0] == no_rek.upper():
            # print(DataSemuaNasabah[i][2])
            DataSemuaNasabah[i][2] = int(DataSemuaNasabah[i][2]) - int(saldo)
            # print(DataSemuaNasabah[i][2])
    return DataSemuaNasabah

def TambahkanSaldo(no_rek, saldo, DataSemuaNasabah = DapatSemuaNasabah()):
    for i in range(0, len(DataSemuaNasabah)):
        if DataSemuaNasabah[i][0] == no_rek.upper():
            # print(DataSemuaNasabah[i][2])
            DataSemuaNasabah[i][2] = int(DataSemuaNasabah[i][2]) + int(saldo)
            # print(DataSemuaNasabah[i][2])
    return DataSemuaNasabah

def prosesTransfer(sumber_rek, tujuan_rek, nominal):
    tempData = KurangkanSaldo(sumber_rek, nominal)
    fixedData = TambahkanSaldo(tujuan_rek, nominal, tempData)
    saveProses(fixedData, 'nasabah.txt')

def saveProses(data, file):
    openFile = open(file, 'w')
    for so_nice in data:
        if so_nice != "\n":
            dataString = str('{0},{1},{2}\n'.format(so_nice[0], so_nice[1], so_nice[2]))
            openFile.write(dataString)

def main():
    print("--=== SELAMAT DATANG DI PAITEN BANK ^_^ ===--")
    print("[1] Buka Rekening")
    print("[2] Setoran Tunai")
    print("[3] Tarik Tunai")
    print("[4] Transfer")
    print("[5] Lihat Data Transfer")
    print("[6] Cek Saldo")
    print("[7] Keluar")

    pilihan = int(input("Masukan Menu pilihan anda : "))
    if pilihan == 1:
        bukaRekening()
    elif pilihan == 2:
        setorTunai()
    elif pilihan == 3:
        TarikTunai()
    elif pilihan == 4:
        Transfer()
    elif pilihan == 5:
        LihatDatTransfer()
    elif pilihan == 6:
        CekSaldo()
    elif pilihan == 7:
        print("Terima kasih atas kunjungan anda ^_^ ...")
    else:
        print("Pilihan menu yang dipilih tidak terdaftar! Silahkan Coba Lagi")

def bukaRekening():
    print("--=== Buka Rekening ===--")
    norek = "REK" + ''.join(random.choice(string.digits) for _ in range(3))
    rekening_name = input("Masukan nama anda disini : ")
    saldo_awal = int(input("Masukan saldo awal : "))
    if os.path.isfile("nasabah.txt"): #mengecek apakah file nasabah.txt ada atau tidak
        newData = open("nasabah.txt", "a+") #bila ada akan menggunakan metode append menambah data
    else:
        newData = open("nasabah.txt", "w") #bila tidak ada akan menggunakan metode overwrite
    stringNasabah = str('{0},{1},{2}\n'.format(norek, rekening_name, saldo_awal))
    newData.write(stringNasabah)
    newData.close()
    print("Rekening atas nama", rekening_name, " berhasil dibuka!")

def setorTunai():
    norek = input("Masukan Nomor Rekening : ")
    nominal = int(input("Masukan Nominal : "))
    validasi = NasabahValid(norek)
    if validasi:
        data_nasabah = DapatSemuaNasabah()
        for i in range(0,len(data_nasabah)):
            if data_nasabah[i][0] == norek.upper():
                data_nasabah[i][2] = int(data_nasabah[i][2]) + nominal
                saveProses(data_nasabah, 'nasabah.txt')
                print("Setor Tunai Senilai", nominal, " dengan nomor rekening", norek.upper(), " Berhasil!")
                break
            else:
                continue
    else:
        print("Gagal Setor Tunai! - Rekening tidak terdaftar!")

 
def TarikTunai():
    norek = input("Masukan Nomor Rekening : ")
    nominal = int(input("Masukan Nominal : "))
    validasi = NasabahValid(norek)
    if validasi:
        data_nasabah = DapatSemuaNasabah()
        for i in range(0,len(data_nasabah)):
            if data_nasabah[i][0] == norek.upper():
                if int(data_nasabah[i][2]) < nominal :
                    print("Gagal tarik tunai! - Saldo tidak mencukupi.")
                    break
                elif int(data_nasabah[i][2]) >= nominal:
                    data_nasabah[i][2] = int(data_nasabah[i][2]) - nominal
                    saveProses(data_nasabah, 'nasabah.txt')
                    print("Tarik tunai senilai", nominal, " dengan nomor rekening", norek.upper(), " Berhasil!")
                    break
            else:
                continue
    else:
        print("Gagal Tarik Tunai! - Rekening tidak terdaftar!")

def Transfer():
    nomor_trf = "TRF" + ''.join(random.choice(string.digits) for _ in range(3))
    no_rekening_sumber = input("Masukan nomor rekening sumber : ").upper()
    dataRekeningSumber = CariNasabah(no_rekening_sumber)
    no_rekening_tujuan = input("Masukan nomor rekening tujuan : ").upper()
    dataRekeningTujuan = CariNasabah(no_rekening_tujuan)
    if dataRekeningSumber:
        if dataRekeningTujuan:
            nominalTransfer = int(input("Masukan Nominal Transfer : "))
            if nominalTransfer <= int(dataRekeningSumber[2]):
                DatTransfer = str('{0},{1},{2},{3}\n'.format(nomor_trf, no_rekening_sumber, no_rekening_tujuan, nominalTransfer))
                checkFileExist = os.path.isfile("transfer.txt")
                if checkFileExist: #mengecek apakah file transfer.txt ada atau tidak
                    newData = open("transfer.txt", "a+") #bila ada akan menggunakan metode append menambah data
                else:
                    newData = open("transfer.txt", "w") #bila tidak ada akan menggunakan metode overwrite
                newData.write(DatTransfer)
                newData.close()
                prosesTransfer(no_rekening_sumber, no_rekening_tujuan, nominalTransfer)
                print("Transfer Senilai : ", nominalTransfer, " dari rekening : ", dataRekeningSumber[0], " ke rekening ", dataRekeningTujuan[0]," berhasil !")
            elif nominalTransfer > int(dataRekeningSumber[2]):
                print("Gagal Transfer! - Saldo Nomor Rekening Sumber tidak mencukupi.")
        else:
            print("Gagal Transfer! - Nomor Rekening Tujuan tidak terdaftar.")
    else:
        print("Gagal Transfer! - Nomor Rekening Sumber tidak terdaftar.")
    
    

def LihatDatTransfer():
    norek = input("Masukan No Rekening : ").upper()
    Validasi = NasabahValid(norek)
    if Validasi : 
        Data_Transfer = DapatSemuaTransfer()
        DatTransferSumber = []
        for i in Data_Transfer : 
            if i[1] == norek : 
                DatTransferSumber.append(i)
            else:
                continue
        if len(DatTransferSumber) == 0:
            print("Data Transfer Kosong!")
        else:
            for i in DatTransferSumber:
               print("{0} {1} {2} {3}\n".format(i[0], i[1],i[2],i[3]))
    else:
        print("Lihat data transfer gagal! - Nomor rekening tidak terdaftar!")

def CekSaldo():
    norek = input("Masukan nomor rekening : ").upper()
    DatNas = DapatSemuaNasabah()
    validasi = NasabahValid(norek)
    if validasi:
        for nasabah in DatNas:
            if nasabah[0] == norek:
                print("Nasabah dengan No. Rekening : ",norek," atas nama : ",nasabah[1]," Memiliki Saldo Senilai : ", nasabah[2])
                break
            else:
                continue
    else:
        print("Gagal Cek Saldo! - Nasabah tidak terdaftar!")
        
main()