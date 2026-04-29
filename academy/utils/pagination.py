from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class LaravelLikePagination(PageNumberPagination):
    page_size_query_param = 'page_size'  # allows ?page_size=xx
    max_page_size = 100

    def get_paginated_response(self, data):
        current_page = self.page.number
        total_pages = self.page.paginator.num_pages
        total_items = self.page.paginator.count
        per_page = self.get_page_size(self.request)
        if per_page is None:
            per_page = self.page_size

        base_url = self.request.build_absolute_uri(self.request.path)

        def build_page_url(page_number):
            return f"{base_url}?page={page_number}&page_size={per_page}"

        # Build the "links" list like Laravel
        links = []
        for i in range(1, total_pages + 1):
            links.append({
                "url": build_page_url(i),
                "label": str(i),
                "active": (i == current_page)
            })

        return Response({
            "current_page": current_page,
            "data": data,
            "first_page_url": build_page_url(1),
            "from": (self.page.start_index() if total_items > 0 else None),
            "last_page": total_pages,
            "last_page_url": build_page_url(total_pages),
            "links": links,
            "next_page_url": build_page_url(current_page + 1) if self.page.has_next() else None,
            "path": base_url,
            "per_page": per_page,
            "prev_page_url": build_page_url(current_page - 1) if self.page.has_previous() else None,
            "to": (self.page.end_index() if total_items > 0 else None),
            "total": total_items,
        })
