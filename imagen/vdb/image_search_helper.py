from pathlib import Path

from imagen.service.image_embeddings.embedding_query import get_image_emb
from imagen.vdb.imagedb_schema import (
    FIELD_IMAGE_NAME,
    FIELD_IMAGE_VECTOR,
)
from imagen.vdb.lancedb_persistence import DISTANCE, execute_knn_search


def image_search(image_path: Path, limit: int = 10, distance: str = DISTANCE.EUCLIDEAN) -> list[dict]:
    embedding = get_image_emb(image_path)
    return execute_knn_search(embedding, FIELD_IMAGE_VECTOR, limit, distance)


if __name__ == "__main__":
    from imagen.config import cfg

    def search_tester(image_path: Path) -> None:
        print("Searching for: ", image_path)
        res = image_search(image_path, 3, DISTANCE.DOT)
        for dic in res:
            print(dic[FIELD_IMAGE_NAME])
            print("\n******************************************\n")

    image_list = list(cfg.image_load_path.glob("*.png"))
    if len(image_list) > 0:
        first_image = image_list[0]
        print(f"== {first_image} ==")
        search_tester(first_image)
