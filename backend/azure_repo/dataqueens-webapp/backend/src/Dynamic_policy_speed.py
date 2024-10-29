import pandas as pd
import random
import math


def speed_dynamic():
    # Load dataset
    file_path = 'data/2023-12-29 15-16-43.csv'  # Replace with your actual file path
    data = pd.read_csv(file_path)

    # Define constants for liability and premium calculations
    L_base = 50000  # Base liability (max liability)
    P_base = 250     # Base monthly premium
    k = 500         # Liability reduction factor
    m = 0.01           # Premium increase factor

    # Ensure dataset has at least 10 rows
    if len(data) < 10:
        raise ValueError("Dataset has fewer than 10 rows. Please provide a larger dataset.")

    # Select 10 consecutive random rows for speed samples
    start_index = random.randint(0, len(data) - 500)
    sample_data = data.iloc[start_index:start_index + 500]
    speeds = [None if math.isnan(sample) else sample for sample in sample_data["Vehicle speed (km/h)"]]

    # Define scoring functions for each policy
    def calculate_scores(speed):
        if speed is not None:
            return {
                'Total Coverage': 0.1 * speed + 0.2 * (L_base - k * speed) + 0.3 * (L_base - k * speed),
                'Economic': 0.7 * speed + 0.7 * (L_base - k * speed) + 0.7 * (L_base - k * speed),
                'Balanced': 0.3 * speed + 0.3 * (L_base - k * speed) + 0.4 * (L_base - k * speed)
            }
        else:
            return {
                'Total Coverage':0,
                'Economic': 0,
                'Balanced': 0
            }

    # Calculate liabilities and premiums for each policy based on speed
    liabilities = {'Total Coverage': [], 'Economic': [], 'Balanced': []}
    premiums = {'Total Coverage': [], 'Economic': [], 'Balanced': []}

    for speed in speeds:
        scores = calculate_scores(speed)
        for policy, score in scores.items():
            liabilities_val = L_base - k * score * score
            premium_val = P_base + m * (L_base - score)
            liabilities[policy].append(None if math.isnan(liabilities_val) else liabilities_val)
            premiums[policy].append(None if math.isnan(premium_val) else premium_val)

    L_base = 50000  # Max liability for normalization

    # Normalize liabilities
    liabilities_normalized = {}
    for policy in liabilities:
        liabilities_normalized[policy] = [
            (liability / L_base) if liability is not None else 0 
            for liability in liabilities[policy]
        ]

    return liabilities_normalized,premiums,speeds

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    liabilities, premiums, speeds = speed_dynamic()

    # Plot speed on the x-axis and normalized liability/premium on the y-axes
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Plot normalized liability for each policy in the desired order
    liability_order = ['Economic', 'Balanced', 'Total Coverage']
    for policy in liability_order:
        ax1.plot(speeds, liabilities[policy], label=f"{policy} Liability", linestyle='-', marker='o')
    ax1.set_xlabel("Avg Speed (km/h)")
    ax1.set_ylabel("Normalized Liability (0 to 1)", color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Create a secondary y-axis for premiums
    ax2 = ax1.twinx()
    premium_order = ['Economic', 'Balanced', 'Total Coverage']
    for policy in premium_order:
        ax2.plot(speeds, premiums[policy], label=f"{policy} Premium", linestyle='--', marker='x')
    ax2.set_ylabel("Monthly Premium ($)", color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    # Add legends for clarity
    ax1.legend(loc="lower center")
    ax2.legend(loc="lower right")

    # Show the plot
    plt.title("Insurance Policy Liability and Premium vs. Speed")
    plt.grid(True)  # Optional: Add grid for better readability
    plt.show()
