from pydantic import parse_obj_as

from core.services import safely_decode_response_json, BaseAPIClient
from products import models

__all__ = ('ProductsAPIClient',)


class ProductsAPIClient(BaseAPIClient):

    async def get_categories(
            self,
            parent_id: int | None = None,
    ) -> tuple[models.CategoryPreview, ...]:
        data = []
        url = '/categories/'
        request_query_params = {}
        if parent_id is not None:
            request_query_params['parent_id'] = parent_id
        while True:
            response = await self._http_client.get(
                url=url,
                params=request_query_params,
            )
            response_data = response.json()
            data += response_data['categories']
            if response_data['is_end_of_list_reached']:
                break
        return parse_obj_as(tuple[models.CategoryPreview, ...], data)

    async def get_products_by_category_id(
            self,
            category_id: int,
    ) -> tuple[models.ProductPreview, ...]:
        url = f'/categories/{category_id}/products/'
        response = await self._http_client.get(url)
        response_json = safely_decode_response_json(response)
        return parse_obj_as(tuple[models.ProductPreview, ...], response_json)

    async def get_category_by_id(
            self,
            category_id: int,
    ) -> models.Category:
        url = f'/categories/{category_id}/'
        response = await self._http_client.get(url)
        response_json = safely_decode_response_json(response)
        return models.Category.parse_obj(response_json)

    async def get_product_by_id(self, product_id: int) -> models.Product:
        url = f'/categories/products/{product_id}/'
        response = await self._http_client.get(url)
        response_json = safely_decode_response_json(response)
        return models.Product.parse_obj(response_json)
