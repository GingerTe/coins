# coding: utf-8
import pytest

from app.models import CoinGroup


@pytest.fixture(scope='function')
def add_groups(db):
    g0 = CoinGroup(id=0, name='group1', order=1)
    db.session.add(g0)
    g1 = CoinGroup(id=1, name='group2', order=2)
    db.session.add(g1)
    g2 = CoinGroup(id=2, parent_id=0, name='group3')
    db.session.add(g2)
    g3 = CoinGroup(id=3, parent_id=1, name='group4')
    db.session.add(g3)
    g4 = CoinGroup(id=4, parent_id=2, name='group5')
    db.session.add(g4)
    yield g0, g1, g2, g3, g4
    CoinGroup.query.delete()


@pytest.mark.parametrize("coin_group_id, parent_id", [
    (0, 0),
    (2, 0),
    (4, 0),
])
def test_get_root(add_groups, coin_group_id, parent_id):
    assert parent_id == CoinGroup.query.get(coin_group_id).get_root().id


def test_get_all_hierarchical(add_groups):
    g0, g1, g2, g3, g4 = add_groups
    assert [
               {
                   'id': g0.id, 'text': g0.name,
                   'children': [
                       {
                           'id': g2.id, 'text': g2.name,
                           'children': [
                               {
                                   'id': g4.id, 'text': g4.name,
                               }
                           ]
                       }
                   ]
               }, {
            'id': g1.id, 'text': g1.name,
            'children': [
                {
                    'id': g3.id, 'text': g3.name,
                }
            ]
        }
           ] == CoinGroup.get_all_hierarchical()


def test_get_all_hierarchical_with_parent_duplication(add_groups):
    g0, g1, g2, g3, g4 = add_groups
    assert [{
        'id': g0.id, 'text': g0.name,
    }, {
        'id': g0.id, 'text': g0.name,
        'children': [
            {
                'id': g2.id, 'text': g2.name,
            }, {
                'id': g2.id, 'text': g2.name,
                'children': [
                    {
                        'id': g4.id, 'text': g4.name,
                    }
                ]
            }
        ]
    }, {
        'id': g1.id, 'text': g1.name,
    }, {
        'id': g1.id, 'text': g1.name,
        'children': [
            {
                'id': g3.id, 'text': g3.name,
            }
        ]
    }
           ] == CoinGroup.get_all_hierarchical(with_parent_duplication=True)
