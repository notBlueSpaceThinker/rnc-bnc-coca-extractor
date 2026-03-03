from .rnc_request import get_concordance_json

def get_ipm(response) -> int | None:

    abs_frequency = response.get("queryStats", {}).get("wordUsageCount", 0)

    subcorpus_size = response.get("subcorpStats", {}).get("wordUsageCount", 0)

    if not subcorpus_size:
        return None

    return abs_frequency / subcorpus_size * 1000000

def get_contexts(response, left_context_size: int = 1, right_context_size: int = 1):
    contexts: dict[str, int] = {}
    for group in response.get("groups"):
        for doc in group.get("docs", []):
            for snippet_group in doc.get("snippetGroups", []):
                for snippet in snippet_group.get("snippets", []):
                    for seq in snippet.get("sequences", []):

                        words = [w for w in seq.get("words", []) if w.get("type") == "WORD"]

                        for i, w in enumerate(words):
                            if w.get("displayParams", {}).get("hit"):
                                left_context = words[max(0, i-left_context_size):i]
                                right_context = words[i+1:min(len(words), i+1+right_context_size)]

                                for w_context in left_context + right_context:
                                    w_neighbor = w_context.get("text")

                                    pair = f"{w.get("text")} {w_neighbor}"

                                    contexts[pair] = contexts.get(pair, 0) + 1

                                break
    return contexts

if __name__ == "__main__":
    data = get_concordance_json("статус")
    print(data.get("queryStats"))
    print(data.get("subcorpStats"))
    print(data.get("corpusStats"))
    print(data.get("sorting"))
    print(get_contexts(data))

    # print(get_ipm(data))