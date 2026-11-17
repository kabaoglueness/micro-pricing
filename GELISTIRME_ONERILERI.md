# MicroPricing analitik model geliştirme önerileri

Bu doküman, MicroPricing mikroiktisadi üretim modelini tek ürünlü deterministik bir başabaş aracından çok boyutlu bir karar destek sistemine dönüştürmek için hazırlanan teknik yol haritasıdır. Model, Yıldız Teknik Üniversitesi İktisat Bölümü müfredatındaki mikroiktisat, yöneylem araştırması, ekonometri ve finansal yönetim kuramlarını atölye üretim dinamikleriyle birleştirir.

---

## 1. Çoklu ürün karması ve bileşik başabaş analizi

### İktisadi temel
Atölyede tek bir ürün üretilmez. Kartlık, sadak ve zihgir gibi farklı marjinal katkı payına ve talep sıklığına sahip ürünler aynı anda satılır. Sabit maliyetler tek bir ürüne yüklenmez; tüm ürünlerin oluşturduğu satış karması bu giderleri ortak karşılar.

### Matematiksel model
Her bir ürün $i \in \{1, \dots, n\}$ için satış adedi $Q_i$ ve toplam satış adedi $Q = \sum Q_i$ olsun.

* **Satış karması ağırlığı ($w_i$).**
  $$w_i = \frac{Q_i}{Q}$$

* **Ağırlıklı ortalama birim katkı payı ($WACM$).**
  $$WACM = \sum_{i=1}^{n} w_i \cdot CM_i = \sum_{i=1}^{n} w_i \cdot (P_i - VC_i)$$

* **Bileşik başabaş satış miktarı ($Q^*$).**
  $$Q^* = \frac{FC}{WACM}$$

* **Ürün bazında başabaş kotaları ($Q^*_i$).**
  $$Q^*_i = Q^* \cdot w_i$$

* **Güvenlik marjı (Margin of safety, MoS).**
  $$MoS = \frac{Q_{\text{hedef}} - Q^*}{Q_{\text{hedef}}} \times 100$$

* **Faaliyet kaldıracı derecesi (Degree of operating leverage, DOL).**
  $$DOL = \frac{\text{Toplam Katkı Payı}}{\text{Net Kâr}} = \frac{\sum Q_i \cdot CM_i}{\sum Q_i \cdot CM_i - FC}$$
  DOL katsayısı, satış hacmindeki %1'lik bir değişimin net kârı yüzde kaç değiştireceğini gösterir.

### Atölye uygulaması
* Kullanıcı ürün hedeflerini girdiğinde sistem bileşik $WACM$ değerini ve her üründen kaç adet satılması gerektiğini otomatik hesaplar.
* Arayüzde satış karmasının kârlılığa etkisini gösteren etkileşimli ağırlık çubukları yer alır.

---

## 2. Kapasite ve zaman kısıtı altında üretim optimizasyonu

### İktisadi temel
Zanaat atölyesinde en kıt kaynak sermaye veya talep değil, zanaatkarın el dikişi ve montaj için ayırabildiği doğrudan çalışma saatidir. Ürünlerin kârlılığı birim satış fiyatına göre değil, harcanan kısıtlı zaman birimi başına getirdiği katkı payına göre sıralanır.

### Matematiksel model: Doğrusal programlama
Atölyenin aylık maksimum işçilik kapasitesi $T_{\text{max}}$ (örneğin 90 saat = 5.400 dakika) ve hammadde bütçesi $B$ olsun. Karar değişkenleri üretilecek ürün miktarları $X_1, X_2, X_3$ olur.

* **Amaç fonksiyonu.** Toplam katkı payı maksimizasyonu:
  $$\max Z = \sum_{i=1}^{n} CM_i \cdot X_i - FC$$

* **Kısıtlar.**
  1. *İşçilik zamanı kısıtı:*
     $$\sum_{i=1}^{n} t_i \cdot X_i \le T_{\text{max}}$$
     (Kartlık için 50 dk, sadak için 240 dk, zihgir için 35 dk)
  2. *Piyasa talep tavanı:*
     $$0 \le X_i \le D_{i,\text{max}} \quad \forall i$$
  3. *Hammadde bütçe kısıtı:*
     $$\sum_{i=1}^{n} (\text{Deri Alanı}_i \cdot \text{Birim Fiyat} + \text{Aksesuar}_i) \cdot X_i \le B$$
  4. *Tamsayılık koşulu:*
     $$X_i \in \mathbb{Z}^+$$

* **Kısıtlı kaynak başına katkı payı metriği ($CM_t$).**
  $$CM_{t, i} = \frac{CM_i}{t_i} \quad (\text{TL / Dakika})$$

