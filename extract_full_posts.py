import json

def extract_posts(elements, stop_index, count=10):
    posts = []
    current_elements = []
    
    # CTAs that typically end a post
    ctas = ['@vitali_rapeika', 'подпишись', 'напиши в комментариях', 'сохрани', 'подписывайся']
    
    elements_before = [e for e in elements if e['start'] < stop_index]
    
    # Iterate backwards to find 10 posts
    # A post ends with a CTA and starts with a headline
    
    current_post_text = []
    posts_found = 0
    
    # This is a bit heuristic, let's look for CTAs
    for e in reversed(elements_before):
        text = e['text']
        current_post_text.insert(0, text)
        
        # Check if the current element is a headline (often bold/caps)
        # Or if we hit the end of the previous post (another CTA)
        
        # Actually, let's use the start indexes I found manually.
        pass

# Manually defined start indexes based on analysis
start_indexes = [
    532130, # 1. Как вести себя богато
    533996, # 2. Эти семейные ритуалы
    536212, # 3. никто не испытывает большего стресса
    537427, # 4. 22 цитаты Достоевского
    539649, # 5. Хочешь узнать мужчину
    540682, # 6. КО МНЕ ВЕРНУЛСЯ ВКУС К ЖИЗНИ
    542335, # 7. 8 вещей, которые ПАПА
    543878, # 8. НЕ СТАВЬ ЦЕЛИ
    545842, # 9. 30 идей для пар
    546954  # 10. В древней книге сказано (Круг на ладони)
]

elements = []
with open('/tmp/all_elements_chunk.jsonl', 'r') as f:
    for line in f:
        elements.append(json.loads(line))

for i, start in enumerate(start_indexes):
    end = start_indexes[i+1] if i+1 < len(start_indexes) else 548340
    post_elements = [e for e in elements if e['start'] >= start and e['start'] < end]
    post_text = "\n".join([e['text'] for e in post_elements])
    print(f"--- POST {i+1} ---")
    print(post_text)
