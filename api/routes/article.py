from typing import Optional

from fastapi import Query
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi_filter import FilterDepends
from sqlalchemy import or_

from db import Article, Tag, ArticleTag
from api.routes.base import BaseRoute
from api.schemas.article import ArticleListSchema, ArticleCreateSchema
from crud.article import (
    get_article_by_code_or_404,
    create_article,
    ArticleFilter,
    get_articles
)
from execptions import UniqueFailed


router = InferringRouter()


@cbv(router)
class ArticleRoute(BaseRoute):
    model = Article
    joined_load = ('tags', )

    @router.get('/{code}')
    def get_article(self, code: str) -> ArticleListSchema:
        article = get_article_by_code_or_404(session=self.session, code=code, joined_load=self.joined_load)
        article.tags = sorted(article.tags, key=lambda tag: tag.name)
        return article

    @router.post('/')
    def create(self, article: ArticleCreateSchema) -> ArticleListSchema:
        self._validate_name_and_code(code=article.code, name=article.name)
        return create_article(self.session, article)

    @router.get('/')
    def list(
            self,
            tag_codes: Optional[list[str]] = Query(default=None),
            filter_obj: ArticleFilter = FilterDepends(ArticleFilter)
    ) -> list[ArticleListSchema]:
        articles = get_articles(self.session, filter_obj, joined_load=self.joined_load)
        if tag_codes:
            articles = (
                self.session
                .execute(
                    articles.join(ArticleTag)
                    .join(Tag)
                    .filter(Tag.code.in_(tag_codes))
                ).scalars().all()
            )
        for article in articles:
            article.tags = sorted(article.tags, key=lambda tag: tag.name)
        return articles

    def _validate_name_and_code(self, code: str, name: str):
        same_articles_count = self.session.query(Article).filter(
            or_(
                Article.name == name,
                Article.code == code
            )
        ).count()
        if same_articles_count:
            raise UniqueFailed(message='Статья с таким именем или кодом уже существует')
