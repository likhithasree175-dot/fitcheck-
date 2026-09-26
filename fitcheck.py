"""
Fit Check — Fashion Style DNA
A terminal quiz that scores your outfit picks against five style archetypes
and reveals your dominant fashion style, with a matplotlib chart at the end.

No extra installs needed beyond matplotlib (which you already had).
Colors use plain ANSI escape codes, built into every terminal.
"""

import time
import matplotlib.pyplot as plt

# ---------------- ANSI colors (no external library needed) ----------------
class C:
    PINK = "\033[38;5;198m"
    LIME = "\033[38;5;154m"
    LILAC = "\033[38;5;183m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"


STYLES = ["Trendy", "Classic", "Boho", "Minimalist", "Ethnic"]
EMOJI = {"Trendy": "🔥", "Classic": "🖤", "Boho": "🌾", "Minimalist": "◻️", "Ethnic": "🪔"}
TAGLINE = {
    "Trendy": "it's giving main character energy, no cap",
    "Classic": "quiet confidence, zero notes, always iconic",
    "Boho": "free spirit era, mixed prints and no rules",
    "Minimalist": "less noise, more intention — quiet luxury",
    "Ethnic": "roots on lock, culture certified, unbothered",
}

QUESTIONS = [
    {
        "question": "1. Pick your go-to weekend outfit:",
        "options": {
            "a": ("Ripped jeans + graphic tee", {"Trendy": 3}),
            "b": ("Plain white shirt + tailored pants", {"Classic": 3}),
            "c": ("Flowy printed dress + layered jewelry", {"Boho": 3}),
            "d": ("Solid color basics, clean lines", {"Minimalist": 3}),
            "e": ("Kurti + dupatta", {"Ethnic": 3}),
        },
    },
    {
        "question": "2. Your favorite color palette:",
        "options": {
            "a": ("Bold neons and bright colors", {"Trendy": 2}),
            "b": ("Black, white, navy", {"Classic": 2}),
            "c": ("Earthy tones - mustard, rust, olive", {"Boho": 2}),
            "d": ("Beige, white, grey", {"Minimalist": 2}),
            "e": ("Reds, golds, jewel tones", {"Ethnic": 2}),
        },
    },
    {
        "question": "3. Accessories you reach for:",
        "options": {
            "a": ("Statement sneakers, chunky jewelry", {"Trendy": 2}),
            "b": ("Simple watch, leather belt", {"Classic": 2}),
            "c": ("Layered bracelets, anklets", {"Boho": 2}),
            "d": ("None, or one small piece", {"Minimalist": 2}),
            "e": ("Jhumkas, bangles", {"Ethnic": 2}),
        },
    },
    {
        "question": "4. Your dream festival/event outfit:",
        "options": {
            "a": ("Something viral from Instagram", {"Trendy": 3}),
            "b": ("A timeless, well-tailored outfit", {"Classic": 3}),
            "c": ("Free-flowing, mixed prints", {"Boho": 3}),
            "d": ("Clean, monochrome fit", {"Minimalist": 3}),
            "e": ("Traditional saree or lehenga", {"Ethnic": 3}),
        },
    },
    {
        "question": "5. How do you shop?",
        "options": {
            "a": ("Whatever's trending this week", {"Trendy": 2}),
            "b": ("Investment pieces that last years", {"Classic": 2}),
            "c": ("Unique finds, thrift stores", {"Boho": 2}),
            "d": ("Only what I truly need", {"Minimalist": 2}),
            "e": ("Festive and family-function wear", {"Ethnic": 2}),
        },
    },
]



def progress_bar(done, total, width=30):
    filled = int(width * (done / total))
    bar = C.LIME + "#" * filled + C.DIM + "-" * (width - filled) + C.RESET
    return f"[{bar}] {done}/{total}"


