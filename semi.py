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

class SuperMeta:
    # All displayable traits, in default order
    trait_types = ['background', 'attachment', 'torso', 'strap', 'head', 'headmask', 'beard', 'hair', 'mask', 'headpiece', 'accessory', 'mouth', 'hand', 'eyes']
    trait_types_nobg = trait_types[1:]
    head_trait_types = [t for t in trait_types if t not in ["hand", "strap", "torso", "attachment"]]
    head_trait_types_nobg = head_trait_types[1:]

    # # headpiece default idx = 10, these should be 8, eg under (instead of?) "hair"
    traits_zidx_exceptions = {
        "Hero": {
            "headpiece": {
                "Elon Wannabe": 8,
                "Paper Bagging It": 8,
                "Blue Balaclava": 8,
                "Blue Balaclava": 8,
                "Stripey Balaclava": 8,
                "Yellow Balaclava": 8,
                "Beat Down": 8,
                "Flying Colors With Hair": 8,
                "Flying Colors": 8,
                "60s Mouseman": 8,
                "Mouseman": 8,
                "Bucket Gal": 8,
                "Super Bucket": 8,
                "Butterfly Guy": 8,
                "Captain Blue": 8,
                "Captain Pink": 8,
                "Captain Rainbow": 8,
                "Captain Marvel-ish": 8,
                "Pussy Cat": 8,
                "The Caffeinator": 8,
                "Game Grinder Black": 8,
                "Game Grinder Blue": 8,
                "Game Grinder Red": 8,
                "Game Grinder White": 8,
                "Udder Destruction": 8,
                "Wild West Brown Hat": 8,
                "Wild West Tan Hat": 8,
                "Crash Landing Red": 8,
                "Crash Landing White": 8,
                "Super Fry": 8,
                "The Kerminator": 8,
                "Beat Up": 8,
                "Blue Hood": 8,
                "Red Hood": 8,
                "White Hood": 8,
                "Cyborg-ish": 8,
                "Shiny Blue": 8,
                "She-Cyborg-ish": 8,
                "Pigeon Guy": 8,
                "The Unblocker": 8,
                "Red Lightning": 8,
                "Aftermath": 8,
                "Pot Head": 8,
                "Star Spangled Bandana": 8,
                "Sushi Guy": 8,
                "Teenage Mutant Ninja Semi": 8,
                "Sub-Sub-Zero": 8,
                "Wolverine-ish": 8,
                "Croissant Headpiece": 8,
                "Deafbeef Headpiece": 8,
                "DeeZe Headpiece": 8,
                "Notsofast Headpiece": 8,
                "Steve.k Headpiece": 8,
                "Bearsnake Headpiece": 8,
                "SeeMikeDraw Headpiece": 8,
                #
                "Black Afro": 6,
                "Comb Over": 6,
                "Frizzy Blonde": 6,
                "Gold Hair": 6,
                "Harley Twin Hair": 6,
                "Hulk-ish Dork Hair": 6,
                "Hulk-ish Quiff": 6,
                "She Hulk-ish Long Hair": 6,
                "She Hulk-ish Hair": 6,
                "Neat Blonde Hair": 6,
                "Neat Brown Hair": 6,
                "Short Dark Hair": 6,
                "Brown Hair": 6,
                "Ginger Hair": 6,
                "Short White Hair": 6,
                "White Hair": 6,
                "Brown Mohawk": 6,
                "White Mohawk": 6,
                "Blonde Quiff": 6,
                "Brunette Quiff": 6,
                "White Quiff": 6,
                "Dork Hair": 6,
                "Half Shave Dark Brown": 6,
                "Half Shave Light Brown": 6,
                "Half Shave White": 6,
                "Half Shave Pink Tips": 6,
                "Undercut Brunette": 6,
                "Undercut Pink Stripe": 6,
                "Griffith Hair": 6,
                "Loopify Hair": 6,
                "Miller Hair": 6,
                "Rafi_0x Hair": 6,
                "Redphone Hair": 6            
            },
            "accessory": {
                "Golden Headpiece": 8,
                "Female Brunette Hair": 8,
                "Female Brunette Hair": 8,
                "Korra-ish Hair": 8,
                "Blue Tips": 8,
                "Long White": 8,
                "Not-Poison Ivy Hair With Pot Hat": 8,
                "Not-Poison Ivy Hair With Flower": 8,
                "Pink Bob": 8,
                "Blue Unicorn": 8,
                "Brunette Unicorn": 8,
                "Pink Unicorn": 8,
                "I Care White Hair": 8,
                "Blue Jewel of Infinite Something Something": 8,
                "Red Jewel of Infinite Something Something": 8,
                "Silver Headpiece": 8,
                "Andolini Hair": 8,
                "Claire Hair": 8,
                "Isenberg Hair": 8            
                }
        },
        "Villain": {
            "headpiece": {
                "Acryllic Hair": 6,
                "Evil Black Afro": 6,
                "Evil Pink Afro": 6,
                "Experimental Haircut": 6,
                "Neat Black Hair With Stripe": 6,
                "Crossbones Clown Hair": 6,
                "Green Clown Hair": 6,
                "Pink Clown Hair": 6,
                "Teal Clown Hair": 6,
                "Devil's Peak": 6,
                "Green Bun Hair": 6,
                "Neat Gray Hair With Stripe": 6,
                "Black Undercut": 6,
                "Black Hair": 6,
                "Other Black Hair": 6,
                "Metal Hair": 6,
                "Black Mohawk": 6,
                "Green Mohawk": 6,
                "Gray Mohawk": 6,
                "Metal Mohawk": 6,
                "Pink Mohawk": 6,
                "Teal Mohawk": 6,
                "Evil White Mohawk": 6,
                "Black Dork Hair": 6,
                "Purple Quiff": 6,
                "Evil Half Shave White": 6,
                "White Undercut With Evil Green Stripe": 6,
                #
                "Bone-dana": 8,
                "Skull Bandana": 8,
                "Stripy Bandana": 8,
                "Evil Black Bucket": 8,
                "Captain A-Scarier": 8,
                "The Lowballer": 8,
                "Evil Gas Mask": 8,
                "Dark Blue Hood": 8,
                "Dark Green Hood": 8,
                "Dark Purple Hood": 8,
                "Maroon Hood": 8,
                "Magnetic-o With Spoon": 8,
                "Magnetic-o With Watch": 8,
                "Banana Headpiece": 8,
                "Banana Viking Helmet": 8,
                "Spiky Bone Pot": 8,
                "Brainiac": 8,
                "Evil Cyborg-ish": 8,
                "Super Evil Tophat": 8,
                "Gremplin Headpiece": 8
            }
        }
    }

    @staticmethod
    def rarity_category(semi, trait, trait_total):
        names = [
            "1/1", "Legendary", "Epic", "Rare", "Uncommon", "Common"
        ]
        cutoffs_heroes = {
            "alignment": [1, 8, 100, 200, 200],
            "Heroicness": [1, 8, 100, 200, 200],
            "background": [1, 8, 100, 200, 200],
            "attachment": [1, 8, 100, 200, 300],
            "torso": [1, 8, 24, 110, 180],
            "strap": [1, 8, 24, 200, 400],
            "head": [1, 8, 24, 200, 300],
            "beard": [1, 8, 24, 50, 500],
            "headmask": [1, 8, 24, 200, 200],
            "headpiece": [1, 8, 24, 80, 130],
            "mask": [1, 8, 24, 160, 200],
            "accessory": [1, 8, 24, 100, 500],
            "hand": [1, 8, 25, 150, 300],
            "eyes": [1, 8, 24, 90, 1500],
            "mouth": [1, 8, 24, 150, 500]
        }
        cutoffs_villains = {
            "alignment": [1, 8, 100, 200, 200],
            "Evilness": [1, 8, 100, 200, 200],
            "background": [1, 8, 40, 100, 200],
            "attachment": [1, 8, 20, 100, 200],
            "torso": [1, 8, 24, 90, 140],
            "strap": [1, 8, 24, 200, 480],
            "head": [1, 10, 50, 250, 400],
            "beard": [1, 8, 24, 50, 600],
            "headmask": [1, 8, 24, 200, 200],
            "headpiece": [1, 8, 24, 80, 130],
            "mask": [1, 8, 24, 160, 200],
            "accessory": [1, 8, 24, 100, 500],
            "hand": [1, 8, 25, 100, 300],
            "eyes": [1, 8, 24, 90, 400],
            "mouth": [1, 8, 24, 85, 400]
        }
        cutoffs = cutoffs_heroes[trait.trait_type] if not "Villain" in semi.name else cutoffs_villains[trait.trait_type]
        for i, c in enumerate(cutoffs):
            if trait.occurrence <= c:
                return names[i]
        return names[-1]

    @staticmethod
    def load():
        meta_original_file = 'resources/meta/supers.json'
        meta_rarities_file = 'resources/meta/supers_rarities.json'
        rarities_available = os.path.isfile(meta_rarities_file)
        with open(meta_rarities_file if rarities_available else meta_original_file, 'r') as file:
            semis = []
            all_traits = []
            semis_json = json.load(file)
            for semi_id in semis_json.keys():
                semi_json = semis_json[semi_id]
                semi = json.loads(json.dumps(semi_json), object_hook=lambda d: SimpleNamespace(**d))
                semis.append(semi)
                if not rarities_available:
                    all_traits.extend([(a.trait_type, a.value) for a in semi.attributes])
            # Generate rarities
            if not rarities_available:
                print("Crunching rarities...")
                num_semis = len(semis)
                trait_rarities = {}
                for trait in all_traits:
                    if trait not in trait_rarities:
                        trait_rarities[trait] = (all_traits.count(trait), all_traits.count(trait) / num_semis)
                for semi in semis:
                    for attr in semi.attributes:
                        attr.occurrence = trait_rarities[(attr.trait_type, attr.value)][0]
                        attr.rarity = trait_rarities[(attr.trait_type, attr.value)][1]
                        attr.rarity_category = SuperMeta.rarity_category(semi, attr, num_semis)
                with open(meta_rarities_file, 'w') as outfile:
                    json.dump({k: v for k, v in enumerate(semis)}, outfile, default=vars)
                print("Done")
            return semis


