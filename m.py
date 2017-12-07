from datetime import datetime
from unittest import mock


params_to_test= [
    {'success': 11, 'failed': 0,
        'sender_response': [
            ['marketing@acme.test', '11 orders was handled during today successfully.'],
        ],
        'logger_response':  'success: failed 0 orders, success 11 orders'
    },
    {'success': 11, 'failed': 9,
        'sender_response': [
            ['marketing@acme.test', 'Just 11 orders was handled during today successfully.\n9 orders had problem with handle'],
            ['support@acme.test', 'Just 11 orders was handled during today successfully.\n9 orders had problem with handle'],
        ],
        'logger_response': 'incident: failed 9 orders, success 11 orders'
    },
    {'success': 0, 'failed': 9,
        'sender_response': [
            ['marketing@acme.test', 'Just 0 orders was handled during today successfully.\n9 orders had problem with handle'],
            ['support@acme.test', 'Just 0 orders was handled during today successfully.\n9 orders had problem with handle'],
        ],
        'logger_response': 'incident: failed 9 orders, success 0 orders'
    },
    {'success': 0, 'failed': 0,
        'sender_response': [
            ['support@acme.test', 'No one order wasn\'t handled during today.'],
        ],
        'logger_response': 'idle: failed 0 orders, success 0 orders'
    },
]


def run_tests():
    for param in params_to_test:
        handler(param['success'], param['failed'])

    with mock.patch('__main__.send_message') as sender_mock:
        with mock.patch('__main__.log_event') as logger_mock:
            for param in params_to_test:
                handler(param['success'], param['failed'])

                sender_calls = []
                for res in param['sender_response']:
                    sender_calls.append(mock.call(res[0], res[1]))
                assert send_message.mock_calls == sender_calls
                sender_mock.reset_mock()

                logger_mock.assert_called_with(param['logger_response'])
                logger_mock.reset_mock()


def handler(success, failed):
    if failed:
        msg = 'Just {0} orders was handled during today successfully.\n{1} orders had problem with handle'.format(success, failed)
        send_message('marketing@acme.test', msg)
        send_message('support@acme.test', msg)
        log_event('incident: failed {1} orders, success {0} orders'.format(success, failed))
    else:
        if success:
            send_message('marketing@acme.test', '{0} orders was handled during today successfully.'.format(success))
            log_event('success: failed {1} orders, success {0} orders'.format(success, failed))
        else:
            send_message('support@acme.test', 'No one order wasn\'t handled during today.')
            log_event('idle: failed {1} orders, success {0} orders'.format(success, failed))


def send_message(recipient, message):
    print('"""\nTO: {}\n{}\n"""'.format(recipient, message))


def log_event(message):
    print('{}: {}'.format(' '.join(datetime.utcnow().isoformat().split('T')), message))


if __name__ == '__main__':
    run_tests()
