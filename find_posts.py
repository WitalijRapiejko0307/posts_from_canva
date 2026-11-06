import json

def find_posts(elements, stop_index):
    posts = []
    current_post = []
    
    # Filter elements before stop_index
    elements_before = [e for e in elements if e['start'] < stop_index]
    
    # Iterate backwards from stop_index
    for e in reversed(elements_before):
        text = e['text']
        current_post.insert(0, e)
        
        # A post starts with a headline (hook)
        # In this doc, hooks are often in ALL CAPS or specific phrases.
        # But we also know they end with @vitali_rapeika or similar CTA.
        # Let's look for CTA first to define boundaries.
        
    # Let's try another way: find all CTAs and then find headlines above them.
    ctas = []
    for i, e in enumerate(elements_before):
        t = e['text'].lower()
        if '@vitali_rapeika' in t or 'подпишись' in t or 'напиши в комментариях' in t or 'сохрани' in t:
            # Check if this is the end of a post (not inside)
            # CTAs usually appear at the end of the post.
            ctas.append(i)
            
    # Group elements into posts based on CTAs
    # This is a bit tricky as a post can have multiple CTA lines.
    # Let's look for the biggest jumps in index or logical breaks.
    
    # Actually, let's just print the elements and manually/regex find the 10 posts.
    for e in elements_before[-500:]: # Look at last 500 elements
        print(f"{e['start']} | {e['text']}")

# Load elements
elements = []
with open('/tmp/all_elements_chunk.jsonl', 'r') as f:
    for line in f:
        elements.append(json.loads(line))

find_posts(elements, 548340)