### Atölye uygulaması
* Sadak tek başına ₺1.800 katkı payı üretse bile 240 dakika sürdüğünde dakikada ₺7.5 katkı payı sağlar. Kartlık 50 dakikada ₺212 katkı payı üretiyorsa dakikada ₺4.24 sağlar.
* Model, simplex veya köşe noktası algoritmasıyla aylık zaman sınırında atölye için kârı maksimize eden üretim adetlerini verir.

---

## 3. Hammadde stok kontrolü ve sipariş boyutu optimizasyonu

### İktisadi temel
Vejetal deri toptan tabaka (ortalama 200 $\text{dm}^2$) olarak alınır. Sık sipariş vermek kargo ve tedarik masrafını artırır. Çok sipariş vermek ise sermaye bağlama maliyetini, derinin ortam neminden etkilenme veya depoda çizilme riskini doğurur.

### Matematiksel model: Ekonomik sipariş miktarı (EOQ)

* **Optimum sipariş miktarı ($EOQ$).**
  $$EOQ = \sqrt{\frac{2 \cdot D \cdot S}{H}}$$
  * $D$: Yıllık toplam deri ihtiyacı ($\text{dm}^2$).
  * $S$: Sipariş başına sabit tedarik maliyeti (kargo, sevk, banka masrafı).
  * $H$: Yıllık $\text{dm}^2$ başına stok tutma maliyeti (paranın faiz veya enflasyon fırsat maliyeti + depo yıpranma payı).

* **Toplam yıllık stok maliyeti ($TC_{\text{stok}}$).**
  $$TC_{\text{stok}} = \left(\frac{D}{Q} \cdot S\right) + \left(\frac{Q}{2} \cdot H\right)$$

* **Yeniden sipariş noktası ($ROP$).**
  $$ROP = (d \cdot L) + SS$$
  * $d$: Günlük ortalama deri sarfiyatı ($\text{dm}^2 / \text{gün}$).
  * $L$: Tedarik süresi (Lead time, gün).
  * $SS$: Güvenlik stoku ($SS = Z_{\alpha} \cdot \sigma_d \cdot \sqrt{L}$).

### Atölye uygulaması
* Atölyenin hangi sıklıkta kaç tabaka deri sipariş etmesi gerektiğini hesaplayan bir tedarik paneli kurulur.
* Deri fiyatındaki olası toptan indirim baremleri modelde basamaklı maliyet eğrisiyle analiz edilir.

---

## 4. Stokastik talep ve maliyet simülasyonu: Monte Carlo analizi

### İktisadi temel
Piyasa deterministik değildir. Aylık sipariş adedi ve deri alış fiyatı sabit kalmaz; mevsimselliğe, kura ve enflasyona bağlı dalgalanır. Risk analizi noktasal tahmin yerine olasılık dağılımı üzerinden kurulur.

### Matematiksel model
1. **Talep dağılımı.**
   $$Q_i \sim \text{Poisson}(\lambda_i) \quad \text{veya} \quad Q_i \sim \text{LogNormal}(\mu_{q,i}, \sigma_{q,i})$$
2. **Hammadde fiyat dalgalanması.**
   $$P_{\text{deri}} \sim \text{Üçgen}(a, m, b) \quad \text{veya} \quad \text{Normal}(\mu_p, \sigma_p)$$
3. **Simülasyon motoru.**
   $N = 10.000$ yineleme boyunca rastgele çekilen parametrelerle kâr fonksiyonu hesaplanır:
   $$\pi^{(k)} = \sum_{i} \left[ P_i - VC_i^{(k)} \right] Q_i^{(k)} - FC^{(k)}$$

* **Çıktı metrikleri.**
  * **Zarar etme olasılığı.** $P(\pi < 0) = \frac{1}{N} \sum \mathbb{I}(\pi^{(k)} < 0)$
  * **Riske maruz kâr (VaR %95).** Dağılımın 5. yüzdelik dilimi.
  * **Beklenen kâr ve standart sapma.** $E[\pi]$, $\sigma_\pi$.

### Atölye uygulaması
* Çıktı, tek bir net kâr sayısı yerine kâr dağılım histogramı ve güven aralığı olarak gösterilir.
* Zanaatkar, atölyenin hangi koşullarda sabit giderlerini karşılayamama riskiyle karşılaşacağını önceden görür.

---

## 5. Dinamik fiyatlandırma ve kâr maksimizasyon noktası

### İktisadi temel
Mevcut esneklik hesabı sabit katsayıyla tek bir test fiyatını inceler. Neoklasik mikroiktisatta firma, marjinal hasılatın marjinal maliyete eşit olduğu noktada ($MR = MC$) kârını maksimize eder.

### Matematiksel model
Doğrusal talep fonksiyonu varsayımı altında:
$$Q(P) = a - b \cdot P \quad (a > 0, b > 0)$$

