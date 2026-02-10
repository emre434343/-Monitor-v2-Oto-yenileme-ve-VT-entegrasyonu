# 🛡️ Siber Tehdit Takip Paneli (PRO)

USOM (Ulusal Siber Olaylara Müdahale Merkezi) API'sini kullanarak gerçek zamanlı zararlı bağlantı takibi yapan, Python tabanlı bir masaüstü uygulamasıdır.

## ✨ Özellikler
- **Canlı Veri:** USOM API üzerinden anlık tehdit çekme.
- **Otomatik Yenileme:** Her 5 dakikada bir veri tabanını günceller.
- **VirusTotal Entegrasyonu:** Tehditlere çift tıklayarak VirusTotal üzerinde analiz başlatma.
- **Raporlama:** Tespit edilen tehditleri `tehditler.txt` olarak dışa aktarma.
- **Kayan Yazı:** En kritik ve güncel tehditleri anlık olarak ekranda kaydırır.

## 🚀 Kurulum ve Çalıştırma
1. Bu depoyu klonlayın: `git clone https://github.com/kullaniciadi/usom-monitor.git`
2. Gerekli kütüphaneyi kurun: `pip install requests`
3. Uygulamayı çalıştırın: `python usom_panel.py`

## 📦 EXE Yapma
Projeyi EXE haline getirmek için şu komutu kullanın:
`python -m PyInstaller --onefile --noconsole --clean --noconfirm usom_panel.py`
