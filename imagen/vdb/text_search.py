from imagen.model.image import Image
from imagen.service.conversion_service import create_text_embeddings
from imagen.vdb.lancedb_persistence import DISTANCE, execute_knn_search


async def text_search(image_description: str, limit: int = 10, distance: str = DISTANCE.EUCLIDEAN) -> list[Image]:
    embedding = await create_text_embeddings(image_description)
    return execute_knn_search(embedding, Image.field.text_vector, limit, distance)


# if __name__ == "__main__":
#     import asyncio

#     def test_list_text_vectors():
#         for i, img in enumerate(tbl.to_pandas()[FIELD_TEXT_VECTOR].to_numpy()):
#             print(i, img)

#     def search_tester(search: str):
#         print("Searching for: ", search)
#         res = asyncio.run(text_search(search, 3, DISTANCE.DOT))
#         for dic in res:
#             print(dic[FIELD_IMAGE_DESCRIPTION])
#             print("\n******************************************\n")

#     def test_text_search_2():
#         search_tester("ritualistic or ceremonial gathering.")

#     def test_text_search_3():
#         search_tester("ancient temple interior with intricate stonework")

#     def test_text_search_4():
#         search_tester(
#             "a person standing in front of a group of people who appear to be part of a ritualistic or ceremonial gathering"
#         )

#     def test_text_search_5():
#         search_tester("adding to the atmosphere of mystery and intrigue")

#     def test_text_search_young_woman():
#         search_tester("young woman")

#     def test_text_transformers():
#         search_tester("transformer robots")

#     test_text_search_3()
