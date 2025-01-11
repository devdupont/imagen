from openai import OpenAI

from imagen.config import cfg

client = OpenAI(api_key=cfg.openai_api_key)


def openai_create_text_embeddings(text: str) -> list[float]:
    return client.embeddings.create(input=[text], model=cfg.openai_embeddings_model).data[0].embedding


if __name__ == "__main__":
    res = openai_create_text_embeddings("This is a sime text.")
    print(len(res))
