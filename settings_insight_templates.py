import time

DASHBOARD_TEMPLATES = [
        {
        'name':'twitter_personal_words',
        'template':{
            "username": "USERNAME",
            "name": "Twitter Wordart",
            "created": time.time(),
            "deleted": False,
            "short_url": { },
            "last_saved": time.time(),
            "widgets": { "something": [ ] },
            "last_saved_pretty": "32 seconds ago",
            "collections": [
                    {
                    "search_results": [],
                    "search_filters": { "time": "[*%20TO%20*]" },
                    "data_points": [
                            {
                            "image_large": "/static/images/thedashboard/data_points/twitter_large.png",
                            "configured_display_name": "",
                            "image_medium": "/static/images/thedashboard/data_points/twitter_medium.png",
                            "configured": False,
                            "image_small": "/static/images/thedashboard/data_points/twitter_small.png",
                            "id": "c2243ff90f0a40009d0785278d4a7169",
                            "elements": [ { "display_name": "Your Twitter username:", "type": "text", "name": "keywords", "value": "", "help": "Enter your Twitter username here" } ],
                            "display_name_short": "Twitter",
                            "full_display_name": "Twitter Search",
                            "type": "twittersearch",
                            "sub_type": "twittersearch",
                            "instructions": "To create amazing word art from you twitter conversations just add your Twitter username to box below and click save."
                        }
                    ],
                    "actions": [
                            {
                            "elements": [ ],
                            "name": "datalayertagging",
                            "configured": True,
                            "image_small": "/static/images/thedashboard/actions/tagging_small.png",
                            "display_name_long": "Tagging",
                            "display_name_short": "Tagging",
                            "content_properties": { "added": [ { "display_name": "Tags", "type": "string", "name": "tags" } ] },
                            "id": "d5995f1afca04efea3c753d8be4d15a4",
                            "instructions": "This actions does not need configuring."
                        }
                    ],
                    "options": [],
                    "outputs": [],
                    "visualizations": [
                            {
                            "elements": [
                                    {
                                    "display_name": "Color Scheme",
                                    "help": "",
                                    "value": "Orange",
                                    "values": ["Blue","Green","Grey","Orange","Purple","RedBlue - Green","Blue - Purple","Green - Blue","Orange - Red","Purple - Red","Yellow - Brown"],
                                    "type": "select",
                                    "name": "colorscheme"
                                },
                                    {
                                    "display_name": "Background",
                                    "help": "",
                                    "value": "Light",
                                    "values": ["Light","Dark"],
                                    "type": "select",
                                    "name": "background"
                                },
                                    {
                                    "display_name": "Style",
                                    "help": "",
                                    "value": "Standard",
                                    "values": ["Standard","Word Mashup"],
                                    "type": "select",
                                    "name": "style"
                                },
                                    {
                                    "display_name": "Word Limit",
                                    "help": "",
                                    "value": "100",
                                    "values": ["100","50","20","10","5"],
                                    "type": "select",
                                    "name": "wordlimit"
                                }
                            ],
                            "name": "d3cloud",
                            "configured": True,
                            "image_small": "/static/images/thedashboard/area_chart.png",
                            "data_dimensions": [
                                    {
                                    "display_name": "Words",
                                    "name": "category1",
                                    "value": {"name": "Tags","value": "action_datalayertagging_tags_s"},
                                    "values": [{"name": "Tags","value": "action_datalayertagging_tags_s"}],
                                    "type": "string",
                                    "help": ""
                                }
                            ],
                            "display_name_long": "Words",
                            "display_name_short": "Words",
                            "unconfigurable_message": "There is no category data available to be plotted. Try adding something like tagging",
                            "type": "javascript",
                            "id": "980feda2bbf34e34a01fa8d2e9ea8b34"
                        }
                    ],
                    "id": "4f43d3b57a9c1b3f3d000000"
                },
                    {
                    "search_results": [],
                    "search_filters": [],
                    "data_points": [],
                    "actions": [],
                    "options": [],
                    "outputs": [],
                    "visualizations": [],
                    "id": "4f43d3b57a9c1b3f3d000001"
                }
            ],
            "community": {
                "challenges": 0,
                "remixes": 0,
                "comments": 0,
                "views": 0
            },
            "accessed": 1,
            "active": True,
            "created_pretty": "",
            "config": [],
            }
    },
        {
        'name':'twitter_sentiment_location',
        'template': {
            "username": '',
            "name": "Sentiment towards your location",
            "created": 1329907410.9264,
            "deleted": False,
            "short_url": {},
            "last_saved": 1329907522.6308,
            "widgets": { "something": [] },
            "last_saved_pretty": "just now",
            "collections": [
                    {
                    "search_results": [],
                    "search_filters": { "time": "[*%20TO%20*]" },
                    "data_points": [
                            {
                            "image_large": "/static/images/thedashboard/data_points/twitter_large.png",
                            "configured_display_name": "Twitter: London",
                            "image_medium": "/static/images/thedashboard/data_points/twitter_medium.png",
                            "configured": False,
                            "image_small": "/static/images/thedashboard/data_points/twitter_small.png",
                            "id": "acb5a095d8f540be81024bef3c86c70c",
                            "elements": [
                                    {
                                    "display_name": "Your Location",
                                    "type": "text",
                                    "name": "keywords",
                                    "value": "",
                                    "help": "The keywords or hashtags that you want to use to search Twitter"
                                }
                            ],
                            "display_name_short": "Twitter",
                            "full_display_name": "Twitter Search",
                            "type": "twittersearch",
                            "sub_type": "twittersearch",
                            "instructions": "Enter your location in the box below and then hit save."
                        }
                    ],
                    "actions": [
                            {
                            "elements": [

                            ],
                            "name": "localsentimentanalysis",
                            "configured": True,
                            "image_small": "/static/images/thedashboard/actions/sentiment_small.png",
                            "display_name_long": "Sentiment Analysis",
                            "display_name_short": "Sentiment",
                            "content_properties": {
                                "added": [
                                        {
                                        "display_name": "Sentiment",
                                        "type": "string",
                                        "name": "sentiment"
                                    }
                                ]
                            },
                            "id": "07cb1042859d4034a3f59849457f5f05",
                            "instructions": "This actions does not need configuring."
                        }
                    ],
                    "options": [

                    ],
                    "outputs": [

                    ],
                    "visualizations": [
                            {
                            "elements": [
                                    {
                                    "display_name": "Color Scheme",
                                    "help": "",
                                    "value": "Blue",
                                    "values": [
                                        "Blue",
                                        "Green",
                                        "Grey",
                                        "Orange",
                                        "Purple",
                                        "RedBlue - Green",
                                        "Blue - Purple",
                                        "Green - Blue",
                                        "Orange - Red",
                                        "Purple - Red",
                                        "Yellow - Brown"
                                    ],
                                    "type": "select",
                                    "name": "colorscheme"
                                },
                                    {
                                    "display_name": "Background Color",
                                    "help": "",
                                    "value": "Light",
                                    "values": [
                                        "Light",
                                        "Dark"
                                    ],
                                    "type": "select",
                                    "name": "background"
                                },
                                    {
                                    "display_name": "Chart Title",
                                    "type": "text",
                                    "name": "title",
                                    "value": "",
                                    "help": ""
                                }
                            ],
                            "name": "googlepiechart",
                            "configured": True,
                            "image_small": "/static/images/lib/Impressions/pie_chart.png",
                            "data_dimensions": [
                                    {
                                    "display_name": "Pie Slices",
                                    "name": "category1",
                                    "value": {
                                        "name": "Sentiment",
                                        "value": "action_localsentimentanalysis_sentiment_s"
                                    },
                                    "values": [
                                            {
                                            "name": "Sentiment",
                                            "value": "action_localsentimentanalysis_sentiment_s"
                                        }
                                    ],
                                    "type": "string",
                                    "help": ""
                                }
                            ],
                            "display_name_long": "Pie Chart",
                            "snapshot": "<svg height=\"250\" width=\"471\" id=\"chart\"><defs id=\"defs\"></defs><rect fill=\"#ffffff\" stroke-width=\"0\" stroke=\"none\" height=\"250\" width=\"471\" y=\"0\" x=\"0\"></rect><g><text fill=\"#000000\" stroke-width=\"0\" stroke=\"none\" font-weight=\"bold\" font-size=\"11\" font-family=\"Arial\" y=\"28.35\" x=\"82\" text-anchor=\"start\">Sentiment towards London</text></g><g><g><text fill=\"#000000\" stroke-width=\"0\" stroke=\"none\" font-size=\"11\" font-family=\"Arial\" y=\"57.35\" x=\"305\" text-anchor=\"start\">negative</text></g><rect fill=\"#9ecae1\" stroke-width=\"0\" stroke=\"none\" height=\"11\" width=\"11\" y=\"48\" x=\"290\"></rect><g><text fill=\"#000000\" stroke-width=\"0\" stroke=\"none\" font-size=\"11\" font-family=\"Arial\" y=\"75.35\" x=\"305\" text-anchor=\"start\">positive</text></g><rect fill=\"#3182bd\" stroke-width=\"0\" stroke=\"none\" height=\"11\" width=\"11\" y=\"66\" x=\"290\"></rect></g><g><path fill=\"#3182bd\" stroke-width=\"1\" stroke=\"#ffffff\" d=\"M177,126L101.36388169389097,111.57163877689919A77,77,0,0,1,177,49L177,126A0,0,0,0,0,177,126\"></path><text fill=\"#ffffff\" stroke-width=\"0\" stroke=\"none\" font-size=\"11\" font-family=\"Arial\" y=\"87.80838324085293\" x=\"131.22014989183137\" text-anchor=\"start\">22%</text></g><g><path fill=\"#9ecae1\" stroke-width=\"1\" stroke=\"#ffffff\" d=\"M177,126L177,49A77,77,0,1,1,101.36388169389097,111.57163877689919L177,126A0,0,0,1,0,177,126\"></path><text fill=\"#ffffff\" stroke-width=\"0\" stroke=\"none\" font-size=\"11\" font-family=\"Arial\" y=\"171.89161675914707\" x=\"200.7798501081686\" text-anchor=\"start\">78%</text></g><g></g></svg>",
                            "display_name_short": "Pie",
                            "unconfigurable_message": "There is no category data available to be plotted. Try adding something like sentiment analysis",
                            "type": "javascript",
                            "id": "8a1694f3f0f444d8adc138452729cb50",
                            "instructions": "The pie chart is perhaps the most widely used chart in business and although some criticize it, it remains a popular choice when you want to visualize proportions and where exact comparison of values is not needed, and they can look really nice."
                        }
                    ],
                    "id": "4f44c6d2c845b3267b000000"
                },
                    {
                    "search_results": [

                    ],
                    "search_filters": [

                    ],
                    "data_points": [

                    ],
                    "actions": [

                    ],
                    "options": [

                    ],
                    "outputs": [

                    ],
                    "visualizations": [

                    ],
                    "id": "4f44c6d2c845b3267b000001"
                }
            ],
            "community": {
                "challenges": 0,
                "remixes": 0,
                "comments": 0,
                "views": 0
            },
            "accessed": 3,
            "active": True,
            "created_pretty": "a minute ago",
            "config": {
                "live": False,
                "description": "",
                "categories": [

                ]
            },
            "id": "4f44c6d2c845b3267b000002"
        }
    }
]