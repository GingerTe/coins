from flask import render_template, redirect, url_for, abort, request, current_app
from flask_login import current_user
from flask_sqlalchemy import get_debug_queries

from app.models import CoinGroup
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


@main.route('/coin-group/')
def coin_group():
    group_id = request.args.get('group')
    if group_id is None:
        return "", 400
    group = CoinGroup.query.get_or_404(int(group_id))
    return render_template('coin-group.html', group=group)
