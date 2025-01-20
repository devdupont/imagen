"""Combine and rank image and text search results."""

from dataclasses import dataclass

from imagen.model.image import Image


@dataclass
class SearchResult:
    """Search result data object."""

    image: Image
    rank: int | float


def combine_results(res_image: list[Image], res_text: list[Image], limit: int) -> list[Image]:
    """Combine and rank image and text search results."""

    def rank_results(res: list[Image]) -> dict[str, SearchResult]:
        return {image.name: SearchResult(image, limit - i) for i, image in enumerate(res)}

    ranked_images = rank_results(res_image)
    ranked_text = rank_results(res_text)
    combined_dict = ranked_images.copy()

    for name, value in ranked_images.items():
        if name not in ranked_text:
            print(f"Image result not ranked: {name}")
            value.rank /= 2  # Only available as text result. Divide by two to penalize

    for name, value in ranked_text.items():
        if name not in combined_dict:
            print(f"Text result not ranked: {name}")
            combined_dict[name] = value
            value.rank /= 2  # Only available as text result. Divide by two to penalize
        else:
            item = combined_dict[name]
            item.rank += value.rank
            if item.image.distance and value.image.distance:
                item.image.distance = (item.image.distance + value.image.distance) / 2

    resp = sorted(combined_dict.values(), key=lambda x: x.rank, reverse=True)
    return [r.image for r in resp[:limit]]
