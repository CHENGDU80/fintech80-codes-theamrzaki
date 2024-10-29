import numpy as np
import matplotlib.pyplot as plt

def agg_dynamic():
    # Constants
    L_base = 50000  # Base liability (min liability)
    k = 2           # Exponential growth factor
    P_base = 200    # Base monthly premium
    m = 10          # Premium increase factor

    # Function to calculate liability
    def calculate_liability(ratio, base_liability, growth_factor, multiplier):
        return base_liability * np.exp(growth_factor * ratio * multiplier)

    # Function to calculate premium
    def calculate_premium(ratio, base_premium, increase_factor):
        return base_premium + increase_factor * ratio * 100  # Increase with the ratio

    # Calculate ratio of aggressive to non-aggressive behavior
    ratios = np.linspace(0, 1, 5)  # Reduced resolution to 5 points

    # Calculate liabilities using the functions
    liabilities_total_coverage = calculate_liability(ratios, L_base, k, 0.8)  # Total Coverage
    liabilities_economic = calculate_liability(ratios, L_base, k, 0.6)         # Economic
    liabilities_balanced = calculate_liability(ratios, L_base, k, 0.7)         # Balanced

    # Calculate premiums using the function
    premiums_total_coverage = calculate_premium(ratios, P_base, m)     # Total Coverage
    premiums_economic = calculate_premium(ratios, P_base, m * 0.8)     # Economic
    premiums_balanced = calculate_premium(ratios, P_base, m * 0.9)     # Balanced

    L_base = 50000  # Base liability (min liability)
    k = 2           # Exponential growth factor

    # Compute max liabilities for normalization
    max_liabilities = {
        'Total Coverage': L_base * np.exp(k * 1 * 0.8),
        'Economic': L_base * np.exp(k * 1 * 0.6),
        'Balanced': L_base * np.exp(k * 1 * 0.7)
    }



    liabilities = {
        'Total Coverage': liabilities_total_coverage.tolist(),
        'Economic': liabilities_economic.tolist(),
        'Balanced': liabilities_balanced.tolist()
    }
    premiums = {
        'Total Coverage': premiums_total_coverage.tolist(),
        'Economic': premiums_economic.tolist(),
        'Balanced': premiums_balanced.tolist()
    }

    # Normalize liabilities
    liabilities_normalized = {}
    for policy in liabilities:
        max_liability = max_liabilities[policy]
        liabilities_normalized[policy] = [
            (liability) / (max_liability - L_base) for liability in liabilities[policy]
        ]

    for idx, val in enumerate(liabilities_normalized[policy]):
        if val >= 1:
            liabilities_normalized[policy][idx] = 1
    return liabilities, premiums, ratios.tolist()

if __name__ == "__main__":
    liabilities, premiums, ratios = agg_dynamic()

    # Plotting
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Bar plot for normalized liabilities
    width = 0.2  # Width of the bars
    bar_positions = np.arange(len(ratios))  # Bar positions

    # Create bar plots with correct spacing
    ax1.bar(bar_positions - width, liabilities["Total Coverage"], width=width,
            label="Total Coverage Liability", alpha=0.7)
    ax1.bar(bar_positions, liabilities["Economic"], width=width,
            label="Economic Liability", alpha=0.7)
    ax1.bar(bar_positions + width, liabilities["Balanced"], width=width,
            label="Balanced Liability", alpha=0.7)

    ax1.set_xlabel("Aggressive to Non-Aggressive Ratio")
    ax1.set_ylabel("Normalized Liability (0 to 1)", color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.set_xticks(bar_positions)  # Set x-tick positions to the bar positions
    ax1.set_xticklabels([f"{ratio:.1f}" for ratio in ratios])  # Set x-tick labels to show ratio values

    # Create a secondary y-axis for premiums
    ax2 = ax1.twinx()

    # Adjusted x-coordinates for line plots to align with the center of the grouped bars
    ax2.plot(bar_positions - width, premiums["Total Coverage"], label="Total Coverage Premium",
             linestyle='-', marker='o', color='black')
    ax2.plot(bar_positions, premiums["Economic"], label="Economic Premium",
             linestyle='--', marker='s', color='red')
    ax2.plot(bar_positions + width, premiums["Balanced"], label="Balanced Premium",
             linestyle='-.', marker='^', color='green')

    ax2.set_ylabel("Monthly Premium ($)", color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    # Add legends for clarity
    ax1.legend(loc="upper left")
    ax2.legend(loc="center left")

    # Show the plot
    plt.title("Insurance Policy Normalized Liability (Bar) and Premium (Line) vs. Aggressive Behavior Ratio")
    plt.grid(True)  # Optional: Add grid for better readability
    plt.show()
