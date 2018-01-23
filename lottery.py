# coding: utf-8
import candy
import orm
import utils


def lottery_participators():
    session = utils.gen_session()
    lottery = None
    for user in orm.User.select():
        try:
            session.headers['x-access-token'] = user.token
            if lottery is None:
                lottery = candy.get_lottery(session)
            balance = candy.get_balance(session)
            if balance > 4000:
                candy.withdraw(session, amount=balance)
                user.balance = 0
            elif balance >= lottery['price']:
                candy.lottery_participators(session, lottery['id'])
                user.balance -= lottery['price']
            user.save()
        except KeyboardInterrupt:
            break
        except Exception, e:
            utils.log('Error: %s', e)


def list_my_lottery():
    session = utils.gen_session()
    for user in orm.User.select():
        try:
            session.headers['x-access-token'] = user.token
            reward = candy.get_my_lottery(session)
            if reward > 0:
                print user.phone, reward
        except KeyboardInterrupt:
            break
        except Exception, e:
            utils.log('Error: %s', e)


if __name__ == '__main__':
    lottery_participators()
