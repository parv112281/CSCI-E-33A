from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("close/<int:listing_id>", views.close_listing, name="close_listing"),
    path("bid/<int:listing_id>", views.place_bid, name="place_bid"),
    path("categories", views.categories, name="categories"),
    path("watchlist/<str:username>", views.watchlist, name="watchlist"),
    path("category/<str:category_title>", views.category, name="category"),
    path(
        "submit_comment/<int:listing_id>",
        views.submit_comment,
        name="submit_comment"),
    path(
        "watch_item/<int:listing_id>",
        views.watch_item,
        name="watch_item"),
    path(
        "stop_watching/<int:listing_id>",
        views.stop_watching,
        name="stop_watching"),
]
