from django.shortcuts import render


def dashboard(request):
    return render(
        request,
        'posts/post_list.html', {
            'body': {
                'devices': [
                    {
                        'name': 'Kitchen',
                        'id': 'kitchen',
                        'device_type': 'actuator',
                        'widget_type': 'switch',
                        'visible': True,
                    },
                    {
                        'name': 'Entrance',
                        'id': 'entrance',
                        'device_type': 'actuator',
                        'widget_type': 'switch',
                        'visible': True,
                    },
                    {
                        'name': 'Backdoor',
                        'id': 'backdoor',
                        'device_type': 'actuator',
                        'widget_type': 'switch',
                        'visible': True,
                    },
                    {
                        'name': 'Living',
                        'id': 'living',
                        'device_type': 'sensor',
                        'widget_type': 'chart',
                        'visible': True,
                    },
                    {
                        'name': 'Basement',
                        'id': 'basement',
                        'device_type': 'sensor',
                        'widget_type': 'chart',
                        'visible': True,
                    },
                ]
            }
        }
    )