def run_quiz():
    """Ask each question and collect scores."""
    scores = {style: 0 for style in STYLES}

    for i, q in enumerate(QUESTIONS, start=1):
        print(progress_bar(i - 1, len(QUESTIONS)))
        print(f"\n{C.BOLD}{q['question']}{C.RESET}")
        for key, (text, _) in q["options"].items():
            print(f"   {C.LILAC}{key}){C.RESET} {text}")

        answer = input(f"\n{C.PINK}>{C.RESET} spill the tea (a/b/c/d/e): ").strip().lower()
        while answer not in q["options"]:
            answer = input(f"{C.PINK}>{C.RESET} bestie that's not an option, try again (a/b/c/d/e): ").strip().lower()

        _, points = q["options"][answer]
        for style, pts in points.items():
            scores[style] += pts
        print()

    print(progress_bar(len(QUESTIONS), len(QUESTIONS)))
    return scores


def show_result(scores):
    """Print a text summary and the dominant style, with a short reveal beat."""
    total = sum(scores.values())
    percentages = {style: round((score / total) * 100, 1) if total else 0 for style, score in scores.items()}
    dominant_style = max(scores, key=scores.get)

    print(f"\n{C.LILAC}the algorithm is cooking...{C.RESET}")
    time.sleep(0.6)

    print(f"\n{C.BOLD}===== YOUR FASHION STYLE DNA ====={C.RESET}\n")
    for style, pct in sorted(percentages.items(), key=lambda kv: kv[1], reverse=True):
        bar_len = int(pct / 2.5)  # scale to ~40 chars max
        color = C.LIME if style == dominant_style else C.LILAC
        bar = color + "#" * bar_len + C.RESET
        tag = f"{C.BOLD}{C.LIME} <- dominant{C.RESET}" if style == dominant_style else ""
        print(f"  {EMOJI[style]} {style:<11} {bar} {pct:>5.1f}%{tag}")

    print(f"\n{C.PINK}{C.BOLD}>> bestie... it's giving: {dominant_style} {EMOJI[dominant_style]}{C.RESET}")
    print(f"{C.LILAC}{TAGLINE[dominant_style]}{C.RESET}")
    print(C.BOLD + "===================================\n" + C.RESET)

    return percentages, dominant_style


def save_report(percentages, dominant_style):
    """Save the result to a text file."""
    with open("fashion_style_report.txt", "w", encoding="utf-8") as f:
        f.write("FASHION STYLE DNA REPORT\n")
        f.write("=" * 30 + "\n")
        for style, pct in percentages.items():
            f.write(f"{style}: {pct}%\n")
        f.write(f"\nDominant Style: {dominant_style}\n")
        f.write(f"Vibe: {TAGLINE[dominant_style]}\n")
    print(f"{C.DIM}report saved as 'fashion_style_report.txt' — screenshot-worthy, just saying{C.RESET}")


def show_chart(percentages, dominant_style):
    """Show a styled bar chart of the style breakdown."""
    styles = list(percentages.keys())
    values = list(percentages.values())
    colors = ["#C8FF4D" if s == dominant_style else "#C9B6FF" for s in styles]

    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor("#180B1F")
    ax.set_facecolor("#180B1F")

    bars = ax.bar(styles, values, color=colors, edgecolor="none", width=0.6)
    ax.set_title(f"Fit Check — Fashion Style DNA  (Dominant: {dominant_style})",
                 color="#FF2E93", fontsize=13, fontweight="bold", pad=14)
    ax.set_ylabel("Match Percentage (%)")
    ax.set_ylim(0, 100)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)

    for bar, v in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 2, f"{v}%",
                 ha="center", fontweight="bold", color="white")

    plt.tight_layout()
    plt.savefig("fashion_style_chart.png", facecolor=fig.get_facecolor())
    print(f"{C.DIM}chart saved as 'fashion_style_chart.png' — post it, don't overthink it{C.RESET}")
    plt.show()


def main():
    print("the assignment: answer 5 questions, find out your fit's whole personality.\n")

    scores = run_quiz()
    percentages, dominant_style = show_result(scores)
    save_report(percentages, dominant_style)
    show_chart(percentages, dominant_style)


if __name__ == "__main__":
    main()
