import json
import os

# Path to blockchain file
BLOCKCHAIN_FILE = 'blockchain.json'


# Function to load the blockchain
def load_blockchain():
    if os.path.exists(BLOCKCHAIN_FILE):
        with open(BLOCKCHAIN_FILE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []  # Return empty if file is corrupted or empty
    else:
        return []


# Function to add a vote to blockchain
def add_vote_to_blockchain(voter_name, candidate_name, party_name):
    blockchain = load_blockchain()
    vote = {
        'voter': voter_name,
        'candidate': candidate_name,
        'party': party_name
    }
    blockchain.append(vote)
    with open(BLOCKCHAIN_FILE, 'w') as file:
        json.dump(blockchain, file, indent=4)
    print("Vote added to blockchain!")


# Function to get all votes (For admin viewing purpose)
def get_all_votes():
    return load_blockchain()


# Optional: Function to print the blockchain (for testing)
def print_blockchain():
    blockchain = load_blockchain()
    for block in blockchain:
        print(block)


# Example usage (Uncomment to test individually)
# if _name_ == "_main_":
#     add_vote_to_blockchain("John Doe", "Alice", "Party A")
#     print_blockchain()