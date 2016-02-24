# coding=utf-8
from django.core.paginator import Paginator as DjangoPaginator, Page
from furl import furl


def make_full(url, page):
    if page != 1:
        return furl(url).remove(['page']).add({"page": page}).url
    return furl(url).remove(['page']).url


def make_query(url, page):
    if page != 1:
        return furl(url).remove(['page']).add({"page": page}).url.split('?')[1]
    try:
        return furl(url).remove(['page']).url.split('?')[1]
    except IndexError:
        return ""


class UrlPage(Page):
    """
    Добавляем возможность ссылки на след страницу
    """

    def __init__(self, url, *args, **kwargs):
        self._url = url
        super(UrlPage, self).__init__(*args, **kwargs)

    def previous_page_url(self):
        """
        Ссылка на предыдущую страницу
        :return: str
        """
        return furl(self._url).remove(['page']).add({"page": self.number-1}).url

    def previous_page_query(self):
        """
        Ссылка на предыдущую страницу
        :return: str
        """
        # query = furl(self._url).query

        return furl(self._url).remove(['page']).add({"page": self.number-1}).url.split("?")[1]

    previous_url = previous_page_url

    def get_previous_url(self):
        return self.previous_page_url()

    def get_next_url(self):
        return self.next_page_url()

    def next_page_url(self):
        """
        Ссылка на следующую страницу
        :return: str
        """
        return furl(self._url).remove(['page']).add({"page": self.number+1}).url

    def next_page_query(self):
        """
        Ссылка на следующую страницу
        :return: str
        """
        return furl(self._url).remove(['page']).add({"page": self.number+1}).url.split("?")[1]

    def pages(self):
        """
        Список из страниц
        """

        def make_full(url, page):
            return furl(url).remove(['page']).add({"page": page}).url

        def make_query(url, page):
            return furl(url).remove(['page']).add({"page": page}).url.split('?')[1]

        pages = []
        for i in range(-3, 0):
            if self.number + i > 0:
                pages.append(
                    {'page': self.number + i,
                     'active': False,
                     'url': make_full(self._url, self.number + i),
                     'query': make_query(self._url, self.number + i)}
                )
        pages.append(
            {'page': self.number,
             'active': True,
             'url': make_full(self._url, self.number),
             'query': make_query(self._url, self.number)}
        )

        for i in range(1, 4):
            if self.number + i <= self.paginator.num_pages:
                pages.append(
                    {'page': self.number + i,
                     'active': False,
                     'url': make_full(self._url, self.number + i),
                     'query': make_query(self._url, self.number + i)}
                )
        return pages


class UrlPaginator(DjangoPaginator):
    """
    Пагинация со ссылкой на страницу
    """

    def __init__(self, url, object_list, per_page, orphans=0,
                 allow_empty_first_page=True, count=None):
        self._url = url
        super(UrlPaginator, self).__init__(
            object_list, per_page, orphans, allow_empty_first_page)
        self._count = count

    def _get_page(self, *args, **kwargs):
        return UrlPage(self._url, *args, **kwargs)

    @property
    def number(self):
        try:
            # print(furl(self._url).args['page'])
            number = int(furl(self._url).args['page'])
        except (TypeError, ValueError, KeyError):
            number = 1
        return number

    def pages(self, number=None):
        """
        number - текущая страница
        :param number: int
        """

        if number is None:
            number = self.number
        else:
            number = self.validate_number(number)

        pages = []
        for i in range(-3, 0):
            if number + i > 0:
                pages.append(self._gen_page(number + i, self._url, False))

        pages.append(self._gen_page(number, self._url, True))

        for i in range(1, 4):
            if number + i <= self.num_pages:
                pages.append(self._gen_page(number + i, self._url, False))
        return pages

    def _gen_page(self, number, url, active):
        return {'number': number,
                'active': active,
                'url': make_full(url, number),
                'query': make_query(url, number)}

    def page(self, number=None):
        """
        Returns a Page object for the given 1-based page number.
        """
        if number is not None:
            url = furl(self._url).remove(['page']).add({"page": number}).url
        else:
            url = self._url

        p = UrlPaginator(url, object_list=self.object_list,
                         per_page=self.per_page, orphans=self.orphans,
                         allow_empty_first_page=self.allow_empty_first_page,
                         count=self._count)

        return p

    def _paginate(self, number=None):
        """
        Returns a Page object for the given 1-based page number.
        """
        if number is not None:
            number = self.validate_number(number)
        else:
            number = self.number
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        if top + self.orphans >= self.count:
            top = self.count
        return self.object_list[bottom:top]

    def __iter__(self):
        return iter(self._paginate(self.number))

    def has_next(self):
        return self.number + 1 <= self.num_pages

    def next(self):
        if not self.has_next():
            raise ValueError("no next page")
        return self._gen_page(self.number + 1, self._url, False)

    def has_prev(self):
        return self.number > 1

    def prev(self):
        if not self.has_prev():
            raise ValueError("no prev page")
        return self._gen_page(self.number - 1, self._url, False)


