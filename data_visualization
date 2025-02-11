# DATA VISUALIZATION



#1) Summary Statistics for District and Tehsil Trends

summary = grouped_data.groupby(['dist_name', 'tehsil_name'])['total_quantity'].describe()
print("Summary Statistics for District and Tehsil Trends:")
print(summary)



#2) Visualizes vaccine usage trends by district and tehsil, plotting individual and multiple trends using subplots. 

import math

#Function to Plot Trends
def plot_trend(district, tehsil):
    # Filter data for the selected district and tehsil
    filtered_data = grouped_data[(grouped_data['dist_name'] == district) &
                                 (grouped_data['tehsil_name'] == tehsil)]

    if filtered_data.empty:
        print(f"No data found for district '{district}' and tehsil '{tehsil}'. Please check the names.")
        return

    # Plot the trend
    plt.figure(figsize=(10, 4))
    plt.plot(filtered_data['transaction_month'], filtered_data['total_quantity'],
             marker='o', color='b', label=f'Total Quantity in {tehsil} Tehsil, {district} District')
    plt.title(f'Trend of Total Quantity in {district} District ({tehsil} Tehsil)', fontsize=14)
    plt.xlabel('Month', fontsize=12)
    plt.ylabel('Total Quantity', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.show()

# Get all unique district and tehsil combinations
district_tehsil_combinations = grouped_data[['dist_name', 'tehsil_name']].drop_duplicates()

# Calculate number of rows and columns for subplots
num_plots = len(district_tehsil_combinations)
cols = 3  # Adjust based on how many columns you want per row
rows = math.ceil(num_plots / cols)

# Create subplots
fig, axes = plt.subplots(rows, cols, figsize=(20, rows * 5))
axes = axes.flatten()  # Flatten to iterate over axes easily

for i, (district, tehsil) in enumerate(district_tehsil_combinations.values):
    # Filter data for each combination
    filtered_data = grouped_data[(grouped_data['dist_name'] == district) &
                                 (grouped_data['tehsil_name'] == tehsil)]

    if not filtered_data.empty:
        # Plot the trend on the respective subplot
        ax = axes[i]
        ax.plot(filtered_data['transaction_month'], filtered_data['total_quantity'],
                color = 'black', marker='o', label=f'{tehsil}, {district}')
        ax.set_title(f'{tehsil} ({district})', fontsize=10)
        ax.set_xlabel('Month', fontsize=8)
        ax.set_ylabel('Total Quantity', fontsize=8)
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.legend(fontsize=8)

# Remove empty subplots
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

# Adjust layout
plt.tight_layout()
plt.show()



#3)  Overall trend of total vaccine quantity used over time by summing data across all districts and tehsils.

# Total quantity over time (all districts and tehsils)
overall_trend = data.groupby('transaction_month')['total_quantity'].sum()

# Plot overall trend
plt.figure(figsize=(12, 6))
plt.plot(overall_trend.index, overall_trend.values, marker='o', color='purple', label='Total Quantity (Overall)')
plt.title('Overall Trend of Total Quantity Over Time', fontsize=14)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Total Quantity', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.show()



#4) Plotting a horizontal bar chart showing the total vaccine quantity distributed in each district.

# Aggregate data by district
district_trends = data.groupby('dist_name')['total_quantity'].sum().sort_values()

# Plot district-wise trends
plt.figure(figsize=(12, 6))
district_trends.plot(kind='barh', color='skyblue')
plt.title('Total Quantity by District', fontsize=14)
plt.xlabel('Total Quantity', fontsize=12)
plt.ylabel('District', fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.6)
plt.show()



#5) Creating a grid of bar charts, each showing the total vaccine quantity distributed across tehsils within a district.

import math

# Get unique districts
districts = data['dist_name'].unique()

# Calculate rows and columns for subplots
num_districts = len(districts)
cols = 3  # Number of columns in the subplot grid
rows = math.ceil(num_districts / cols)  # Number of rows needed

# Create a figure with subplots
fig, axes = plt.subplots(rows, cols, figsize=(20, rows * 5))
axes = axes.flatten()  # Flatten to iterate over axes easily

for i, district in enumerate(districts):
    # Group data by tehsil for the current district
    tehsil_trends = data[data['dist_name'] == district].groupby('tehsil_name')['total_quantity'].sum().sort_values()

    if not tehsil_trends.empty:
        # Plot on the respective subplot
        ax = axes[i]
        tehsil_trends.plot(kind='barh', color='pink', ax=ax)
        ax.set_title(f'{district} District', fontsize=12)
        ax.set_xlabel('Total Quantity', fontsize=10)
        ax.set_ylabel('Tehsil', fontsize=10)
        ax.grid(axis='x', linestyle='--', alpha=0.6)

# Remove unused subplots
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

# Adjust layout and display
plt.tight_layout()
plt.show()



#6) Generating a heatmap to visualize the total vaccine quantity distributed across districts over time.

import seaborn as sns

# Prepare data for heatmap: Group by month and district
heatmap_data = data.groupby(['transaction_month', 'dist_name'])['total_quantity'].sum().unstack()

# Format the index to show only the date part
heatmap_data.index = heatmap_data.index.strftime('%Y-%m-%d')  # Format dates as YYYY-MM-DD

# Plot heatmap
plt.figure(figsize=(14, 8))
sns.heatmap(heatmap_data, cmap='flare', annot=True, fmt='.0f', linewidths=0.5)
plt.title('Heatmap of Total Quantities Over Time by District', fontsize=16)
plt.xlabel('District', fontsize=12)
plt.ylabel('Month', fontsize=12)
plt.show()



#7) Creating a boxplot to analyze any seasonal trends in total vaccine quantities by month.

# Extract month names for seasonal trends
data['month'] = data['transaction_month'].dt.month_name()

# Plot boxplot for seasonal trends
plt.figure(figsize=(14, 6))
sns.boxplot(x='month', y='total_quantity', data=data, order=[
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'],palette='rocket')
plt.title('Seasonal Trends in Total Quantities', fontsize=16)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Total Quantity', fontsize=12)
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.show()
