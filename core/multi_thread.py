from concurrent.futures import ThreadPoolExecutor, as_completed

def dipatch_cases(task, cases, max_workers, **kwargs):
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(task, **case, **kwargs) 
            for case in cases
        ]
        for future in as_completed(futures):
            results.append(future.result())
    
    return results