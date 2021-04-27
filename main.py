import pandas as pd
import matplotlib.pyplot as plt


class restoran:
    def __init__(self):
        self.id_restoran = 0
        self.pelayanan = 0
        self.makanan = 0

        # Fuzzifikasi (Fuzzy Input)
        self.makanan_enak = -1  # Range [7, 10]
        self.makanan_tidakenak = -1  # Range [1, 4]

        self.pelayanan_baik = -1  # Range [90, 100]
        self.pelayanan_biasa = -1  # Range [40, 60]
        self.pelayanan_jelek = -1  # Range [1, 20]

        # Inferensi (Fuzzy Output)
        self.bagus = []  # Masukkan Semua Nilai Yang Mungkin untuk Bagus
        self.buruk = []  # Masukkan Semua Nilai Yang Mungkin untuk Buruk
        self.bagus_akhir = 0  # Nilai Terkecil dari list Bagus
        self.buruk_akhir = 0  # Nilai Terkecil dari list Buruk

        # Defuzzifikasi (Crisp Input)
        self.nilai_akhir = 0

    def tampilData(self):
        print(
            'id restoran: {} \n nilai pelayanan: {} \n nilai makanan: {} \n nilai akhir: {} \n   makanan_enak: {} \n   makanan_tidakenak: {} \n   pelayanan_baik: {} \n   pelayanan_biasa: {} \n   pelayanan_jelek: {} \n   persentase bagus: {} \n   persentase buruk: {}'
            .format(self.id_restoran, self.pelayanan, self.makanan,
                    self.nilai_akhir, self.makanan_enak,
                    self.makanan_tidakenak, self.pelayanan_baik,
                    self.pelayanan_biasa, self.pelayanan_jelek,
                    self.bagus_akhir, self.buruk_akhir))


def fuzzifikasi(restoran_temp):
    for i in range(len(restoran_temp)):
        # Perhitungan pelayanan
        if restoran_temp[i].pelayanan >= 1 and restoran_temp[i].pelayanan <= 20:
            restoran_temp[i].pelayanan_jelek = 1
        elif restoran_temp[i].pelayanan > 20 and restoran_temp[
                i].pelayanan < 40:
            restoran_temp[i].pelayanan_jelek = -(restoran_temp[i].pelayanan -
                                                 40) / (40 - 20)
            restoran_temp[i].pelayanan_biasa = (restoran_temp[i].pelayanan -
                                                20) / (40 - 20)
        elif restoran_temp[i].pelayanan >= 40 and restoran_temp[
                i].pelayanan <= 60:
            restoran_temp[i].pelayanan_biasa = 1
        elif restoran_temp[i].pelayanan > 60 and restoran_temp[
                i].pelayanan < 90:
            restoran_temp[i].pelayanan_biasa = -(restoran_temp[i].pelayanan -
                                                 90) / (90 - 60)
            restoran_temp[i].pelayanan_baik = (restoran_temp[i].pelayanan -
                                               60) / (90 - 60)
        elif restoran_temp[i].pelayanan >= 90 and restoran_temp[
                i].pelayanan <= 100:
            restoran_temp[i].pelayanan_baik = 1

        if restoran_temp[i].makanan >= 1 and restoran_temp[i].makanan <= 4:
            restoran_temp[i].makanan_tidakenak = 1
        elif restoran_temp[i].makanan > 4 and restoran_temp[i].makanan < 7:
            restoran_temp[i].makanan_tidakenak = -(restoran_temp[i].makanan -
                                                   7) / (7 - 4)
            restoran_temp[i].makanan_enak = (restoran_temp[i].makanan -
                                             4) / (7 - 4)
        elif restoran_temp[i].makanan >= 7 and restoran_temp[i].makanan <= 10:
            restoran_temp[i].makanan_enak = 1

    return restoran_temp


