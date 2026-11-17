# MicroPricing | Üretim Analitiği ve Fiyatlandırma Karar Motoru

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)
[![Status: Production Ready](https://img.shields.io/badge/Status-Production%20Ready-emerald.svg)](#)
[![Domain: Applied Microeconomics](https://img.shields.io/badge/Domain-Applied%20Microeconomics-indigo.svg)](#)

> **Geliştirici:** Enes Kabaoğlu  
> **Unvan:** YTÜ İktisat Bölümü  
> **Uzmanlık Alanı:** Mikroiktisat, Yöneylem Araştırması, Üretim Maliyetleri ve Fiyatlandırma Matematiği

---

## 1. Akademik ve İktisadi Amaç

Geleneksel butik üretim atölyeleri ve imalat işletmeleri, hammadde fiyat dalgalanmalarına, enflasyonist şoklara ve kapasite kısıtlarına karşı savunmasız kalabilmektedir. Üreticiler çoğunlukla birim satış fiyatını doğrudan maliyetin üzerine sezgisel bir marj ekleyerek belirler; oysa bu yöntem **sabit maliyet amortismanını**, **kısıtlı işçilik süresini** ve **fiyat esnekliği karşısındaki talep erozyonunu** hesaba katmaz.

**MicroPricing**, Yıldız Teknik Üniversitesi İktisat müfredatındaki kuramsal yaklaşımları (Mikroiktisat, Yöneylem Araştırması, Ekonometri ve Finansal Yönetim) üretim verileriyle harmanlayan bir karar destek sistemidir. 

Projenin temel amacı;
1. Atölyenin başabaş satış eşiklerini ($Q^*$) tekil ve bileşik ürün bazında belirlemek,
2. Deri, lojistik ve genel gider şoklarına karşı işletmenin dayanıklılığını 2 boyutlu stres matrisleriyle test etmek,
3. Talebin fiyat esnekliğini ($\varepsilon$) dikkate alarak kârı maksimize eden telafi fiyatlarını dinamik olarak türetmektir.

---

## 2. Matematiksel Model ve İktisadi Formülasyon

Sistem, neoklasik firma teorisi ve maliyet-hacim-kâr (CVP - Cost-Volume-Profit) analizine dayanan deterministik ve esnek bir altyapı işletir:

### A. Sabit Maliyetler ($FC$ - Fixed Costs)
Aylık üretim hacminden ve satış miktarından bağımsız, işletmenin sürekliliği için katlanılan zorunlu amortisman ve altyapı giderleri:
$$FC = \sum FC_k = \text{Alet Amortismanı} + \text{Atölye Genel Gideri} + \text{Dijital Platform/Domain Masrafı}$$

### B. Birim Değişken Maliyet ($VC$ - Variable / Marginal Cost)
Üretilen her ilave ürün için harcanan doğrudan hammadde, işçilik ve operasyonel maliyet:
$$VC = (A_{\text{deri}} \times P_{\text{deri}}) + (N_{\text{mıknatıs}} \times P_{\text{mıknatıs}}) + \left(\frac{T_{\text{işçilik}}}{60} \times W_{\text{saat}}\right) + C_{\text{sarf}} + C_{\text{lojistik}}$$

### C. Katkı Payı ($CM$ - Contribution Margin) ve Oranı ($CMR$)
Satış fiyatından birim değişken maliyet düşüldükten sonra sabit giderlerin amortismanına ve net kâra aktarılan tutar:
$$CM = P - VC$$
$$CMR = \frac{CM}{P} = \frac{P - VC}{P}$$

### D. Başabaş Noktası ($Q^*$ - Break-Even Quantity)
Toplam hasılatın ($TR = P \cdot Q$) toplam maliyete ($TC = FC + VC \cdot Q$) eşitlendiği, yani ekonomik kârın sıfır olduğu ($\pi = 0$) kritik eşik:
$$Q^* = \frac{FC}{P - VC} = \frac{FC}{CM}$$
* $Q < Q^*$ durumunda firma net faaliyet zararı yazar: $\pi < 0$
* $Q > Q^*$ durumunda her bir ilave satış $CM$ kadar marjinal kâr sağlar: $\pi = CM \cdot (Q - Q^*)$

### E. Çoklu Satış Karması ve Ağırlıklı Ortalama Katkı Payı ($WACM$)
Birden fazla ürünün (Kartlık, Sadak, Zihgir) aynı anda üretildiği karma portföyde sabit giderler ortak havuzdan karşılanır:
* Her bir ürünün satış karmasındaki payı: $w_i = \frac{Q_i}{\sum Q_k}$
* Ağırlıklı ortalama birim katkı payı:
  $$WACM = \sum_{i=1}^{n} w_i \cdot CM_i = \sum_{i=1}^{n} w_i \cdot (P_i - VC_i)$$
* Bileşik başabaş hacmi:
  $$Q^*_{\text{bileşik}} = \frac{FC}{WACM}$$

### F. Güvenlik Marjı ($MoS$) ve Faaliyet Kaldıracı ($DOL$)
* **Güvenlik Marjı (Margin of Safety):** Mevcut veya hedeflenen satış hacminin başabaş noktasından ne kadar uzakta olduğunu gösteren tampon:
  $$MoS = \frac{Q_{\text{hedef}} - Q^*}{Q_{\text{hedef}}} \times 100$$
* **Faaliyet Kaldıracı Derecesi (Degree of Operating Leverage):** Satış hacmindeki %1'lik bir değişimin net kâr üzerindeki çarpan etkisi:
  $$DOL = \frac{\text{Toplam Katkı Payı}}{\text{Net Faaliyet Kârı}} = \frac{Q \cdot CM}{(Q \cdot CM) - FC}$$

### G. Talebin Fiyat Esnekliği ($\varepsilon$) ve Telafi Fiyatı Modeli
Fiyat artışları karşısında talebin verdiği oransal tepki ve kâr nötr telafi fiyatlaması:
$$\varepsilon = \frac{\%\Delta Q}{\%\Delta P} = \frac{(Q_1 - Q_0) / Q_0}{(P_1 - P_0) / P_0}$$
* Bir maliyet şokunda ($\Delta VC$) mevcut kârı veya katkı payı oranını korumak için gereken minimum telafi fiyatı:
  $$P_{\text{telafi}} = \frac{VC + \Delta VC}{1 - CMR_{\text{baz}}}$$

---

## 3. Temel Özellikler ve Karar Destek Modülleri

1. **Canlı Mikroiktisadi Başabaş Grafiği:**
   - Toplam Gelir ($TR$) ve Toplam Maliyet ($TC$) doğrularının kesişim noktası ($Q^*$).
   - İktisat teorisine uygun mikroiktisadi alan boyaması: Başabaşın solunda kalan açık kırmızı şeffaf **Zarar Alanı**, sağında kalan açık mavi şeffaf **Kâr Alanı**.
   - Eksenlerde birim kalabalığı olmadan saf sayılar, uçlarda net `₺` ve `Adet` başlıkları.

2. **Serbest Adım ve Tavan Ölçeği:**
   - Grafiğin yatay eksenini 1'erli, 2'şerli, 3'erli veya 5'erli adımlarla inceleme imkânı.
   - Atölyenin fiili kapasitesine göre tavan üretim adedini serbestçe belirleme.

3. **Çok Boyutlu Maliyet Şokları Simülatörü:**
   - Hammadde (vejetal deri dm² fiyatı), lojistik (kargo/paketleme) veya atölye genel giderlerine yönelik özel yüzdesel şok girişi.
   - 4'lü hazır makro senaryo karşılaştırma kartları (Mevcut Durum, Deri Krizi, Lojistik Sıçraması, Genel Stagflasyon).

4. **Canlı Telafi Fiyatı Motoru:**
   - Maliyet şoku sonrasında atölyenin marjinal kârlılığını kaybetmemesi için ürünün satılması gereken asgari fiyatı anlık hesaplar.

5. **2 Boyutlu Kârlılık Duyarlılık Matrisi (Stress Test Matrix):**
   - Satış fiyatı ($\pm \%15$) ve maliyet şoku ($\%0 - \%50$) eksenlerinde tüm kâr/zarar olasılıklarını renk kodlarıyla haritalandırır:
     - 🟢 **Yeşil:** Hedef kârlılığın korunduğu güvenli alan.
     - 🔵 **Mavi:** Başabaş ve baz durum eşiği.
     - 🔴 **Kırmızı:** Sabit maliyetlerin karşılanamadığı zarar bölgesi.

6. **Talebin Fiyat Esnekliği Simülatörü:**
   - Zanaatkarın fiyat artışı yaptığında talepte oluşacak erimeyi ($\varepsilon$) simüle ederek net ciro ve kârın tepe noktasını bulmasını sağlar.

7. **Tam Ürün Kataloğu ve Parametre Yönetimi:**
   - Hazır ürünler: *El Yapımı Vejetal Deri Kartlık*, *Geleneksel Tirkeş / Sadak*, *El Dikişi Deri Okçu Zihgiri*.
   - Tek tıkla yeni ürün ekleme, malzeme sarfiyatı, işçilik süresi ve saatlik ücretleri dinamik düzenleme.

---

## 4. Mimari ve Dosya Yapısı

```
micro-pricing/
│
├── index.html                   # Bağımsız, modern ve reaktif karar motoru web arayüzü (Tailwind CSS, Chart.js)
├── README.md                    # İktisadi kuram, matematiksel model ve kullanım kılavuzu
├── LICENSE                      # GNU General Public License v3.0 (GPLv3)
├── .gitignore                   # Python, OS ve IDE geçici dosya filtreleri
├── DESIGN_DECISIONS.md          # Tipografi, renk paleti ve katı UI/UX tasarım standartları kaydı
├── GELISTIRME_ONERILERI.md      # Yöneylem (Doğrusal Programlama) ve ileri ekonometri geliştirme yol haritası
├── SM-LOGO.jpg                  # Platform kimlik görseli
│
├── scripts/
│   └── micro_model.py           # Mikroiktisat matematik motoru (Python CLI / Veri boru hattı)
│
└── public/
    └── data/
        └── pricing_data.json    # Tekil ve bileşik model metriklerinin yapılandırılmış JSON çıktısı
```

---

## 5. Kurulum ve Çalıştırma

Proje sıfır harici bağımlılık ilkesiyle tasarlanmıştır. Karmaşık derleme adımları veya paket yükleyicileri gerektirmez.

### Yöntem 1: Yerel Web Sunucusu ile (Önerilen)
Terminal veya komut istemcisinde proje dizinine gidip dahili Python HTTP sunucusunu başlatın:

```bash
git clone https://github.com/eneskabaoglu/micro-pricing.git
cd micro-pricing
python -m http.server 3000
```

Ardından tarayıcınızdan şu adrese gidin:
```
http://localhost:3000
```

### Yöntem 2: Doğrudan Tarayıcıda Açma
Herhangi bir sunucu kurmadan doğrudan `index.html` dosyasına çift tıklayarak veya tarayıcınıza sürükleyerek çalıştırabilirsiniz:
- Chrome, Edge, Safari, Firefox ve Brave tam uyumludur.

### Yöntem 3: Python Matematik Motorunu Çalıştırma
Veri modelini doğrulamak veya `pricing_data.json` dosyasını terminal üzerinden yeniden hesaplamak için:

```bash
python scripts/micro_model.py
```

Konsol çıktısı:
```text
============================================================
MicroPricing Mikroiktisadi Analiz Motoru Başarıyla Çalıştırıldı
============================================================
Toplam Sabit Maliyet (FC): ₺1,000.00/ay

--- Tekil Ürün Mikroiktisat Metrikleri ---
• El Yapımı Vejetal Deri Kartlık:
   Fiyat (P): ₺550.0 | Değişken Mal. (VC): ₺338.0 | Katkı Payı (CM): ₺212.0 (%38.55)
   Başabaş Eşiği (Q*): 5 adet | Hedef Satış: 30 adet -> Net Kâr: ₺5360.0
• Geleneksel Tirkeş / Sadak:
   Fiyat (P): ₺2800.0 | Değişken Mal. (VC): ₺1662.0 | Katkı Payı (CM): ₺1138.0 (%40.64)
   Başabaş Eşiği (Q*): 1 adet | Hedef Satış: 6 adet -> Net Kâr: ₺5828.0
• El Dikişi Deri Okçu Zihgiri:
   Fiyat (P): ₺320.0 | Değişken Mal. (VC): ₺181.5 | Katkı Payı (CM): ₺138.5 (%43.28)
   Başabaş Eşiği (Q*): 8 adet | Hedef Satış: 25 adet -> Net Kâr: ₺2462.5

--- Çoklu Satış Karması (Bileşik Model) ---
• Toplam Hedef Satış (Q): 61 adet | Toplam Ciro: ₺41300.0
• Ağırlıklı Ortalama Katkı Payı (WACM): ₺272.96
• Bileşik Başabaş Noktası (Q*): 4 toplam ürün (Ciro: ₺2708.2)
• Güvenlik Marjı (MoS): %93.44 | Faaliyet Kaldıracı (DOL): 1.06
• Konsolide Net Kâr: ₺15650.5
============================================================
```

---

## 6. Tasarım ve Tipografi Standartları

Projenin arayüz mimarisi, [DESIGN_DECISIONS.md](DESIGN_DECISIONS.md) belgesinde kayıt altına alınan katı kurallarla korunur:
- **Yazı Tipleri:** Başlıklar ve sayısal veriler için `Space Grotesk` (`tabular-nums`), gövde metinleri için `Inter`. Daktilo fontu (`font-mono`) yasaklanmıştır.
- **Renk Paleti:** `#f4f6fa` zemin, kobalt mavisi (`#2563eb`) vurgular, zümrüt yeşili kâr alanları ve gül kırmızısı zarar uyarıları.
- **Mikro Etkileşimler:** Popover tabanlı özel dropdown kontrolleri, klavye dostu slider bileşenleri ve yumuşak animasyon geçişleri.

---

## 7. Lisans

Bu proje [GNU General Public License v3.0](LICENSE) (GPLv3) kapsamında açık kaynak olarak lisanslanmıştır.  
Copyright (c) 2026 **Enes Kabaoğlu**.