class SemiSuper(object):
    def __init__(self, token_id, artwork_root, meta):
        self.token_id = token_id
        self.artwork_root = artwork_root
        self.meta = meta
        self.name = meta.name
        self.is_villain = "Villain" in meta.name

    def meta_trait(self, trait_type):
        try:
            attr = next(filter(lambda a: a.trait_type == trait_type, self.meta.attributes))
            return attr.value if attr is not None else None
        except:
            return None

    @property
    def opensea_url(self):
        return "https://opensea.io/assets/0xac87febdf7ef7d5f930497cafab9c25d35b932f9/{}".format(self.token_id)

    @property
    def path(self):
        return "{}/{}".format(self.artwork_root, self.token_id)

    @property
    def pfp(self):
        return "{}/{}.png".format(self.path, self.token_id)
    
    @property
    def pfp_gif(self):
        return "{}/{}.gif".format(self.path, self.token_id)

    @property
    def pfp_custom(self):
        return "{}/{}-custom.png".format(self.path, self.token_id)

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

    def get_traits_assets(self, include_trait_types=SuperMeta.trait_types):
        semi_traits_ordered = SuperMeta.trait_types.copy()
        semi_traits = [(a.trait_type, a.value) for a in self.meta.attributes if a.trait_type in semi_traits_ordered and a.trait_type in include_trait_types]
        # re-arrange our official trait order based on any exceptions (Put this in the meta-data gen?)
        for trait_type, trait_value in semi_traits:
            try:
                e = SuperMeta.traits_zidx_exceptions[self.meta_trait("alignment")][trait_type]
                semi_traits_ordered.insert(e[trait_value]+1, semi_traits_ordered.pop(semi_traits_ordered.index(trait_type)))
            except:
                pass
        semi_traits = [t for t in semi_traits_ordered if t in [st[0] for st in semi_traits]]
        return list(map(lambda t: "{}/{}.png".format(self.path, t), semi_traits))


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
            imagetools.pfp(semi, trait_types=SuperMeta.trait_types).save(semi.pfp)

        if not cache or not os.path.isfile(semi.pfp_nobg):
            imagetools.pfp(semi, trait_types=SuperMeta.trait_types_nobg).save(semi.pfp_nobg)

        if not cache or not os.path.isfile(semi.head):
            imagetools.pfp(semi, trait_types=SuperMeta.head_trait_types, xy=(0,45)).save(semi.head)

        if not cache or not os.path.isfile(semi.head_nobg):
            imagetools.pfp(semi, trait_types=SuperMeta.head_trait_types_nobg, xy=(0,45)).save(semi.head_nobg)

        if not cache or not os.path.isfile(semi.gm):
            imagetools.gm(semi, trait_types=SuperMeta.trait_types_nobg).save(semi.gm)

        if not cache or not os.path.isfile(semi.gn):
            imagetools.gm(semi, trait_types=SuperMeta.trait_types_nobg, gn=True).save(semi.gn)

        return semi

    @staticmethod
    def pfp_custom(token_id, trait_types):
        semi = SuperFactory.get(token_id)
        custom = imagetools.pfp(semi, trait_types=trait_types).save(semi.pfp_custom)
        return semi

    @staticmethod
    def catchphrase(token_id, phrase):
        semi = SuperFactory.get(token_id)
        imagetools.catchphrase(semi, SuperMeta.trait_types_nobg, phrase).save(semi.catchphrase)
        return semi

    @staticmethod
    def vs(token_id, token_id2, fight_round=None):
        semi = SuperFactory.get(token_id)
        semi_opponent = SuperFactory.get(token_id2)
        imagetools.vs(semi, semi_opponent, SuperMeta.trait_types_nobg, fight_round).save(semi.vs)
        return (semi, semi_opponent)

    @staticmethod
    async def vs_gif(token_id=None):
        if token_id is not None:
            semi = SuperFactory.get(token_id)
            opps = [SuperFactory.get(i) for i in random.sample(range(0, 5554), 10)]
            return imagetools.gifio([imagetools.vs(semi, opp, SuperMeta.trait_types_nobg) for opp in opps])
        else:
            opps1 = [SuperFactory.get(i) for i in random.sample(range(0, 5554), 10)]
            opps2 = [SuperFactory.get(i) for i in random.sample(range(0, 5554), 10)]
            return imagetools.gifio([imagetools.vs(opps[0], opps[1], SuperMeta.trait_types_nobg) for opps in list(zip(opps1, opps2))])

#
# CLI
#
async def gen(token_ids):
    for token_id in token_ids:
        semi = SuperFactory.get(token_id, cache=False)
        SuperFactory.catchphrase(token_id, "This is not a test of the emergency broadcasting system, this is the real deal!")
        SuperFactory.pfp_custom(token_id, trait_types=["head", "torso"])
        SuperFactory.vs(token_id, random.randint(0, 5554))

async def main(argv):
    if len(argv) == 0:
        return
    if argv[0] == "--all":
        all_ids = map(lambda i: str(i), range(0, 5555))
        await gen(all_ids, cache=False)
    else:
        await gen(argv)
            
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(main(sys.argv[1:]))

