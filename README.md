# Uniques text file

Uniques text file, Python'da args kütüphanesi kullanmadan parametre alan consol uygulaması. Txt dosyasındaki unique satırları .txt olarak almanıza olanak sağlıyor. Sıralama alogirtması olarak QuickShort kullanılmıştır.

## Parametreler
|Paramentre | Açıklama | Varsayılan |
| :---: | :---: | :---:|
|-infile | İşlem yapılacak dosyanın dosya yolu | None|
|-outfile | Çıktı olarak verilecek dosyanın adı | {dosyaAdi}_out.txt|
| -sort | Çıktıyı alfabetik sıralama | False |
| -deleteblank | Çıktıdaki boşlukları sil | False |
| -casesensitive | Harflerin boyut duyarlılığı | True |


# Çalıştırmak
Örnek çalıştırma kodu.
```sh
python uniques.py -infile test.txt
```

