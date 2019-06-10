import boto3
import logging
import json
import numpy as np

logger = logging.getLogger()
logger.setLevel(logging.INFO)


REGION='us-east-1'
PROBABILITY_THRESHOLD=0.40

# Must be set to the name specified when you created the endpoint using the CreateEndpoint API
SAGEMAKER_ENDPOINT_NAME = 'DEMO-imageclassification-ep--2019-06-10-02-00-45'
object_categories = ['3RT2023-1NF30', 'CWB9-11-30D15', 'MC9A-30-01-K7-S-E', 'XTCE009B01', 'LC1D09KUE']

# Must be set to the name specified when you created the endpoint using the CreateEndpoint API
# SAGEMAKER_ENDPOINT_NAME = 'DEMO-imageclassification-ep--2019-06-06-13-57-25'
# object_categories = ['ak47', 'american-flag', 'backpack', 'baseball-bat', 'baseball-glove', 'basketball-hoop', 'bat', 'bathtub', 'bear', 'beer-mug', 'billiards', 
#     'binoculars', 'birdbath', 'blimp', 'bonsai-101', 'boom-box', 'bowling-ball', 'bowling-pin', 'boxing-glove', 'brain-101', 'breadmaker', 'buddha-101', 'bulldozer', 
#     'butterfly', 'cactus', 'cake', 'calculator', 'camel', 'cannon', 'canoe', 'car-tire', 'cartman', 'cd', 'centipede', 'cereal-box', 'chandelier-101', 'chess-board', 
#     'chimp', 'chopsticks', 'cockroach', 'coffee-mug', 'coffin', 'coin', 'comet', 'computer-keyboard', 'computer-monitor', 'computer-mouse', 'conch', 'cormorant', 
#     'covered-wagon', 'cowboy-hat', 'crab-101', 'desk-globe', 'diamond-ring', 'dice', 'dog', 'dolphin-101', 'doorknob', 'drinking-straw', 'duck', 'dumb-bell', 
#     'eiffel-tower', 'electric-guitar-101', 'elephant-101', 'elk', 'ewer-101', 'eyeglasses', 'fern', 'fighter-jet', 'fire-extinguisher', 'fire-hydrant', 'fire-truck', 
#     'fireworks', 'flashlight', 'floppy-disk', 'football-helmet', 'french-horn', 'fried-egg', 'frisbee', 'frog', 'frying-pan', 'galaxy', 'gas-pump', 'giraffe', 'goat', 
#     'golden-gate-bridge', 'goldfish', 'golf-ball', 'goose', 'gorilla', 'grand-piano-101', 'grapes', 'grasshopper', 'guitar-pick', 'hamburger', 'hammock', 
#     'harmonica', 'harp', 'harpsichord', 'hawksbill-101', 'head-phones', 'helicopter-101', 'hibiscus', 'homer-simpson', 'horse', 'horseshoe-crab', 
#     'hot-air-balloon', 'hot-dog', 'hot-tub', 'hourglass', 'house-fly', 'human-skeleton', 'hummingbird', 'ibis-101', 'ice-cream-cone', 'iguana', 
#     'ipod', 'iris', 'jesus-christ', 'joy-stick', 'kangaroo-101', 'kayak', 'ketch-101', 'killer-whale', 'knife', 'ladder', 'laptop-101', 'lathe', 
#     'leopards-101', 'license-plate', 'lightbulb', 'light-house', 'lightning', 'llama-101', 'mailbox', 'mandolin', 'mars', 'mattress', 'megaphone', 
#     'menorah-101', 'microscope', 'microwave', 'minaret', 'minotaur', 'motorbikes-101', 'mountain-bike', 'mushroom', 'mussels', 'necktie', 'octopus', 
#     'ostrich', 'owl', 'palm-pilot', 'palm-tree', 'paperclip', 'paper-shredder', 'pci-card', 'penguin', 'people', 'pez-dispenser', 'photocopier', 
#     'picnic-table', 'playing-card', 'porcupine', 'pram', 'praying-mantis', 'pyramid', 'raccoon', 'radio-telescope', 'rainbow', 'refrigerator', 
#     'revolver-101', 'rifle', 'rotary-phone', 'roulette-wheel', 'saddle', 'saturn', 'school-bus', 'scorpion-101', 'screwdriver', 'segway', 
#     'self-propelled-lawn-mower', 'sextant', 'sheet-music', 'skateboard', 'skunk', 'skyscraper', 'smokestack', 'snail', 'snake', 'sneaker', 
#     'snowmobile', 'soccer-ball', 'socks', 'soda-can', 'spaghetti', 'speed-boat', 'spider', 'spoon', 'stained-glass', 'starfish-101', 
#     'steering-wheel', 'stirrups', 'sunflower-101', 'superman', 'sushi', 'swan', 'swiss-army-knife', 'sword', 'syringe', 'tambourine', 
#     'teapot', 'teddy-bear', 'teepee', 'telephone-box', 'tennis-ball', 'tennis-court', 'tennis-racket', 'theodolite', 'toaster', 'tomato', 
#     'tombstone', 'top-hat', 'touring-bike', 'tower-pisa', 'traffic-light', 'treadmill', 'triceratops', 'tricycle', 'trilobite-101', 'tripod', 
#     't-shirt', 'tuning-fork', 'tweezer', 'umbrella-101', 'unicorn', 'vcr', 'video-projector', 'washing-machine', 'watch-101', 'waterfall', 
#     'watermelon', 'welding-mask', 'wheelbarrow', 'windmill', 'wine-bottle', 'xylophone', 'yarmulke', 'yo-yo', 'zebra', 'airplanes-101', 'car-side-101', 
#     'faces-easy-101', 'greyhound', 'tennis-shoes', 'toad', 'clutter']
    

# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemaker-runtime.html#SageMakerRuntime.Client.invoke_endpoint
def sagemaker_searchByClassification(productImage):
    
    runtime = boto3.client(service_name='sagemaker-runtime', region_name=REGION)
    
    image = bytearray(productImage);
    
    # try:
    response = runtime.invoke_endpoint(
        EndpointName=SAGEMAKER_ENDPOINT_NAME, 
        Body=image,
        ContentType='application/x-image'

    )
    
    bodyResponse = response['Body'].read()
    contentType = response['ContentType']        
    probability = json.loads(bodyResponse) 


    index = np.argmax(probability)
    
    print('============ index={}'.format(index))
    print(object_categories[index], probability[index])
    print('===================')
    
    if probability[index] <= PROBABILITY_THRESHOLD:
        return 'PRODUCT_NOT_FOUND_DUE_TO_LOW_PROBABLITY', ''

    print('Result: label - {} , probability - {}'.format(object_categories[index], probability[index]))

    return 'PRODUCT_FOUND', object_categories[index]
    # except: 
    #     return 'PRODUCT_NOT_FOUND', ''