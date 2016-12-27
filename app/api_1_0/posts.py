from flask import g, jsonify, request, current_app, url_for
from flask_httpauth import HTTPBasicAuth


from . import api
from .errors import unauthorized, forbidden, not_acceptable, bad_request
from ..models.post import Post
from .. import db

auth = HTTPBasicAuth()


@api.route('/posts/view/<int:id>', methods=['GET'])
def post_view(id):
    post = Post.query.get_or_404(id)
    post.increase_read_count(post.read_counts+1)
    print(post.read_counts)
    print(post.author_id, post.title, post.body, post.timestamp)

    return jsonify({'message': 'ok'})


@auth.login_required
@api.route('/posts/pagination', methods=['GET'])
def post_pagination():
    per_page = current_app.config['FLASKY_POSTS_PER_PAGE']
    page = request.args.get('page', 1, type=int)
    if page == 1:
        # memorize last board id
        obj = Post.query.order_by(Post.id.desc()).first()
        query_id = obj.id
    else:
        query_id = request.args.get('query_id', type=int)

    posts = Post.query.order_by(Post.id.desc()).filter(Post.id <= query_id).limit(per_page).offset(page*per_page)

    next_item = dict()
    next_item['query_id'] = query_id

    if posts.count() == 0:
        next_item['count'] = 0
        next_item['next'] = -999
    else:
        next_item['count'] = posts.count()
        next_item['next'] = page + 1

    return jsonify({'message': 'ok', 'next_item': next_item})


@auth.login_required
@api.route('/posts/')
def get_posts():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.id.desc()).paginate(
        page,
        per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_posts', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_posts', page=page+1, _external=True)

    for post in posts:
        print(post.id, post.timestamp, post.title)

    return jsonify({
        'prev': prev,
        'next': next,
        'count': pagination.total
    })