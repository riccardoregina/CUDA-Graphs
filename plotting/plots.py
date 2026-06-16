import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import curve_fit

# Set global aesthetics for Matplotlib/Seaborn
plt.rcParams.update({
    'font.size': 18,
    'axes.labelsize': 18,
    'xtick.labelsize': 15,
    'ytick.labelsize': 15,
    'legend.fontsize': 15,
})
sns.set_theme(style="whitegrid", rc={
    'font.size': 18,
    'axes.labelsize': 18,
    'xtick.labelsize': 15,
    'ytick.labelsize': 15,
    'legend.fontsize': 15,
})

COLORS = {1000: 'tab:blue', 1000000: 'tab:orange', 10000000: 'tab:green'}

def get_label(t):
    if t == 1000: return "Threads 1e+03"
    elif t == 1000000: return "Threads 1e+06"
    elif t == 10000000: return "Threads 1e+07"
    else: return f"Threads {t:.0e}".replace("e+0", "e+").replace("e+", "e+0")

def plot_figure_2(csv_path='../application/output/output_increase_nodes.csv', output_dir='.'):
    if not os.path.exists(csv_path):
        print(f"File not found: {csv_path}")
        return
        
    df = pd.read_csv(csv_path)
    # Filter for graph mode if multiple modes exist, assuming mode 1 is graph
    if 'mode' in df.columns and 1 in df['mode'].unique():
        df = df[df['mode'] == 1]
    
    fig, ax1 = plt.subplots(figsize=(12, 8))
    ax2 = ax1.twinx()
    
    threads = sorted(df['threads'].unique())
    
    for i, t in enumerate(threads):
        df_t = df[df['threads'] == t].sort_values('mini_batch_size')
        x = df_t['mini_batch_size'].values
        y_line = df_t['graph_creation_mean'].values
        y_err = df_t['graph_creation_std'].values
        y_bar = df_t['gpu_memory_mib'].values
        
        color = COLORS.get(t, 'black')
        label = get_label(t)
        
        # Line plot on left axis
        ax1.plot(x, y_line, marker='o', color=color, label=f"{label} (Creation)", linewidth=2)
        ax1.fill_between(x, y_line - y_err, y_line + y_err, color=color, alpha=0.2)
        
        # Bar plot dodging: offset is -width, 0, +width
        # Dynamic width to scale correctly on linear x-axis
        w = x * 0.1
        offset = (i - 1) * w
        
        ax2.bar(x + offset, y_bar, width=w, color=color, alpha=0.3, edgecolor='none', label=f"{label} (Mem)")

    ax1.set_xlabel('mini_batch_size')
    ax1.set_ylabel('Graph Creation Time Mean (s)')
    ax2.set_ylabel('GPU Memory (MiB)')
    
    # Combine legends carefully
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left', framealpha=0.9)
    
    plt.title('Graph Creation Overhead and Memory Usage')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'figure_2.png'), dpi=300)
    plt.close()

def plot_figure_3(csv_path='../application/output/output_increase_nodes.csv', output_dir='.'):
    if not os.path.exists(csv_path):
        print(f"File not found: {csv_path}")
        return
        
    df = pd.read_csv(csv_path)
    if 'mode' in df.columns and 1 in df['mode'].unique():
        df = df[df['mode'] == 1]
    
    fig, ax1 = plt.subplots(figsize=(14, 8))
    ax2 = ax1.twinx()
    ax3 = ax1.twinx()
    
    # Crucial instruction: move the third axis outwards
    ax3.spines['right'].set_position(('outward', 60))
    
    # Function to fit: T_E = a/S + b
    def fit_func(S, a, b):
        return a / S + b

    axes = [ax1, ax2, ax3]
    threads = sorted(df['threads'].unique())
    
    ax1.set_xlabel('mini_batch_size')
    ax1.set_xscale('log')
    
    for i, t in enumerate(threads):
        df_t = df[df['threads'] == t].sort_values('mini_batch_size')
        x = df_t['mini_batch_size'].values
        y = df_t['exec_time_mean'].values
        y_err = df_t['exec_time_std'].values
        
        color = COLORS.get(t, 'black')
        label = get_label(t)
        
        ax = axes[i]
        
        # Plot empirical data
        ax.plot(x, y, color=color, marker='o', linestyle='--', alpha=0.5, label=f'{label} (Data)')
        ax.fill_between(x, y - y_err, y + y_err, color=color, alpha=0.2)
        
        # Fit curve
        try:
            popt, _ = curve_fit(fit_func, x, y, bounds=(0, np.inf))
            x_fit = np.logspace(np.log10(x.min()), np.log10(x.max()), 500)
            y_fit = fit_func(x_fit, *popt)
            ax.plot(x_fit, y_fit, color=color, linewidth=3, linestyle='-', label=f'{label} (Fitted)')
        except Exception as e:
            print(f"Could not fit curve for {label}: {e}")
            
        ax.set_ylabel(f'Exec Time (s) - {label}', color=color)
        ax.tick_params(axis='y', labelcolor=color)

    # Combine legends
    lines, labels = [], []
    for ax in axes:
        l, lab = ax.get_legend_handles_labels()
        lines.extend(l)
        labels.extend(lab)
    
    # Place legend so it doesn't overlap data
    ax1.legend(lines, labels, loc='upper right', bbox_to_anchor=(0.95, 0.95), framealpha=0.9)
    
    plt.title('Graph Execution Time')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'figure_3.png'), dpi=300)
    plt.close()

