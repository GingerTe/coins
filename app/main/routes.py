from flask import render_template, redirect, url_for, abort, request, current_app, flash
from flask_login import current_user
from flask_sqlalchemy import get_debug_queries

from app.models import CoinGroup, Coin
from . import main
from .. import db


@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration,
                   query.context))
    return response


@main.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'


@main.app_context_processor
def get_main_groups():
    groups = CoinGroup.query.filter_by(parent=None).order_by(CoinGroup.order).all()
    return dict(groups=groups)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/coins/<int:group_id>/', methods=['GET', 'POST'])
def coins(group_id):
    group = CoinGroup.query.get_or_404(group_id)
    return render_template('coins.html', group=group)


@main.route('/coins/<int:coin_id>/change-availability/', methods=['POST'])
def change_coin_got(coin_id):
    coin = Coin.query.get_or_404(coin_id)
    coin.is_got = not coin.is_got
    flash('Монета {} теперь {} наличии'.format(coin.name, coin.is_got and 'в' or 'не в'))
    db.session.commit()
    return redirect(url_for(request.args['redirect'], group_id=request.args['group_id']))
