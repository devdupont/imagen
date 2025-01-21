from openai import OpenAI

from imagen.config import cfg

client = OpenAI(api_key=cfg.openai_api_key)


def text_embeddings(text: str) -> list[float]:
    if cfg.openai_embeddings_model is None:
        msg = "OpenAI embeddings model is not defined in the config"
        raise ValueError(msg)
    return client.embeddings.create(input=[text], model=cfg.openai_embeddings_model).data[0].embedding


if __name__ == "__main__":
    res = text_embeddings("This is a sime text.")
    print(len(res))
