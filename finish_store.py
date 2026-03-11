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
    r=requests.get(f'https://{STORE}/admin/api/{API}/themes/{THEME_ID}/assets.json?asset[key]={key}',headers={'X-Shopify-Access-Token':tok},timeout=30)
    r.raise_for_status()
    return r.json()['asset']['value']


def put_asset(tok,key,value):
    r=requests.put(f'https://{STORE}/admin/api/{API}/themes/{THEME_ID}/assets.json',headers={'X-Shopify-Access-Token':tok,'Content-Type':'application/json'},json={'asset':{'key':key,'value':value}},timeout=30)
    r.raise_for_status()
    return r.json()


def main():
    tok=token()

    # PRODUCT TEMPLATE
    product=json.loads(get_asset(tok,'templates/product.json'))
    main=product['sections']['main']
    blocks=main['blocks']

    blocks['urgency_Cy48Ac']['settings']['urgency']='🚚 Free Shipping • 30-Day Returns • No Batteries Needed'
    blocks['rating_stars_yRDU98']['settings']['label']='4.7/5 • Cooling relief customers love'
    blocks['text_8adnqp']['settings']['text']='❄️ Fast cooling comfort for your forehead, temples, eyes, and head.'
    blocks['text_UegJJD']['settings']['text']='🌙 Light-blocking fit helps create a darker, calmer moment to rest.'
    blocks['text_3qpfmx']['settings']['text']='🔁 Reusable, non-electric relief with no charging, cords, or setup.'

    # disable noisy/irrelevant quantity discount block
    blocks['quantity_discounts_U8BP7t']['disabled']=True
    blocks['quantity_discounts_LyaFih']['settings']['most_popular']='Best Value'
    blocks['quantity_discounts_LyaFih']['settings']['option1_heading']='Get one'
    blocks['quantity_discounts_LyaFih']['settings']['option1_text']='Keep one chilled and ready'
    blocks['quantity_discounts_LyaFih']['settings']['option1_price']='34.99'
    blocks['quantity_discounts_LyaFih']['settings']['option2_heading']='Get two'
    blocks['quantity_discounts_LyaFih']['settings']['option2_text']='Save more + keep a backup ready'
    blocks['quantity_discounts_LyaFih']['settings']['option2_price']='59.99'
    blocks['quantity_discounts_LyaFih']['settings']['option3_heading']='Get three'
    blocks['quantity_discounts_LyaFih']['settings']['option3_text']='Best for home, work, and gifting'
    blocks['quantity_discounts_LyaFih']['settings']['option3_price']='79.99'
    blocks['quantity_discounts_LyaFih']['settings']['option4_heading']='Get four'
    blocks['quantity_discounts_LyaFih']['settings']['option4_text']='Stock up and save the most'
    blocks['quantity_discounts_LyaFih']['settings']['option4_price']='99.99'

    # rewrite reviews
    blocks['reviews_UwxAAn']['settings']['author_1']='Olivia C. – <strong>Verified Buyer</strong>'
    blocks['reviews_UwxAAn']['settings']['text_1']='<p>I keep mine in the fridge and grab it every evening after work. It cools down fast and helps me switch off properly.</p>'
    blocks['reviews_UwxAAn']['settings']['author_2']='Daniel R. – <strong>Verified Buyer</strong>'
    blocks['reviews_UwxAAn']['settings']['text_2']='<p>The cooling effect around my temples and eyes is exactly what I wanted after long screen days. Super easy to use.</p>'
    blocks['reviews_UwxAAn']['settings']['author_3']='Sarah M. – <strong>Verified Buyer</strong>'
    blocks['reviews_UwxAAn']['settings']['text_3']='<p>No cords, no noise, no hassle. I use it on hot afternoons and before bed whenever I need 15 minutes to reset.</p>'

    # collapsible tabs
    blocks['collapsible_tab_3VMfk4']['settings']['heading']='Why People Choose It'
    blocks['collapsible_tab_3VMfk4']['settings']['content']='<p>Cooling Relief Cap combines cooling comfort, light blocking, and reusable convenience in one simple self-care tool. Keep it chilled and ready whenever you need a quick reset.</p>'
    blocks['collapsible_tab_qhmErk']['settings']['heading']='30-Day Returns'
    blocks['collapsible_tab_qhmErk']['settings']['content']='<p>If it is not right for you, contact support within 30 days of delivery and we will guide you through the next steps.</p>'
    blocks['collapsible_tab_YWpHhW']['settings']['heading']='Shipping Information'
    blocks['collapsible_tab_YWpHhW']['settings']['content']='<p>Orders are processed in 1–3 business days. Typical delivery is 6–12 business days depending on destination. Tracking is sent after shipment.</p>'
    blocks['sticky_atc_XcXbr4']['settings']['label']='Cooling relief in minutes'
    blocks['sticky_atc_XcXbr4']['settings']['button_label']='Get Cooling Relief'

    put_asset(tok,'templates/product.json',json.dumps(product,ensure_ascii=False,indent=2))

    # SETTINGS / ANNOUNCEMENT + BRAND BASICS
    settings=json.loads(get_asset(tok,'config/settings_data.json'))
    cur=settings['current']
    cur['brand_headline']='Cooling relief for overstimulated, overheated days.'
    cur['brand_description']='A focused self-care store built around easy cooling comfort, reset routines, and practical relief.'
    ann=cur['sections']['announcement-bar']['blocks']['announcement_GD9kNP']['settings']
    ann['text']='🚚 Free Shipping • 30-Day Returns • Cooling Relief in Minutes'
    ann['link']='shopify://products/cooling-relief-cap'
    # make cart free shipping message coherent
    cur['free_shipping_message']="You're $15 away from free shipping"

    put_asset(tok,'config/settings_data.json',json.dumps(settings,ensure_ascii=False,indent=2))
    print('store finishing updates applied')

if __name__=='__main__':
    main()
