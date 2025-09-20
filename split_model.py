#!/usr/bin/env python3
"""
Script to split large pickle file into smaller parts for GitHub upload
and reconstruct them when needed.
"""
import os
import pickle

def split_pickle_file():
    """Split the large pickle file into parts under 100MB"""
    model_file = 'house_price_model.pkl'

    if not os.path.exists(model_file):
        print(f"Model file {model_file} not found!")
        return

    # Read the original pickle file
    with open(model_file, 'rb') as f:
        data = f.read()

    # Split into 80MB chunks to be safe (GitHub limit is 100MB)
    chunk_size = 80 * 1024 * 1024  # 80MB
    total_size = len(data)
    num_parts = (total_size + chunk_size - 1) // chunk_size

    print(f"Original file size: {total_size / (1024*1024):.1f}MB")
    print(f"Splitting into {num_parts} parts...")

    # Create parts
    for i in range(num_parts):
        start = i * chunk_size
        end = min((i + 1) * chunk_size, total_size)
        chunk = data[start:end]

        part_filename = f'house_price_model.pkl.part{i+1:02d}'
        with open(part_filename, 'wb') as f:
            f.write(chunk)

        part_size = len(chunk) / (1024*1024)
        print(f"Created {part_filename}: {part_size:.1f}MB")

    # Create info file
    info = {
        'original_filename': model_file,
        'total_parts': num_parts,
        'total_size': total_size,
        'chunk_size': chunk_size
    }

    with open('model_parts.info', 'wb') as f:
        pickle.dump(info, f)

    print(f"\nSplit complete! Created {num_parts} parts and info file.")
    print("You can now safely delete the original large file.")

def reconstruct_pickle_file():
    """Reconstruct the original pickle file from parts"""
    info_file = 'model_parts.info'

    if not os.path.exists(info_file):
        print("Info file not found! Cannot reconstruct.")
        return False

    # Read info
    with open(info_file, 'rb') as f:
        info = pickle.load(f)

    original_filename = info['original_filename']
    total_parts = info['total_parts']

    print(f"Reconstructing {original_filename} from {total_parts} parts...")

    # Check if all parts exist
    missing_parts = []
    for i in range(1, total_parts + 1):
        part_filename = f'house_price_model.pkl.part{i:02d}'
        if not os.path.exists(part_filename):
            missing_parts.append(part_filename)

    if missing_parts:
        print(f"Missing parts: {missing_parts}")
        return False

    # Reconstruct file
    with open(original_filename, 'wb') as outfile:
        for i in range(1, total_parts + 1):
            part_filename = f'house_price_model.pkl.part{i:02d}'
            with open(part_filename, 'rb') as infile:
                outfile.write(infile.read())
            print(f"Added {part_filename}")

    print(f"Reconstruction complete! Created {original_filename}")
    return True

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == 'reconstruct':
        reconstruct_pickle_file()
    else:
        split_pickle_file()