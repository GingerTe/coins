import json

from flask import render_template, redirect, url_for, abort, request, current_app, flash
from flask_login import login_required
from flask_sqlalchemy import get_debug_queries

from app.main.forms import EditCoinForm
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
@login_required
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
@login_required
def index():
    return render_template('index.html')


@main.route('/coins/<int:group_id>/', methods=['GET', 'POST'])
@login_required
def coins(group_id):
    group = CoinGroup.query.get_or_404(group_id)
    return render_template('coins.html', group=group)


@main.route('/coin/<int:coin_id>/change-availability/', methods=['POST'])
@login_required
def change_coin_got(coin_id):
    coin = Coin.query.get_or_404(coin_id)
    coin.is_got = not coin.is_got
    flash('Монета {} теперь {} наличии'.format(coin.name, coin.is_got and 'в' or 'не в'))
    db.session.commit()
    return redirect(url_for('main.coins', group_id=coin.group.get_root().id))


@main.route('/coin/<int:coin_id>/', methods=['GET', 'POST'])
@login_required
def edit_coin(coin_id):
    form = EditCoinForm()
    coin = Coin.query.get_or_404(coin_id)

    if request.method == 'GET':
        fill_form_from_model(coin, form)

    else:
        if form.validate_on_submit():
            fill_model_from_form(coin, form)
            db.session.commit()
            flash('Монета {} изменена'.format(coin.name))
            return redirect(url_for(request.endpoint, coin_id=coin_id))

    return render_template('edit-coin.html', coin=coin, form=form,
                           coin_group_data=json.dumps(CoinGroup.get_all_hierarchical(with_parent_duplication=True),
                                                      ensure_ascii=False))


@main.route('/coin/new/', methods=['GET', 'POST'])
@login_required
def add_coin():
    form = EditCoinForm()
    coin = Coin()

    if form.validate_on_submit():
        fill_model_from_form(coin, form)
        db.session.add(coin)
        db.session.commit()
        flash('Монета {} добавлена'.format(coin.name))
        return redirect(url_for('main.coins', group_id=coin.group.get_root().id))

    return render_template('edit-coin.html', coin=coin, form=form,
                           coin_group_data=json.dumps(CoinGroup.get_all_hierarchical(with_parent_duplication=True),
                                                      ensure_ascii=False))


def fill_model_from_form(coin, form):
    coin.mint_id = form.mint.data and int(form.mint.data) or None
    coin.name = form.name.data
    coin.year = form.year.data
    coin.description = form.description.data
    coin.description_url = form.description_url.data
    coin.num = form.num.data
    coin.date = form.date.data
    coin.is_got = form.is_got.data
    coin.group_id = form.group.data


def fill_form_from_model(coin, form):
    form.mint.data = coin.mint_id
    form.name.data = coin.name
    form.year.data = coin.year
    form.mint.data = str(coin.mint_id)
    form.description.data = coin.description
    form.description_url.data = coin.description_url
    form.num.data = coin.num
    form.date.data = coin.date
    form.is_got.data = coin.is_got
    form.group.data = coin.group_id
