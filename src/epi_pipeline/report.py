from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt


def plot_district(df: pd.DataFrame, district: str, out_path: str) -> None:
    """Plots and saves a single district's time series chart."""
    d = df[df["district"] == district].copy()
    if d.empty:
        return

    # Ensure week column is datetime for clean plot axis formatting
    d["week"] = pd.to_datetime(d["week"])

    # Ensure target output folder exists
    out_file = Path(out_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(d["week"], d["cases"], label="Cases")

    if "threshold" in d.columns:
        ax.plot(d["week"], d["threshold"], "--", label="Alert threshold")

    # Flexible check for alert/outbreak column
    alert_col = "alert" if "alert" in d.columns else "outbreak"
    if alert_col in d.columns:
        a = d[d[alert_col] == True]
        if not a.empty:
            ax.scatter(a["week"], a["cases"], color="red", zorder=3, label="Alert")

    ax.set_title(district)
    ax.set_xlabel("Week")
    ax.set_ylabel("Cases")
    ax.legend()
    fig.savefig(out_file, dpi=150, bbox_inches="tight")
    plt.close(fig)


def generate_report(
    df: pd.DataFrame, 
    report_path: str = "results/report.md", 
    charts_dir: str = "results/charts"
) -> None:
    """
    Generates PNG charts for all unique districts and creates the markdown report.
    """
    df = df.copy()
    df["week"] = pd.to_datetime(df["week"])

    # 1. Loop through all districts and save individual PNG charts
    for district in df["district"].unique():
        chart_path = f"{charts_dir}/{district}.png"
        plot_district(df, district, chart_path)

    # 2. Write executive results/report.md file
    out_file = Path(report_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)

    alert_col = "alert" if "alert" in df.columns else "outbreak"
    alerts_df = df[df[alert_col] == True] if alert_col in df.columns else pd.DataFrame()

    lines = [
        "# Epidemiological Surveillance Report\n",
        f"**Total Districts Monitored:** {df['district'].nunique()}",
        f"**Surveillance Period:** {df['week'].min().strftime('%Y-%m-%d')} to {df['week'].max().strftime('%Y-%m-%d')}\n",
        "## Flagged Outbreak Alerts\n"
    ]

    if not alerts_df.empty:
        lines.append("| District | Week | Cases | Threshold |")
        lines.append("| --- | --- | --- | --- |")
        for _, row in alerts_df.iterrows():
            week_str = row["week"].strftime("%Y-%m-%d")
            cases_val = int(row["cases"]) if pd.notna(row["cases"]) else "N/A"
            thresh = round(row["threshold"], 1) if "threshold" in row and pd.notna(row["threshold"]) else "N/A"
            lines.append(f"| {row['district']} | {week_str} | {cases_val} | {thresh} |")
    else:
        lines.append("No outbreak alerts detected during this period.")

    out_file.write_text("\n".join(lines))