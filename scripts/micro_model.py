"""
MicroPricing - Mikroiktisadi Üretim ve Fiyatlandırma Karar Motoru
Geliştirici: Enes Kabaoğlu (YTÜ İktisat)
Açıklama: Atölye sabit maliyetleri (FC), deri ve sarf değişken maliyetleri (VC),
katkı payı (CM), başabaş noktası (Q*), ağırlıklı ortalama katkı payı (WACM),
güvenlik marjı (MoS) ve faaliyet kaldıracı (DOL) hesaplama motoru.
"""

import json
import os
import math

# 1. Varsayılan Atölye Sabit Maliyetleri (Aylık FC - Fixed Costs)
DEFAULT_FIXED_COSTS = {
    "tools_depreciation": 350.0,   # Çatal zımba, kesim matı, çekiç, bıçak amortismanı
    "workshop_overhead": 400.0,    # Elektrik, sarf malzeme, aydınlatma
    "digital_presence": 250.0      # Domain, hosting, e-ticaret platform masrafı
}

# 2. Varsayılan Ürün Kataloğu
DEFAULT_PRODUCTS = [
    {
        "id": "deri_kartlik",
        "name": "El Yapımı Vejetal Deri Kartlık",
        "category": "Deri Aksesuar",
        "sale_price": 550.0,
        "leather_dm2": 3.5,
        "leather_price_per_dm2": 28.0,
        "magnets_count": 2,
        "magnet_unit_price": 12.5,
        "thread_glue_packaging": 35.0,
        "labor_minutes": 50,
        "hourly_wage": 150.0,
        "shipping_cost": 55.0,
        "monthly_target_sales": 30
    },
    {
        "id": "okculuk_sadak",
        "name": "Geleneksel Tirkeş / Sadak",
        "category": "Okçuluk Ekipmanı",
        "sale_price": 2800.0,
        "leather_dm2": 26.0,
        "leather_price_per_dm2": 32.0,
        "magnets_count": 0,
        "magnet_unit_price": 0.0,
        "thread_glue_packaging": 120.0,
        "labor_minutes": 240,
        "hourly_wage": 150.0,
        "shipping_cost": 110.0,
        "monthly_target_sales": 6
    },
    {
        "id": "deri_zihgir",
        "name": "El Dikişi Deri Okçu Zihgiri",
        "category": "Okçuluk Ekipmanı",
        "sale_price": 320.0,
        "leather_dm2": 0.8,
        "leather_price_per_dm2": 30.0,
        "magnets_count": 0,
        "magnet_unit_price": 0.0,
        "thread_glue_packaging": 15.0,
        "labor_minutes": 35,
        "hourly_wage": 150.0,
        "shipping_cost": 55.0,
        "monthly_target_sales": 25
    }
]

