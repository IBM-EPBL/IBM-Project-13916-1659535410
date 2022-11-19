from clarifai_grpc.grpc.api import service_pb2, resources_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
import requests
import json

YOUR_CLARIFAI_API_KEY = ""
YOUR_APPLICATION_ID = ""

def getNutritionData(food):
    query_url= f'https://api.wolframalpha.com/v2/query?input=nutritional+information+of+{food}&format=plaintext&output=JSON&appid=DEMO'
    print(query_url)
    response = requests.get(query_url)
    data = response.json()
    print(data)
    res = data['queryresult']['pods'][1]['subpods'][0]['plaintext']

    var = res.split()
    calories = var[var.index('calories')+1]
    fat = var[var.index('fat', var.index('fat')+1)+1:var.index('fat', var.index('fat')+1)+3]
    carbs = var[var.index('carbohydrates')+1:var.index('carbohydrates')+3]
    protein = var[var.index('protein')+1:var.index('protein')+3]
    # check and convert mg to g
    if fat[1] == 'mg':
        fat[0] = float(fat[0])/1000
        fat[1] = 'g'
    if carbs[1] == 'mg':
        carbs[0] = float(carbs[0])/1000
        carbs[1] = 'g'
    if protein[1] == 'mg':
        protein[0] = float(protein[0])/1000
        protein[1] = 'g'

    print(calories, fat[0], carbs[0], protein[0])
    return calories, fat[0], carbs[0], protein[0]

def getFoodName(image):
    # This is how you authenticate.
    metadata = (("authorization", f"Key {YOUR_CLARIFAI_API_KEY}"),)
    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)

    request = service_pb2.PostModelOutputsRequest(
        model_id="food-item-v1-recognition",
        user_app_id=resources_pb2.UserAppIDSet(app_id=YOUR_APPLICATION_ID),
        inputs=[
            resources_pb2.Input(
                data=resources_pb2.Data(image=resources_pb2.Image(
                        base64=image))
            )
        ],
    )
    response = stub.PostModelOutputs(request, metadata=metadata)

    if response.status.code != status_code_pb2.SUCCESS:
        print(response)
        raise Exception(f"Request failed, status code: {response.status}")

    for concept in response.outputs[0].data.concepts:
        print("%12s: %.2f" % (concept.name, concept.value))

    print(response.outputs[0].data.concepts[0].name)
    food = response.outputs[0].data.concepts[0].name
    return food
