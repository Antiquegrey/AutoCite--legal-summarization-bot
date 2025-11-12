import os
import asyncio
from backend_api import processing  # Import your processing file
import time

# --- Configuration ---
SOURCE_DIR = "full_texts"     # Folder with your 50 legal docs
OUTPUT_DIR = "model_summaries"  # Where to save Gemini's summaries
# ---------------------

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

async def process_file(filename):
    """Reads a file, sends it to Gemini, and saves the summary."""
    
    # --- NEW: Check if summary already exists ---
    output_path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(output_path):
        print(f"  SKIPPING {filename}: Summary already exists.")
        return
    # --- END NEW BLOCK ---

    print(f"Processing {filename}...")
    
    # Read the source text
    try:
        with open(os.path.join(SOURCE_DIR, filename), 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print(f"  ERROR reading {filename}: {e}")
        return

    # Call your Gemini function
    try:
        llm_response = await processing.analyze_legal_text_with_gemini(text)
        
        # Extract just the summary
        summary, _ = processing.extract_and_hyperlink_citations(llm_response)
        
        # Save the summary
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(summary)
            
        print(f"  SUCCESS: Saved summary for {filename}")

    except Exception as e:
        # This will catch the 429 error and print it
        print(f"  ERROR processing {filename} with Gemini: {e}")

async def main():
    start_time = time.time()
    
    # Get all .txt files from the source directory
    try:
        filenames = [f for f in os.listdir(SOURCE_DIR) if f.endswith('.txt')]
    except FileNotFoundError:
        print(f"Error: Source directory not found: {SOURCE_DIR}")
        print("Please create a folder named 'full_texts' and put your 50 .txt files in it.")
        return

    if not filenames:
        print(f"No .txt files found in {SOURCE_DIR}")
        return

    print(f"Found {len(filenames)} files to process.")
    
    # --- FIX: Process files sequentially to avoid rate limits ---
    # Instead of using asyncio.gather to run all at once,
    # we run them one by one in a simple loop.
    
    count = 0
    for filename in filenames:
        await process_file(filename)
        count += 1
        print(f"  ({count}/{len(filenames)})")
        
        # Add a 1-second delay to stay well under the 15/min limit
        await asyncio.sleep(1) 
    # --- END FIX ---
    
    end_time = time.time()
    print(f"\nProcessing complete in {end_time - start_time:.2f} seconds.")

if __name__ == "__main__":
    # This runs the async main function
    asyncio.run(main())