* **Ters talep fonksiyonu.**
  $$P(Q) = \frac{a}{b} - \frac{1}{b} Q$$

* **Toplam hasılat ($TR$).**
  $$TR(Q) = P(Q) \cdot Q = \frac{a}{b} Q - \frac{1}{b} Q^2$$

* **Marjinal hasılat ($MR$).**
  $$MR(Q) = \frac{d(TR)}{dQ} = \frac{a}{b} - \frac{2}{b} Q$$

* **Marjinal maliyet ($MC$).**
  Sabit birim değişken maliyet varsayımıyla $MC = VC$.

* **Optimum üretim miktarı ve satış fiyatı ($MR = MC$).**
  $$\frac{a - 2Q}{b} = VC \implies Q^* = \frac{a - b \cdot VC}{2}$$
  $$P^* = \frac{a + b \cdot VC}{2b}$$

* **Fiyat esnekliğiyle ilişki (Lerner endeksi kuralı).**
  $$\frac{P - MC}{P} = \frac{1}{|\varepsilon_d|}$$

### Atölye uygulaması
* Arayüzde fiyat kaydırıcısı hareket ettirildikçe $TR$ ve $TC$ eğrileri arasındaki dikey mesafenin (kâr) maksimuma ulaştığı tepe noktası grafik üzerinde işaretlenir.

---

## 6. Zanaat üretiminde fire oranı ve öğrenme eğrisi modeli

### İktisadi temel
Deri dikdörtgen bir levha değildir. Hayvanın sırt, boyun ve karın bölgelerinin lif yapısı farklıdır; yara izleri ve kenar geometrisi nedeniyle zanaatta fire oranı %15 ile %30 arasında değişir. Ayrıca zanaatkar bir modeli tekrar ürettikçe el alışkanlığı kazanır, dikiş süresi logaritmik olarak kısalır.

### Matematiksel model

* **Efektif deri sarfiyatı (Fire faktörü).**
  $$DM^2_{\text{brüt}} = \frac{DM^2_{\text{net}}}{1 - \gamma}$$
  Burada $\gamma \in [0, 0.40]$ fire katsayısıdır.

* **Öğrenme eğrisi (Wright modeli).**
  Üretilen kümülatif birim sayısı $n$ arttıkça $n$'inci birimin işçilik süresi $t(n)$ azalır:
  $$t(n) = t_1 \cdot n^{-b}$$
  * $t_1$: İlk prototipin üretim süresi (dakika).
  * $r$: Öğrenme oranı (örneğin %85; her üretim hacmi ikiye katlandığında süre %15 düşer).
  * $b$: Öğrenme parametresi ($b = -\frac{\ln(r)}{\ln(2)}$).

* **Kümülatif ortalama işçilik maliyeti.**
  $$VC_{\text{emek}}(n) = \left( \frac{1}{n} \sum_{k=1}^{n} t(k) \right) \cdot \frac{\text{Saatlik Ücret}}{60}$$

### Atölye uygulaması
* Yeni bir model tasarlanıp üretime alındığında maliyetin sabit kalmadığı, üretim hacmi arttıkça birim marjinal maliyetin azaldığı dinamik olarak izlenir.

---

## 7. Nakit dönüş döngüsü ve işletme sermayesi dinamiği

### İktisadi temel
Kârlılık ile likidite aynı şey değildir. Deri peşin alınır, rafta bekler, sipariş üzerine üretilir, kargolanır ve pazaryeri komisyon kesintisi sonrası ödemeyi 14 ile 28 gün arasında serbest bırakır. Atölye kârlı olsa dahi nakit dönüş süresi uzunsa nakit darboğazına girer.

### Matematiksel model: Nakit dönüş döngüsü (CCC)
$$CCC = DIO + DSO - DPO$$

* **Stokta bekleme süresi ($DIO$).**
  $$DIO = \frac{\text{Ortalama Stok Değeri}}{\text{Satılan Malın Maliyeti (COGS)}} \times 365$$
* **Alacak tahsil süresi ($DSO$).**
  $$DSO = \frac{\text{Pazaryeri ve Müşteri Alacakları}}{\text{Toplam Satış}} \times 365$$
* **Borç ödeme süresi ($DPO$).**
  $$DPO = \frac{\text{Tedarikçi Borçları}}{\text{Hammadde Alımları}} \times 365$$

* **Gereken asgari işletme sermayesi ($NWC$).**
  $$NWC = \frac{CCC}{365} \cdot \text{Yıllık Toplam Faaliyet Maliyeti}$$

### Atölye uygulaması
* Pazaryeri komisyon oranları ve ödeme bloke süreleri parametre olarak girildiğinde atölyenin operasyonu sürdürmek için kasada tutması gereken minimum nakit rezervi hesaplanır.

---

