
from itertools import count
from os import mkdir
from calc import CharacterEXPFilter
from scrapers.base import BaseScraper
from utils import URL , ImageManipulation, random_char_image, add_cards, fix_amount

from typing import TYPE_CHECKING
from bs4 import BeautifulSoup
from calc import CharacterAscensionFilter
from PIL import ImageFont, ImageDraw, Image, ImageFilter
from io import BytesIO
from os.path import exists

class CharacterScraper(BaseScraper):

    def __init__(self,   client,  url: URL, **kwargs) -> None:
        super().__init__( client, url)
        
        self.type = 'characters'
        print(kwargs)
        self.__dict__.update(kwargs)
        

  
    def get_total_ascension_dict(self, ascension_dict: str):
    
        total = {}    

       
        
        for level in ascension_dict:
            items = ascension_dict[level]
            for itm in items:
                if itm['title'] not in total:
                    total[itm['title']] = {'txt': fix_amount(itm['txt']), 'img': itm['img'], 'card_bg': itm['card_bg']}
                else:
                    total[itm['title']]['txt'] += fix_amount(itm['txt'])        

        return_form = []

        for name in total:
            return_form.append({'title': name, 'txt': total[name]['txt'], 'img': total[name]['img'], 'card_bg': total[name]['card_bg']})
        return return_form


    def _scrape(self):

        '''
        
        scraping script different for each type of page
        
        '''

        src = self.client._session.get(self.url).content
        bs = BeautifulSoup(src, 'lxml')
        infobox = bs.find('aside', {'role': 'region'})

        data = self.get_datasource(infobox, datasources=[{'div': 'h2', 'ds': 'name', 'type': 'txt'},
                                                {'ds':'image'},
                                                {'div': 'td', 'ds': 'rarity'},
                                                {'div': 'td', 'ds': 'weapon'},
                                                {'div': 'td', 'ds': 'element'},
                                                {'ds': 'birthday'},
                                                {'ds': 'constellation', 'type': 'txt_list'},
                                                {'ds': 'region'},
                                                {'ds': 'affiliation', 'type': 'txt_list'},
                                                {'ds': 'dish'},
                                                {'ds': 'obtain', 'type': 'txt_list'},
                                                {'ds': 'mother'},
                                                {'ds': 'siblings', 'type': 'txt_list'},
                                                {'ds': 'voiceEN', 'type': 'txt_list'},
                                                {'ds': 'voiceKR', 'type': 'txt_list'},
                                                {'ds': 'voiceCN', 'type': 'txt_list'},
                                                {'ds': 'voiceJP', 'type': 'txt_list'}])
        

        self.data = {
            **self.data,
            **data
        }


        table = self.get_table(bs, 'Ascensions_and_Stats')

        
        ascension_dict = {}
        if table is not None:
            rows = table.find_all('td', {'colspan': '6'})
            for c,row in enumerate(rows,1):
                if c not in ascension_dict:
                    ascension_dict[str(c)] = []

                images = row.find_all('div', {'class': 'card_container'})
                for image in images:
                    dict_ = self.get_card_info(image)
                    ascension_dict[str(c)].append(dict_)
            

        total = self.get_total_ascension_dict(ascension_dict)
        ascension_dict['total'] = total
            

        self.data['ascension'] = ascension_dict

        filter_data = []
        table = self.get_table(bs, 'Talent_Upgrade')
        if table is not None:
            cols = table.find_all('tr')[1:]
            fixed_rows = [[], [], [], [], []]
            #mora, common item, talent mat, talent mat , talent mat
            for row in cols:
                index = 0
                items = row.find_all('td')
                for itm in items:
                    c = itm.find('div', {'class': 'card_container'})
                    if c is not None:
                        card = self.get_card_info(c)
                        fixed_rows[index].append(card)
                        index += 1          
                
                while index < 5:
                    if index < len(fixed_rows):
                        fixed_rows[index].append(None)
                    index += 1
            
            filter_data = CharacterAscensionFilter(fixed_rows).data

        self.data['talent_upgrade'] = filter_data
        levels = [20, 40, 50, 60, 70, 80, 90]
        data =  [CharacterEXPFilter(d).cards for d in levels]

        self.data['leveling_usage'] = data

        table = self.get_table(bs, 'Talents')
        self.data['talents'] = []
        if table is not None:
            
            rows = list(table.find('tr').find_next_siblings())
            talent = {}
            for row in rows:
                
                cols = row.find_all("td")
                
                if len(cols) == 3:

                    if len(talent) != 0:
                        talent = dict()

                    icon = self.find_image(cols[0])
                    name = cols[1].text.strip()
                    type_ = cols[2].text.strip()
                    talent['name'] = name
                    talent['icon'] = icon
                    talent['type'] =  type_
                    talent['previews'] =  []
                    talent['description'] =  ''
                    
                else:
                    text = row.text
                    gameplay_text = row.find('div', {'data-expandtext': '▼Gameplay Notes▼'}).text if row.find('div', {'data-expandtext': '▼Gameplay Notes▼'}) is not None else ''
                    ats_text = row.find('div', {'data-expandtext': '▼Attribute Scaling▼'}).text if row.find('div', {'data-expandtext': '▼Attribute Scaling▼'}) is not None else ''
                    preview_text = row.find('div', {'data-expandtext': '▼Preview▼'}).text if row.find('div', {'data-expandtext': '▼Preview▼'}) is not None else ''
                    bolds = row.find_all('b')
                    text = text.replace(gameplay_text,'', 1).replace(ats_text,'', 1).replace(preview_text,'',1)
                    for b in bolds:
                        text = text.replace(b.text, f'**{b.text}**\n',1)
                    talent['description'] = text

                    previews = row.find('div', {'data-expandtext': '▼Preview▼'}) if row.find('div', {'data-expandtext': '▼Preview▼'}) is not None else None
                 
                    if previews is not None:

                        preview_gifs = previews.find_all('figure')
                        for prevgif in preview_gifs:

                            text = prevgif.find('figcaption').text if prevgif.find('figcaption') is not None else ''

                            img = self.find_image(prevgif)
                            talent['previews'].append({'text': text, 'img': img})
                    
                    self.data['talents'].append(talent)

        table = self.get_table(bs, 'Constellation')
        self.data['constellations'] = []
        if table is not None:
            const = {}
            rows = table.find_all('tr')[1:]
            for row in rows:

                cols = row.find_all("td")
                if len(cols) == 3:

                    if len(const) != 0:
                        const = dict()
                    
                    icon = self.find_image(cols[0])
                    name = cols[1].text.strip()
                    level = cols[2].text.strip()
                    const['name'] = name
                    const['icon'] = icon
                    const['level'] = level
                
                else:

                    description = row.text
                    const['description'] = description
                    if const not in self.data['constellations']:
                        self.data['constellations'].append(const)

            '''
            
            character completed hopefully 
            '''
            

 



    @property
    def withoutcards(self):

        data = self.data.copy()
        
        ascension_dict = {}
        
        if 'ascension' in data:
            if bool(data['ascension']):
                for level in data['ascension']:
                    if bool(data['ascension'][level]):
                        if level not in ascension_dict:
                            ascension_dict[level] = []
                        for itm in data['ascension'][level]:
                            ascension_dict[level].append({
                                'title': itm['title'],
                                'txt': itm['txt']
                            })
        
        data['ascension'] = ascension_dict
        talent_dict = {}
        if 'talent_upgrade' in data:
            if bool(data['ascension']):
                for level in data['talent_upgrade']:
                    if bool(data['talent_upgrade'][level]):
                        if level not in talent_dict:
                            talent_dict[level] = []
                        
                        for itm in data['talent_upgrade'][level]:
                            d_ = itm.copy()                            
                            if 'mats' in itm:
                                mats = [{
                                        'title': it['title'],
                                        'txt': it['txt']
                                } for it in itm['mats']]
                            else:
                                mats = []
                            d_['mats'] = mats
                            talent_dict[level].append(d_)
        data['talent_upgrade'] = talent_dict

        return data
    
    @property
    def cardimage(self):        
        images = self.data.get('image', None)
        img_url = None
        if images is not None:
            for img in images:
                if 'wish' in img.lower():
                    img_url = images[img]
        if img_url is not None:

            return ImageManipulation.create_image_card(self.name, img_url, False ,'', -350, 95)
    
    def create_ascension_card(self, zerochan: bool = False, save: bool = False):
        '''
    
        creates ascension card
        
        '''
        char = self.data   

        
        img_url = None

        

        images = self.data.get('image', None)
        if images is not None:
            for img in images:
                if 'wish' in img.lower():
                    img_url = images[img]

        if zerochan:
            random_img = random_char_image(self.client.zerochan, self.name)
            if random_img is not None:
                img_url = random_img.url

        if img_url is not None:
            if zerochan:
                card =  ImageManipulation.create_image_card(self.name, img_url, False ,'Ascension and Talent Mats')
            else:
                card =  ImageManipulation.create_image_card(self.name, img_url, False ,'Ascension and Talent Mats',  -350, 95)
            max_item = 5
            start_x = card.size[0] // 2 - 250
            start_y = 250   
            end_x = start_x + (112*5)
            
            if len(self.data['ascension']['total']) != 0:                
                card = ImageManipulation.paste_cards(card, (start_x, start_y), (end_x,0), self.data['ascension']['total'])

           
            rows = len(self.data['ascension']['total']) // 5
            
           
            sum_cards = []

            cards_ = CharacterEXPFilter(90, card_exp_mat=['hw']).cards['cards']        
            sum_cards = add_cards(cards_)

            if len(self.data['talent_upgrade']['total']) != 0:
                sum_cards = add_cards(sum_cards,self.data['talent_upgrade']['total'])          #      
                sum_cards = add_cards(sum_cards,self.data['talent_upgrade']['total'])          # TRIPLE CROWN     
                sum_cards = add_cards(sum_cards,self.data['talent_upgrade']['total'])          #
            
            end_x = start_x + (112 * (len(sum_cards) // 2))
            card = ImageManipulation.paste_cards(card, (start_x, (start_y + 122) +(122 * rows)), (end_x, 0), sum_cards)   
            

            if save:

                if not exists(self.client.images_path+self.name+"/"):
                    mkdir(self.client.images_path+self.name+"/")
                if not exists(self.client.images_path+self.name+"/ascension_talents/"):
                    mkdir(self.client.images_path+self.name+"/ascension_talents/")

                card.save(self.client.images_path+self.name+"/ascension_talents/ascension.png")

            return card
        
    def create_constellation_card(self, zerochan: bool = False, save: bool = False):

        rand = None

        images = self.data.get('image', None)
        if images is not None:
            for img in images:
                if 'wish' in img.lower():

                    rand = images[img]
        if zerochan:
            rand = random_char_image(self.client.zerochan,  self.name)
            rand = rand.url if rand is not None else None
        if rand is not None:
            card = ImageManipulation.create_image_card_wh('Constellations', rand, 1200, 450)
            if 'constellations' in self.data:
                consts = self.data['constellations']

                for const in consts:
                    img_ = const['icon']
                    with self.client._session.get(img_ ) as f:
                        bytes_ = BytesIO(f.content)
                        font = ImageFont.truetype('font.otf', 18)
                        img = Image.open(bytes_, 'r').convert('RGBA')

                        img_new = Image.new('RGBA', img.size)
                        pixels = img.load()    
                        for x in range(img.size[0]):
                            for y in range(img.size[1]):  
                                
                                if pixels[x,y][0] > 150 and pixels[x,y][1] > 150 and pixels[x,y][2] > 150:
                                    img_new.putpixel((x,y), pixels[x,y])
                        img_new = img_new.filter(ImageFilter.SMOOTH())
                        card.paste(img_new, (350 + (consts.index(const) * 138), 120), img_new)
                        text = const['name'].replace(' ','\n', 99)
                        print(text)
                        draw = ImageDraw.Draw(card)
                        size = draw.textsize(text)
                        print(350 + ((consts.index(const) * 138) // 2) - size[0] // 2)
                        draw.text((350 + (consts.index(const) * 138)+ 8, 250), text=text, align='center', font=font, fill=(255,255,255, 150))


                if save:
        
                    if not exists(self.client.images_path+self.name+"/"):
                        mkdir(self.client.images_path+self.name+"/")
                    

                    card.save(self.client.images_path+self.name+"/constellations.png")
    @property
    def constellationcard(self):
        rand = random_char_image(self.client.zerochan,  self.name)
        card = ImageManipulation.create_image_card_wh('Constellations', rand.url, 1200, 450)
        if 'constellations' in self.data:
            consts = self.data['constellations']

            for const in consts:
                img_ = const['icon']
                with self.client._session.get(img_ ) as f:
                    bytes_ = BytesIO(f.content)
                    font = ImageFont.truetype('font.otf', 18)
                    img = Image.open(bytes_, 'r').convert('RGBA')

                    img_new = Image.new('RGBA', img.size)
                    pixels = img.load()    
                    for x in range(img.size[0]):
                        for y in range(img.size[1]):  
                            
                            if pixels[x,y][0] > 150 and pixels[x,y][1] > 150 and pixels[x,y][2] > 150:
                                img_new.putpixel((x,y), pixels[x,y])
                    img_new = img_new.filter(ImageFilter.SMOOTH())
                    card.paste(img_new, (350 + (consts.index(const) * 138), 120), img_new)
                    text = const['name'].replace(' ','\n', 99)
                    print(text)
                    draw = ImageDraw.Draw(card)
                    size = draw.textsize(text)
                    print(350 + ((consts.index(const) * 138) // 2) - size[0] // 2)
                    draw.text((350 + (consts.index(const) * 138)+ 8, 250), text=text, align='center', font=font, fill=(255,255,255, 150))
        return card
    
    