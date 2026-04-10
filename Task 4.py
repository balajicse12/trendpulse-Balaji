import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

# ─────────────────────────────────────────────
# STEP 1 — Setup
# ─────────────────────────────────────────────

# Load the analysed CSV produced by Task 3
df = pd.read_csv("data/trends_analysed.csv")
print(f"Loaded {len(df)} rows from data/trends_analysed.csv")

# Create the outputs/ folder if it doesn't already exist
os.makedirs("outputs", exist_ok=True)

# Use a clean built-in style for all charts
plt.style.use("seaborn-v0_8-whitegrid")

# ─────────────────────────────────────────────
# CHART 1 — Top 10 Stories by Score (horizontal bar chart)
# ─────────────────────────────────────────────

# Sort by score descending and take the top 10 rows
top10 = df.sort_values("score", ascending=False).head(10)

# Shorten any title longer than 50 characters so bars fit neatly
# We add "..." to signal that the title was cut
top10 = top10.copy()
top10["short_title"] = top10["title"].apply(
    lambda t: t[:50] + "..." if len(t) > 50 else t
)

fig1, ax1 = plt.subplots(figsize=(10, 6))

# barh draws horizontal bars; we reverse the order so the highest score is at the top
ax1.barh(
    top10["short_title"][::-1],   # y-axis: story titles (reversed)
    top10["score"][::-1],          # x-axis: scores (reversed to match)
    color="#4C72B0",
    edgecolor="white",
    height=0.6,
)

ax1.set_title("Top 10 Stories by Score", fontsize=14, fontweight="bold", pad=12)
ax1.set_xlabel("Score", fontsize=11)
ax1.set_ylabel("Story Title", fontsize=11)

# Add the score value at the end of each bar for easy reading
for i, (score, title) in enumerate(zip(top10["score"][::-1], top10["short_title"][::-1])):
    ax1.text(score + 10, i, str(score), va="center", fontsize=9)

plt.tight_layout()
plt.savefig("outputs/chart1_top_stories.png", dpi=150, bbox_inches="tight")
plt.close()  # Close the figure to free memory before creating the next one
print("Saved outputs/chart1_top_stories.png")

# ─────────────────────────────────────────────
# CHART 2 — Stories per Category (bar chart)
# ─────────────────────────────────────────────

# Count how many stories belong to each category
category_counts = df["category"].value_counts()

# Assign a distinct colour to each category bar
colours = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B2"]

fig2, ax2 = plt.subplots(figsize=(8, 5))

bars = ax2.bar(
    category_counts.index,   # x-axis: category names
    category_counts.values,  # y-axis: story counts
    color=colours[:len(category_counts)],
    edgecolor="white",
    width=0.6,
)

ax2.set_title("Number of Stories per Category", fontsize=14, fontweight="bold", pad=12)
ax2.set_xlabel("Category", fontsize=11)
ax2.set_ylabel("Number of Stories", fontsize=11)

# Label each bar with its count directly above it
for bar in bars:
    ax2.text(
        bar.get_x() + bar.get_width() / 2,   # horizontal centre of bar
        bar.get_height() + 0.3,               # just above the top of the bar
        str(int(bar.get_height())),
        ha="center", va="bottom", fontsize=10
    )

plt.tight_layout()
plt.savefig("outputs/chart2_categories.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved outputs/chart2_categories.png")

# ─────────────────────────────────────────────
# CHART 3 — Score vs Comments (scatter plot)
# ─────────────────────────────────────────────

# Split the DataFrame into popular and non-popular stories
# using the is_popular column added in Task 3
popular     = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

fig3, ax3 = plt.subplots(figsize=(8, 5))

# Plot non-popular stories first (they sit behind popular ones)
ax3.scatter(
    not_popular["score"],
    not_popular["num_comments"],
    color="#AEC6CF",
    alpha=0.7,
    s=60,
    label="Not popular",
    edgecolors="white",
    linewidths=0.5,
)

# Plot popular stories on top in a stronger colour so they stand out
ax3.scatter(
    popular["score"],
    popular["num_comments"],
    color="#C44E52",
    alpha=0.85,
    s=80,
    label="Popular (above avg score)",
    edgecolors="white",
    linewidths=0.5,
)

ax3.set_title("Score vs Number of Comments", fontsize=14, fontweight="bold", pad=12)
ax3.set_xlabel("Score", fontsize=11)
ax3.set_ylabel("Number of Comments", fontsize=11)

# Add a legend so the reader knows which colour means what
ax3.legend(fontsize=10)

plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved outputs/chart3_scatter.png")

# ─────────────────────────────────────────────
# BONUS — Combined Dashboard (all 3 charts in one figure)
# ─────────────────────────────────────────────

# Create a figure with 1 row and 3 columns of subplots side by side
fig, (ax_a, ax_b, ax_c) = plt.subplots(1, 3, figsize=(18, 6))

# ── Dashboard panel A: Top 10 stories ──
ax_a.barh(
    top10["short_title"][::-1],
    top10["score"][::-1],
    color="#4C72B0", edgecolor="white", height=0.6,
)
ax_a.set_title("Top 10 Stories by Score", fontsize=11, fontweight="bold")
ax_a.set_xlabel("Score", fontsize=9)
ax_a.set_ylabel("Story Title", fontsize=9)
ax_a.tick_params(axis="y", labelsize=7)  # smaller font so long titles fit

# ── Dashboard panel B: Stories per category ──
ax_b.bar(
    category_counts.index,
    category_counts.values,
    color=colours[:len(category_counts)],
    edgecolor="white", width=0.6,
)
ax_b.set_title("Stories per Category", fontsize=11, fontweight="bold")
ax_b.set_xlabel("Category", fontsize=9)
ax_b.set_ylabel("Number of Stories", fontsize=9)

# ── Dashboard panel C: Score vs comments scatter ──
ax_c.scatter(
    not_popular["score"], not_popular["num_comments"],
    color="#AEC6CF", alpha=0.7, s=50, label="Not popular",
    edgecolors="white", linewidths=0.5,
)
ax_c.scatter(
    popular["score"], popular["num_comments"],
    color="#C44E52", alpha=0.85, s=65, label="Popular",
    edgecolors="white", linewidths=0.5,
)
ax_c.set_title("Score vs Comments", fontsize=11, fontweight="bold")
ax_c.set_xlabel("Score", fontsize=9)
ax_c.set_ylabel("Number of Comments", fontsize=9)
ax_c.legend(fontsize=8)

# Overall dashboard title sits above all three panels
fig.suptitle("TrendPulse Dashboard", fontsize=16, fontweight="bold", y=1.02)

plt.tight_layout()
plt.savefig("outputs/dashboard.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved outputs/dashboard.png")

print("\nAll charts saved to outputs/")