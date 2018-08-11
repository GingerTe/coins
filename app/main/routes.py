from flask import render_template, redirect, url_for, abort, request, current_app, flash
from flask_login import current_user
from flask_sqlalchemy import get_debug_queries

from app.main.forms import EditCoinForm
from app.models import CoinGroup, Coin, Mint
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


@main.route('/coin/<int:coin_id>/', methods=['GET', 'POST'])
def edit_coin(coin_id):
    coin = Coin.query.get_or_404(coin_id)
    form = get_coin_form()
    if request.method == 'GET':
        form.mint.data = coin.mint_id
        form.name.data = coin.name
        form.year.data = coin.year
        form.description.data = coin.description
        form.description_url.data = coin.description_url
        form.num.data = coin.num
        form.date.data = coin.date
        form.is_got.data = coin.is_got

    else:
        if form.validate_on_submit():
            coin.mint_id = int(form.mint.data)
            coin.name = form.name.data
            coin.year = form.year.data
            coin.description = form.description.data
            coin.description_url = form.description_url.data
            coin.num = form.num.data
            coin.date = form.date.data
            coin.is_got = form.is_got.data
            db.session.commit()
            flash('Монета {} изменена'.format(coin.name))
            return redirect(url_for(request.endpoint, coin_id=coin_id))

    return render_template('edit-coin.html', coin=coin, form=form)


def get_coin_form():
    form = EditCoinForm()

    form.mint.choices = [(str(mint.id), mint.abbr) for mint in (Mint.query.order_by(Mint.name).all())]
    return form
