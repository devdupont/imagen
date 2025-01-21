from pathlib import Path

from imagen.model.image import Image
from imagen.service.image.embedding import image_embeddings
from imagen.vdb.lancedb_persistence import DISTANCE, execute_knn_search


def image_search(image_path: Path, limit: int = 10, distance: str = DISTANCE.EUCLIDEAN) -> list[Image]:
    embedding = image_embeddings(image_path)
    return execute_knn_search(embedding, Image.field.image_vector, limit, distance)


if __name__ == "__main__":
    from imagen.config import cfg

    def search_tester(image_path: Path) -> None:
        print("Searching for: ", image_path)
        for image in image_search(image_path, 3, DISTANCE.DOT):
            print(image.name)
            print("\n******************************************\n")

    image_list = list(cfg.image_load_path.glob("*.png"))
    if len(image_list) > 0:
        first_image = image_list[0]
        print(f"== {first_image} ==")
        search_tester(first_image)