## 8. Birim iktisadı ve müşteri yaşam boyu değeri (LTV / CAC)

### İktisadi temel
Geleneksel okçuluk niş bir alandır. Müşteri genellikle tek bir zihgir alıp ayrılmaz; tirkeş, sadak ve bakım mumu gibi tamamlayıcı ürünleri zaman içinde tekrar sipariş eder. Dijital pazarlama maliyetleri ürünün tekil kârına değil, müşterinin tüm yaşam döngüsü değerine oranlanır.

### Matematiksel model
* **Müşteri edinme maliyeti ($CAC$).**
  $$CAC = \frac{\text{Aylık Reklam ve Pazarlama Harcaması}}{\text{Yeni Kazanılan Müşteri Sayısı}}$$

* **Müşteri yaşam boyu değeri ($LTV$).**
  $$LTV = \sum_{t=1}^{T} \frac{(R_t - VC_t) \cdot (1 - \text{Churn})^t}{(1 + d)^t}$$
  Sadeleştirilmiş kohort formülü:
  $$LTV = \frac{AOV \cdot CM_{\text{oran}} \cdot f}{\text{Churn Oranı}}$$
  * $AOV$: Ortalama sepet tutarı (Average Order Value).
  * $CM_{\text{oran}}$: Ortalama katkı payı oranı.
  * $f$: Yıllık sipariş sıklığı.
  * $\text{Churn}$: Müşteri kayıp oranı.
  * $d$: İskonto oranı.

* **Sürdürülebilirlik rasyosu.**
  $$\frac{LTV}{CAC} \ge 3.0 \quad \text{ve} \quad \text{Geri Ödeme Süresi (Payback)} \le 6 \text{ Ay}$$

### Atölye uygulaması
* Reklam harcamasının başabaş üzerindeki yükü ve müşteri sadakatinin uzun vadeli atölye gelirine etkisi simüle edilir.

---

## 9. Ampirik ekonometrik modelleme ve talep tahmini

### İktisadi temel
Amaç, talebin fiyat esnekliğini dışsal bir varsayım olarak almak yerine, atölyenin geçmiş sipariş verileri üzerinden ekonometrik regresyonla doğrudan tahmin etmektir.

### Matematiksel model: Çift logaritmik talep modeli
$$\ln(Q_t) = \beta_0 + \beta_1 \ln(P_t) + \beta_2 \ln(\text{Gelir}_t) + \beta_3 \text{Trend}_t + \epsilon_t$$

* Bu spesifikasyonda $\beta_1$ katsayısı doğrudan sabit fiyat esnekliğini ($\varepsilon_d$) verir:
  $$\varepsilon_d = \frac{\partial \ln Q}{\partial \ln P} = \beta_1$$
* **Hipotez testleri.**
  * $H_0: \beta_1 = 0$ ($t$-istatistiği ve $p$-değeri).
  * Belirleyicilik katsayısı ($R^2$) ve Durbin-Watson otokorelasyon testi.

### Atölye uygulaması
* Python tarafındaki `scripts/micro_model.py` içine `statsmodels` veya saf `numpy` matris cebiriyle ($OLS: \hat{\beta} = (X'X)^{-1}X'y$) çalışan hafif bir ekonometrik tahmin fonksiyonu eklenir.

---

## 10. Uygulama ve fazlandırma planı

Modellerin aşamalı olarak projeye dahil edilmesi planlanır:

### Faz 1: Çoklu ürün ve kısıtlı kaynak optimizasyonu
* Çoklu ürün karması ($WACM$) ve bileşik başabaş formülleri `scripts/micro_model.py` içine yazılır.
* Doğrusal programlama ile aylık çalışma saati sınırında optimum ürün üretim adetleri hesaplanır.
* `index.html` arayüzüne atölye geneli bileşik başabaş kartı ve kapasite doluluk göstergesi eklenir.

### Faz 2: Stok ve sipariş optimizasyonu (EOQ ve fire)
* Vejetal deri fire katsayısı ($\gamma$) ve tabaka bazlı $EOQ$ formülleri eklenir.
* Basamaklı toptan alım indirimleri ve yeniden sipariş noktası ($ROP$) paneli kurulur.

### Faz 3: Risk ve olasılık simülasyonu (Monte Carlo)
* Tarayıcı tarafında veya Python betiğinde 5.000 döngülük Monte Carlo simülasyonu çalıştırılır.
* Kâr dağılım histogramı ve zarar olasılığı yüzdesi Chart.js ile görselleştirilir.

### Faz 4: Dinamik kâr maksimizasyonu ve ekonometri
* Ters talep fonksiyonu üzerinden $MR = MC$ optimizasyon noktası hesaplanır.
* Geçmiş satış verisi yüklendiğinde otomatik OLS esneklik kestirimi yapan modül devreye alınır.
