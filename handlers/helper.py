from typing import List, Tuple, Dict


def gen_analytic_result(data: List[Tuple]) -> List[Dict]:
    result = []
    for row in data:
        result.append({
            "executed_at": str(row[1]),
            "interval": row[2],
            "search_phrase": row[3],
            "statistics": {
                "top_hashtags": row[4],
                "top_phrases": row[5],
                "top_publisher": row[6],
                "tweet_count": row[7],
            }
        })

    return result
