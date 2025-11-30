import csv
import json
import math
import csv
import json
import math
import os

def load_borrower_data(filepath):
    """Loads borrower data into a dictionary keyed by borrower_id."""
    borrowers = {}
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            borrowers[row['borrower_id']] = {
                'loan_type': row['loan_type'],
                'principal': float(row['principal_outstanding']),
                'dpd': int(row['dpd'])
            }
    return borrowers

def load_chat_scenarios(filepath):
    """Loads chat scenarios from JSON."""
    with open(filepath, 'r') as f:
        return json.load(f)

def round_nearest_100(amount):
    """Rounds amount to the nearest 100."""
    return int(round(amount / 100.0) * 100)

def calculate_min_offer(borrower, chat_history):
    """
    Calculates the minimum acceptable offer based on policy.
    """
    principal = borrower['principal']
    dpd = borrower['dpd']
    loan_type = borrower['loan_type']
    
    # Check for keywords in user messages
    user_text = " ".join([msg['content'].lower() for msg in chat_history if msg['role'] == 'user'])
    
    job_loss = ('job loss' in user_text) or ('unemployment' in user_text) or ('lost my job' in user_text)
    medical = ('hospital' in user_text) or ('medical' in user_text)
    
    max_discount_percent = 0.0
    
    if loan_type == 'Personal Loan':
        # Default
        max_discount_percent = 0.20
        
        # DPD Rule
        if dpd > 90:
            max_discount_percent = max(max_discount_percent, 0.35)
            
        # Medical Rule
        if medical:
            max_discount_percent = max(max_discount_percent, 0.45)
            
        # Job Loss Rule (Highest priority/discount for PL)
        if job_loss:
            max_discount_percent = max(max_discount_percent, 0.50)
            
    elif loan_type == 'Credit Card':
        # Small Balance Rule (Overrides everything else for CC)
        if principal < 50000:
            max_discount_percent = 0.10
        else:
            # Standard
            max_discount_percent = 0.30
            
            # High DPD
            if dpd > 90:
                max_discount_percent = max(max_discount_percent, 0.50)

    # Calculate Floor Price
    discount_amount = principal * max_discount_percent
    min_offer = principal - discount_amount
    
    return round_nearest_100(min_offer)

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'data')
    
    borrower_file = os.path.join(data_dir, 'borrower_data.csv')
    chat_file = os.path.join(data_dir, 'chat_scenarios.json')
    submission_file = os.path.join(base_dir, 'submission.csv')
    
    print("Loading data...")
    borrowers = load_borrower_data(borrower_file)
    scenarios = load_chat_scenarios(chat_file)
    
    print(f"Processing {len(scenarios)} scenarios...")
    
    results = []
    for scenario in scenarios:
        s_id = scenario['scenario_id']
        b_id = scenario['borrower_id']
        chat = scenario['chat_history']
        
        if b_id not in borrowers:
            print(f"Warning: Borrower {b_id} not found!")
            continue
            
        borrower = borrowers[b_id]
        min_offer = calculate_min_offer(borrower, chat)
        
        results.append({'scenario_id': s_id, 'min_acceptable_offer': min_offer})
        
    print("Writing submission file...")
    with open(submission_file, 'w', newline='') as f:
        fieldnames = ['scenario_id', 'min_acceptable_offer']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in results:
            writer.writerow(row)
            
    print(f"Done! Submission saved to {submission_file}")

if __name__ == "__main__":
    main()
        