def inferensi(restoran_temp):
    for i in range(len(restoran_temp)):
        if restoran_temp[i].makanan_tidakenak != -1:
            if restoran_temp[i].pelayanan_jelek != -1:
                restoran_temp[i].buruk.append(
                    min(restoran_temp[i].makanan_tidakenak,
                        restoran_temp[i].pelayanan_jelek))
            if restoran_temp[i].pelayanan_biasa != -1:
                restoran_temp[i].buruk.append(
                    min(restoran_temp[i].makanan_tidakenak,
                        restoran_temp[i].pelayanan_biasa))
            if restoran_temp[i].pelayanan_baik != -1:
                restoran_temp[i].buruk.append(
                    min(restoran_temp[i].makanan_tidakenak,
                        restoran_temp[i].pelayanan_baik))
        if restoran_temp[i].makanan_enak != -1:
            if restoran_temp[i].pelayanan_jelek != -1:
                restoran_temp[i].buruk.append(
                    min(restoran_temp[i].makanan_enak,
                        restoran_temp[i].pelayanan_jelek))
            if restoran_temp[i].pelayanan_biasa != -1:
                restoran_temp[i].bagus.append(
                    min(restoran_temp[i].makanan_enak,
                        restoran_temp[i].pelayanan_biasa))
            if restoran_temp[i].pelayanan_baik != -1:
                restoran_temp[i].bagus.append(
                    min(restoran_temp[i].makanan_enak,
                        restoran_temp[i].pelayanan_baik))

        if len(restoran_temp[i].bagus) != 0:
            restoran_temp[i].bagus_akhir = max(restoran_temp[i].bagus)

        if len(restoran_temp[i].buruk) != 0:
            restoran_temp[i].buruk_akhir = max(restoran_temp[i].buruk)

    return restoran_temp


def defuzzifikasi(sample: int, rest: restoran) -> restoran:
    #Parameter fungsi keanggotaan
    parm = {
        "batas_bawah": 1,
        "buruk_c": 40,
        "buruk_d": 80,
        "bagus_a": 40,
        "bagus_b": 80,
        "batas_atas": 100
    }

    pembilang = 0
    penyebut = 0
    increment = 100 // sample
    for i in (range(sample - 0)):
        bilangan = (i + 1) * increment
        # print(bilangan)
        if bilangan <= parm['buruk_c']:  #Pengecekkan jika berada dari titik buruk_c ke bawah
            pembilang += bilangan * rest.buruk_akhir
            penyebut += rest.buruk_akhir
        elif bilangan >= parm['bagus_b']:  #Pengecekkan jika berada dari titik bagus_b ke atas
            pembilang += bilangan * rest.bagus_akhir
            penyebut += rest.bagus_akhir
        else:  #Pengecekkan jika berada di antara / transisi
            nilai_asli_buruk = -(bilangan - parm['buruk_d']) / (
                parm['buruk_d'] - parm['buruk_c'])
            nilai_asli_bagus = (bilangan - parm['bagus_a']) / (
                parm['bagus_b'] - parm['bagus_a'])

            nilai_terkecil_buruk = min([nilai_asli_buruk, rest.buruk_akhir])
            nilai_terkecil_bagus = min([nilai_asli_bagus, rest.bagus_akhir])

            nilai_max = max([nilai_terkecil_buruk, nilai_terkecil_bagus])

            pembilang += bilangan * nilai_max
            penyebut += nilai_max

    rest.nilai_akhir = pembilang // penyebut

    return rest


def NilaiAkhirSort(restoran_temp: [restoran()]):
    restoran_temp = sorted(restoran_temp,
                           key=lambda x: x.nilai_akhir,
                           reverse=1)
    return restoran_temp


if __name__ == "__main__":
    # Memasukkan file ke dalam dataframe menggunakan pandas
    df = pd.read_excel('./data/raw/restoran.xlsx')
    restoran_data = []

    # Memasukkan data dari dataframe ke dalam list
    for i in range(len(df)):
        restoran_temp = restoran()
        restoran_temp.id_restoran = df.iloc[i][0]
        restoran_temp.pelayanan = df.iloc[i][1]
        restoran_temp.makanan = df.iloc[i][2]
        restoran_data.append(restoran_temp)

    # Meluakukan fuzzifikasi
    restoran_data = fuzzifikasi(restoran_data)

    # Melakukan Inferensi
    restoran_data = inferensi(restoran_data)

    # Melakukan defuzzifikasi
    for i in range(len(restoran_data)):
        restoran_data[i] = defuzzifikasi(20, restoran_data[i])

    # Sorting berdasarkan nilai akhir
    restoran_data = NilaiAkhirSort(restoran_data)

    # Membuat data akhir yang akan dimasukkan ke dalam excel peringkat.xls
    data_akhir = []
    for i in range(10):
        data_temp = []
        data_temp.append(restoran_data[i].id_restoran)
        data_temp.append(restoran_data[i].nilai_akhir)
        data_temp.append(restoran_data[i].pelayanan)
        data_temp.append(restoran_data[i].makanan)
        data_akhir.append(data_temp)

    df_akhir = pd.DataFrame(data_akhir,
                            columns=['id', 'nilai_akhir', 'pelayanan', 'makanan'])

    df_akhir.to_excel('./data/processed/peringkat.xls', encoding='xlwt')
