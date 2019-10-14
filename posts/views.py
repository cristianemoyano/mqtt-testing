from django.http import HttpResponse
import json

body = {
    "config": {
        "clientid": "hmr1",
        "statusprefix": "hmr1/status/",
        "setprefix": "hmr1/set/",
        "mqttHost": "localhost",
        "mqttPort": 11883
    },
    "defaults": {
        "xs": 4,
        "sm": 3,
        "md": 2,
        "waitingcolor": "grey"
    },
    "views": {
        "main": {
            "title": "Main View",
            "defaults": {
                "color": "#000000",
                "backcolor": "#c0c0c0"
            },
            "rows": [
                {
                    "defaults": {
                        "oncolor": "orange",
                        "offcolor": "#c0c0c0",
                        "xs": 2,
                        "sm": 2,
                        "md": 1
                    },
                    "title": "Alarm",
                    "cols":
                    [
                        {
                            "id": "outdoor-monitor",
                            "text": "Outdoor",
                            "val": 1
                        },
                        {
                            "id": "alarm-status",
                            "text": "ALARMA",
                            "offtext": "KEIN ALARM",
                            "val": 0,
                            "xs": 10,
                            "sm": 10,
                            "md": 11,
                            "oncolor": "red",
                            "readonly": 0
                        }
                    ]
                },
                {
                    "title": "Windows",
                    "cols":
                    [
                        {
                            "id": "open-windows",
                            "text": "Windows",
                            "val": 0,
                            "oncolor": "cyan",
                            "offcolor": "#c0c0c0",
                            "xs": 12,
                            "sm": 12,
                            "md": 12,
                            "readonly": 1,
                            "offtext": "All closed"
                        }
                    ]
                }
            ]
        },
        "cam": {
            "title": "Cam View",
            "defaults": {
                "color": "#000000",
                "backcolor": "#808080",
                "xs": 12,
                "sm": 12,
                "md": 6
            },
            "rows": [
                {
                    "title": "Cameras",
                    "cols":
                    [
                        {
                            "id": "cam-entrance",
                            "text": "Cam entrance",
                            "interval": 2000,
                            "val": 0,
                            "imgurl": "http://<web-cam-ip>/path/to/image.jpg"
                        },
                        {
                            "id": "cam-garden",
                            "text": "Cam garden",
                            "interval": 2000,
                            "val": 0,
                            "imgurl": "http://<web-cam-ip>/path/to/image.jpg"
                        }
                    ]
                }
            ]
        }
    }
}


def post_list(request):
    return HttpResponse(json.dumps(body), content_type='application/json', )
