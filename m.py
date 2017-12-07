from datetime import datetime
from unittest import mock

def run_tests():
    handler(11, 0)
    handler(11, 9)
    handler(0, 9)
    handler(0, 0)

    with mock.patch('__main__.send_message') as sender_mock:
        with mock.patch('__main__.log_event') as logger_mock:
            handler(11, 0)
            sender_mock.assert_called_with(
                'marketing@acme.test',
                '11 orders was handled during today successfully.'
            )
            sender_mock.reset_mock()
            logger_mock.assert_called_with('success: failed 0 orders, success 11 orders')
            logger_mock.reset_mock()

            handler(11, 9)
            assert send_message.mock_calls == [
                mock.call(
                    'marketing@acme.test',
                    (
                        'Just 11 orders was handled during today successfully.\n'
                        '9 orders had problem with handle'
                    )
                ),
                mock.call(
                    'support@acme.test',
                    (
                        'Just 11 orders was handled during today successfully.\n'
                        '9 orders had problem with handle'
                    )
                )
                ]
            sender_mock.reset_mock()
            logger_mock.assert_called_with('incident: failed 9 orders, success 11 orders')
            logger_mock.reset_mock()

            handler(0, 0)
            sender_mock.assert_called_with(
                'support@acme.test',
                'No one order wasn\'t handled during today.'
            )
            logger_mock.assert_called_with('idle: failed 0 orders, success 0 orders')

def handler(s, f):
    if f:
        m = 'Just '+str(s)+' orders was handled during today successfully.\n'+str(f)+' orders had problem with handle'
        send_message('marketing@acme.test', m)
        send_message('support@acme.test', m)

    if s and not f:
        m = str(s)+' orders was handled during today successfully.'
        send_message('marketing@acme.test', m)

    if not s and not f:
        m = message = 'No one order wasn\'t handled during today.'
        send_message('support@acme.test', m)

    if f:
        log_m = 'incident: failed '+str(f)+' orders, success '+str(s)+' orders'
        log_event(log_m)

    if s and not f:
        log_m = 'success: failed '+str(f)+' orders, success '+str(s)+' orders'
        log_event(log_m)

    if not s and not f:
        log_m = 'idle: failed '+str(f)+' orders, success '+str(s)+' orders'
        log_event(log_m)

def send_message(u, m):
    print('"""\nTO: {}\n{}\n"""'.format(u, m))

def log_event(message):
    print('{}: {}'.format(datetime.utcnow().isoformat(), message))


if __name__ == '__main__':
    run_tests()