def plot_figure_4(csv_path='../application/output/output_increase_nodes.csv', output_dir='.'):
    if not os.path.exists(csv_path):
        print(f"File not found: {csv_path}")
        return
        
    df = pd.read_csv(csv_path)
    if 'mode' in df.columns:
        df = df[df['mode'] == 1].copy()
    
    df['Total_Time'] = df['graph_creation_mean'] + df['exec_time_mean']
    df['Total_Time_std'] = np.sqrt(df['graph_creation_std']**2 + df['exec_time_std']**2)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xscale('log')
    
    # Function to fit: Total Time = A*S + B/S + C
    def fit_func(S, A, B, C):
        return A * S + B / S + C
        
    threads = sorted(df['threads'].unique())
    
    for t in threads:
        df_t = df[df['threads'] == t].sort_values('mini_batch_size')
        x = df_t['mini_batch_size'].values
        y_total = df_t['Total_Time'].values
        y_err = df_t['Total_Time_std'].values
        
        min_emp = np.min(y_total)
        ratio_emp = y_total / min_emp
        ratio_err = y_err / min_emp
        
        color = COLORS.get(t, 'black')
        label = get_label(t)
        
        # Plot real data
        ax.plot(x, ratio_emp, marker='o', linestyle='--', color=color, alpha=0.5, label=f'{label} (Data)')
        ax.fill_between(x, ratio_emp - ratio_err, ratio_emp + ratio_err, color=color, alpha=0.2)
        
        # Fit curve
        try:
            p0 = [1e-6, 1e-2, 1e-2]
            popt, _ = curve_fit(fit_func, x, y_total, p0=p0, bounds=(0, np.inf), maxfev=10000)
            A, B, C = popt
            
            # Theoretical min occurs at S = sqrt(B/A)
            S_min = np.sqrt(B / A)
            min_teorico = fit_func(S_min, A, B, C)
            
            x_fit = np.logspace(np.log10(x.min()), np.log10(x.max()), 500)
            y_fit = fit_func(x_fit, A, B, C)
            ratio_fit = y_fit / min_teorico
            
            ax.plot(x_fit, ratio_fit, color=color, linewidth=3, label=f'{label} (Fitted)')
        except Exception as e:
            print(f"Could not fit curve for {label}: {e}")
            
    ax.set_xlabel('mini_batch_size')
    ax.set_ylabel('Ratio (Total Time / Min Total Time)')
    ax.legend(loc='upper right', framealpha=0.9)
    plt.title('Optimal Batch Size (U-Curve Ratio)')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'figure_4.png'), dpi=300)
    plt.close()

def plot_figure_6(csv_base_path='../application/output/output_kernels_increase_it.csv', 
                  csv_graph_path='../application/output/output_graph_increase_it.csv', 
                  output_dir='.'):
    if not os.path.exists(csv_base_path):
        print(f"File not found: {csv_base_path}. Make sure to generate this data first.")
        return
    if not os.path.exists(csv_graph_path):
        print(f"File not found: {csv_graph_path}. Make sure to generate this data first.")
        return
        
    df_base_full = pd.read_csv(csv_base_path)
    df_graph_full = pd.read_csv(csv_graph_path)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    threads = sorted(df_base_full['threads'].unique())
    
    for t in threads:
        df_base = df_base_full[df_base_full['threads'] == t].sort_values('outer_iterations')
        df_graph = df_graph_full[df_graph_full['threads'] == t].sort_values('outer_iterations')
        
        # Merge on outer_iterations to align data
        merged = pd.merge(df_base, df_graph, on='outer_iterations', suffixes=('_base', '_graph'))
        
        if merged.empty:
            continue
            
        x = merged['outer_iterations'].values
        mean_base = merged['exec_time_mean_base'].values
        std_base = merged['exec_time_std_base'].values
        mean_graph = merged['exec_time_mean_graph'].values
        std_graph = merged['exec_time_std_graph'].values
        
        speedup = mean_base / mean_graph
        err = speedup * np.sqrt((std_base / mean_base)**2 + (std_graph / mean_graph)**2)
        
        color = COLORS.get(t, 'black')
        label = get_label(t)
        
        ax.plot(x, speedup, marker='o', color=color, linewidth=2, label=label)
        ax.fill_between(x, speedup - err, speedup + err, color=color, alpha=0.2)

    ax.axhline(1.0, color='red', linestyle='--', linewidth=2, label='Break-even (Y=1.0)')
    ax.set_xlabel('outer_iterations')
    ax.set_ylabel('Speed-up (Baseline / Graph)')
    ax.set_ylim(0, 3.5)
    ax.legend(loc='upper left', framealpha=0.9)
    plt.title('Speed-up: Baseline vs Graph')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'figure_6.png'), dpi=300)
    plt.close()

if __name__ == '__main__':
    # Define directories
    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(base_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Path to CSV files
    app_output_dir = os.path.join(base_dir, '..', 'application', 'output')
    csv_nodes = os.path.join(app_output_dir, 'output_increase_nodes.csv')
    csv_kernels = os.path.join(app_output_dir, 'output_kernels_increase_it.csv')
    csv_graph = os.path.join(app_output_dir, 'output_graph_increase_it.csv')
    
    print("Generating Figure 2...")
    plot_figure_2(csv_path=csv_nodes, output_dir=output_dir)
    
    print("Generating Figure 3...")
    plot_figure_3(csv_path=csv_nodes, output_dir=output_dir)
    
    print("Generating Figure 4...")
    plot_figure_4(csv_path=csv_nodes, output_dir=output_dir)
    
    print("Generating Figure 6...")
    plot_figure_6(csv_base_path=csv_kernels, csv_graph_path=csv_graph, output_dir=output_dir)
    
    print(f"All plots have been saved to {output_dir}")
