from flask import g, jsonify, request, current_app, url_for

from app.api_1_0 import api
from app.api_1_0.authentication import auth
from app.api_1_0.errors import unauthorized, forbidden, not_acceptable, bad_request
from app.models.post import Post
from app.models.comment import Comment


@api.route('/posts/view/<int:post_id>', methods=['GET'])
@auth.login_required
def get_post(post_id):
    print('called')
    post = Post.query.get_or_404(post_id)
    post.increase_read_count(post.read_counts+1)
    print(post.read_counts)
    print(post.author_id, post.title, post.body, post.timestamp)

    return jsonify({'message': 'ok'})


# todo comment loading jsonify needs to be implemented
@api.route('/posts/view/<int:post_id>/comments/', methods=['GET'])
@auth.login_required
def get_post_comments(post_id):
    post = Post.query.get_or_404(post_id)
    comments = post.comments.order_by(Comment.timestamp.asc())
    if not comments.first():
        print('empty')
    else:
        for comment in comments:
            print('#', comment.post_id, comment.body, comment.timestamp)

    return jsonify({'message': 'ok'})


# todo comment posting
@api.route('/posts/view/<int:post_id>/comments/', methods=['POST'])
@auth.login_required
def set_post_comments(post_id):
    pass


@api.route('/posts/pagination', methods=['GET'])
@auth.login_required
def post_pagination():
    per_page = current_app.config['FLASKY_POSTS_PER_PAGE']
    page = request.args.get('page', 1, type=int)
    if page == 1:
        # memorize last board id
        obj = Post.query.order_by(Post.id.desc()).first()
        query_id = obj.id
    else:
        query_id = request.args.get('query_id', type=int)

    posts = Post.query.order_by(Post.id.desc()).filter(Post.id <= query_id).limit(per_page).offset((page-1)*per_page)
    for post in posts:
        print(post.title, post.read_counts)

    next_item = dict()
    next_item['query_id'] = query_id

    if posts.count() == 0:
        next_item['count'] = 0
        next_item['next'] = -999
    else:
        next_item['count'] = posts.count()
        next_item['next'] = page + 1

    return jsonify({'message': 'ok', 'next_item': next_item})


@api.route('/posts/')
@auth.login_required
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