def calculate_product_metrics(product, fixed_costs_total):
    """
    Mikroiktisadi formülleri tekil ürün üzerinde işletir.
    FC: Fixed Costs (Sabit Maliyetler)
    VC: Variable Costs (Birim Değişken Maliyet)
    CM: Contribution Margin (Katkı Payı = P - VC)
    Q*: Break-even Quantity (Başabaş Noktası = FC / CM)
    """
    # Değişken Maliyet Kalemleri (VC)
    cost_leather = round(product["leather_dm2"] * product["leather_price_per_dm2"], 2)
    cost_magnets = round(product["magnets_count"] * product["magnet_unit_price"], 2)
    cost_labor = round((product["labor_minutes"] / 60.0) * product["hourly_wage"], 2)
    cost_other = round(product["thread_glue_packaging"] + product["shipping_cost"], 2)
    
    unit_variable_cost = round(cost_leather + cost_magnets + cost_labor + cost_other, 2)
    sale_price = float(product["sale_price"])
    
    # Katkı Payı (Contribution Margin): CM = P - VC
    contribution_margin = round(sale_price - unit_variable_cost, 2)
    contribution_margin_ratio = round((contribution_margin / sale_price) * 100, 2) if sale_price > 0 else 0.0
    
    # Başabaş Noktası (Break-Even Quantity): Q* = FC / CM
    if contribution_margin > 0:
        breakeven_units = math.ceil(fixed_costs_total / contribution_margin)
        breakeven_revenue = round(breakeven_units * sale_price, 2)
    else:
        breakeven_units = None
        breakeven_revenue = None

    # Hedef Satışta Aylık Kâr: π = (P - VC) * Q - FC
    target_q = product.get("monthly_target_sales", 20)
    monthly_revenue = round(sale_price * target_q, 2)
    monthly_profit = round((contribution_margin * target_q) - fixed_costs_total, 2)
    profit_margin_pct = round((monthly_profit / monthly_revenue) * 100, 2) if monthly_revenue > 0 else 0.0

    # Grafik serisi üretimi (0 adetten 2 x breakeven adedine kadar TR ve TC eğrileri)
    max_q = max((breakeven_units or 10) * 2, target_q + 10, 20)
    curve_data = []
    step = max(1, max_q // 15)
    for q in range(0, max_q + 1, step):
        total_revenue = round(sale_price * q, 2)
        total_cost = round(fixed_costs_total + (unit_variable_cost * q), 2)
        curve_data.append({
            "units": q,
            "total_revenue": total_revenue,
            "total_cost": total_cost,
            "profit": round(total_revenue - total_cost, 2)
        })

    return {
        "cost_breakdown": {
            "leather": cost_leather,
            "magnets": cost_magnets,
            "labor": cost_labor,
            "other": cost_other,
            "total_variable_cost": unit_variable_cost
        },
        "economics": {
            "sale_price": sale_price,
            "unit_variable_cost": unit_variable_cost,
            "contribution_margin": contribution_margin,
            "contribution_margin_ratio_pct": contribution_margin_ratio,
            "breakeven_units": breakeven_units,
            "breakeven_revenue": breakeven_revenue,
            "target_sales_units": target_q,
            "monthly_projected_revenue": monthly_revenue,
            "monthly_projected_profit": monthly_profit,
            "profit_margin_pct": profit_margin_pct
        },
        "curve_data": curve_data
    }

def calculate_composite_metrics(analyzed_products, fixed_costs_total):
    """
    Çoklu ürün satış karması (Sales Mix) ve bileşik başabaş analizi.
    WACM: Weighted Average Contribution Margin (Ağırlıklı Ortalama Katkı Payı)
    Q*_composite: FC / WACM
    MoS: Margin of Safety (Güvenlik Marjı %)
    DOL: Degree of Operating Leverage (Faaliyet Kaldıracı)
    """
    total_target_q = sum(p["analysis"]["economics"]["target_sales_units"] for p in analyzed_products)
    if total_target_q == 0:
        return {}

    total_cm = sum(
        p["analysis"]["economics"]["contribution_margin"] * p["analysis"]["economics"]["target_sales_units"]
        for p in analyzed_products
    )
    total_revenue = sum(
        p["analysis"]["economics"]["sale_price"] * p["analysis"]["economics"]["target_sales_units"]
        for p in analyzed_products
    )
    
    # Ağırlıklı Ortalama Katkı Payı
    wacm = round(total_cm / total_target_q, 2)
    
    # Bileşik Başabaş Adedi
    composite_breakeven_units = math.ceil(fixed_costs_total / wacm) if wacm > 0 else None
    avg_price = total_revenue / total_target_q
    composite_breakeven_revenue = round(composite_breakeven_units * avg_price, 2) if composite_breakeven_units else None
    
    # Net Kâr
    net_profit = round(total_cm - fixed_costs_total, 2)
    
    # Güvenlik Marjı (Margin of Safety %): (Q_target - Q*) / Q_target * 100
    mos_pct = round(((total_target_q - composite_breakeven_units) / total_target_q) * 100, 2) if composite_breakeven_units and total_target_q > 0 else 0.0
    
    # Faaliyet Kaldıracı (Degree of Operating Leverage): Toplam CM / Net Kâr
    dol = round(total_cm / net_profit, 2) if net_profit > 0 else None

    # Ürün bazında satış karması oranları (w_i) ve başabaş kotaları
    product_mix = []
    for p in analyzed_products:
        q_i = p["analysis"]["economics"]["target_sales_units"]
        w_i = round(q_i / total_target_q, 4)
        quota_i = math.ceil(composite_breakeven_units * w_i) if composite_breakeven_units else 0
        product_mix.append({
            "id": p["id"],
            "name": p["name"],
            "target_units": q_i,
            "mix_weight": w_i,
            "breakeven_quota_units": quota_i
        })

    return {
        "total_target_units": total_target_q,
        "total_projected_revenue": round(total_revenue, 2),
        "total_contribution_margin": round(total_cm, 2),
        "weighted_average_cm": wacm,
        "composite_breakeven_units": composite_breakeven_units,
        "composite_breakeven_revenue": composite_breakeven_revenue,
        "margin_of_safety_pct": mos_pct,
        "degree_of_operating_leverage": dol,
        "net_profit": net_profit,
        "product_mix": product_mix
    }

def main():
    fixed_costs_total = sum(DEFAULT_FIXED_COSTS.values())
    
    analyzed_products = []
    for prod in DEFAULT_PRODUCTS:
        metrics = calculate_product_metrics(prod, fixed_costs_total)
        prod_data = dict(prod)
        prod_data["analysis"] = metrics
        analyzed_products.append(prod_data)

    composite = calculate_composite_metrics(analyzed_products, fixed_costs_total)

    output = {
        "fixed_costs": {
            "items": DEFAULT_FIXED_COSTS,
            "total_monthly": fixed_costs_total
        },
        "products": analyzed_products,
        "portfolio_composite": composite
    }

    output_path = os.path.join(os.path.dirname(__file__), "..", "public", "data", "pricing_data.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("=" * 60)
    print("MicroPricing Mikroiktisadi Analiz Motoru Başarıyla Çalıştırıldı")
    print("=" * 60)
    print(f"Toplam Sabit Maliyet (FC): ₺{fixed_costs_total:,.2f}/ay")
    print("\n--- Tekil Ürün Mikroiktisat Metrikleri ---")
    for p in analyzed_products:
        eco = p["analysis"]["economics"]
        cb = p["analysis"]["cost_breakdown"]
        print(f"• {p['name']}:")
        print(f"   Fiyat (P): ₺{eco['sale_price']} | Değişken Mal. (VC): ₺{cb['total_variable_cost']} | Katkı Payı (CM): ₺{eco['contribution_margin']} (%{eco['contribution_margin_ratio_pct']})")
        print(f"   Başabaş Eşiği (Q*): {eco['breakeven_units']} adet | Hedef Satış: {eco['target_sales_units']} adet -> Net Kâr: ₺{eco['monthly_projected_profit']}")

    print("\n--- Çoklu Satış Karması (Bileşik Model) ---")
    print(f"• Toplam Hedef Satış (Q): {composite['total_target_units']} adet | Toplam Ciro: ₺{composite['total_projected_revenue']}")
    print(f"• Ağırlıklı Ortalama Katkı Payı (WACM): ₺{composite['weighted_average_cm']}")
    print(f"• Bileşik Başabaş Noktası (Q*): {composite['composite_breakeven_units']} toplam ürün (Ciro: ₺{composite['composite_breakeven_revenue']})")
    print(f"• Güvenlik Marjı (MoS): %{composite['margin_of_safety_pct']} | Faaliyet Kaldıracı (DOL): {composite['degree_of_operating_leverage']}")
    print(f"• Konsolide Net Kâr: ₺{composite['net_profit']}")
    print("=" * 60)
    print(f"Veri çıktı dosyası güncellendi: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    main()
