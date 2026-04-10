import pandas as pd
import numpy as np

def main():
    print("Starting Data Analysis...")
    
    input_file = "data/trends_clean.csv"
    
    try:
        # Load the clean CSV from Task 2
        df = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f"Error: Could not find {input_file}. Please run Task 2 first.")
        return

    # Print the shape (rows, columns)
    print(f"\nLoaded data: {df.shape}")
    
    # Print the first 5 rows to inspect the data
    print("\nFirst 5 rows:")
    print(df.head())

    # Calculate and print overall averages using Pandas
    avg_score = df['score'].mean()
    avg_comments = df['num_comments'].mean()
    
    # The ',.0f' formats the number with commas and zero decimal places
    print(f"\nAverage score   : {avg_score:,.0f}")
    print(f"Average comments: {avg_comments:,.0f}")


    print("\n--- NumPy Stats ---")
    
    # Extract the 'score' column as a NumPy array for mathematical operations
    scores_array = df['score'].to_numpy()
    
    # Calculate statistics using NumPy
    mean_score = np.mean(scores_array)
    median_score = np.median(scores_array)
    std_score = np.std(scores_array)
    max_score = np.max(scores_array)
    min_score = np.min(scores_array)

    print(f"Mean score   : {mean_score:,.0f}")
    print(f"Median score : {median_score:,.0f}")
    print(f"Std deviation: {std_score:,.0f}")
    print(f"Max score    : {max_score:,.0f}")
    print(f"Min score    : {min_score:,.0f}")

    # Find the category with the most stories
    # value_counts() sorts by count descending, so index 0 is the highest
    category_counts = df['category'].value_counts()
    top_category_name = category_counts.index[0]
    top_category_count = category_counts.iloc[0]
    print(f"\nMost stories in: {top_category_name} ({top_category_count} stories)")

    # Find the story with the most comments
    # idxmax() gives us the row index where 'num_comments' is at its maximum
    max_comments_idx = df['num_comments'].idxmax()
    top_story_title = df.loc[max_comments_idx, 'title']
    top_story_comments = df.loc[max_comments_idx, 'num_comments']
    print(f"Most commented story: \"{top_story_title}\" — {top_story_comments:,} comments")


    
    # Calculate 'engagement' (comments per upvote)
    # We add +1 to the score to prevent a ZeroDivisionError just in case
    df['engagement'] = df['num_comments'] / (df['score'] + 1)
    
    # Create the boolean 'is_popular' column
    # This evaluates to True if the score is greater than the NumPy mean we calculated earlier
    df['is_popular'] = df['score'] > mean_score

    output_file = "data/trends_analysed.csv"
    
    # Save the updated DataFrame back to a new CSV file
    df.to_csv(output_file, index=False)
    
    print(f"\nSaved to {output_file}")

if __name__ == "__main__":
    main()