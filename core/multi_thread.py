from concurrent.futures import ThreadPoolExecutor, as_completed

def dipatch_cases(task, cases: list[dict], max_threads: int, timeout: int, **kwargs):
    results = []
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [
            executor.submit(task, **case, **kwargs) 
            for case in cases
        ]
        for future in as_completed(futures):
            results.append(future.result())
    
    return results