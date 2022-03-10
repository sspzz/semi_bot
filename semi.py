import os
from os import path
import sys
import json
import asyncio
from types import SimpleNamespace
import urllib.request
import imagetools
import zipfile
import random

class SemiSuper(object):
    def __init__(self, token_id, artwork_root, meta):
        self.token_id = token_id
        self.artwork_root = artwork_root
        self.meta = meta
        self.name = meta.name
        self.is_villain = "Villain" in meta.name

    def make_catchphrase(self, phrase):
        imagetools.catchphrase(self, phrase).save(self.catchphrase)

    def make_vs(self, semi_opponent, fight_round=None):
        imagetools.vs(self, semi_opponent, fight_round).save(self.vs)

    def meta_trait(self, trait_type):
        return next(filter(lambda a: a.trait_type == trait_type, self.meta.attributes)).value

    @property
    def path(self):
        return "{}/{}".format(self.artwork_root, self.token_id)

    @property
    def pfp(self):
        return "{}/{}.png".format(self.path, self.token_id)
    
    @property
    def pfp_nobg(self):
        return "{}/{}-nobg.png".format(self.path, self.token_id)

    @property
    def head(self):
        return "{}/{}-head.png".format(self.path, self.token_id)
    
    @property
    def head_nobg(self):
        return "{}/{}-head-nobg.png".format(self.path, self.token_id)

    @property
    def gm(self):
        return "{}/{}-gm.png".format(self.path, self.token_id)

    @property
    def gn(self):
        return "{}/{}-gn.png".format(self.path, self.token_id)

    @property
    def vs(self):
        return "{}/{}-vs.png".format(self.path, self.token_id)

    @property
    def catchphrase(self):
        return "{}/{}-catchphrase.png".format(self.path, self.token_id)

    @property
    def background_color(self):
        bg_name = meta_trait("background")


    @property
    def traits(self):
        return [
            "{}/eyes.png".format(self.path),
            "{}/hand.png".format(self.path),
            "{}/mouth.png".format(self.path),
            "{}/accessory.png".format(self.path),
            "{}/headpiece.png".format(self.path),
            "{}/mask.png".format(self.path),
            "{}/hair.png".format(self.path),
            "{}/beard.png".format(self.path),
            "{}/headmask.png".format(self.path),
            "{}/head.png".format(self.path),
            "{}/strap.png".format(self.path),
            "{}/torso.png".format(self.path),
            "{}/attachment.png".format(self.path),
            "{}/background.png".format(self.path)
        ]

class SuperMeta:
    @staticmethod
    def load():
        with open('resources/meta/supers.json', 'r') as file:
            semis = []
            all_traits = []
            semis_json = json.load(file)
            for semi_id in semis_json.keys():
                semi_json = semis_json[semi_id]
                semi = json.loads(json.dumps(semi_json), object_hook=lambda d: SimpleNamespace(**d))
                semis.append(semi)
                all_traits.extend(list(map(lambda a: "{}: {}".format(a.trait_type, a.value), semi.attributes)))
            num_semis = len(semis)            
            # Not very optimized, but calculate rarities for all traits, then update the original metadata
            # flattened = sum(list(map(lambda s: list(map(lambda a: "{}: {}".format(a.trait_type, a.value), s.attributes)), semis)), [])
            trait_rarities = {}
            for trait in all_traits:
                if trait not in trait_rarities:
                    trait_rarities[trait] = all_traits.count(trait) / num_semis            
            # Then update the meta data for each semi with the rarity for it's traits
            def rarity_name(rarity, total):
                if rarity < 2 / total:
                    return "Artifact"
                elif rarity <= 14 / total:
                    return "Legendary"
                elif rarity <= 42 / total:
                    return "Epic"
                elif rarity <= 98 / total:
                    return "Rare"
                elif rarity <= 1110 / total:
                    return "Uncommon"
                else:
                    return "Common"
            for semi in semis:
                for attr in semi.attributes:
                    attr.rarity = trait_rarities["{}: {}".format(attr.trait_type, attr.value)]
                    attr.rarity_name = rarity_name(attr.rarity, num_semis)

            return semis


class SuperFactory:
    semis_meta = SuperMeta.load()

    @staticmethod
    def get(token_id, cache=True):
        token_id = int(token_id)

        path_artwork = "{}/artwork".format(os.getcwd())
        if not os.path.isdir(path_artwork):
            os.makedirs(path_artwork)

        semi = SemiSuper(token_id, path_artwork, SuperFactory.semis_meta[token_id])

        def download_content():
            zip_file = "{}/{}.zip".format(path_artwork, token_id)
            endpoint_semi_artwork = 'https://nftz.semisupers.com/layers/{}.zip'
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(endpoint_semi_artwork.format(token_id), zip_file)
            zip_ref = zipfile.ZipFile(zip_file, 'r')
            zip_ref.extractall(semi.path)
            os.remove(zip_file)    

        # Download and generate content
        if not cache or not os.path.isfile(semi.path):
            download_content()
        if not cache or not os.path.isfile(semi.pfp):
            imagetools.pfp(semi).save(semi.pfp)
        if not cache or not os.path.isfile(semi.pfp_nobg):
            imagetools.pfp(semi, background=False).save(semi.pfp_nobg)
        if not cache or not os.path.isfile(semi.head):
            imagetools.head(semi).save(semi.head)
        if not cache or not os.path.isfile(semi.head_nobg):
            imagetools.head(semi, background=False).save(semi.head_nobg)
        if not cache or not os.path.isfile(semi.gm):
            imagetools.gm(semi).save(semi.gm)
        if not cache or not os.path.isfile(semi.gn):
            imagetools.gm(semi, gn=True).save(semi.gn)

        return semi


#
# CLI
#
async def gen(token_ids):
    for token_id in token_ids:
        semi = SuperFactory.get(token_id, cache=False)
        semi.make_catchphrase("This is a test of the emergency broadcasting system!")
        semi2 = SuperFactory.get(random.randint(0, 5554), cache=False)
        semi.make_vs(semi2)

async def main(argv):
    if len(argv) == 0:
        return
    if argv[0] == "--all":
        all_ids = map(lambda i: str(i), range(0, 5555))
        await gen(all_ids, cache=False)
    else:
        await gen(argv)
            
if __name__ == "__main__":
    print(SuperFactory.semis_meta[5340])
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(main(sys.argv[1:]))

