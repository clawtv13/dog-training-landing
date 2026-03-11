#!/usr/bin/env python3
import json, os, requests

STORE=os.environ['SHOPIFY_STORE'].replace('https://','').rstrip('/')
CLIENT_ID=os.environ['SHOPIFY_CLIENT_ID']
CLIENT_SECRET=os.environ['SHOPIFY_CLIENT_SECRET']
API=os.environ.get('SHOPIFY_API_VERSION','2025-01')
THEME_ID='197989826891'


def token():
    r=requests.post(
        f'https://{STORE}/admin/oauth/access_token',
        headers={'Content-Type':'application/x-www-form-urlencoded'},
        data={'grant_type':'client_credentials','client_id':CLIENT_ID,'client_secret':CLIENT_SECRET},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()['access_token']


def get_asset(tok,key):
    r=requests.get(
        f'https://{STORE}/admin/api/{API}/themes/{THEME_ID}/assets.json?asset[key]={key}',
        headers={'X-Shopify-Access-Token':tok}, timeout=30)
    r.raise_for_status()
    return r.json()['asset']['value']


def put_asset(tok,key,value):
    r=requests.put(
        f'https://{STORE}/admin/api/{API}/themes/{THEME_ID}/assets.json',
        headers={'X-Shopify-Access-Token':tok,'Content-Type':'application/json'},
        json={'asset':{'key':key,'value':value}}, timeout=30)
    r.raise_for_status()
    return r.json()


def main():
    tok=token()
    data=json.loads(get_asset(tok,'templates/product.json'))
    sections=data['sections']

    # Add/replace supporting sections under main product
    sections['rich_text_relief_intro'] = {
      'type':'rich-text',
      'blocks':{
        'heading':{'type':'heading','settings':{'heading':'More Than a Cold Pack. It’s a Reset Tool.','heading_size':'h1'}},
        'text':{'type':'text','settings':{'text':'<p>Cooling Relief Cap is built for the moments when your head feels hot, tense, overloaded, or overstimulated. Keep it chilled and ready for a fast, low-effort reset at home, after work, or before bed.</p>'}},
        'button':{'type':'button','settings':{'button_label':'Get Cooling Relief','button_link':'shopify://products/cooling-relief-cap','button_style_secondary':False,'button_label_2':'','button_link_2':'','button_style_secondary_2':False}}
      },
      'block_order':['heading','text','button'],
      'name':'t:sections.rich-text.presets.name',
      'settings':{'desktop_content_position':'center','content_alignment':'center','color_scheme':'','full_width':True,'padding_top':40,'padding_bottom':20}
    }

    sections['multicolumn_core_benefits'] = {
      'type':'multicolumn',
      'blocks':{
        'col1':{'type':'column','settings':{'icon':'','title':'Fast Cooling Comfort','text':'<p>Wraparound cooling feel across the forehead, temples, eyes, and head in minutes.</p>','link_label':'','link':''}},
        'col2':{'type':'column','settings':{'icon':'','title':'Dark, Calm Reset','text':'<p>The stretch-fit design can help block light and create a quieter moment to rest.</p>','link_label':'','link':''}},
        'col3':{'type':'column','settings':{'icon':'','title':'Reusable & Effortless','text':'<p>No cables, no charging, no setup. Chill it, wear it, and use it again whenever needed.</p>','link_label':'','link':''}}
      },
      'block_order':['col1','col2','col3'],
      'name':'t:sections.multicolumn.presets.name',
      'settings':{'title':'Why People Actually Buy It','heading_size':'h1','image_width':'full','image_ratio':'adapt','columns_desktop':3,'column_alignment':'left','background_style':'primary','button_label':'','button_link':'','color_scheme':'','columns_mobile':'1','swipe_on_mobile':False,'padding_top':10,'padding_bottom':10}
    }

    sections['image_with_text_use_cases'] = {
      'type':'image-with-text',
      'blocks':{
        'heading':{'type':'heading','settings':{'heading':'Built for High-Friction Days','heading_size':'h2'}},
        'text':{'type':'text','settings':{'text':'<p>Use it after long laptop sessions, on overheated afternoons, after stressful days, or before bed when you want 10–20 minutes of cool, dark quiet.</p><p>It is simple enough to become part of your routine, which is exactly why it gets used instead of forgotten.</p>','text_style':'body'}},
        'button':{'type':'button','settings':{'button_label':'Keep One Ready','button_link':'shopify://products/cooling-relief-cap','button_style_secondary':False}}
      },
      'block_order':['heading','text','button'],
      'name':'t:sections.image-with-text.presets.name',
      'settings':{'image':'shopify://shop_images/S90d90803ac5a41719536e5cc9a997fdbN.webp','height':'adapt','desktop_image_width':'medium','layout':'image_first','desktop_content_position':'top','desktop_content_alignment':'left','content_layout':'no-overlap','section_color_scheme':'','color_scheme':'','image_behavior':'none','mobile_content_alignment':'left','padding_top':20,'padding_bottom':20}
    }

    sections['multicolumn_how_it_works'] = {
      'type':'multicolumn',
      'blocks':{
        'step1':{'type':'column','settings':{'icon':'','title':'1. Chill It','text':'<p>Place it in the fridge or freezer for at least 10 minutes.</p>','link_label':'','link':''}},
        'step2':{'type':'column','settings':{'icon':'','title':'2. Pull It On','text':'<p>Wear it over the forehead, temples, eyes, and head as desired.</p>','link_label':'','link':''}},
        'step3':{'type':'column','settings':{'icon':'','title':'3. Reset','text':'<p>Relax for 10–20 minutes and let the cooling compression do the rest.</p>','link_label':'','link':''}}
      },
      'block_order':['step1','step2','step3'],
      'name':'t:sections.multicolumn.presets.name',
      'settings':{'title':'How It Works','heading_size':'h1','image_width':'full','image_ratio':'adapt','columns_desktop':3,'column_alignment':'left','background_style':'primary','button_label':'','button_link':'','color_scheme':'','columns_mobile':'1','swipe_on_mobile':False,'padding_top':10,'padding_bottom':10}
    }

    sections['testimonials_product_extra'] = {
      'type':'testimonials',
      'blocks':{
        't1':{'type':'column','settings':{'title':'I keep mine in the fridge and use it almost every evening.','text':'<p>It cools down fast and helps me switch off properly after work.</p>','image_pos':'below_description','author':'<em><strong>— Olivia C.</strong></em>'}},
        't2':{'type':'column','settings':{'title':'The best part is how easy it is.','text':'<p>No straps, no mess, no holding an ice pack in place. I just put it on and lie down for a few minutes.</p>','image_pos':'below_description','author':'<em><strong>— Daniel R.</strong></em>'}},
        't3':{'type':'column','settings':{'title':'Perfect for hot days and overstimulated evenings.','text':'<p>It became part of my nightly wind-down routine almost immediately.</p>','image_pos':'below_description','author':'<em><strong>— Sarah M.</strong></em>'}}
      },
      'block_order':['t1','t2','t3'],
      'name':'Testimonials',
      'settings':{'title':'Why Customers Keep Reaching For It','testimonials_per_row':3,'gap':20,'show_stars':True,'stars_color':'#ffd700','background_color':'#f8f8f9','show_quotes':True,'padding_top':30,'padding_bottom':30}
    }

    sections['rich_text_final_close'] = {
      'type':'rich-text',
      'blocks':{
        'heading':{'type':'heading','settings':{'heading':'Keep One Chilled and Ready.','heading_size':'h1'}},
        'text':{'type':'text','settings':{'text':'<p>If what you want is a fast, reusable, low-effort way to cool down and switch off for a few minutes, this is exactly what Cooling Relief Cap is built for.</p>'}},
        'button':{'type':'button','settings':{'button_label':'Shop Cooling Relief Cap','button_link':'shopify://products/cooling-relief-cap','button_style_secondary':False,'button_label_2':'','button_link_2':'','button_style_secondary_2':False}}
      },
      'block_order':['heading','text','button'],
      'name':'t:sections.rich-text.presets.name',
      'settings':{'desktop_content_position':'center','content_alignment':'center','color_scheme':'','full_width':True,'padding_top':40,'padding_bottom':52}
    }

    data['order'] = [
      'colors_changer_aDXkpK',
      'main',
      'rich_text_relief_intro',
      'multicolumn_core_benefits',
      'image_with_text_use_cases',
      'multicolumn_how_it_works',
      'testimonials_product_extra',
      'rich_text_final_close',
      'frequently_bought_together_z4GahM',
      'builder_p98UdB',
      'builder_JUkPnd'
    ]

    put_asset(tok,'templates/product.json',json.dumps(data,ensure_ascii=False,indent=2))
    print('product template expanded')

if __name__=='__main__':
    main()
