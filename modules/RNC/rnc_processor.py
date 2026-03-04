from .rnc_request import concordance_json, word_portrait_json

from pprint import pprint


def get_ipm(response: dict) -> int | None:

    abs_frequency = response.get("queryStats", {}).get("wordUsageCount", 0)

    subcorpus_size = response.get("subcorpStats", {}).get("wordUsageCount", 0)

    if not subcorpus_size:
        return None

    return abs_frequency / subcorpus_size * 1000000


def get_contexts(response: dict, left_context_size: int = 1, right_context_size: int = 1) -> dict:
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


def get_semantic_labels(response: dict) -> list:
    labels = []
    for item in response.get("propsData", {}).get("items", []):
        for field in item.get("parsingFields", []):
            if field.get("name") == "sem":
                for value in field.get("value", []):

                    tag = value.get("valString", {}).get("v")
                    if tag:
                        labels.append(tag)

    return list(set(labels))


def get_similar_words(response: dict, top_n: int = 10) -> list[tuple]:
    similar_words = []
    similar_data = response.get("similarData", [])
    if similar_data:
        values = similar_data[0].get("values", [])
        for item in values[:top_n]:
            similar_words.append((item.get("word"), item.get("weight")))

    return similar_words

def get_years_usage(response: dict, start=None, end=None):
    pass


def get_word_sketch(response: dict) -> dict[list[tuple]]:
    sketch = {}
    for collocate_group in response.get("sketchData", {}).get("collocates", {}):

        relation_type = collocate_group.get("sketchSynRelation")

        if relation_type not in sketch:
            sketch[relation_type] = []

        for collocate in collocate_group.get("collocations", []):

            word = collocate.get("collocate", {}).get("valString", {}).get("v")
            value = collocate.get("metrics", {})[0].get("value")

            if word:
                sketch[relation_type].append((word, value))
    return sketch



if __name__ == "__main__":
    target = "имидж"
    data = word_portrait_json(target)
    # print(get_semantic_labels(data))
    # pprint(get_similar_words(data))
    print(data.keys())
    pprint(get_word_sketch(data))
    


