import pandas as pd
import glob
import os

def main():
    # 1. Load the JSON File
    # We use glob to find any file starting with 'trends_' and ending in '.json' in the 'data/' folder
    json_files = glob.glob("data/trends_*.json")
    
    if not json_files:
        print("Error: No JSON files found in the 'data/' folder. Please run Task 1 first.")
        return

    # Use the first file found
    input_file = json_files[0]
    
    # Load the data into a DataFrame
    df = pd.read_json(input_file)
    initial_count = len(df)
    print(f"Loaded {initial_count} stories from {input_file}")

    # 2. Clean the Data
    
    # ISSUE: Duplicates - Remove any rows with the same post_id
    df = df.drop_duplicates(subset=['post_id'])
    print(f"After removing duplicates: {len(df)}")

    # ISSUE: Missing values - Drop rows where critical info is missing
    # This removes any row where ID, Title, or Score is null
    df = df.dropna(subset=['post_id', 'title', 'score'])
    print(f"After removing nulls: {len(df)}")

    # ISSUE: Low quality - Remove stories where score is less than 5
    df = df[df['score'] >= 5]
    print(f"After removing low scores: {len(df)}")

    # ISSUE: Data types - Ensure score and num_comments are integers
    # This prevents errors in Task 3 during mathematical analysis
    df['score'] = df['score'].astype(int)
    df['num_comments'] = df['num_comments'].astype(int)

    # ISSUE: Whitespace - Strip extra spaces from the title column
    df['title'] = df['title'].str.strip()

    # 3. Save as CSV
    output_file = "data/trends_clean.csv"
    
    # Ensure the 'data' directory exists (though it should from Task 1)
    os.makedirs("data", exist_ok=True)
    
    # Save the cleaned DataFrame
    df.to_csv(output_file, index=False)
    
    print(f"\nSaved {len(df)} rows to {output_file}")

    # 4. Print Summary: Stories per category
    print("\nStories per category:")
    # value_counts() gives us a quick count of items in each category
    summary = df['category'].value_counts()
    for category, count in summary.items():
        print(f"  {category:<15} {count}")

if __name__ == "__main__":
    main()