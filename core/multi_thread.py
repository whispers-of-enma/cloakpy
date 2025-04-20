from concurrent.futures import ThreadPoolExecutor, as_completed

def dipatch_cases(task, cases: list[dict], max_threads: int, **kwargs):
    results = []
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {
            executor.submit(task, **case, **kwargs): case
            for case in cases
        }
        for future in as_completed(futures):
            case = futures[future]
            if future.result():
                results.append(case)
    
    return results