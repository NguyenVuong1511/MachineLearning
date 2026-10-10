import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def setup_plot(title, xlabel, ylabel, figsize=(10, 6)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    # Ẩn viền trên và viền phải
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    return fig, ax

def add_value_labels(ax, spacing=5, format_str="{:.3f}"):
    for rect in ax.patches:
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2
        
        # Nếu thanh cột quá thấp thì in số ở trên, cao thì in ở trên
        if y_value > 0:
            ax.annotate(format_str.format(y_value),
                        (x_value, y_value),
                        xytext=(0, spacing), 
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=10)

def plot_experiment_2_3_cosine_vs_baseline(fig_dir):
    """Bảng 4.1: So sánh Cosine vs Baseline (tại min_freq = 60)"""
    labels = ['K = 5', 'K = 10', 'K = 20']
    cosine_hr = [0.201, 0.254, 0.312]
    baseline_hr = [0.029, 0.046, 0.069]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = setup_plot('So sánh Hit-rate: Mô hình Cosine vs Baseline (min_freq=60)', '', 'Hit-rate')
    
    ax.bar(x - width/2, cosine_hr, width, label='Cosine', color='#2ca02c')
    ax.bar(x + width/2, baseline_hr, width, label='Baseline', color='#7f7f7f')

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend(loc='upper left')
    add_value_labels(ax)

    plt.tight_layout()
    plt.savefig(fig_dir / '1_cosine_vs_baseline.png', dpi=300)
    plt.close()

def plot_experiment_2_3_hitrate_trend(fig_dir):
    """Bảng 4.1: Xu hướng Hit-rate theo K cho từng min_freq"""
    k_values = [5, 10, 20]
    
    # Dữ liệu Hit-rate cosine
    mf_5 = [0.195, 0.244, 0.303]
    mf_20 = [0.196, 0.246, 0.305]
    mf_60 = [0.201, 0.254, 0.312]
    mf_150 = [0.219, 0.275, 0.344]

    fig, ax = setup_plot('Sự thay đổi của Hit-rate theo K và min_freq', 'Số lượng gợi ý (K)', 'Hit-rate')
    
    ax.plot(k_values, mf_5, marker='o', label='min_freq = 5', color='#1f77b4', linewidth=2)
    ax.plot(k_values, mf_20, marker='s', label='min_freq = 20', color='#ff7f0e', linewidth=2)
    ax.plot(k_values, mf_60, marker='^', label='min_freq = 60', color='#2ca02c', linewidth=2, markersize=8)
    ax.plot(k_values, mf_150, marker='D', label='min_freq = 150', color='#d62728', linewidth=2)

    ax.set_xticks(k_values)
    ax.legend()
    plt.tight_layout()
    plt.savefig(fig_dir / '2_hitrate_trend_by_min_freq.png', dpi=300)
    plt.close()

def plot_experiment_1_representation(fig_dir):
    """Bảng 4.2: So sánh Item-Invoice và Item-Customer"""
    labels = ['K = 5', 'K = 10', 'K = 20']
    item_invoice_hr = [0.201, 0.254, 0.312]
    item_customer_hr = [0.198, 0.262, 0.332]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = setup_plot('So sánh Hit-rate: Item-Invoice vs Item-Customer', '', 'Hit-rate')
    
    ax.bar(x - width/2, item_invoice_hr, width, label='Item-Invoice (Cấu hình chọn)', color='#1f77b4')
    ax.bar(x + width/2, item_customer_hr, width, label='Item-Customer', color='#ffb347')

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend(loc='upper left')
    add_value_labels(ax)

    plt.tight_layout()
    plt.savefig(fig_dir / '3_representation_comparison.png', dpi=300)
    plt.close()

def plot_validation_vs_test(fig_dir):
    """Bảng 4.4: So sánh Validation và Test để chứng minh không data leakage"""
    labels = ['Hit-rate@20 (cosine)', 'Hit-rate@20 (baseline)', 'Coverage@20']
    val_scores = [0.312, 0.069, 0.846]
    test_scores = [0.314, 0.070, 0.844]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = setup_plot('Kiểm chứng rò rỉ dữ liệu: Validation vs Test', '', 'Giá trị')
    
    ax.bar(x - width/2, val_scores, width, label='Tập Validation', color='#9467bd')
    ax.bar(x + width/2, test_scores, width, label='Tập Test', color='#8c564b')

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    add_value_labels(ax)

    plt.tight_layout()
    plt.savefig(fig_dir / '4_val_vs_test.png', dpi=300)
    plt.close()

def plot_error_analysis(fig_dir):
    """Bảng 4.5 & 4.6: Phân tích lỗi theo độ hiếm và kích thước giỏ hàng"""
    # 1. Theo độ hiếm
    rarity_labels = ['60 - 150\n(Hiếm)', '150 - 500\n(Vừa)', '500 - 5k\n(Phổ biến)', '> 5k\n(Rất phổ biến)']
    rarity_hr = [0.000, 0.150, 0.221, 0.447]

    fig, ax = setup_plot('Hit-rate theo mức độ phổ biến của sản phẩm', '', 'Hit-rate')
    ax.bar(rarity_labels, rarity_hr, color='#17becf', width=0.5)
    add_value_labels(ax)
    plt.tight_layout()
    plt.savefig(fig_dir / '5a_error_rarity.png', dpi=300)
    plt.close()

    # 2. Theo kích thước giỏ
    basket_labels = ['2-3 SP', '4-10 SP', '11-30 SP', '> 30 SP']
    basket_hr = [0.447, 0.447, 0.304, 0.164]

    fig, ax = setup_plot('Hit-rate theo kích thước giỏ hàng', '', 'Hit-rate')
    ax.bar(basket_labels, basket_hr, color='#bcbd22', width=0.5)
    add_value_labels(ax)
    plt.tight_layout()
    plt.savefig(fig_dir / '5b_error_basket_size.png', dpi=300)
    plt.close()

def main():
    fig_dir = Path("reports/figures")
    fig_dir.mkdir(parents=True, exist_ok=True)
    
    print("Dang tao bieu do 1: Cosine vs Baseline...")
    plot_experiment_2_3_cosine_vs_baseline(fig_dir)
    
    print("Dang tao bieu do 2: Hit-rate trend...")
    plot_experiment_2_3_hitrate_trend(fig_dir)
    
    print("Dang tao bieu do 3: Item-invoice vs Item-customer...")
    plot_experiment_1_representation(fig_dir)
    
    print("Dang tao bieu do 4: Validation vs Test...")
    plot_validation_vs_test(fig_dir)
    
    print("Dang tao bieu do 5: Phan tich loi...")
    plot_error_analysis(fig_dir)
    
    print(f"Tat ca bieu do da duoc luu tai {fig_dir.absolute()}")

if __name__ == '__main__':
    main()
