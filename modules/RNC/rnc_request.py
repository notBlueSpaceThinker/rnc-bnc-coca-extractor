from ..config import load_RNC_token, load_corpus_settings

import requests


TOKEN = load_RNC_token()
DATE_START = load_corpus_settings().DATE_START
DATE_END = load_corpus_settings().DATE_END
SUBCORPUS = load_corpus_settings().RNC_SUBCORPUS


def get_concordance_json(word, corpus=SUBCORPUS) -> dict | None:
    url = "https://ruscorpora.ru/api/v1/lex-gramm/concordance"

    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    request_body = {
        "corpus": {"type": corpus},
        "subcorpus": {
            "sectionValues": [
                {
                    "conditionValues": [
                        {
                            "fieldName": "created",
                            "intRange": {
                                "begin": int(DATE_START),
                                "end": int(DATE_END)
                            }
                        }
                    ]
                }
            ]
        },
        "lexGramm": {
            "sectionValues": [
                {
                    "subsectionValues": [
                        {
                            "conditionValues": [
                                {"fieldName": "lex", "text": {"v": word}}
                            ]
                        }
                    ]
                }
            ]
        },
        "format": "json",
        "size": 10
    }

    response = requests.post(url, json=request_body, headers=headers)

    if response.status_code != 200:
        print(response.json().get("message"))
        return None

    return response.json()

if __name__ == "__main__":

    data = get_concordance_json("статус")


    print(data.get("queryStats"))
    print(data.get("subcorpStats"))
    print(data.get("corpusStats"))
    print(data.get("groups"))
    # print(data.get("groups"))
    # print(TOKEN)