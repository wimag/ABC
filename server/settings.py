# elastic search
HOST = "176.112.219.149"
PORT = 9200
INDEX = "rg"

# posts
POST_MAX_LENGTH = 300
LEFT_BLOCK_LENGTH = 40

# graph
GRAPH_PATH = "../graph/graph.bin"
DRAW_RADIUS = 1

# use Quality Analysis
USE_QA = False

# auth
keys = {
    'SOCIAL_TWITTER': {
        'consumer_key': 'twitter consumer key',
        'consumer_secret': 'twitter consumer secret'
    },
    'SOCIAL_FACEBOOK': {
        'consumer_key': 'XXXXX',
        'consumer_secret': 'XXXXX',
        'request_token_params': {'scope': 'email,publish_stream'}
    }
}
