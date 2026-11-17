# MicroPricing üretim analitiği tasarım kararları raporu

Bu doküman, MicroPricing üretim analitiği ve fiyatlandırma karar motoru projesinde uygulanan tasarım standartlarını, reddedilen unsurları ve teknik gerekçelerini belgeler.

---

## 1. Onaylanan tasarım standartları

* **Renk teması ve matris renk kodlaması.**
  * Taban: `#f4f6fa` (açık gri-mavi ton).
  * Kartlar: `#ffffff`, kenarlıklar `#dce1ea`.
  * Birincil vurgu: Kobalt mavisi (`#2563eb`).
  * İki boyutlu duyarlılık matrisi renkleri:
    * Yeşil (`#059669` / `bg-emerald-50 text-emerald-700`): Kârlı alan.
    * Mavi (`#2563eb` / `bg-blue-50 text-blue-700`): Başabaş ve baz durum eşiği.
    * Kırmızı (`#dc2626` / `bg-rose-50 text-rose-700`): Zarar alanı.

* **Tipografi ve metin kuralları.**
  * Başlıklar ve sayılar: `Space Grotesk` (`tabular-nums`).
  * Gövde metinleri: `Inter`.
  * Formül ve etiketler `Space Grotesk` ile yazılır. Monospace fontlar (`font-mono`) kullanılmaz.

* **Grafik eksenleri ve mikroiktisadi bölge boyaması.**
  * Eksen değerlerindeki birim tekrarları kaldırıldı. Eksenlerde yalnızca sayılar yer alır.
  * Birimler (`₺` ve `Adet`) eksen uçlarında tek bir başlık olarak belirtilir.
  * Grafik alanı iki eğri arasındaki ilişkiye göre boyanır:
    * Zarar bölgesi ($Q < Q^*$): Toplam maliyet toplam hasılatı aştığında iki çizgi arası şeffaf kırmızıdır (`rgba(239, 68, 68, 0.14)`).
    * Kâr bölgesi ($Q \ge Q^*$): Toplam hasılat toplam maliyeti aştığında iki çizgi arası şeffaf mavidir (`rgba(37, 99, 235, 0.14)`).
    * Alt çizginin altı şeffaf kalır.
  * Grafik adım aralığı (1'erli, 2'şerli, 3'erli, 5'erli) ve tavan adet sınırı kullanıcı tarafından belirlenir.

* **Üst menü ve başlık hiyerarşisi.**
  * Sol kısım: `MicroPricing` ana başlığı ve altında `Üretim analitiği` alt başlığı.
  * Sağ kısım: `Üretim maliyetleri ve fiyatlandırma karar motoru` başlığı.
  * Başlık altı çizgisi doğrudan metin harflerinin hemen altına (`pb-0.5 border-b-2`) yerleştirildi.

* **Stres modülü bileşen sıralaması.**
  1. **Mevcut baz durum ve şok senaryo kartları.** Sayfa başında baz durum ile üç temel piyasa şokunun kâr ve maliyet karşılaştırması yer alır.
  2. **Maliyet şoku stres testi.** Belirlenen yüzde oranında zam girilerek telafi satış fiyatı ve yeni başabaş noktası hesaplanır.
  3. **İki boyutlu kârlılık duyarlılık matrisi.** Seçilen şok kalemine (`Hammadde`, `Lojistik`, `Tüm Maliyetler`) göre fiyat ve maliyet kesişim tablosu sunulur.
  4. **Fiyat esnekliği hesabı.** Talep esnekliği katsayısı ($\epsilon$) ve test fiyatı üzerinden beklenen talep ve kâr hesaplanır.
  5. **İktisadi çıkarım kartı.** Talep esnekliği ve zanaat atölyelerinde fiyatlama gücünün teorik ilkeleri açıklanır.

* **Ürün eylemlerinin gruplanması.** Yeni ürün butonu, ürün yönetimi satırında Düzenle butonunun yanında konumlandırıldı.

* **Özel menü bileşenleri.** Tarayıcının varsayılan açılır menüsü yerine kart tipi popover ve özel tarih aralığı takvimi uygulandı.

* **Açık kaynak lisansı.** Proje lisansı olarak türetilen çalışmaların da açık kaynak kalmasını garanti eden GNU General Public License v3.0 (GPLv3) kabul edildi.

---

## 2. Reddedilen tasarım tercihleri

* **Permissive (Gevşek) Lisanslar (MIT vb.).** Kodun kapalı kaynak ticarileştirilmesine izin veren MIT lisansı yerine copyleft koruması sağlayan GPLv3 seçildi.

* **Metinden ayrık çizgiler.** Metin ile alt çizgi arasında boşluk bırakan konteyner kenarlıkları kaldırıldı; çizgi harflerin tabanına hizalanır.
* **Sabit tekil şok kalıpları.** Kullanıcının maliyet kalemini veya şok oranını değiştiremediği yapılar yerine serbest parametre girişi sağlandı.
* **Matrisin dar kolona sıkıştırılması.** Karar matrisi tam genişlikte konumlandırıldı.
* **Eksenlerde birim kalabalığı.** Her değerin yanına ₺ veya adet yazılması kaldırıldı; birimler eksen uçlarına taşındı.
* **Tüm grafik tabanının boyanması.** Yalnızca gelir ile maliyet arasındaki net kâr (mavi) ve net zarar (kırmızı) alanları boyanır.
* **Sabit grafik eksen adımları.** Kullanıcıya serbest adım ve tavan sınır kontrolü verildi.
* **Üst menüde dağınık rozetler.** Temizlendi.
* **Tarayıcı varsayılanı açılır menü.** Kaldırıldı.
* **Plus Jakarta Sans fontu.** Kaldırıldı.
* **Monospace fontlar (`font-mono`).** Kaldırıldı.
