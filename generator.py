from aitextgen import aitextgen

ai = aitextgen(model_folder='model')


def generateforout(prompting=""):
    return ai.generate_one(prompt=prompting,
                           max_length=256,
                           temperature=1.0,
                           top_p=0.9)
